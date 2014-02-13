Title: Pygit2
Date: 2014-02-10 11:00

---
### Pygit2 是什么

[Pygit2](https://github.com/libgit2/pygit2) 是一个 Python 的 C 扩展，实际上
是 [libgit2](https://github.com/libgit2/libgit2) 的 Python 接口。

我们自己 fork 了 Pygit2 的仓库，做了一些上游不愿意接纳的更改，所以 CODE 一直
用的是自己的 [douban Pygit2](https://github.com/douban/pygit2)。

跟上游的主要区别：

1. 把 libgit2 内嵌到 Pygit2 里面，做了静态编译，不再依赖系统的 libgit2 版本，方便升级 Pygit2。
1. 一直采用最新版本的 libgit2，原 Pygit2 项目本身比较稳定，不能及时的使用 libgit2 最新的方法。
1. 为了性能写了一些特殊的方法。

当然，我们也把一些修改推回上游了，并且也及时的跟上游同步。

Pygit2 的 git 功能依赖 libgit2，目前基本的对象访问 API 和基础操作 API 都比较成熟了，但整体上
的 git 命令还不成熟。 如果想用 Pygit2 完全替换 git 命令还是不行的。不过用来加速 Web 应用还是
够用的，唯一的遗憾是有些内存泄漏。
