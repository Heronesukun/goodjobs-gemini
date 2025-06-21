
# 导入Google GenAI SDK
from google import genai
from google.genai import types
from prompts import INTRODUCE, TAGS, CHARACTER, JOBSOURCE, CHAT, INTERSET, NEEDRESUME, NEEDWORKS
from config import Config
from tools import getLLMReply, getMatchScore
from schema import JobScore, InterestValue, NeedResume, NeedWorks
import json

# 初始化Google GenAI客户端
client = genai.Client(api_key=Config.api_key)

# 默认参数
options = Config.default_options


def __streamChat(sys_prompt: str, prompt: str, options: dict = options, model: str = Config.think_model) -> str:
    """自定义的流式回复"""
    content = ''
    # 创建消息内容 - 移除system role的Content
    contents = [
        types.Part.from_text(text=prompt)
    ]
    
    # 配置生成参数 - 添加system_instruction
    config = types.GenerateContentConfig(
        system_instruction=sys_prompt,
        temperature=options.get("temperature", 0.6),
        max_output_tokens=options.get("max_output_tokens", 8192),
    )
    
    # 流式生成内容
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=config
    ):
        if chunk.text:
            word = chunk.text
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
    # 创建消息内容
    contents = [
        types.Part.from_text(text=f"# 职位介绍:\n{job}\n\n# 我的简历:\n{resume}")
    ]
    
    # 配置生成参数
    config = types.GenerateContentConfig(
        system_instruction=JOBSOURCE,
        temperature=options.get("temperature", 0.6),
        max_output_tokens=options.get("max_output_tokens", 8192),
    )
    
    # 流式生成内容
    for chunk in client.models.generate_content_stream(
        model=Config.think_model,
        contents=contents,
        config=config
    ):
        if chunk.text:
            word = chunk.text
            content += word
            print(word, end="", flush=True)
    print()
    reply = getLLMReply(content)
    # 先直接提取数字
    r = getMatchScore(reply)
    if r is not None:
        return r
    # 实在不行用大模型提取
    extract_contents = [
        types.Part.from_text(text=f"从以下内容中提取匹配度数值: \n{reply}")
    ]
    
    # 配置生成参数，使用结构化输出
    extract_config = types.GenerateContentConfig(
        temperature=0.2,
        response_mime_type="application/json",
        response_schema={
            "type": "object",
            "properties": {
                "score": {"type": "integer", "description": "匹配度分数"}
            },
            "required": ["score"]
        }
    )
    
    response = client.models.generate_content(
        model=Config.think_model,
        contents=extract_contents,
        config=extract_config
    )
    
    return json.loads(response.text)["score"]


def __calcInterestValue(msgs: list):
    """计算兴趣值"""
    # 创建消息内容
    contents = []
    
    # 添加对话历史
    for msg in msgs:
        contents.append(types.Part.from_text(text=msg.content))
    
    # 配置生成参数，使用结构化输出
    config = types.GenerateContentConfig(
        system_instruction=INTERSET,
        temperature=0.2,
        response_mime_type="application/json",
        response_schema={
            "type": "object",
            "properties": {
                "value": {"type": "boolean", "description": "是否感兴趣"}
            },
            "required": ["value"]
        }
    )
    
    response = client.models.generate_content(
        model=Config.chat_model,
        contents=contents,
        config=config
    )
    
    return json.loads(response.text)["value"]


def replyMsg(msgs: list, resume: str, character: str):
    # 计算兴趣值
    interest = __calcInterestValue(list(msgs))
    if not interest:
        return ''
    # 获取回复
    content = ''
    
    # 创建系统提示
    system_prompt = CHAT.format(
        resume=resume,
        character=character
    )
    
    # 创建消息内容
    contents = []
    
    # 添加对话历史
    for msg in msgs:
        contents.append(types.Part.from_text(text=msg.content))
    
    # 配置生成参数
    config = types.GenerateContentConfig(
        system_instruction=system_prompt,
        temperature=0.4,
        max_output_tokens=options.get("max_output_tokens", 8192),
    )
    
    # 流式生成内容
    for chunk in client.models.generate_content_stream(
        model=Config.chat_model,
        contents=contents,
        config=config
    ):
        if chunk.text:
            word = chunk.text
            content += word
            print(word, end="", flush=True)
    print()
    return getLLMReply(content)


def isNeedResume(msgs: list):
    """判断是否需要简历"""
    # 创建消息内容
    contents = []
    
    # 添加对话历史
    for msg in msgs:
        contents.append(types.Part.from_text(text=msg.content))
    
    # 配置生成参数，使用结构化输出
    config = types.GenerateContentConfig(
        system_instruction=NEEDRESUME,
        temperature=0.2,
        response_mime_type="application/json",
        response_schema={
            "type": "object",
            "properties": {
                "need": {"type": "boolean", "description": "是否需要简历"}
            },
            "required": ["need"]
        }
    )
    
    response = client.models.generate_content(
        model=Config.chat_model,
        contents=contents,
        config=config
    )
    
    return json.loads(response.text)["need"]


def isNeedWorks(msgs: list):
    """判断是否需要作品集"""
    # 创建消息内容
    contents = []
    
    # 添加对话历史
    for msg in msgs:
        contents.append(types.Part.from_text(text=msg.content))
    
    # 配置生成参数，使用结构化输出
    config = types.GenerateContentConfig(
        system_instruction=NEEDWORKS,
        temperature=0.2,
        response_mime_type="application/json",
        response_schema={
            "type": "object",
            "properties": {
                "need": {"type": "boolean", "description": "是否需要作品集"}
            },
            "required": ["need"]
        }
    )
    
    response = client.models.generate_content(
        model=Config.chat_model,
        contents=contents,
        config=config
    )
    
    return json.loads(response.text)["need"]
