Title: ORZ
Date: 2014-02-13 08:00

---
### ORZ 是什么
[ORZ](https://github.com/douban/douban-orz) 不是 ORM，只是封装了基础的数据库 CRUD 及其 Cache 管理，
并尽可能提供基于Pythonic的方式进行扩展的数据层。

### 简介

假如数据库声明是这样的

    CREATE TABLE `dummy_yummy` (
      `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
      `uid` int(11),
      `username` varchar(20) NOT NULL,
      `subject_id` int(11) NOT NULL,
      `user_id` int(11) NOT NULL,
      `subtype` varchar(50),
      PRIMARY KEY (`id`),
      KEY `user_id` (`user_id`),
      KEY `subject_id_subtype_idx` (`subject_id`, `subtype`),
      KEY `uid` (`uid`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='';

之前我们会这样写

    class DummyYummy(object):
        OBJ_CACHE = 'dummyyummy-obj:%s'
        USER_INDEX_CACHE = 'dummyyummy-user:%s'
        SUBJECT_SUBTYPE_INDEX_CACHE = 'dummyyummy-subject:%s|subtype:%s'
        UID_INDEX_CACHE = 'dummyyummy-uid:%s'

        def __init__(self, id, uid, username, subject_id, user_id, subtype):
            self.id = id
            self.uid = uid
            self.username = username
            self.subject_id = subject_id
            self.user_id = user_id
            self.subtype = subtype


        @classmethod
        def create(cls, uid, username, subject_id, user_id, subtype):
            id = store.exexute('insert into dummy_yummy (`uid`, `username`, `subject_id`, `user_id`, `subtype`)'
                               'values (%s, %s, %s, %s, %s)', (uid, username, subject_id, user_id, subtype))
            store.commit()

            mc.delete(cls.SUBJECT_SUBTYPE_INDEX_CACHE % (subject_id, subtype))
            mc.delete(cls.UID_INDEX_CACHE % uid)
            mc.delete(cls.USER_INDEX_CACHE % user_id)

            ins = cls(id, uid, username, subject_id, user_id, subtype)
            mc.set(cls.OBJ_CACHE % ins.id, ins)
            return ins

        def update_subject_id(self, subject_id):
            store.execute('update dummy_yummy set subject_id=%s where id=%s', (subject_id, self.id))
            store.commit()

            mc.delete(self.SUBJECT_SUBTYPE_INDEX_CACHE % (self.subject_id, self.subtype))

            self.subject_id = subject_id

            mc.delete(self.SUBJECT_SUBTYPE_INDEX_CACHE % (subject_id, self.subtype))
            mc.delete(self.OBJ_CACHE % self.id)

        @classmethod
        def gets(cls, ids):
            mc.get_multi(ids)
            return [cls.get(id=id) for id in ids]


        @cache(USER_INDEX_CACHE % "{user_id}")
        def _gets_by_user_id(cls, user_id):
            return [id for id, in store.execute("select id from dummy_yummy where user_id = %s", user_id)]

        def gets_by_user_id(cls, user_id):
            return cls.gets(cls._gets_by_user_id(user))

        @cache(SUBJECT_SUBTYPE_INDEX_CACHE % ("{subject_id}", "{subtype}"))
        def _gets_by_subject_id_and_subtype(cls, subject_id, subtype):
            return [id for id, in store.execute("select id from dummy_yummy where subject_id = %s and subtype = %s", (subject_id, subtype))]

        def gets_by_subject_id_and_subtype(cls, subject_id, subtype):
            return cls.gets(cls._gets_by_subject_id_and_subtype(cls, subject_id, subtype))

        @cache(UID_INDEX_CACHE % "{uid}")
        def _gets_by_uid(cls, uid):
            return [id for id, in store.execute("select id from dummy_yummy where uid = %s", uid)]

        def gets_by_uid(cls, uid):
            return cls.gets(cls._gets_by_uid(cls, uid))

然后我们这样用

    Dummy.gets_by_subject_id_and_subtype(subject_id, subtype):
    Dummy.gets_by_uid(uid)
    Dummy.gets_by_user_id(user_id)


    dummy_obj = Dummy.create(uid=uid, subject_id=subject_id, subtype=subtype, user_id=user_id, username=username)

    dummy_obj.update_subject_id(subject_id=subject_id)

使用ORZ以后我们这样写

    from ORZ.exports import OrzBase

    setup(your_store, your_mc)

    class DummyYummy(OrzBase):
        __orz_table__ = 'dummy_yummy'
        uid = OrzField(as_key=OrzField.KeyType.ONLY_INDEX)
        username = OrzField()
        subject_id = OrzField(as_key=OrzField.KeyType.ONLY_INDEX)
        user_id = OrzField(as_key=OrzField.KeyType.ONLY_INDEX)
        subtype = OrzField(as_key=OrzField.KeyType.ONLY_INDEX)

于是我们这样用

    Dummy.gets_by(uid=uid)
    Dummy.gets_by(subject_id=subject_id, subtype=subtype)
    Dummy.gets_by(user_id=user_id)

    dummy_obj = Dummy.create(uid=uid, subject_id=subject_id, subtype=subtype, user_id=user_id, username=username)

    dummy_obj.subject_id = subject_id
    dummy_obj.save()



