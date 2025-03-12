# AI 帮你找工作
- 目前支持平台：
  - boss直聘
- 目前实现的功能：
  - 根据职位匹配度打招呼
  - 投递简历
  - 代聊天
## 将项目下载到本地
```
// github
git clone https://github.com/gbcdby/goodjobs.git

// gitee
git clone https://gitee.com/gbcdby/goodjobs.git
```
## 安装Ollama
项目的模型服务依赖ollama，可以参考[ollama](https://ollama.ai/)
## 安装python的后端依赖
```
// 进入项目目录
cd goodJobs

// 安装依赖
pip install -r requirements.txt
```
将本地的简历示例md文件替换成自己的简历
```
cp resume-example.md resume.md
```
然后将 resume.md 文件中的内容替换成自己的简历，markdown 格式，可以通过 kimi 等大模型提取

config.py文件中可以切换思考与聊天模型

最后启动后端服务
```
python main.py
```
## 部署浏览器插件
页面操作依赖篡改猴插件，下载完毕后将 web_script.js 文件的内容粘贴到插件中，然后访问boss直聘网站即可