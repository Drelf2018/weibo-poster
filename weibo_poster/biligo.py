from dataclasses import dataclass
from json import loads
from typing import Callable, Coroutine

import httpx
from aiowebsocket.converses import AioWebSocket
from bilibili_api.user import User
from bilibili_api.utils.AsyncEvent import AsyncEvent

from .utils import Post, isAsync, logger


class DanmakuPost(Post):
    @classmethod
    def transform(cls: "DanmakuPost", event: dict):
        content: dict = event["content"]
        info: list = content["info"]
        pic: str = ""
        if isinstance(info[0][13], dict):  
            pic = info[0][13].get("url", "")
        time = int(info[0][4] / 1000)
        roomid = str(event["live_info"]["room_id"])
        return {
            "mid": f"{roomid}_{time}",
            "time": time,
            "text": info[1],
            "type": "danmaku",
            "source": roomid,

            "uid": str(info[2][0]),
            "name": info[2][1],
            "face": "",
            "pendant": "",
            "description": "",

            "follower": "",
            "following": "",

            "attachment": [],
            "picUrls": [pic] if pic else [],
            "repost": None
        }

    async def update(self):
        user = User(self.uid)
        data = await user.get_user_info()
        self.face = data["face"]
        self.pendant = data.get("pendant", {}).get("image", "")
        self.description = data["sign"]
        data = await user.get_relation_info()
        self.follower = data["follower"]
        self.following = data["following"]
        return self


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

    def on(self, event_name: str, filter: Callable = lambda *_, **__: True) -> Callable:
        """
        装饰器注册事件监听器。

        Args:
            event_name (str): 事件名。
        """
        def decorator(func: Coroutine):
            isAsyncFunction = isAsync(filter)
            async def wapper(args):
                if isAsyncFunction:
                    if not await filter(*args):
                        return
                elif not filter(*args):
                    return
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
                if evt["command"] == "DANMU_MSG":
                    self.dispatch(evt["command"], (RoomInfo(**evt["live_info"]), DanmakuPost.parse(evt)))
