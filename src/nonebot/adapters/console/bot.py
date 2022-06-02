from typing import Any, Union

from nonebot.adapters import Bot as BaseBot
from nonebot.adapters import Event
from nonebot.typing import overrides
from .message import Message, MessageSegment


class Bot(BaseBot):
    # def __init__(self, adapter: "Adapter", config: BotConfig):
    #     self.adapter = adapter
    #     self.bot_config = config

    @overrides(BaseBot)
    async def send(
            self,
            event: Event,
            message: Union[str, Message, MessageSegment],
            **kwargs,
    ) -> Any:
        """
        :py:class: `adapter_console.adapter.Adapter`
        :param :func:`adapter_console.adapter.Adapter._call_api`
        :param event:  :py:class: `adapter_console.adapter.Adapter`
        """
        await self.call_api("send_message", message=message)
