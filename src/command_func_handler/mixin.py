import re
from typing import Any, override

from mcdreforged.api.all import PluginEvent, ServerInformation
from mcdreforged.handler.impl import AbstractMinecraftHandler
from mcdreforged.handler.impl.abstract_minecraft_handler import (
    _does_mc_version_has_execute_command,
)
from mcdreforged.utils.types.message import MessageText


def handler_generator(
    mixin: Any, base: Any, name: str, class_name: str = "CommandFuncHandler"
) -> type:
    @override
    def get_name(self) -> str:
        _ = self
        return name

    dynamic_class = type(class_name, (mixin, base), {"get_name": get_name})
    return dynamic_class


class CommandFuncMixin(AbstractMinecraftHandler):
    def parse_server_stdout(self, text: str):
        info = super().parse_server_stdout(text)
        if not info.player:
            m = re.fullmatch(
                r"(?:\[Not Secure\] )?\[(?P<name>[^\]]+)\] (?P<message>.*)",
                info.content or "",
            )
            if m and m["name"] == "Server":
                info.player, info.content = "!function", m["message"]
            elif m and m["name"] == "@":
                info.player, info.content = "!commandblock", m["message"]
        return info

    @override
    def get_send_message_command(self, target: str, message: MessageText, server_information: ServerInformation) -> str | None:
        try:
            can_do_execute = _does_mc_version_has_execute_command(server_information.version)
        except (ValueError, IndexError):
            # TODO: logging?
            can_do_execute = False
        
        command = None
        if not target.startswith("!"):
            command = f'tellraw {target} {self.format_message(message, server_information=server_information)}'
            if can_do_execute:
                # Mute the "No player was found" output when no player is online by using the "execute at" command
                command = f'execute at @p run {command}'
        return command


class NewHandlerMixin(PluginEvent):
    def __init__(self, handler_name: str, handler_mixin: str, handler_class: str):
        super().__init__("NewHandlerMixin")
        self.handler_name = handler_name
        self.handler_mixin = handler_mixin
        self.handler_class = handler_class
