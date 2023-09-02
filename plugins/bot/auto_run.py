import os
from asyncio import create_task, create_subprocess_exec, subprocess, sleep

from mody.Redis import db
from mody.get_info import sudo_info
from mody.mod import Bot


async def auto_run():
    while not await sleep(10):
        proc = await create_subprocess_exec(
            "screen",
            "-ls",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        res = stdout.decode()
        for session in db.smembers(f'{Bot.me.id}:{sudo_info.id}:sessions'):
            if session[:50] not in res:
                os.system(f'screen -d -m -S {session[:50]} python3 users.py {session}')


create_task(auto_run())
