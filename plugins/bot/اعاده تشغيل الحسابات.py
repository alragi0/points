import os
import re
from asyncio import subprocess, create_subprocess_exec

from pyrogram import Client
from pyrogram.types import Message

from mody.Redis import db
from mody.mod import Bfilter


@Client.on_message(Bfilter("⌯ تحديث"))
async def restartall(client: Client, message: Message):
    proc = await create_subprocess_exec(
        "ls",
        "/run/screen/S-root",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    res = stdout.decode().split('\n')
    for session in db.smembers(f'{client.me.id}:{message.from_user.id}:sessions'):
        for res2 in res:
            if session[:50] in res2:
                num = re.findall("(.+)." + session[:50], res2)[0]
                print(f'kill screen {num}')
                os.system(f'kill {num}')
    await message.reply('⌯ تم اعاده تشغيل الحسابات')
