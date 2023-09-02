from os import execle, environ
from sys import executable

from pyrogram import Client
from pyrogram.types import Message

from mody.Keyboards import login_key
from mody.Redis import db
from mody.get_session import getSession
from mody.mod import Bfilter


@Client.on_message(Bfilter("⌯ تسجيل الدخول"))
async def login_to_me(client: Client, message: Message):
    user, get_me, session = await getSession(message, login_key)
    db.set(f'{client.me.id}:{get_me.id}:session', session)
    db.set(f'{client.me.id}:restart', '3mod')
    await message.reply('⌯ تم تسجيل الدخول انتظر 5 ثواني')
    args = [executable, "main.py"]
    execle(executable, *args, environ)
