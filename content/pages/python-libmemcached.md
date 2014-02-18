Title: Python-libmemcached
Date: 2014-02-18 12:00

---
Python-libmemcached 安装依赖 libmemcached， 豆瓣使用的 libmemcached 是自己打过 patch 的。

### Ubuntu

#### Install patched package

```
sudo apt-get install build-essential g++
wget  https://github.com/xtao/douban-patched/raw/master/libmemcached-douban-1.0.18.tar.gz
tar zxf libmemcached-1.0.18.tar.gz
cd libmemcached-1.0.18
./configure && make && sudo make install
cd ..
rm -rf python-libmemcached
rm -rf libmemcached*
sudo ldconfig
```

#### Install with patch

```
sudo apt-get install build-essential g++
wget https://launchpad.net/libmemcached/1.0/1.0.18/+download/libmemcached-1.0.18.tar.gz
git clone https://github.com/douban/python-libmemcached
tar zxf libmemcached-1.0.18.tar.gz
cd libmemcached-1.0.18
patch -p1 < ../python-libmemcached/patches/1.0/behavior.patch
patch -p1 < ../python-libmemcached/patches/1.0/empty_string.patch 
patch -p1 < ../python-libmemcached/patches/1.0/touch_expire-1.0.patch
./configure && make && sudo make install
cd ..
rm -rf python-libmemcached
rm -rf libmemcached*
sudo ldconfig
```
