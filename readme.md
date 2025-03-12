# AI 帮你找工作
- 目前支持平台：
  - boss直聘
- 目前实现的功能：
  - 根据职位匹配度打招呼
  - 投递简历
  - 代聊天
## 准备工作
将项目 git 到本地
```
git clone xxx
```
安装依赖
```
cd goodJobs
pip install -r requirements.txt
```
将本地的简历 md 文件替换成自己的简历
```
cp resume-example.md resume.md
```
然后将文件中的内容替换成自己的简历，md 格式，可以通过 kimi 等大模型提取

---
## 运行项目
```
python main.py
```