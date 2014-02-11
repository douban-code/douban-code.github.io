Title: Ellen
Date: 2014-02-07 18:00

Code的Git库
=============

Ellen是基于Git命令和Pygit2的一个库，Code使用的Git操作都是基于Ellen的。

[Pygit2](http://github.com/libgit2/pygit2)也是使用的Code团队修改过的版本。

因为Pygit2或者Libgit2还不够成熟的原因，个别地方仍然需要单独起一个进程调用git命令。
所以才有了这样一个Git的封装库。
