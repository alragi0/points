from asyncio import get_event_loop
from pyrogram import Client

async def getBot_token():
    try:
        # تعريف الرقم التوكن هنا مباشرة
        token = '6109895485:AAE43imQ2y0W_yDx5B_Fsdod_SWt7MyrKQg'
        bot = Client('MainBot', 27786450, '1fb7b1af2837205d7ce8d77cefc0acbd',
                     no_updates=True, in_memory=True, bot_token=token)
        await bot.start()

        sudo_username = 'YYNNXXXX'
        get_sudo = await bot.get_chat(sudo_username)

        user_bot = 'EEObot'
        get_bot_tmwel = await bot.get_chat(user_bot)

        # تعريف المتغير sudo_id
        sudo_id = 6699312679
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        await bot.stop()
        return token, get_sudo, get_bot, get_bot_tmwel, sudo_id

token, sudo_info, get_bot, get_bot_tmwel, sudo_id = get_event_loop().run_until_complete(getBot_token())
