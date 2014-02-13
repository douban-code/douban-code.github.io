Title: Scanner
Date: 2014-02-10 13:00

Scanner 是什么
--------------
一个类似 Ruby Stringscanner 的 Python C 扩展。

Scanner 的用途
--------------
在开发 Linguist 的时候，发现 Linguist Python 版的性能有问题，通过 profile 发现是正则匹配的问题，
于是把 Ruby 使用的正则库移植到了 Python。是为提高 Linguist 性能的一个 Python 扩展库。

