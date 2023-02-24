from weibo_poster import Poster, WeiboRequest, BiliGo, RoomInfo, logger

poster = Poster(188888131, "e2ac9d62-bf44-4672-8cbb-2b420bc5cb0f", "http://localhost:5664")
biligo = BiliGo("poster", "http://localhost:8080", 14703541)

@biligo.on("DANMU_MSG")
async def recv(roomInfo: RoomInfo, event: dict):
    info = event['info']
    logger.info(f'{roomInfo.room_id} {info[2][1]} {info[1]}')

async def weibo(uid: str):
    post = None
    async for post in session.posts(uid):
        await poster.update(post)
    if post is not None:
        async for comment in session.comments(post):
            if comment.uid == uid:
                await poster.update(comment)

Poster.add_job(fn=weibo, name="七海", count=1, start=2, args=["7198559139"])
Poster.run(Poster.stepBrother, poster)