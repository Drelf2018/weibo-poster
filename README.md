<p align="center">
  <a href="https://github.com/Drelf2018/weibo-poster/">
    <img src="https://user-images.githubusercontent.com/41439182/220989932-10aeb2f4-9526-4ec5-9991-b5960041be1f.png" height="200" alt="weibo-poster">
  </a>
</p>

<div align="center">

# weibo-poster

_✨ 基于 [weibo-webhook](https://github.com/Drelf2018/weibo-webhook) 的博文提交器 ✨_  


</div>

<p align="center">
  <a href="https://没写哈哈/">文档</a>
  ·
  <a href="https://pypi.org/project/weibo-poster/">下载</a>
  ·
  <a href="https://github.com/Drelf2018/weibo-poster/tree/main/test">开始使用</a>
</p>

额 pip 会用不

```python
pip install weibo-poster
```

python 会写不

```python
from weibo_poster import BiliGo, DanmakuPost, Poster, RoomInfo, WeiboRequest, logger

poster = Poster(188888131, "", "")
session = WeiboRequest("")
biligo = BiliGo("poster", "http://localhost:8080", 21452505)

PostList = list()

async def uidFilter(_: RoomInfo, danmaku: DanmakuPost):
    if danmaku.uid == "434334701":
        await danmaku.update()
        return True
    return False

@biligo.on("DANMU_MSG", uidFilter)
async def recv(roomInfo: RoomInfo, danmaku: DanmakuPost):
    logger.info(danmaku)

@Poster.job(name="七海", start=2, args=["7198559139"])
async def weibo(uid: str):
    await poster.online()
    post = None
    async for post in session.posts(uid):
        if post.mid not in PostList:
            PostList.append(post.mid)
            await poster.update(post)
    if post is not None:
        async for comment in session.comments(post):
            if comment.uid == uid:
                await poster.update(comment)

Poster.run(biligo.run, poster)
```

哦那你就会了