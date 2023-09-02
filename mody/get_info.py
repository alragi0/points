from asyncio import get_event_loop
from pyrogram import Client

async def getBot_token():
    try:
        token = '6139441987:AAHruDcEcx-GGrpO7pw04wojJO_2Qy8Guug'
        bot = Client('MainBot', 27786450, '1fb7b1af2837205d7ce8d77cefc0acbd',
                     no_updates=True, in_memory=True, bot_token=token)
        await bot.start()
    except:
        token = '6109895485:AAE43imQ2y0W_yDx5B_Fsdod_SWt7MyrKQg'
        bot = Client('MainBot', 27786450, '1fb7b1af2837205d7ce8d77cefc0acbd',
                     no_updates=True, in_memory=True, bot_token=token)
        await bot.start()
    
    try:
        sudo_username = 'YYNNXXXX'
        get_sudo = await bot.get_chat(sudo_username)
    except:
        sudo_username = 'YYNNXXXX'  # تغيير إذا لزم الأمر
        get_sudo = await bot.get_chat(sudo_username)
    
    try:
        user_bot = 'EEObot'
        get_bot_tmwel = await bot.get_chat(user_bot)
    except:
        user_bot = 'EEObot'  # تغيير إذا لزم الأمر
        get_bot_tmwel = await bot.get_chat(user_bot)
    
    try:
        sudo_id = 6699312679
        get_bot = await bot.get_me()
    except:
        sudo_id = 6699312679  # تغيير إذا لزم الأمر
        get_bot = await bot.get_me()
        
    await bot.stop()
    return token, get_sudo, get_bot, get_bot_tmwel

token, sudo_info, get_bot, get_bot_tmwel = get_event_loop().run_until_complete(getBot_token())
