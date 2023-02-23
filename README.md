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
from bilibili_api.live import LiveDanmaku
from weibo_poster import Poster, WeiboRequest

room = LiveDanmaku(21452505)
poster = Poster(188888131, "", "")
session = WeiboRequest("")


@room.on("DANMU_MSG")
async def recv(event):
    print("1")

async def weibo(uid: str):
    post = None
    async for post in session.posts(uid):
        await poster.update(post)
    if post is not None:
        async for comment in session.comments(post):
            if comment.uid == uid:
                await poster.update(comment)

Poster.add_job(fn=weibo, name="七海", count=1, start=2, args=["7198559139"])
Poster.run(room.connect, poster)
```

哦那你就会了