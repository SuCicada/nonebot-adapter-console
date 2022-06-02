#!/usr/bin/env python3

import nonebot
from src.nonebot.adapters.console import Adapter as ConsoleAdapter

nonebot.init()
app = nonebot.get_asgi()

driver = nonebot.get_driver()
driver.register_adapter(ConsoleAdapter)

nonebot.load_builtin_plugins("echo")
# nonebot.load_from_toml("pyproject.toml")

if __name__ == "__main__":
    nonebot.logger.warning("Always use `nb run` to start the bot instead of manually running!")
    nonebot.run(app="__mp_main__:app")
