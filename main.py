'''
Description: 入口函数
Author: 嘎嘣脆的贝爷
Date: 2025-02-14 13:01:28
LastEditTime: 2025-03-07 12:52:47
LastEditors: 嘎嘣脆的贝爷
'''

from fastapi import FastAPI, Body
from core import calcJobScore, replyMsg, isNeedResume, isNeedWorks
from cache import cache
from schema import Msg


app = FastAPI()


@app.get("/tags", summary="获取职位标签")
async def get_tags():
    return {
        'tags': cache.tags
    }


@app.get("/get-introduce", summary="获取自我介绍")
async def get_introduce():
    return {
        'introduce': cache.introduce
    }


@app.post("/get-job-score", summary="获取职位匹配度")
async def get_job_score(job: str = Body(..., description="职位信息")):
    return {
        'score': calcJobScore(job, cache.resume)
    }


@app.post("/reply", summary="回复消息")
async def reply(msgs: list[Msg] = Body(..., description="消息列表")):
    return replyMsg(msgs, cache.resume, cache.character)


@app.post("/is-need-resume", summary="是否需要简历")
async def is_need_resume(msgs: list[Msg] = Body(..., description="消息列表")):
    return {
        'need': isNeedResume(msgs)
    }


@app.post("/is-need-works", summary="是否需要作品集")
async def is_need_works(msgs: list[Msg] = Body(..., description="消息列表")):
    return {
        'need': isNeedWorks(msgs)
    }


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
