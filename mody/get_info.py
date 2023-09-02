from asyncio import get_event_loop
from pyrogram import Client

# تعريف المتغيرات
TOKEN = '6139441987:AAHruDcEcx-GGrpO7pw04wojJO_2Qy8Guug'
sudo_username = 'YYNNXXXX'
user_bot = 'EEObot'
sudo_id = 6699312679

async def getBot_token():
    try:
        bot = Client('MainBot', 27786450, '1fb7b1af2837205d7ce8d77cefc0acbd',
                     no_updates=True, in_memory=True, bot_token=TOKEN)
        await bot.start()
    except:
        token = TOKEN
        bot = Client('MainBot', 27786450, '1fb7b1af2837205d7ce8d77cefc0acbd',
                     no_updates=True, in_memory=True, bot_token=token)
        await bot.start()

    try:
        get_sudo = await bot.get_chat(sudo_username)
    except:
        get_sudo = await bot.get_chat(sudo_username)

    try:
        get_bot_tmwel = await bot.get_chat(user_bot)
    except:
        get_bot_tmwel = await bot.get_chat(user_bot)

    try:
        from info import sudo_id
    except:
        file = open('info.py', 'a')
        file.write(f'sudo_id = {get_sudo.id}\n')
        file.close()
    get_bot = await bot.get_me()
    await bot.stop()
    return TOKEN, get_sudo, get_bot, get_bot_tmwel

# استدعاء الدالة وتخزين القيم
token, sudo_info, get_bot, get_bot_tmwel = get_event_loop().run_until_complete(getBot_token())
