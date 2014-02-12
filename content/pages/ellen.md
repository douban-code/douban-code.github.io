Title: Ellen
Date: 2014-02-07 18:00

CODE 的 git 库
--------------

Ellen 是基于 git 命令和 Pygit2 的一个 Python 库，CODE 使用的 git 操作都是基于 Ellen 的。

[Pygit2](http://github.com/libgit2/pygit2) 也是使用的 CODE 团队修改过的版本。

因为 Pygit2 或者 libgit2 还不够成熟的原因，个别地方仍然需要单独起一个进程调用 git 命令。
所以才有了这样一个 git 的封装库。
