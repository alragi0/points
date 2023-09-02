import functools
from asyncio.exceptions import TimeoutError

import asyncio
import pyrogram

loop = asyncio.get_event_loop()


class CommandCanceled(Exception):
    pass


pyrogram.errors.CommandCanceled = CommandCanceled


def patch(obj):
    def wrapper(container):
        for name, func in filter(lambda item: getattr(item[1], 'patchable', False), container.__dict__.items()):
            old = getattr(obj, name, None)
            setattr(obj, 'old' + name, old)
            setattr(obj, name, func)
        return container

    return wrapper


def patchable(func):
    func.patchable = True
    return func


@patch(pyrogram.client.Client)
class Client(pyrogram.Client):
    @patchable
    def __init__(self, *args, **kwargs):
        self.listening = {}
        self.using_mod = True

        self.old__init__(*args, **kwargs)

    @patchable
    async def listen(self, chat_id, filters=None, timeout=None):
        future = loop.create_future()
        future.add_done_callback(
            functools.partial(self.clear_listener, chat_id)
        )
        self.listening.update({
            chat_id: {"future": future, "filters": filters}
        })
        return await asyncio.wait_for(future, timeout)

    @patchable
    async def ask(self, message, text, filters=None, creply_markup=False, timeout=300, *args,
                  **kwargs) -> "pyrogram.types.Message":
        request = await message.reply(text, *args, **kwargs)
        chat_id = message.chat.id + (message.from_user or message.sender_chat).id
        try:
            response = await self.listen(chat_id, filters, timeout)
        except TimeoutError:
            await message.reply('⌯ انتهت مدة الانتظار', reply_markup=creply_markup)
            raise
        response.request = request
        if response.text in ['⌯ الغاء', "الغاء ورجوع"]:
            await response.reply('⌯ تم الغاء الامر بنجاح', reply_markup=creply_markup)
            raise CommandCanceled
        else:
            return response

    @patchable
    def clear_listener(self, chat_id, future):
        try:
            if future == self.listening[chat_id]["future"]:
                self.listening.pop(chat_id, None)
        except Exception as e:
            print(e)

    @patchable
    def cancel_listener(self, chat_id):
        listener = self.listening.get(chat_id)
        if not listener or listener['future'].done():
            return

        listener['future'].set_exception(CommandCanceled())
        self.clear_listener(chat_id, listener['future'])


@patch(pyrogram.handlers.message_handler.MessageHandler)
class MessageHandler():
    @patchable
    def __init__(self, callback: callable, filters=None):
        self.user_callback = callback
        self.old__init__(self.resolve_listener, filters)

    @patchable
    async def resolve_listener(self, client, message, *args):
        listener = client.listening.get(message.chat.id + (message.from_user or message.sender_chat).id)
        if listener and not listener['future'].done():
            listener['future'].set_result(message)
        else:
            if listener and listener['future'].done():
                client.clear_listener(message.chat.id + (message.from_user or message.sender_chat).id,
                                      listener['future'])
            await self.user_callback(client, message, *args)

    @patchable
    async def check(self, client, update):
        listener = client.listening.get(update.chat.id + (update.from_user or update.sender_chat).id)

        if listener and not listener['future'].done():
            return await listener['filters'](client, update) if callable(listener['filters']) else True

        return (
            await self.filters(client, update)
            if callable(self.filters)
            else True
        )


@patch(pyrogram.types.messages_and_media.message.Message)
class Message(pyrogram.types.messages_and_media.message.Message):
    @patchable
    async def ask(self, text, *args, **kwargs) -> "pyrogram.types.Message":
        return await self._client.ask(self, text, *args, **kwargs)
