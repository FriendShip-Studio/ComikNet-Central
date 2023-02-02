import sys
import asyncio
import datetime
import aiomysql
if sys.platform != "win32":
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from src.models.database import history, tags, comments
from src.config.database_conn import TORTOISE_ORM_CONFIG

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

register_tortoise(
    app, config=TORTOISE_ORM_CONFIG, add_exception_handlers=True,
    generate_schemas=False)


@app.post("/record")
async def update_history(uid: int, cid: int):

    if((await history.filter(uid=uid).count() != 0) and (await history.filter(uid=uid).order_by("-update_time").first()).cid == cid):
        return Response(status_code=200)
    else:
        await history.create(uid=uid, cid=cid, update_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    return Response(status_code=201)


@app.get("/latestHistory")
async def get_latest_history(uid: int):
    res = await history.filter(uid=uid).order_by("-update_time").first()
    if res is None:
        return None
    else:
        return {
            "cid": res.cid,
            "update_date": res.update_time.strftime("%Y-%m-%d"),
            "update_time": res.update_time.strftime("%H:%M:%S")
        }


@app.get("/history")
async def get_history(uid: int):

    if((await history.filter(uid=uid).count()) == 0):
        return []

    res_list = []
    for res in await history.filter(uid=uid).order_by("-update_time").all():
        res_list.append({
            "cid": res.cid,
            "update_date": res.update_time.strftime("%Y-%m-%d"),
            "update_time": res.update_time.strftime("%H:%M:%S")
        })

    return res_list


@app.post("/tag")
async def update_tag(uid: int, tag: str):

    if((await tags.filter(uid=uid, tag=tag).count()) != 0):
        return Response(status_code=200)
    else:
        await tags.create(uid=uid, tag=tag)
        return Response(status_code=201)


@app.get("/tags")
async def get_tags(uid: int):

    res_list = []
    for res in await tags.filter(uid=uid).all():
        res_list.append(res.tag)
    return res_list


@app.post("/comment")
async def send_comment(uid: int, aid: int, comment: str):

    await comments.create(uid=uid, aid=aid, comment=comment, comment_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    return Response(status_code=201)


@app.get("/comments")
async def get_comments(aid: int = None, uid: int = None):

    if((aid is not None and uid is not None) or (uid is None and aid is None)):
        return Response(status_code=400)

    res_list = []
    if(aid is not None):
        for res in await comments.filter(aid=aid).all():
            res_list.append({
                "aid": res.aid,
                "uid": res.uid,
                "comment": res.comment,
                "comment_time": res.comment_time.strftime("%Y-%m-%d %H:%M:%S")
            })
        return res_list
    else:
        for res in await comments.filter(uid=uid).all():
            res_list.append({
                "aid": res.aid,
                "uid": res.uid,
                "comment": res.comment,
                "comment_time": res.comment_time.strftime("%Y-%m-%d %H:%M:%S")
            })
        return res_list
