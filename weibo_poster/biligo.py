from json import loads
from typing import Callable, Coroutine
from dataclasses import dataclass

import httpx
from aiowebsocket.converses import AioWebSocket
from bilibili_api.utils.AsyncEvent import AsyncEvent

from .utils import logger


@dataclass
class RoomInfo:
    room_id: int
    uid: int
    title: str
    name: str
    cover: str
    user_face: str
    user_description: str


class Receive:
    "异步接收"

    def __init__(self, recv: Callable):
        self.recv = recv

    def __aiter__(self):
        return self

    async def __anext__(self):
        return loads(await self.recv())


class BiliGo(AsyncEvent):
    """
    连接 biligo-ws-live 的适配器
    """

    def __init__(self, aid: str, url: str, *listening_rooms):
        super().__init__()
        #  接入 biligo-ws-live 时的 id 用来区分不同监控程序
        self.aid = aid
        # biligo-ws-live 运行地址
        self.url = url
        # 将监听房间号告知 biligo-ws-live
        httpx.post(self.url+'/subscribe', headers={"Authorization": self.aid}, data={'subscribes': list(listening_rooms)})

    def on(self, event_name: str) -> Callable:
        """
        装饰器注册事件监听器。

        Args:
            event_name (str): 事件名。
        """
        def decorator(func: Coroutine):
            async def wapper(args):
                return await func(*args)

            self.add_event_listener(event_name, wapper)
            return func

        return decorator

    async def run(self):
        """
        阻塞异步连接
        """

        async with AioWebSocket(self.url + f"/ws?id={self.aid}") as aws:
            logger.info('Adapter 连接成功')
            async for evt in Receive(aws.manipulator.receive):
                roomInfo = RoomInfo(**evt["live_info"])
                self.dispatch(evt['command'], (roomInfo, evt["content"]))
