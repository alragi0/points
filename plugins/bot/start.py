from pyrogram import Client

from mody.Keyboards import start_key, login_key
from mody.Redis import db
from mody.mod import Bfilter


@Client.on_message(Bfilter('/start'))
async def start(client, message):
    if db.get(f'{client.me.id}:{message.from_user.id}:session'):
        await message.reply('⌯ مرحبا عزيزي \n⌯ يمكنك التحكم في حساباتك من هنا \n⌯ مطور  البوت : @YYNXX', reply_markup=start_key)
    else:
        await message.reply('⌯ يجب تسجبل الدخول بهذا الحساب', reply_markup=login_key)


@Client.on_message(Bfilter('⌯ حساباتي'))
async def count_of_userbots(client, message):
    await message.reply(f"⌯ عدد حساباتك : {db.scard(f'{client.me.id}:{message.from_user.id}:sessions')}")
