import sys
import asyncio
if sys.platform != "win32":
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

from fastapi import FastAPI, Response, Depends
from fastapi.middleware.cors import CORSMiddleware

from src.utils.asyncMySQL import AsyncMySQL
from src.utils.parseDateTime import parseDateTime


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.on_event("startup")
async def startup():
    global db
    db = AsyncMySQL()
    await db.init()


@app.on_event("shutdown")
async def shutdown():
    await db.close()


@app.get("/history")
async def get_history(uid: str, page: int = 1, isReverse: bool = False):

    res = await db.search("CID,update_time", "history", f"UID={uid}",
                          f"{(page-1)*20},{page*20}",
                          f"update_time {'ASC' if isReverse else 'DESC'}")

    ret_list = [{
        "cid": item[0],
        "update_time":parseDateTime(item[1])
    } for item in res]

    return ret_list


@app.delete("/history")
async def delete_history(uid: str):
    await db.delete("history", f"UID={uid}")
    return Response(status_code=200)


@app.post("/record")
async def update_history(uid: str, cid: str):

    res = await db.search("CID", "history", f"UID={uid}", "1", "update_time DESC")

    if(res == () or str(res[0][0]) != cid):
        await db.insert("history", "UID,CID,update_time", f"{uid},{cid},NOW()")
    else:
        return Response(status_code=200)
    
    return Response(status_code=201)


@ app.get("/tags")
async def get_tags(uid: str):

    res = await db.search("tag", "tags", f"UID={uid}")

    return res


@ app.post("/tag")
async def update_tag(uid: str, tag: str):
    if(await db.search("tag", "tags", f"UID={uid} AND tag='{tag}'")):
        return Response(status_code=200)
    else:
        await db.insert("tags", "UID,tag", f"{uid},'{tag}'")
    return Response(status_code=201)


@ app.get("/comments")
async def get_comments(aid: str = None, uid: str = None, page: int = 1, isReverse: bool = False):

    if(aid and uid):
        return Response(status_code=400)
    elif(aid):
        res = await db.search("UID,AID,comment,comment_time", "comments", f"AID={aid}",
                              f"{(page-1)*20},{page*20}",
                              f"comment_time {'ASC' if isReverse else 'DESC'}")
    elif(uid):
        res = await db.search("UID,AID,comment,comment_time", "comments", f"UID={uid}",
                              f"{(page-1)*20},{page*20}",
                              f"comment_time {'ASC' if isReverse else 'DESC'}")
    else:
        return Response(status_code=400)

    ret_list = [{
        "uid": item[0],
        "aid": item[1],
        "comment": item[2],
        "comment_time": parseDateTime(item[3])
    } for item in res]

    return ret_list
