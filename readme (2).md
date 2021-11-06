# 模板项目

## 复制过去需要修改的文件列表

* 尽量用配置的方式，进行引用一次性修改完。
* tools.sh
* start.sh
* rqkscron
* config.py
* db_conf.py

## 现行环境下使用到的工具，插件。



## 如何使用？
- 执行init.py


## 思考
- 如何一键创建项目呢？

## 环境安装&&服务启动
`pip3 install -r requirements.txt -i https://pypi.douban.com/simple`
`uvicorn app.main:app --reload`


## 数据库
- 模板里没有使用到数据库模型
""" 附上三个SQLAlchemy教程

SQLAlchemy的基本操作大全 
    http://www.taodudu.cc/news/show-175725.html

Python3+SQLAlchemy+Sqlite3实现ORM教程 
    https://www.cnblogs.com/jiangxiaobo/p/12350561.html

SQLAlchemy基础知识 Autoflush和Autocommit
    https://zhuanlan.zhihu.com/p/48994990
"""
