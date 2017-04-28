### Nginx模块 ngx_http_limit_req_module 限制请求速率

##### Example Configuration

The `ngx_http_limit_req_module` module (0.7.21) is used to limit the request processing rate per a defined key, in particular, the processing rate of requests coming from a single IP address. The limitation is done using the “leaky bucket” method.

`ngx_http_limit_req_module`模块用于限制对每个定义键的请求处理速率，特别是，单个IP客户每秒处理的请求数。实现的原理是使用“漏桶”原理。

```
http {
    limit_req_zone $binary_remote_addr zone=one:10m rate=1r/s;

    ...

    server {

        ...

        location /search/ {
            limit_req zone=one burst=5;
        }
```

##### Directives

###### limit_req

```
Syntax: limit_req zone=name [burst=number] [nodelay];
Default:    —
Context:    http, server, location
```

Sets the shared memory zone and the maximum burst size of requests. If the requests rate exceeds the rate configured for a zone, their processing is delayed such that requests are processed at a defined rate. Excessive requests are delayed until their number exceeds the maximum burst size in which case the request is terminated with an error 503 (Service Temporarily Unavailable). By default, the maximum burst size is equal to zero. For example, the directives

设置共享内存区和最大数请求数。当请求的速率大于配置的速率，那么这些请求将会被延迟处理。如果，有过多的请求被延迟，超过了最大突发请求数的限制，服务器将返回503状态码。默认情况下，最大突发限制为0。例如，以下指令配置：

```
limit_req_zone $binary_remote_addr zone=one:10m rate=1r/s;

server {
    location /search/ {
        limit_req zone=one burst=5;
    }
```

allow not more than 1 request per second at an average, with bursts not exceeding 5 requests.

允许每秒不超过1个请求，最大突发请求数量不大于5。

If delaying of excessive requests while requests are being limited is not desired, the parameter `nodelay` should be used:

如果不希望突发请求被延时执行，那么可以使用`nodelay`参数。

```
limit_req zone=one burst=5 nodelay;
```

There could be several `limit_req` directives. For example, the following configuration will limit the processing rate of requests coming from a single IP address and, at the same time, the request processing rate by the virtual server:

```
limit_req_zone $binary_remote_addr zone=perip:10m rate=1r/s;
limit_req_zone $server_name zone=perserver:10m rate=10r/s;

server {
    ...
    limit_req zone=perip burst=5 nodelay;
    limit_req zone=perserver burst=10;
}
```

These directives are inherited from the previous level if and only if there are no `limit_req` directives on the current level.

如果当前级别中没有配置，这些指令会继承上一级的指令。

###### limit_req_log_level

```
Syntax: limit_req_log_level info | notice | warn | error;
Default:    
limit_req_log_level error;
Context:    http, server, location
This directive appeared in version 0.8.18.
```

Sets the desired logging level for cases when the server refuses to process requests due to rate exceeding, or delays request processing. Logging level for delays is one point less than for refusals; for example, if `“limit_req_log_level notice”` is specified, delays are logged with the info level.

###### limit_req_status

```
Syntax: limit_req_status code;
Default:    
limit_req_status 503;
Context:    http, server, location
This directive appeared in version 1.3.15.
```

Sets the status code to return in response to rejected requests.

设置拒绝请求时候的http返回状态码。

###### limit_req_zone

```
Syntax: limit_req_zone key zone=name:size rate=rate;
Default:    —
Context:    http
```

Sets parameters for a shared memory zone that will keep states for various keys. In particular, the state stores the current number of excessive requests. The `key` can contain text, variables, and their combination. Requests with an empty key value are not accounted.

> Prior to version 1.7.6, a `key` could contain exactly one variable.

Usage example:

```
limit_req_zone $binary_remote_addr zone=one:10m rate=1r/s;
```

Here, the states are kept in a 10 megabyte zone “one”, and an average request processing rate for this zone cannot exceed 1 request per second.

以上的配置，设置了名为“one”的存储区，大小为10兆字节，请求速率为每个客户端IP每秒1个请求。

A client IP address serves as a key. Note that instead of `$remote_addr`, the `$binary_remote_addr` variable is used here. The `$binary_remote_addr` variable’s size is always 4 bytes for IPv4 addresses or 16 bytes for IPv6 addresses. The stored state always occupies 64 bytes on 32-bit platforms and 128 bytes on 64-bit platforms. One megabyte zone can keep about 16 thousand 64-byte states or about 8 thousand 128-byte states. If the zone storage is exhausted, the server will return the 503 (Service Temporarily Unavailable) error to all further requests.

The rate is specified in requests per second (r/s). If a rate of less than one request per second is desired, it is specified in request per minute (r/m). For example, half-request per second is 30r/m.

From:[Module ngx_http_limit_req_module](http://nginx.org/en/docs/http/ngx_http_limit_req_module.html#limit_req_zone)

Reference: [Nginx模块 ngx_http_limit_req_module 限制请求速率](http://blog.csdn.net/loophome/article/details/50767907)