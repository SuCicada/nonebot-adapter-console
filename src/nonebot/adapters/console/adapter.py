import asyncio
from typing import Any, Dict, List, Union

from nonebot.adapters import Adapter as BaseAdapter
from nonebot.drivers import (
    URL,
    Driver,
    ReverseDriver,
    WebSocket,
    WebSocketServerSetup,
)
from nonebot.exception import WebSocketClosed
from nonebot.message import handle_event
from nonebot.typing import overrides

from .bot import Bot
from .event import Event
from .message import Message, MessageSegment
from .utils import *


class Adapter(BaseAdapter):
    @overrides(BaseAdapter)
    def __init__(self, driver: Driver, **kwargs: Any):
        super().__init__(driver, **kwargs)
        # self.adapter_config = AdapterConfig(**self.config.dict())
        self.connections: Dict[str, WebSocket] = {}
        self.tasks: List[asyncio.Task] = []
        self.setup()

    @classmethod
    @overrides(BaseAdapter)
    def get_name(cls) -> str:
        return "Console"

    def setup(self) -> None:
        if isinstance(self.driver, ReverseDriver):
            ws_setup = WebSocketServerSetup(
                URL("/console"), self.get_name(), self._handle_ws
            )
            self.driver.setup_websocket_server(ws_setup)

    async def _handle_ws(self, websocket: WebSocket) -> None:
        self_id = websocket.request.headers.get("x-self-id")

        await websocket.accept()
        bot = Bot(self, self_id)
        self.connections[self_id] = websocket
        self.bot_connect(bot)

        log("INFO", f"<y>Bot {self_id}  </y> connected")
        # await websocket.send("dsfsfsdfsdf")

        try:
            while True:
                data = await websocket.receive()
                print(data)
                # json_data = json.loads(data)
                # event = json_data['event']
                # await websocket.send(data)
                # await self._call_api(bot, data)
                event_json = {
                    "post_type": "message",
                    # "message": [{"text": data}]
                    "text": data,
                }
                event = Event.parse_event(event_json)
                if event:
                    asyncio.create_task(handle_event(bot, event))

                # await handle_event(bot, event)


        # if event:
        #     asyncio.create_task(bot.handle_event(event))

        except WebSocketClosed as e:
            log("WARNING", f"WebSocket for Bot {self_id} closed by peer")
        except Exception as e:
            log(
                "ERROR",
                "<r><bg #f8bbd0>Error while process data from websocket"
                f"for bot {self_id}.</bg #f8bbd0></r>",
                e,
            )
            try:
                await websocket.close()
            except Exception as e:
                log('ERROR', 'websocket.close error', e)
        finally:
            log('INFO', f" Bot {self_id} disconnect")
            self.connections.pop(self_id, None)
            self.bot_disconnect(bot)

    @overrides(BaseAdapter)
    async def _call_api(self, bot: Bot, api: str, **data) -> Any:
        await getattr(self, api)(bot, **data)

    async def send_message(self, bot: Bot, message: Union[str, Message, MessageSegment]) -> Any:
        ws: WebSocket = self.connections.get(bot.self_id)
        message_list = []
        if isinstance(message, str):
            message_list.append(message)
        if isinstance(message, Message):
            message_list = [str(m) for m in message]

        for m in message_list:
            await ws.send(m)
