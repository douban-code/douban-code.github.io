Title: Getting started
Date: 2014-02-01 08:00

---
目前 CODE 仅开放了一个框架，支持：

* clone & push project
* create project
* create user

---
### 准备环境

* MySQL
* Memcached
* Python >= 2.7
* pip >= 1.4.1
* virtualenv
* git

---
### 部署

```
git clone https://github.com/douban/code.git
cd code
mysql -uroot -e 'create database valentine;'
mysql -uroot -D valentine < code/databases/schema.sql
virtualenv venv
. venv/bin/activate
pip install cython
pip install -U setuptools
pip install -r requirements.txt
gunicorn -w 2 -b 127.0.0.1:8000 app:app
```

---
### 定制 config

* 创建自己的 config 文件

```
touch {CODE_REPO}/code/local_config.py
```

* 覆盖 `code/config.py` 默认设置

```
vim {CODE_REPO}/code/local_config.py
```

---
### FAQ

1. code.config.DOMAIN 是指的是程序运行的域名，包含IP地址和端口，例如: `http://127.0.0.1:8000/`
