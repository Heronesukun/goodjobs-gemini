'''
Description: 配置文件
Author: 嘎嘣脆的贝爷
Date: 2025-02-14 21:56:01
LastEditTime: 2025-02-17 22:57:26
LastEditors: 嘎嘣脆的贝爷
'''


class Config:
    # 本地的简历名称
    resume_name = 'resume.md'
    # Google AI Studio API配置
    api_key = 'AIzaSyC8Rt30A_nZsEcV17r-ZG_MnpCxdQPDVx4'  # 替换为您的API密钥
    # 模型配置
    think_model = 'gemini-2.0-flash'  # 思考模型
    chat_model = 'gemini-2.0-flash'   # 聊天模型
    # 默认参数
    default_options = {
        "temperature": 0.6,
        "max_output_tokens": 8192,
    }
    # # 思考模型
    # think_model = 'qwen3'
    # # 聊天模型
    # chat_model = 'qwen3'
