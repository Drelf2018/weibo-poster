from bilibili_api.live import LiveDanmaku
from weibo_poster import Poster, WeiboRequest

room = LiveDanmaku(21452505)


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