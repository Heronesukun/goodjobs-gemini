```
# AI 帮你找工作
支持boss直聘网页版的自动找工作程序

## 功能特性

- 🎯 **智能职位匹配**：根据简历内容自动计算职位匹配度
- 💬 **自动打招呼**：生成个性化的求职打招呼语
- 📄 **智能简历投递**：自动判断是否需要投递简历
- 🤖 **AI代聊天**：模拟真实求职者与HR进行对话
- 🏢 **平台支持**：目前支持Boss直聘平台

## 环境要求

- Python 3.8+
- Google AI Studio API Key

## 快速开始

### 1. 克隆项目

```bash
# GitHub
git clone https://github.com/gbcdby/goodjobs.
git
cd goodjobs

```
### 2. 安装依赖
```
pip install -r requirements.txt
```
主要依赖包括：

- fastapi==0.115.8
- pydantic==2.10.6
- uvicorn==0.34.0
- google-genai==0.8.5
### 3. 获取Google AI Studio API Key
1. 访问 Google AI Studio
2. 登录您的Google账号
3. 点击「Get API Key」创建新的API密钥
4. 复制生成的API密钥
### 4. 配置API Key
编辑 config.py 文件，将您的API密钥替换到相应位置：

```
class Config:
    # Google AI Studio API配置
    api_key = '您的API密钥'  # 替换为您的实际API密
    钥
```
### 5. 准备简历文件
1. 将您的简历保存为 resume.md 文件（Markdown格式）
2. 如果没有Markdown格式的简历，可以使用Kimi、ChatGPT等AI工具将您的简历转换为Markdown格式
3. 确保简历文件放在项目根目录下
### 6. 启动服务
```
python main.py
```
服务启动后，API将在 http://0.0.0.0:8000 上运行。

### 7. 部署浏览器插件
1. 安装浏览器插件管理器（如Tampermonkey）
2. 创建新的用户脚本
3. 将 web_script.js 文件的内容复制到脚本中
4. 保存并启用脚本
5. 访问Boss直聘网站即可使用

### 8. 其他问题
如果遇上插件不起作用，暂停再打开插件，或者刷新页面，也可以尝试联系原作者（油猴脚本我不会）
本代码源代码地址为https://gitee.com/gbcdby/goodjobs
复刻的目的是为了帮助像我这样本地无法流畅运行ollama的因此使用外接api
