from mcdreforged.api.all import (
    CommandSource,
    Info,
    PluginServerInterface,
    ServerInterface,
    SimpleCommandBuilder,
)
from mcdreforged.handler.impl import (
    ArclightHandler,
    Bukkit14Handler,
    BukkitHandler,
    CatServerHandler,
    ForgeHandler,
    VanillaHandler,
)

from command_func_handler.config import get_config
from command_func_handler.mixin import (
    CommandFuncMixin,
    NewHandlerMixin,
    handler_generator,
)

builder = SimpleCommandBuilder()
debugging: bool = False


def get_built_in_handler():

    server = ServerInterface.get_instance()
    if not server:
        raise RuntimeError("Server instance is not available.")
    handler = server.get_mcdr_config().get("handler", "")

    if handler == "vanilla_handler":
        return VanillaHandler
    elif handler == "forge_handler":
        return ForgeHandler
    elif handler == "bukkit_handler":
        return BukkitHandler
    elif handler == "bukkit14_handler":
        return Bukkit14Handler
    elif handler == "cat_server_handler":
        return CatServerHandler
    elif handler == "arclight_handler":
        return ArclightHandler


def on_load(server: PluginServerInterface, _):
    config = get_config(server)
    if not config.enable_handler:
        return
    for i in server.get_plugin_list():
        if (
            "handler" in i
            and i != "command_func_handler"
            and config.disable_when_detected_conflict
        ):
            return
    builder.register(server)
    server.logger.info(
        f"Basing on handler {server.get_mcdr_config().get('handler', '')}"
    )
    base = get_built_in_handler()
    handler = handler_generator(CommandFuncMixin, base, "command_func_handler")
    server.register_server_handler(handler())
    server.dispatch_event(
        NewHandlerMixin(
            "command_func_handler", "CommandFuncMixin", "CommandFuncHandler"
        ),
        ("command_func_handler", "CommandFuncMixin", "CommandFuncHandler"),
    )


@builder.command("!!command_func_handler debug")
def on_debug(src: CommandSource):
    global debugging
    if not src.has_permission(4):
        src.reply("Permission denied!")
        return
    debugging = True
    src.reply("Enabled debugging mode for command_func_handler.")


def on_info(server: PluginServerInterface, info: Info):
    if not debugging or info.is_from_console:
        return
    player = info.player
    if not player or not player.startswith("!"):
        return
    match player:
        case "!function":
            server.logger.info(
                f"Info '{info.content}' is from server command or function."
            )
        case "!commandblock":
            server.logger.info(f"Info '{info.content}' is from command blocks.")


def no_debug():
    global debugging
    debugging = False


def on_server_stop(_: PluginServerInterface):
    no_debug()


def on_unload(_: PluginServerInterface):
    no_debug()
