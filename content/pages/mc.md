Title: MC
Date: 2014-02-01 08:00

缓存接口mc简介
------------
缓存是优化系统性能的工具。豆瓣使用[Memcached](http://memcached.org/)作为缓存系统，通过一个单实例的变量作为该系统的访问接口。

访问途径
-------

要访问缓存，需要使用 `corelib/mc.py` 中的mc变量。mc是类cmemcached.Client的单实例对象。在调用它的模块中，要这样引用它

    from corelib.mc import mc

API
---

Memcached的接口非常简单。它是一个键值对（key-value pair）存储系统，最常用的是设置、获取和删除操作。

### set：设置

在Memcached中，添加操作与修改操作相同。要设置一个值，可以调用：

    key = 'user_number'
    value = 100
    mc.set(key, value)


这个缓存设置之后，会一直存在，直到被删除，或者存储不够用，被新的内容从内存中挤出去。如果要让内容自动过期，可以：

    USER_NUMBER_EXPIRES = 3600
    mc.set(key, value, USER_NUMBER_EXPIRES)


通过第三个参数掺入过期时间，以秒为单位。

### get，get_multi：获取

随时可以从缓存中重新获得放入的数据：

    value = mc.get(key)


如果这个key在缓存中不存在，或者已经过期，get方法将返回None。

还可以一次获取多个键值的内容，提高访问效率：

    values = mc.get_multi([key1, key2, key3])

### delete：删除

删除操作会把缓存中的指定键值立即过期：

    mc.delete(key)

### incr，decr：自增，自减

如果保存值是整形，还可以通过incr和decr对数据直接增加或减少：

    mc.incr(key)
    mc.decr(key)


默认自增或自减1。也可以制定要增减的量：

    mc.incr(key, 10)


缓存原则
-------

首先，必须要认识到：缓存是对性能做优化的手段，而不是开发的目的。在开发过程中，缓存应该是最后被引入的内容。代码不应该依赖于缓存，没有缓存支持，代码也应该可以正常运行。

另外，基于数据更新的考虑，对于放入缓存的内容，我们有以下原则：

1. 类的实例化对象，应该单独缓存，每个key只缓存一个对象
2. 禁止缓存类的实例化对象的列表
3. 缓存的值是列表时，列表中的每个值应该是简单类型，比如对象的id

这个原则的目的是为了避免这种情况：

  假设，类User的实例user1，同时存在于1000个用户的关注列表中。当user1修改了自己的网名时，我们需要把1000个用户的关注列表全部过期，否则user1在这些用户的列表中的网名永远都不能正确显示。

这样存储对象的列表的大量过期，会带来很严重的问题：

* 缓存过期频繁，缓存命中率过低
* 难以维护对象与相关列表的对应关系，甚至无法找到所有缓存该对象的相关列表，执行过期操作

对应这个例子，豆瓣实际采用的缓存策略是：

  user1只在一个key（u:user1_id）中缓存，其他所有相关的列表，都只存储user_id。

这样在任何需要使用user1的地方，都可以从 u:user1_id 这个缓存中得到user1的最新信息，从而避免了缓存不一致的问题。

命名规则
-------

mc命名规范基本为：

    功能名称:id
    功能名称:id:id2:id3


例如：

    minisite:converse
    page_by_name:pk14:2002


在命名中，冒号“:”用来分割功能名称及各id，下划线“_”用来在功能名称中代替空格。

在使用缓存时，要注意缓存名称不会出现冲突。在比较早的代码中，缓存名称中的功能名称经常使用缩写。这类缩写在 ``luzong/__init__.py`` 中通过手工记录，以防止重名。在现在的代码中，功能名称部分都采用更易读的方式，其中包含所在模块、所在类、所在产品线的代号等，把重名范围限制在模块、类或产品线内部，由产品线工程师维护，负责避免重名。

注意：

  缓存中key的名字必须是字符串类型，并且不允许包含空格：chr(32)以及小于chr(32)的任何控制字符。utf-8字符是允许的。常见的错误，就是把用户输入的内容未经过滤，直接作为cache key的一部分；需要大家根据自己的应用，生成key时做过滤、变换、转义等必须的处理。

应用实例
-------

### 取内容

下面是取一个相册图片示例的方法（代码已经过改造），典型的取一个对象的例子：

     def get_photo(photo_id):
         key = 'photo:%s' % photo_id
         photo = mc.get(key)
         if photo is None:
             cursor = store.get_cursor(table='photo')
             cursor.execute('select id, creator_id, album_id, create_time, '
                            'n_comments, properties, privacy '
                            'from photo where id=%s', photo_id)
             row = cursor.fetchone()
             if row:
                 photo = Photo(*row)
                 mc.set(key, photo)
         return photo


下面是取一个列表中所有图片的方法，典型的取一个列表的例子：

     def get_photos(photo_ids):
         ps = mc.get_multi(['photo:%s' % id for id in photo_ids])
         all_photos = [id and ps.get('photo:%s' % id) or get_photo(id)
                       for id in photo_ids]
         return all_photos


请通过上面两个例子，重新回顾“缓存原则”。

### 用装饰符cache简化编程

用 `luzong/utils` 中的decorator可以简化取单个对象的例子：

     from luzong.utils import cache

     @cache('photo:{photo_id}')
     def get_photo(photo_id):
         cursor = store.get_cursor(table='photo')
         cursor.execute('select id, creator_id, album_id, create_time, '
                        'n_comments, properties, privacy '
                        'from photo where id=%s', photo_id)
         row = cursor.fetchone()
         if row:
                return Photo(*row)


这样，开发时只针对数据库编程，在代码完成后针对适当的函数添加cache装饰符，即可完成性能优化的工作。

### 用装饰符pcache简化编程

`luzong/utils` 中还有另外一个用于缓存系统的装饰符 pcache。它可以帮助对带有 limit 参数的函数增加缓存支持，一般这些函数对应于网站上的翻页功能：pcache只缓存其中“第一页”内容。

下面是一个例子：

     @pcache('random_group', 300, 3600)
     def random_groups(limit):
         cursor = store.get_cursor(table='15_minute_group')
         cursor.execute('select gids from `15_minute_group`')
         row = cursor.fetchone()
         if row and row[0]:
             return row[0].split('|')[:limit]
         else:
             return []


这里只缓存limit为300时的返回值。如果有请求的limit不超过300，则直接从缓存中的内容返回数据。
