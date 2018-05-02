## CloudFront SSL/TLS Negotiation Failure Isuue

最早发现CloudFront 502错误，没有搞清楚错误的源头，纠结起CDN和Load Balance会不会像浏览器一样跟踪HTTP 3xx重定向（自动请求新的URL）。

How CloudFront Processes HTTP 3xx Status Codes from Your Origin
When CloudFront requests an object from your Amazon S3 bucket or custom origin server, your origin sometimes returns an HTTP 3xx status code, which typically indicates either that the URL has changed (301, Moved Permanently, or 307, Temporary Redirect) or that the object hasn't changed since the last time CloudFront requested it (304, Not Modified). CloudFront caches 3xx responses for the duration specified by the settings in your CloudFront distribution and by the header fields that your origin returns along with an object. For more information, see Specifying [How Long Objects Stay in a CloudFront Edge Cache (Expiration)](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Expiration.html).

简单的说，CloudFront不会跟踪重定向，仅把重定向转发给客户端。Load Balancer基本上就更不会跟踪重定向了，也仅仅转发用户请求和server响应而已。。

### CloudFront HTTP 502 Status Code (Bad Gateway)

An HTTP 502 status code (Bad Gateway) indicates that CloudFront wasn't able to serve the requested object because it couldn't connect to the origin server.

The reasons maybe as following:

1. SSL/TLS Negotiation Failure Between CloudFront and a Custom Origin Server
2. Origin Is Not Responding with Supported Ciphers/Protocols
3. SSL/TLS Certificate on the Origin Is Expired, Invalid, Self-signed, or the Certificate Chain Is in the Wrong Order
4. Origin Is Not Responding on Specified Ports in Origin Settings

#### SSL/TLS Negotiation Failure Between CloudFront and a Custom Origin Server

If you use a custom origin and you configured CloudFront to require HTTPS between CloudFront and your origin, the problem might be mismatched domain names. The SSL/TLS certificate that is installed on your origin includes a domain name in the **Common Name** field and possibly several more in the **Subject Alternative Names** field. (CloudFront supports wildcard characters in certificate domain names.) One of the domain names in the certificate must match one or both of the following values:

1. The value that you specified for Origin Domain Name for the applicable origin in your distribution.

2. **The value of the Host header if you configured CloudFront to forward the Host header to your origin**. For more information about forwarding the Host header to your origin, see [Configuring CloudFront to Cache Objects Based on Request Headers](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/header-caching.html).

If the domain names don't match, the SSL/TLS handshake fails, and CloudFront returns an HTTP status code 502 (Bad Gateway) and sets the `X-Cache` header to Error from `cloudfront`.

To determine whether domain names in the certificate match the `Origin Domain Name` in the distribution or the `Host` header, you can use an online SSL checker or OpenSSL. If the domain names don't match, you have two options:

1. Get a new SSL/TLS certificate that includes the applicable domain names.
2. Change the distribution configuration so CloudFront no longer tries to use SSL to connect with your origin.

#### Online SSL Checker

To find an SSL test tool, search the Internet for "online ssl checker." Typically, you specify the name of your domain, and the tool returns a variety of information about your SSL/TLS certificate. Confirm that the certificate contains your domain name in the **Common Names** or **Subject Alternative Names** fields.

#### OpenSSL

To determine whether CloudFront is able to establish a connection with your origin, you can use OpenSSL to try to make an SSL/TLS connection to your origin and to verify that the certificate on your origin is correctly configured. If OpenSSL is able to make a connection, it returns information about the certificate on the origin server.

The command that you use depends on whether you use a client that supports SNI (Server Name Indication).

Client supports SNI

```
openssl s_client –connect domainname:443 –servername domainname
```

Client doesn't support SNI

```
openssl s_client –connect domainname:443
```

Replace domainname with the applicable value:

If you aren't forwarding the `Host` header to the origin – Replace `domainname` with your origin's domain name.

If you are forwarding the `Host` header to the origin – Replace `domainname` with the CNAME that you're using with your CloudFront distribution.


### 阿里云CDN如何处理源站的302跳转

对网站的前端界面根据客户终端的设备来决定提供对应的界面样式是常见的网站设计需求。该需求的常见设计思路是源站根据用户的请求然后在源站对用户的请求做302的跳转到对应的页面上进行服务。 

在对网站部署CDN后由于CDN的产品性质，CDN会对用户的访问资源缓存到CDN的节点上以便后续可以加快用户的访问，这种情况下就可能会出现第一个用户访问后会对对应的302的请求进行缓存。而其他不同终端设备的用户通过该URL进行访问的时候就会出现访问到的页面情况仍然是第一个用户缓存的302的请求到的页面上。这就会造成用户源站设置的对不同终端的适配功能失效。

要解决这种问题的思路就是设置对第一个请求的URL不缓存，而对302跳转后的页面进行缓存。这样设置就可保证用户源站的终端配置功能可以生效的同时也可以实现CDN对于页面的加速。CDN对于缓存的配置暂时支持两种：目录和后缀名，用户可以结合这两种的缓存配置以及其优先级来根据自己的站点目录结构定义初始URL不缓存，而对于其他的URL缓存；

另外更为方便的方法是用户可以在源站对于初始页面设置不缓存，**因为源站的不缓存策略对于CDN是具有最高优先级的**。只要该页面的response中带有下述头信息就保证该页面不缓存：

```
Cache-control:no-cache,no-store,private
Cache-control:s-maxage=0,max-age=0
pragma:no-cache
```

[How CloudFront Processes HTTP 3xx Status Codes from Your Origin](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/http-3xx-status-codes.html)

[HTTP 502 Status Code (Bad Gateway)](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/http-502-bad-gateway.html)

[CDN如何处理源站的302跳转](https://help.aliyun.com/knowledge_detail/40128.html)