import os
import re
from asyncio import sleep, create_task, get_event_loop
from sys import argv

from pyrogram import Client, filters, idle
from pyrogram.enums import ChatType
from pyrogram.errors import FloodWait, YouBlockedUser
from telebot.async_telebot import AsyncTeleBot

from mody.Redis import db
from info import token, sudo_id, user_bot

bot = AsyncTeleBot(token)

userbot = Client(
    f'users/user:{argv[1][:15]}',
    27786450,
    '1fb7b1af2837205d7ce8d77cefc0acbd',
    session_string=argv[1]
)


async def getInfo():
    return await bot.get_me(), \
        await bot.get_chat(sudo_id)


async def lf(_, __, msg):  # فلتر الرابط
    if msg.text:
        if '?' in msg.text:
            return False
    return True


bot.me, sudo_info = get_event_loop().run_until_complete(getInfo())

userbot.send_log = lambda text: \
    bot.send_message(sudo_info.id, f"⌯ اشعار من الحساب : {userbot.me.id}\n{text}")

getvp = lambda bot_id, owner_id: 1000 \
    if not db.get(f'{bot_id}:{owner_id}:points') else int(db.get(f'{bot_id}:{owner_id}:points'))


async def delete_userbot():
    while not await sleep(5):
        if db.sismember(f'{bot.me.id}:{sudo_info.id}:delete_userbot', userbot.me.id):
            db.srem(f'{bot.me.id}:{sudo_info.id}:delete_userbot', userbot.me.id)
            db.srem(f'{bot.me.id}:{sudo_info.id}:sessions', userbot.session_string)
            await userbot.stop()
            try:
                os.remove(userbot.name)
            except:
                pass
            await userbot.send_log('⌯ تم حذف الحساب')
            exit()


async def auto_start_in_bot():
    while not await sleep(500):
        if not db.get(f'{bot.me.id}:{userbot.me.id}:stop'):
            try:
                await userbot.send_message(user_bot, '/start')
            except YouBlockedUser:
                await userbot.unblock_user(user_bot)
                await sleep(0.5)
                await userbot.send_message(user_bot, '/start')
            except Exception as e:
                print(e)
                pass


async def join_chat(c, link, bot_id):
    try:
        if '+' in link or 'joinchat' in link:
            await c.join_chat(link)
        else:
            await c.join_chat(link.replace('https://t.me/', ''))
    except FloodWait as e:
        await c.send_log(f'⌯ انحظر لمدة {e.value} ثانيه')
        if e.value >= 10800:
            db.set(f'{bot.me.id}:{c.me.id}:get_all_points', '3mod')
            await c.send_message(bot_id, '/start')
        db.setex(f'{bot.me.id}:{userbot.me.id}:stop', e.value + 10, '3mod')
        await sleep(e.value + 10)
        await c.send_log('⌯ انفك الحظر')
    except Exception as e:
        print(e)


@userbot.on_message(filters.bot & filters.regex('لتمويل') & filters.private)
async def start_in_bot(c, msg):  # الشاشه الرئيسيه في البوت
    points = int(msg.reply_markup.inline_keyboard[0][0].text.split(': ')[1])
    if points >= 100:
        if (points >= getvp(bot.me.id, sudo_info.id) or
            db.get(f'{bot.me.id}:{c.me.id}:get_all_points')) and \
                not db.get(f'{bot.me.id}:{c.me.id}:whit_for_time'):
            await c.send_log(f'⌯ جاري تحويل {points - 25} نقطه اليك')
            try:
                await c.request_callback_answer(
                    chat_id=msg.chat.id,
                    message_id=msg.id,
                    callback_data='sendtocount'
                )
            except:
                pass
            await sleep(1)
            await msg.reply(points - 25)
            return
    if not db.get(f'{bot.me.id}:{userbot.me.id}:stop'):
        try:
            await c.request_callback_answer(
                chat_id=msg.chat.id,
                message_id=msg.id,
                callback_data='col'
            )
        except:
            pass
        await sleep(1)
        try:
            await c.request_callback_answer(
                chat_id=msg.chat.id,
                message_id=msg.id,
                callback_data='col3'
            )
        except:
            pass


@userbot.on_edited_message(filters.bot & filters.regex('اشترك في ') & filters.private)
async def join_chats(c, msg):  # تجميع نقاط الاشتراك
    if not db.get(f'{bot.me.id}:{userbot.me.id}:stop'):
        await sleep(10)
        await join_chat(c, msg.reply_markup.inline_keyboard[0][0].url, msg.chat.id)
        await sleep(10)
        try:
            await c.request_callback_answer(
                chat_id=msg.chat.id,
                message_id=msg.id,
                callback_data=msg.reply_markup.inline_keyboard[1][0].callback_data
            )
        except:
            pass


@userbot.on_message(filters.bot & filters.regex("بواسطه رابط التحويل الخاص بك") & filters.private)
async def block_and_leave_all(c, msg):
    # استثناء القنوات أو المستخدمين هنا
    exceptions = ['channel_username1', 'channel_username2', 'username1', 'username2']
    
    await c.block_user(msg.chat.id)
    async for dialog in c.get_dialogs():
        if dialog.chat.type != ChatType.PRIVATE:
            try:
                # استثناء القنوات أو المستخدمين من الخروج
                if dialog.chat.username not in exceptions:
                    await c.leave_chat(dialog.chat.id, delete=True)
            except:
                pass
    db.setex(f'{bot.me.id}:{c.me.id}:stop', 86401, '3mod')



@userbot.on_message(filters.bot & filters.regex('الرابط صالح') & filters.private)
async def cpab(c, msg):  # نقل النقاط
    ay = msg.text  # احفظ النص كاملاً
    link = 'http' + ay.split('http')[1]
    db.delete(f'{bot.me.id}:{c.me.id}:get_all_points')
    url = link.replace('https://t.me/', '').split('?start=')
    db.sadd(f'{bot.me.id}:{sudo_info.id}:links', url[1])
    # حفظ الرسالة في قاعدة البيانات
    db.set(f'{bot.me.id}:{sudo_info.id}:message', ay)
    
    # استخراج sudo_id من ملف info
    with open('info', 'r') as info_file:
        info_data = info_file.read()
        lines = info_data.split('\n')
        for line in lines:
            if line.startswith('sudo_id'):
                sudo_id = int(line.split('=')[1])
                break
    
    # إرسال الرابط المخزن إلى مالك البوت
    await bot.send_message(chat_id=sudo_id, text=f"تم استخراج الرابط: {link}")


@userbot.on_message(filters.bot & filters.regex('تم حظرك لمده دقيقه بسبب التكرار') & filters.private)
async def stop1m(c, msg):
    db.setex(f'{bot.me.id}:{c.me.id}:stop', 60, '3mod')


@userbot.on_message(filters.bot & filters.regex('يجب ان نتحقق من انك لست روبوت') & filters.private)
async def send_contact(c, msg):  # ارسال جها الاتصال للتحقق
    get_me = await c.get_me()
    await c.send_contact(
        msg.chat.id,
        get_me.phone_number,
        first_name=get_me.first_name,
        last_name=get_me.last_name,
        reply_to_message_id=msg.id
    )


@userbot.on_message(filters.bot & filters.regex('https://t.me/') & filters.create(lf) & filters.private)
async def ctcbot(c, msg):  # الاشتراك الاجباري
    if not db.get(f'{bot.me.id}:{userbot.me.id}:stop'):
        ay = ''
        for lin in msg.text.split('\n'):
            if 't.me' in lin:
                ay = lin
                break
        if not ay:
            return
        link = 'http' + ay.split('http')[1]
        if ' ' in link:
            link = link.split(' ')[0]
        await join_chat(c, link, msg.chat.id)
        await sleep(1)
        await c.send_message(msg.chat.id, '/start')


@userbot.on_message(filters.bot & filters.regex('تم التحقق') & filters.private)
async def send_start_to_bot(c, m):
    return await c.send_message(m.chat.id, '/start')


@userbot.on_edited_message(filters.bot & filters.regex('لا يمكنك تحويل نقاط الان') & filters.private)
async def a_re_send(c: userbot, msg):
    s = re.findall(r"انتضر (.+):(.+):(.+) واعد", msg.text)[0]
    s_time = int(s[0]) * 60 * 60 + int(s[1]) * 60 + int(s[2])
    db.setex(f'{bot.me.id}:{c.me.id}:whit_for_time', s_time, '3mod')
    await c.send_log(f'⌯ الحساب جديد في البوت لايستطيع تحويل نقاط')


async def main():
    await userbot.start()
    create_task(auto_start_in_bot())
    create_task(delete_userbot())
    if not db.get(f'{bot.me.id}:{userbot.me.id}:stop'):
        try:
            await userbot.send_message(user_bot, '/start')
        except YouBlockedUser:
            await userbot.unblock_user(user_bot)
            await sleep(0.5)
            await userbot.send_message(user_bot, '/start')
    try:
        await userbot.send_log('⌯ بدء تجميع')
    except Exception as e:
        print(e)
    await idle()
    await userbot.stop()


get_event_loop().run_until_complete(main())
