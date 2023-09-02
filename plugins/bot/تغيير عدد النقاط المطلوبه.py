from pyrogram import Client, filters
from pyrogram.types import Message

from mody.Keyboards import start_key, cancel
from mody.Redis import db
from mody.mod import Bfilter


@Client.on_message(Bfilter("⌯ تعيين النقاط"))
async def pin_points_nember(client: Client, message: Message):
    message = await message.ask('⌯ ارسل عدد النقاط المطلوبه', filters.text, start_key, reply_markup=cancel)
    try:
        db.set(f'{client.me.id}:{message.from_user.id}:points', int(message.text))
        await message.reply('⌯ تم تثبيت عدد النقاط المطلوبه', reply_markup=start_key)
    except:
        await message.reply('⌯ يجب ان يكون العدد عباره عن ارقام', reply_markup=start_key)
