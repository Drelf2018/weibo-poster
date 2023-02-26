from weibo_poster import BiliGo, DanmakuPost, Poster, RoomInfo, WeiboRequest, logger

poster = Poster(188888131, "e2ac9d62-bf44-4672-8cbb-2b420bc5cb0f", "http://localhost:5664")
biligo = BiliGo("poster", "http://localhost:8080", 14703541)
PostList = list()

async def uidFilter(_: RoomInfo, danmaku: DanmakuPost):
    if danmaku.uid == "188888131":
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