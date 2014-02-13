Title: Getting started
Date: 2014-02-01 08:00

---
目前 CODE 仅开放了一个框架，支持：

* clone & push project
* create project
* create user

### 准备环境

* MySQL
* Memcached
* Python
* pip
* virtualenv
* git

### 开发

```
git clone https://github.com/douban-code/code.git
cd code
mysql -uroot -e 'create database valentine;'
mysql -uroot -D valentine < code/databases/schema.sql
virtualenv venv
. venv/bin/activate
pip install cython
pip install -U setuptools
pip install -r requirements.txt
gunicorn -b 127.0.0.1:8000 app:app
```
