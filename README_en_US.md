- English
- [中文（简体）](README.md)

# CommandFuncHandler-MCDR
Forked from [MCDR-Commandblock-Handler](https://github.com/Dainsleif233/MCDR-Commandblock-Handler), with an improved code structure and enhanced plugin features; uses the same GPLv3 license.

CommandFuncHandler is a processor designed for Minecraft commands and functions, enabling functions and command blocks to use MCDR commands.

CommandFuncHandler and other plugins of the same type are not officially supported by MCDReforged and are not affiliated with its maintainers. If you encounter any issues, please report them in [Issues](https://github.com/Mooling0602/CommandFuncHandler-MCDR/issues).

## Usage
Configure the server handler in `config.yml` under the MCDR working directory. See [handler](https://docs.mcdreforged.com/en/latest/configuration.html#handler) for details.
> Currently, only MCDR's built-in server handler is supported. Support for third-party handlers requires the HandlerManager plugin (in development).

If you are not using any other plugins of the server-handler type, this plugin should work out of the box. If you encounter problems, try checking the configuration file.
> The configuration file is usually located at `config/command_func_handler/config.yml`.

In theory, the plugin can be made compatible with other third-party server-handler plugins through the "HandlerMixin specification" of the [HandlerManager](https://github.com/Mooling0602/HandlerManager-MCDR) plugin (still in development), but those plugins must be adapted, and compatibility is not guaranteed.

If you find that the plugin is not working as expected, you can use the `!!command_func_handler debug` command to enable debug mode and view the plugin's log output for troubleshooting.

## Permissions
You can set permissions for the function `!function` and the command block `!commandblock` in `permission.yml` under the MCDR working directory. See [Permission](https://docs.mcdreforged.com/en/latest/permission.html#permission) for details.

Below is an example configuration that allows functions and command blocks to use MCDR commands with administrator-level permissions:

```yml
admin:
- '!commandblock'
- '!function'
```

## License
This project uses the GPLv3 license. For details, please see the [LICENSE](LICENSE) file.
