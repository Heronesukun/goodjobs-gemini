'''
Description: 程序缓存
Author: 嘎嘣脆的贝爷
Date: 2025-02-16 17:15:30
LastEditTime: 2025-02-16 19:22:40
LastEditors: 嘎嘣脆的贝爷
'''
import os
import json
from core import getIntroduce, getTags, getCharacter
from config import Config


class Cache:
    def __init__(self):
        if not os.path.exists(Config.resume_name):
            raise FileNotFoundError('未找到简历文件')
        resume_lock_name = '-lock.'.join(Config.resume_name.split('.'))
        if os.path.exists(resume_lock_name):
            with open(resume_lock_name, 'r')as f:
                resume_lock = f.read()
        else:
            resume_lock = ''
        with open(Config.resume_name, 'r')as f:
            self.resume = f.read()
        if self.resume != resume_lock or not os.path.exists('cache.json'):
            with open(resume_lock_name, 'w')as f:
                f.write(self.resume)
            self.introduce = getIntroduce(self.resume)
            self.character = getCharacter(self.resume)
            self.tags = getTags(self.resume)
            with open('cache.json', 'w')as f:
                f.write(json.dumps({
                    'introduce': self.introduce,
                    'character': self.character,
                    'tags': self.tags,
                }, ensure_ascii=False))
        else:
            with open('cache.json', 'r')as f:
                cache = json.loads(f.read())
                self.introduce = cache.get('introduce')
                self.character = cache.get('character')
                self.tags = cache.get('tags', [])


cache = Cache()
