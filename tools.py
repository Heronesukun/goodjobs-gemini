'''
Description: 工具
Author: 嘎嘣脆的贝爷
Date: 2025-02-14 22:31:43
LastEditTime: 2025-02-16 01:12:05
LastEditors: 嘎嘣脆的贝爷
'''
import re


def getLLMReply(content: str) -> str:
    """
    获取大模型的回复
    """
    return content.split('</think>\n')[-1].strip()


def getMatchScore(text: str) -> int | None:
    """从文本直接获取匹配度数值"""
    # 如果只有数值
    if re.search('^\d+$', text):
        return int(text)
    # 分成多行，寻找匹配度
    for i in text.split('\n'):
        if re.search('匹配.*?\d+', i):
            return int(re.search('\d+', i).group())
