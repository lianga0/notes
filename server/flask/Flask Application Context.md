### Flask Application Context

> 2018.04.09

#### Locality of the Context

The application context is created and destroyed as necessary. **It never moves between threads and it will not be shared between requests.** As such it is the perfect place to store database connection information and other things. The internal stack object is called `flask._app_ctx_stack`. Extensions are free to store additional information on the topmost level, assuming they pick a sufficiently unique name and should put their information there, instead of on the `flask.g` object which is reserved for user code.


#### 应用上下文的局部变量

**应用上下文会按需创建并销毁。它不会在线程间移动，并且也不会在请求间共享。**如此，它是一个存储数据库连接信息或是别的东西的最佳位置。内部的栈对象称为 `flask._app_ctx_stack`。 扩展可以在栈的最顶端自由储存信息，前提是使用唯一的名称，相反 `flask.g` 对象是为用户代码保留。


`flask.current_app`因为是当前Flask应用实例的代理，所以其中存在的值，可以在多个Request之间共享（前提是：处理不同Request时，Flask对象配置为可以重用）。


`ctx.py`文件中的AppContext类的对象，在不同的Request之间是不共享的。因为g是他的一个成员变量，所以flask.g在每个Request之间并不共享。

也就是Flask文档中讲的，应用上下文不会在线程间移动，并且也不会在请求间共享。这里特指的应用上下文对象。


[The Application Context](http://flask.pocoo.org/docs/0.12/appcontext/)

[应用上下文](http://www.pythondoc.com/flask/appcontext.html)

[Flask中的请求上下文和应用上下文](http://python.jobbole.com/87680/)