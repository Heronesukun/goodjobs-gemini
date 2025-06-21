
class Config:
    # 本地的简历名称
    resume_name = 'resume.md'
    # Google AI Studio API配置
    api_key =   # 替换为您的API密钥
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
