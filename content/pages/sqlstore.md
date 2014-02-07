Title: SQLStore
Date: 2014-02-01 08:00

数据库接口sqlstore
=================

简介
----

豆瓣使用[MySQL](http://www.mysql.com/)数据库。在豆瓣的代码中，有一个简单封装的数据库接口。这个接口屏蔽了后端的复杂性，对使用者，只需要调用少数几个方法即可完成对数据库的访问。

访问途径
-------

要访问数据库，需要使用 `luzong/sqlstore.py` 中的store变量。store是类SqlStore的单实例对象。在调用它的模块中，要这样引用它


    from luzong.sqlstore import store


SqlStore使用第三方模块[MySQLdb](http://sourceforge.net/projects/mysql-python/)访问数据库。

参见：[《MySQLdb User's Guide》](http://mysql-python.sourceforge.net/MySQLdb.html "MySQLdb官方文档") 


获得游标
-------

在访问数据表之前，首先需要用store的get_cursor方法获得游标::

    cursor = store.get_cursor(table='user')
    

以上是要访问user表时，获得游标的方法。table参数必须正确的传入参数，要与之后执行的SQL语句是同一个表名；否则会导致访问数据失败。

如果同一个cursor要同时访问多个表，可以传入tables参数来调用


    cursor = store.get_cursor(tables=['user', 'user2'])


这时，要由调用者保证user和user2表是存储在同一个数据库中，否则，运行时会抛出错误。

警告：get_cursor的ro参数已经作废。如果在任何代码中发现这个参数还在使用，请删掉。


执行SQL
-------

在获得游标之后，就可以通过游标执行SQL语句了。调用execute方法执行


    cursor.execute('select id, screen_name from user where id=%s', user_id)


多个参数时::


    cursor.execute('insert into user2 (email, password, id) '
                   'values(%s, %s, %s)', (email, password, id))


警告：注意传递SQL参数的方法，必须把SQL和参数分别传给execute。禁止用Python语法拼装SQL语句。以下写法会带来很大的安全隐患（SQL注入），是禁止使用的写法：


    # 有安全漏洞的调用方式，不应采用！
    cursor.execute('select id, screen_name from user where id=%s' % user_id)


注意：在被迫必须拼装SQL语句时，必须获得团队技术负责人的确认，完成后要进行代码复审。并且，在拼装SQL的语句前，要有注释，说明原因。

execute执行UPDATE、DELETE等语句后，会有返回值，通过返回值，可以知道这次执行共影响到多少行记录。


获取数据
-------

执行SELECT之后，需要获得返回数据，通常有三种方式：fetchone，fetchall，迭代器。


  1. fetchone

    fetchone可以获得一行返回数据
    
        row = cursor.fetchone()
        if row:
            id, screen_name = row

    如果没有数据，fetchone将返回None。

  2. fetchall

    fetchall可以一次性获取所有检索的数据::


        rows = cursor.fetchall()
        for row in rows:
            id, screen_name = row
            #...


    如果没有数据，fetchall将返回一个空列表。

  3. 迭代器

    cursor对象在执行SELECT之后，可以作为一个迭代器（Iterator）使用，顺序获取所有数据::

        for row in cursor:
            id, screen_name = row
            #...


    获取多条数据时，推荐使用迭代器。因为迭代器使用简单，而且可以随处理随获取数据，速度快，节省内存。


数据库事务处理
------------

豆瓣的数据库访问接口没有开启自动提交机制。所以，当执行INSERT、UPDATE、DELETE等修改数据的SQL语句后，必须显式调用提交命令::

    cursor.connection.commit()

数据处理失败，需要回滚已修改数据时，要调用::

    cursor.connection.rollback()


访问单表时的简化
--------------

对于只访问一个表的情况，可以使用更简便的调用方式：直接使用store执行和获取数据。下面是一个例子


    rows = store.execute('select id, screen_name from user where id=%s', id)
    for id, screen_name in rows:
        #...

    if store.execute('insert into user2 (email, password, id) '
                     'values(%s, %s, %s)', (email, password, id)):
        store.commit()


store直接提供了游标的execute、commit、rollback方法，调用execute时会自动处理get_cursor，使用合适的游标执行SQL语句。


关于表结构
---------


豆瓣有多种存储设备，当要增加新表时，需要注意：

 * 较大的数据，如长文本，不应放入数据库（应放在分布式数据库DoubanDB中）
