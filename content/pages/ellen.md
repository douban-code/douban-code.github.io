Title: Ellen
Date: 2014-02-07 18:00

Code的GIT封装
=============

Ellen是基于git命令和pygit2的一个包装，Code使用的git操作都是基于ellen的。

[pygit2](http://github.com/libgit2/pygit2)也是使用的我们自己修改过的版本。

因为pygit2或者libgit2还不够成熟的原因，个别地方仍然需要单独起一个进程调用git命令。
所以才有了这样一个GIT的封装库。
