Title: SQLStore
Date: 2014-02-01 08:00

---
MySQL 数据库接口
----------------

### 简介

豆瓣使用 [MySQL](http://www.mysql.com/) 数据库。在豆瓣的代码中，有一个简单封装的数据库接口。
这个接口屏蔽了后端的复杂性，对使用者，只需要调用少数几个方法即可完成对数据库的访问。

### 访问方法

要访问数据库，需要使用 `code/libs/store.py` 中的 store 变量。store 是类 SqlStore 的单实例对象。
在调用它的模块中，要这样引用它

    from code.libs.store import store

SqlStore 使用第三方模块 [MySQLdb](http://sourceforge.net/projects/mysql-python/) 访问数据库。

参见：[《MySQLdb User's Guide》](http://mysql-python.sourceforge.net/MySQLdb.html "MySQLdb官方文档")

### 获得游标

在访问数据表之前，首先需要用 store 的 get_cursor 方法获得游标::

    cursor = store.get_cursor(table='user')

以上是要访问 user 表时，获得游标的方法。table 参数必须正确的传入参数，要与之后执行的 SQL 语句是同一个表名；
否则会导致访问数据失败。

如果同一个 cursor 要同时访问多个表，可以传入 tables 参数来调用

    cursor = store.get_cursor(tables=['user', 'user2'])

这时，要由调用者保证 user 和 user2 表是存储在同一个数据库中，否则，运行时会抛出错误。

警告：get_cursor 的 ro 参数已经作废。如果在任何代码中发现这个参数还在使用，请删掉。


### 执行 SQL

在获得游标之后，就可以通过游标执行 SQL 语句了。调用 execute 方法执行

    cursor.execute('select id, screen_name from user where id=%s', user_id)

多个参数时

    cursor.execute('insert into user2 (email, password, id) '
                   'values(%s, %s, %s)', (email, password, id))

警告：注意传递 SQL 参数的方法，必须把 SQL 和参数分别传给 execute。禁止用 Python 语法拼装 SQL 语句。
以下写法会带来很大的安全隐患（SQL 注入），是禁止使用的写法：

    # 有安全漏洞的调用方式，不应采用！
    cursor.execute('select id, screen_name from user where id=%s' % user_id)

注意：在被迫必须拼装 SQL 语句时，必须获得团队技术负责人的确认，完成后要进行代码复审。并且，
在拼装 SQL 的语句前，要有注释，说明原因。

execute 执行 UPDATE、DELETE 等语句后，会有返回值，通过返回值，可以知道这次执行共影响到多少行记录。


### 获取数据

执行 SELECT 之后，需要获得返回数据，通常有三种方式：fetchone，fetchall，迭代器。

  1. fetchone

    fetchone 可以获得一行返回数据

        row = cursor.fetchone()
        if row:
            id, screen_name = row

    如果没有数据，fetchone 将返回 None。

  2. fetchall

    fetchall 可以一次性获取所有检索的数据

        rows = cursor.fetchall()
        for row in rows:
            id, screen_name = row
            #...


    如果没有数据，fetchall 将返回一个空列表。

  3. 迭代器

    cursor 对象在执行 SELECT 之后，可以作为一个迭代器（Iterator）使用，顺序获取所有数据

        for row in cursor:
            id, screen_name = row
            #...

    获取多条数据时，推荐使用迭代器。因为迭代器使用简单，而且可以随处理随获取数据，速度快，节省内存。


### 数据库事务处理

豆瓣的数据库访问接口没有开启自动提交机制。所以，当执行 INSERT、UPDATE、DELETE 等修改数据的 SQL 语句后，
必须显式调用提交命令

    cursor.connection.commit()

数据处理失败，需要回滚已修改数据时，要调用

    cursor.connection.rollback()


### 访问单表时的简化

对于只访问一个表的情况，可以使用更简便的调用方式：直接使用 store 执行和获取数据。
下面是一个例子

    rows = store.execute('select id, screen_name from user where id=%s', id)
    for id, screen_name in rows:
        #...

    if store.execute('insert into user2 (email, password, id) '
                     'values(%s, %s, %s)', (email, password, id)):
        store.commit()

store 直接提供了游标的 execute、commit、rollback 方法，调用 execute 时会自动处理 get_cursor，使用合适的游标执行 SQL 语句。


### 关于表结构

豆瓣有多种存储设备，当要增加新表时，需要注意：

 * 较大的数据，如长文本，不应放入数据库（应放在分布式数据库DoubanDB中）
