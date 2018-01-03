### ERR_SSL_PROTOCOL_ERROR with Nginx

今天在Nginx中配置网站SSL证书时，按照之前的方法配置后，Chrome通过HTTPS访问总是出错。开始怀疑证书有问题，对照几遍配置和之前申请的证书后没有发现什么明显问题。后来看Chrome提示`ERR_SSL_PROTOCOL_ERROR`错误，Google发现有人碰到相同问题，主要原因是配置HTTPS server的`listen`指令时忘记添加`SSL`值，所以导致浏览器认为Server没有证书。详细情况如下：

Hi, I have kind of a reverse proxy setup with Nginx, here's my config:

```
server {
        listen 80;
        server_name discourse.jonaharagon.com;
        return 301 https://discourse.jonaharagon.com$request_uri;
}
server {
        listen 443;
        server_name discourse.jonaharagon.com;
        ssl_certificate /discourse.jonaharagon.com/fullchain.pem;
        ssl_certificate_key /discourse.jonaharagon.com/privkey.pem;
        location / {
                proxy_pass      http://discourse.jonaharagon.com:25654/;
                proxy_read_timeout      90;
                proxy_redirect  http://discourse.jonaharagon.com:25654/ https://discourse.jonaharagon.com;
        }
}
```

Chrome on my laptop and phone are returning an `ERR_SSL_PROTOCOL_ERROR` and SSL Labs is telling me my site doesn't even have a certificate. The two certificate files do exist, and this same type of configuration works perfectly on other servers of mine. I can't think of any reason this shouldn't work, but maybe I'm just being dumb. Nginx gives no errors and works fine, and I've tried everything I can think of, I even made the files and directories all with 777 permissions (this isn't a production server, it'll be down in a few days) and nothing.

##### Any idea?

##### Answer

Well, something is wrong indeed:

```
osiris@desktop ~ $ openssl s_client -connect discourse.jonaharagon.com:443 -servername discourse.jonaharagon.com
CONNECTED(00000003)
139865335457424:error:140770FC:SSL routines:SSL23_GET_SERVER_HELLO:unknown protocol:s23_clnt.c:795:
---
no peer certificate available
---
No client certificate CA names sent
---
SSL handshake has read 7 bytes and written 342 bytes
---
New, (NONE), Cipher is (NONE)
Secure Renegotiation IS NOT supported
Compression: NONE
Expansion: NONE
---
osiris@desktop ~ $ telnet discourse.jonaharagon.com 443
Trying 162.243.30.30...
Connected to discourse.jonaharagon.com.
Escape character is '^]'.
GET / HTTP/1.1
Host: discourse.jonaharagon.com

HTTP/1.1 200 OK
Server: nginx/1.4.6 (Ubuntu)
(...)
```


From the [nginx docs](http://nginx.org/en/docs/http/configuring_https_servers.html):

To configure an HTTPS server, the ssl parameter must be enabled on listening sockets in the server block, and the locations of the server certificate and private key files should be specified:

```
server {
    listen              443 ssl;
    server_name         www.example.com;
    ssl_certificate     www.example.com.crt;
    ssl_certificate_key www.example.com.key;
    ssl_protocols       TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers         HIGH:!aNULL:!MD5;
    ...
}
```

So that's your problem. You've got to add ssl to the listen 443 part to enable TLS in the first place...


From: [ERR_SSL_PROTOCOL_ERROR with Nginx](https://community.letsencrypt.org/t/err-ssl-protocol-error-with-nginx/9584/2)