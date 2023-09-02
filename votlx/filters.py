import re
from typing import Union, List

from pyrogram import filters, Client
from pyrogram.types import Message, CallbackQuery, InlineQuery, Update


def msg(pattern: Union[str, List[str]]):
    async def func(flt, client: Client, update: Update):
        if isinstance(update, Message):
            value = update.text
        elif isinstance(update, CallbackQuery):
            value = update.data
        elif isinstance(update, InlineQuery):
            value = update.query
        else:
            raise ValueError(f"Message Test filter doesn't work with {type(update)}")
        if value:
            username = client.me.username or ''
            if username != '':
                value = value.replace(f'@{username}', '')
            if isinstance(pattern, list):
                for ay in pattern:
                    if value == ay:
                        return True
                return False
            else:
                return bool(pattern == value)

    return filters.create(
        func,
        "MessageTestFilter"
    )


filters.msg = msg


def cmd(commands: Union[str, List[str]], prefixes: Union[str, List[str]] = None, case_sensitive: bool = False):
    command_re = re.compile(r"([\"'])(.*?)(?<!\\)\1|(\S+)")

    async def func(flt, client: Client, message: Message):
        username = client.me.username or ""
        text = message.text
        message.command = None

        if not text:
            return False

        for prefix in flt.prefixes:
            if not text.startswith(prefix):
                continue

            without_prefix = text[len(prefix):]

            for cmd in flt.commands:
                if not re.match(rf"^(?:{cmd}(?:@?{username})?)(?:\s|$)", without_prefix,
                                flags=re.IGNORECASE if not flt.case_sensitive else 0):
                    continue

                without_command = re.sub(rf"{cmd}(?:@?{username})?\s?", "", without_prefix, count=1,
                                         flags=re.IGNORECASE if not flt.case_sensitive else 0)

                message.command = [cmd] + [
                    re.sub(r"\\([\"'])", r"\1", m.group(2) or m.group(3) or "")
                    for m in command_re.finditer(without_command)
                ]

                return True

        return False

    commands = commands if isinstance(commands, list) else [commands]
    commands = {c if case_sensitive else c.lower() for c in commands}

    prefixes = [] if prefixes is None else prefixes
    prefixes = prefixes if isinstance(prefixes, list) else [prefixes]
    prefixes = set(prefixes) if prefixes else {""}

    return filters.create(
        func,
        "CmdFilter",
        commands=commands,
        prefixes=prefixes,
        case_sensitive=case_sensitive
    )


filters.cmd = cmd
