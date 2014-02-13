Title: Quixote
Date: 2014-02-10 16:00

豆瓣使用的web开发框架基础是quixote。

---
[Quixote](http://www.mems-exchange.org/software/quixote/) 是一个早期的 Web 开发框架，
目前最新版本是 2.x。豆瓣使用 1.x 版本 Quixote。

Quixote 的哲学很简单，通过模块和类实现 url 中的目录，通过函数、方法实现最终的 url 节点。

在阅读 CODE 代码、查找某个 url 对应的 CODE 代码地址时，可以从 `code/views/__init__.py` 文件为源头看起。

#### [html]

quixote 本身提供 html 模板功能，可以实现 View 的功能。如果在函数定义中增加 `[html]` 标记，
quixote 就会把该函数的任何字符串输出作为响应返回给用户。来自豆瓣的一个例子：

    def page_ui [html] (request, subject, rating=None):
       #...
       site_panel(request, title, cat_id=subject.cat_id)
       request.rating=rating
       main_layout(request, left_content, right_content, subject, grid='',
                   action=subject.url(), lzform=None)
       site_footer(request)

这种写法只能用于 .ptl 文件中，是 quixote 特有的文件格式，除了支持 `[html]` 和 `[plain]` 标记外，其他语法与 py 文件相同。

注意：由于这样的模板系统不适合 Controller 和 View 分开，也不适合后台开发、前端 UI 各自独立工作，
现在已经不再使用 quixote 的模板功能，转而使用 mako 模板开发。在新写任何页面时，不用新建 .ptl 文件，
也不要添加使用 `[html]` 的函数。如果工作中复用用到 .ptl 中的内容，最好把它们重构成使用 mako 模板的代码。

#### _q_exports

quixote 中还定义了一些特殊用途的变量及函数。遵循 Quixote 的规范就可以实现自己需要的 url 形式。

_q_exports 是其中最重要的一个。所有要暴露在 url 共供用户访问的函数、模块等的名字，必须这个列表中注册。

#### _q_index

_q_index 用作函数或者方法，可以实现该层 url 目录的默认页面。
比如 code.views.users.new._q_index 。

#### _q_access

_q_access 可以存放预处理逻辑，在访问本目录以及其下所有子目录、方法之前，都会执行该函数中的功能。
常见的应用场景有检查用户身份、统一处理输入数据等。可以去 code/views/api/__init__.py 查看统一设置返回数据类型为json的处理方法。

Quixote 不会去检查 _q_access 的返回值，如需中止处理过程，要显式抛出异常。


#### _q_lookup

有时 url 的某个层次是动态的，无法在 _q_exports 中全部列出。比如，豆瓣的条目地址 /subject/1045466/，条目数字id以万记，全部列出是不可能的。这是就需要用到 _q_lookup 函数，他定义了在 _q_exports 中找不到对应的处理函数时，
应该如何处理。比如，下面是条目页面的一个例子：

    def _q_lookup(request, name):
       if name:
           return SubjectUI(request, name)
       raise TraversalError("empty or wrong subject id")

在这个例子中，条目 id 被作为 name 传入，然后由 SubjectUI 渲染出用户看到的页面代码。

#### _q_exception_handler

_q_exception_handler 提供了捕获异常，显示定制的错误页面的机会。可以去 `code/views/__init__.py` 文件查看例子代码。

关于 Quixote 更加详细的介绍，请参考 Hongqn 编写的 [Quixote ~ 豆瓣动力核心](http://wiki.woodpecker.org.cn/moin/ObpLovelyPython/AbtQuixote) 一文。


### web安全

用户访问豆瓣，是通过web界面。web安全是豆瓣服务安全的重要一环。在web安全中，XSS、CSRF、SQL注入等是常见的漏洞。
在豆瓣代码中，为了保障安全，有些专门的机制。ck就是其中之一。

ck 是challenge key的缩写，它是每个用户不同的，用途是避免CSRF攻击。所有会造成数据变更的请求，如发帖、关注朋友、删除日记等，都需要在form中带有ck，
以便校验该请求的确是由用户浏览器发起的访问，而不是其他程序构造、诱骗浏览器自动发起的请求。所有POST都会被自动检查ck。

另外，在web页面上显示用户提交数据时，也需要做转义，以免运行了恶意代码。使用ptl的htmltext、code/views/utils里的safescape方法，转义在mako中会自动进行，
只要不仅使用n过滤器，处理用户数据后再在页面显示，可以避免此类XSS漏洞。

