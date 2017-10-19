### nginx 499错误码

> From: http://www.cnblogs.com/xiaohuo/archive/2012/08/09/2630305.html

今天发现nginx有不少的499错误，大约占了将近0.5%，而且是在新上线了一个含upstream的业务之后。

grep一下nginx源码，定义在ngx_request_t.h

```
/*
* HTTP does not define the code for the case when a client closed
* the connection while we are processing its request so we introduce
* own code to log such situation when a client has closed the connection
* before we even try to send the HTTP header to it
*/
#define NGX_HTTP_CLIENT_CLOSED_REQUEST 499
```

这下就很清楚了，这是nginx定义的一个状态码，用于表示这样的错误：服务器返回http头之前，客户端就提前关闭了http连接。

再grep下“NGX_HTTP_CLIENT_CLOSED_REQUEST”，发现目前这个状态值只在ngx_upstream中赋值。

upstream在以下几种情况下会返回499：

（1）upstream 在收到读写事件处理之前时，会检查连接是否可用：ngx_http_upstream_check_broken_connection，

```
    if (c->error) { //connecttion错误
　　　　 ……
        if (!u->cacheable) { //upstream的cacheable为false，这个值跟http_cache模块的设置有关。指示内容是否缓存。
            ngx_http_upstream_finalize_request(r, u, NGX_HTTP_CLIENT_CLOSED_REQUEST);
        }
}
```

如上代码，当连接错误时会返回499。

（2）server处理请求未结束，而client提前关闭了连接，此时也会返回499。

（3）在一个upstream出错，执行next_upstream时也会判断连接是否可用，不可用则返回499。

总之，这个错误的比例升高可能表明服务器upstream处理过慢，导致用户提前关闭连接。而正常情况下有一个小比例是正常的。