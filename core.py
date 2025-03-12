'''
Description: 一些具体实现
Author: 嘎嘣脆的贝爷
Date: 2025-02-16 01:13:59
LastEditTime: 2025-03-10 22:03:47
LastEditors: 嘎嘣脆的贝爷
'''
from ollama import chat, Message
from prompts import INTRODUCE, TAGS, CHARACTER, JOBSOURCE, CHAT, INTERSET, NEEDRESUME, NEEDWORKS
from config import Config
from tools import getLLMReply, getMatchScore
from schema import JobScore, InterestValue, NeedResume, NeedWorks
import json


# 默认参数
options = {
    "temperature": 0.6,
    "num_ctx": 10240
}


def __streamChat(sys_prompt: str, prompt: str, options: dict = options, model: str = Config.think_model) -> str:
    """自定义的流式回复"""
    content = ''
    for i in chat(model, [
        Message(role='system', content=sys_prompt),
        Message(role='user', content=prompt)
    ], stream=True, options=options):
        word = i.message.content
        content += word
        print(word, end="", flush=True)
    print()
    return getLLMReply(content)


def getIntroduce(resume: str):
    """生成自我介绍"""
    return __streamChat(INTRODUCE, resume)


def getTags(resume: str):
    """获取匹配标签"""
    return __streamChat(TAGS, resume).split(' ')


def getCharacter(resume: str):
    """获取性格特点"""
    return __streamChat(CHARACTER, resume)


def calcJobScore(job: str, resume: str):
    """计算职位匹配度"""
    content = ''
    for i in chat(Config.think_model, [
        Message(role='system', content=JOBSOURCE),
        Message(
            role='user',
            content=f"# 职位介绍:\n{job}\n\n# 我的简历:\n{resume}",
        )
    ], stream=True, options={
            "temperature": 0.6,
            "num_ctx": 10240,
    }):
        word = i.message.content
        content += word
        print(word, end="", flush=True)
    print()
    reply = getLLMReply(content)
    # 先直接提取数字
    r = getMatchScore(reply)
    if r != None:
        return r
    # 实在不行用大模型提取
    return json.loads(chat(Config.think_model, [
        Message(role='user', content='从以下内容中提取匹配度数值: \n' + reply),
    ], format=JobScore.model_json_schema()).message.content)['score']


def __calcInterestValue(msgs: list):
    """计算兴趣值"""
    msgs.insert(0, Message(role='system', content=INTERSET))
    return json.loads(chat(Config.chat_model, msgs, format=InterestValue.model_json_schema(), options={
        "temperature": 0.2,
        "num_ctx": 10240,
    }).message.content)['value']


def replyMsg(msgs: list, resume: str, character: str):
    # 计算兴趣值
    interest = __calcInterestValue(list(msgs))
    if not interest:
        return ''
    # 获取回复
    content = ''
    msgs.insert(0, Message(role='system', content=CHAT.format(
        resume=resume,
        character=character
    )))
    for i in chat(Config.chat_model, messages=msgs, stream=True, options={
        "temperature": 0.4,
        "num_ctx": 10240,
    }):
        word = i.message.content
        content += word
        print(word, end="", flush=True)
    print()
    return getLLMReply(content)


def isNeedResume(msgs: list):
    """判断是否需要简历"""
    msgs.insert(0, Message(role='system', content=NEEDRESUME))
    return json.loads(chat(Config.chat_model, msgs, format=NeedResume.model_json_schema(), options={
        "temperature": 0.2,
        "num_ctx": 10240,
    }).message.content)['need']


def isNeedWorks(msgs: list):
    """判断是否需要作品集"""
    msgs.insert(0, Message(role='system', content=NEEDWORKS))
    return json.loads(chat(Config.chat_model, msgs, format=NeedWorks.model_json_schema(), options={
        "temperature": 0.2,
        "num_ctx": 10240,
    }).message.content)['need']
