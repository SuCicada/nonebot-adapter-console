from nonebot.adapters import Event as BaseEvent
from nonebot.typing import overrides
from typing_extensions import Literal

# from .model import *
from .message import Message


class Event(BaseEvent):
    __event__ = ""

    # time: int
    # self_id: int
    post_type: str

    @overrides(BaseEvent)
    def get_type(self) -> str:
        return self.post_type

    @overrides(BaseEvent)
    def get_event_name(self) -> str:
        return self.post_type

    @overrides(BaseEvent)
    def get_event_description(self) -> str:
        return str(self.dict(
            by_alias=True, exclude_none=True,
            exclude={"telegram_model"})
        )

    @overrides(BaseEvent)
    def get_message(self) -> Message:
        raise ValueError("Event has no message!")

    @overrides(BaseEvent)
    def get_plaintext(self) -> str:
        raise ValueError("Event has no message!")

    @overrides(BaseEvent)
    def get_user_id(self) -> str:
        raise ValueError("Event has no context!")

    @overrides(BaseEvent)
    def get_session_id(self) -> str:
        raise ValueError("Event has no context!")

    @overrides(BaseEvent)
    def is_tome(self) -> bool:
        return False

    @classmethod
    def parse_event(cls, obj: dict) -> "Event":
        return MessageEvent._parse_event(obj)


class MessageEvent(Event):
    """消息事件"""

    __event__ = "message"
    # post_type: Literal["message"]
    # sub_type: str
    # user_id: int
    # message_type: str
    # message_id: int
    message: Message = Message()

    # raw_message: str
    # font: int
    to_me: bool = False

    @overrides(Event)
    def get_event_name(self) -> str:
        return "event_name"
        # sub_type = getattr(self, "sub_type", None)
        # return f"{self.post_type}.{self.message_type}" + (
        #     f".{sub_type}" if sub_type else ""
        # )

    @overrides(Event)
    def get_message(self) -> Message:
        return self.message

    @overrides(Event)
    def get_plaintext(self) -> str:
        return self.message.extract_plain_text()

    @overrides(Event)
    def get_user_id(self) -> str:
        return str(self.user_id)

    @overrides(Event)
    def get_session_id(self) -> str:
        return str(self.user_id)

    @overrides(Event)
    def is_tome(self) -> bool:
        return self.to_me

    @classmethod
    def _parse_event(cls, obj: dict) -> 'Event':
        message = Message.parse_obj(obj)
        event = PrivateMessageEvent.parse_obj(obj)
        setattr(event, "message", message)
        return event


class PrivateMessageEvent(MessageEvent):
    # from_: User = Field(alias="from")
    __event__ = "message.private"

    # message_type: Literal["private"]
    @overrides(MessageEvent)
    def is_tome(self) -> bool:
        return True
