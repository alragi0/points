from asyncio import get_event_loop

from pyrogram import Client


async def getBot_token():
    try:
        from info import token
        bot = Client('MainBot', 27786450, '1fb7b1af2837205d7ce8d77cefc0acbd',
                     no_updates=True, in_memory=True, bot_token=token)
        await bot.start()
    except:
        token = input('token:\n')
        bot = Client('MainBot', 27786450, '1fb7b1af2837205d7ce8d77cefc0acbd',
                     no_updates=True, in_memory=True, bot_token=token)
        await bot.start()
        file = open('info.py', 'a')
        file.write(f'token = \'{token}\'\n')
        file.close()
    try:
        from info import sudo_username
        get_sudo = await bot.get_chat(sudo_username)
    except:
        sudo_username = input('sudo_username:\n')
        get_sudo = await bot.get_chat(sudo_username)
        file = open('info.py', 'a')
        file.write(f'sudo_username = \'{get_sudo.username}\'\n')
        file.close()
    try:
        from info import user_bot
        get_bot_tmwel = await bot.get_chat(user_bot)
    except:
        user_bot = input('user_bot:\n')
        get_bot_tmwel = await bot.get_chat(user_bot)
        file = open('info.py', 'a')
        file.write(f'user_bot = \'{get_bot_tmwel.username}\'\n')
        file.close()
    try:
        from info import sudo_id
    except:
        file = open('info.py', 'a')
        file.write(f'sudo_id = {get_sudo.id}\n')
        file.close()
    get_bot = await bot.get_me()
    await bot.stop()
    return token, get_sudo, get_bot, get_bot_tmwel


token, sudo_info, get_bot, get_bot_tmwel = get_event_loop().run_until_complete(getBot_token())

