from mcdreforged.api.all import (
    CommandSource,
    Info,
    PluginServerInterface,
    ServerInterface,
    SimpleCommandBuilder,
    event_listener,
)
from mcdreforged.handler.impl import (
    ArclightHandler,
    Bukkit14Handler,
    BukkitHandler,
    CatServerHandler,
    ForgeHandler,
    VanillaHandler,
)

from command_func_handler.config import get_config, DefaultConfig, disable_handler
from command_func_handler.mixin import (
    CommandFuncMixin,
    handler_generator,
    handler_name,
    handler_event_dispatcher,
)

psi = ServerInterface.psi()
config = DefaultConfig()
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


def event_dispatcher():
    handler_event_dispatcher(psi)


def disable_register_handler():
    disable_handler(psi)


def on_load(server: PluginServerInterface, _):
    global config, psi
    config = get_config(server)
    psi = server
    whether_register_handler: bool = config.enable_handler
    if whether_register_handler and config.disable_when_detected_conflict:
        for i in server.get_plugin_list():
            if "handler" in i and i != handler_name:
                whether_register_handler = False
                break
    if whether_register_handler:
        handler_base = get_built_in_handler()
        handler = handler_generator(CommandFuncMixin, handler_base)
        server.register_server_handler(handler())
    event_dispatcher()


@builder.command(f"!!{handler_name} debug")
def on_debug(src: CommandSource):
    global debugging
    if not src.has_permission(4):
        src.reply("Permission denied!")
        return
    debugging = True
    src.reply(f"Enabled debugging mode for {handler_name}.")


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


@event_listener("HandlerManagerEvent")
def on_event_handler_manager(server: PluginServerInterface, _: str, __: str):
    server.logger.info("Detected HandlerManagerEvent, but no impl for this at present.")


def no_debug():
    global debugging
    debugging = False


def on_server_stop(_: PluginServerInterface):
    no_debug()


def on_unload(_: PluginServerInterface):
    no_debug()
