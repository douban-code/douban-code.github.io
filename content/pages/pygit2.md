Title: Pygit2
Date: 2014-02-10 11:00

libgit2 bindings in Python
==========================

[pygit2](https://github.com/libgit2/pygit2)是一个Python的C扩展，实际上
是[libgit2](https://github.com/libgit2/libgit2)的python接口。

我们自己fork了pygit2的仓库，做了一些上游不愿意接纳的更改，所以Code一直
用的是自己的[douban pygit2](https://github.com/douban/pygit2)。

跟上游的主要区别：

1. 把libgit2内嵌到pygit2里面，做了静态编译，不再依赖系统的libgit2版本，方便升级pygit2。
1. 一直采用最新版本的libgit2，pygit2本身比较稳定，不能及时的使用libgit2最新的方法。
1. 为了性能写了一些特殊的方法。

当然，我们也把一些修改推回上游了，并且也及时的跟上游同步。

Pygit2的git功能依赖libgit2，目前基本的对象API和基础操作API都比较成熟了，整体上的git命令还不成熟。
如果想用pygit2完全替换git命令还是不行的。不过用来加速WEB应用还是够用的，唯一的遗憾是有些内存泄漏。
