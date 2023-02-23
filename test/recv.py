from apscheduler.schedulers.asyncio import AsyncIOScheduler
from weibo_poster import Poster, Post, logger, parse_text, get_content, countLog
import asyncio

scheduler = AsyncIOScheduler()

@countLog(1)
async def get():
    try:
        for pdata in await poster.post():
            post = Post.parse(pdata)
            ...
        print(post)
        print(post.data)
        ts, _ = parse_text(post.text)
        content = get_content(ts)
        logger.info(content)
    except Exception as e:
        logger.error(e)

scheduler.add_job(get, "interval", seconds=5)

async def main():
    await poster.login()
    scheduler.start()
    while True:
        await asyncio.sleep(1)

asyncio.new_event_loop().run_until_complete(main())