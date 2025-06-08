# Configuration and Settings

`jgtpy` relies on the **jgtutils** package to read configuration values. Two files are commonly used:

- `config.json` – contains credentials and paths required by services.
- `settings.json` – provides default arguments for CLI tools.

The helper functions from `jgtutils.jgtcommon` automatically look for these files in the current directory, in `~/.jgt/` or `/etc/jgt/`. Environment variables `JGT_CONFIG`, `JGT_SETTINGS`, and related variants can override the location or content.

CLI parsers created with `jgtutils.jgtcommon.new_parser` call `parse_args`, which attaches the loaded settings to the returned namespace.

Use `jgtutils.jgtcommon.readconfig()` to access credentials and `jgtutils.jgtcommon.get_settings()` for user preferences.
