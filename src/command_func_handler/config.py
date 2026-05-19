from mcdreforged.api.all import PluginServerInterface, Serializable


class DefaultConfig(Serializable):
    enable_handler: bool = True
    disable_when_detected_conflict: bool = True


def get_config(server: PluginServerInterface) -> DefaultConfig:
    return server.load_config_simple(file_name="config.yml", target_class=DefaultConfig)  # ty: ignore[invalid-return-type]
