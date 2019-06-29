## Nginx使用gzip对json数据传输进行压缩

> 2019.6.20

服务器与客户端采用json格式数据通信时，当传输数据非常大时使用gzip压缩，将会大量的减少服务器流量以及客户端请求速度。Nginx中可以非常方便的直接配置启用压缩，而不用修改后端服务器代码。

Nginx样例配置项目如下：

```
    location /test/ {
        proxy_pass   http://127.0.0.1:5000;
        gzip            on;
        gzip_min_length 1000;
        gzip_proxied    any;
        gzip_types      text/plain application/xml application/json;
    }
```

可以能方便的启用压缩传输。对于配置项中参数详细意义，可以参考Nginx官网的[Module ngx_http_gzip_module](http://nginx.org/en/docs/http/ngx_http_gzip_module.html)页面进一步了解。

### 客户端访问

当Nginx服务器配置启用gzip压缩后，客户端发起HTTP访问时，应当添加`Accept-Encoding: gzip, deflate`头。否则，Nginx仍然会在HTTP body中返回未压缩的JSON数据。

例如，可以使用如下CURL参数进行请求：

```
curl https://www.baidu.com -H "Accept-Encoding: gzip, deflate" -o baidu.gz
```

另外，curl支持--compressed参数，查了下官方文档，其说明为：

```
--compressed 

(HTTP) Request a compressed response using one of the algorithms curl supports, and save the uncompressed document. If this option is used and the server sends an unsupported encoding, curl will report an error.
```

意思是，curl 会向网站请求压缩后的文档（gzip格式），然后会自动解压返回解压后的数据。

### Enabling Decompression

The ngx_http_gunzip_module module is a filter that decompresses responses with “Content-Encoding: gzip” for clients that do not support “gzip” encoding method. The module will be useful when it is desirable to store data compressed to save space and reduce I/O costs.

This module is not built in Nginx by default, it should be enabled with the --with-http_gunzip_module configuration parameter.

```
location /storage/ {
    gunzip on;
    ...
}
```

[Module ngx_http_gzip_module](http://nginx.org/en/docs/http/ngx_http_gzip_module.html)

[Compression and Decompression](https://docs.nginx.com/nginx/admin-guide/web-server/compression/)

[MIME types (IANA media types)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types)

[Accept-Encoding](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Accept-Encoding)

[Module ngx_http_gunzip_module](http://nginx.org/en/docs/http/ngx_http_gunzip_module.html)