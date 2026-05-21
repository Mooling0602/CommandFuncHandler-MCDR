from mcdreforged.api.all import PluginServerInterface, Serializable
from command_func_handler.mixin import handler_name


class DefaultConfig(Serializable):
    enable_handler: bool = True
    disable_when_detected_conflict: bool = True


def get_config(server: PluginServerInterface) -> DefaultConfig:
    return server.load_config_simple(file_name="config.yml", target_class=DefaultConfig)  # ty: ignore[invalid-return-type]


def disable_handler(server: PluginServerInterface):
    _config = DefaultConfig()
    _config.enable_handler = False
    server.save_config_simple(_config, "config.yml")
    server.reload_plugin(handler_name)
