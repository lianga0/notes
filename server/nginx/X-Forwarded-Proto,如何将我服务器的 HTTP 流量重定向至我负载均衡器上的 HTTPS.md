### 如何将我服务器的 HTTP 流量重定向至我负载均衡器上的 HTTPS？

#### 问题

我在 Elastic Load Balancing (ELB) 负载均衡器上使用 HTTP 和 HTTPS。ELB 在卸载 SSL，并且后端仅在一个 HTTP 端口侦听 (HTTPS 至 HTTP)。我希望所有通过端口 80 进入我的 Web 服务器的所有流量都重定向至 HTTPS 端口 443，但我不希望将我的后端侦听器更改到端口 443。在重定向流量时，我的网站停止工作，我收到如下错误消息：ERR_TOO_MANY_REDIRECTS。如何解决此问题？

#### 简短描述

此错误通常是由如下原因造成的：

1. Web 服务器上将 HTTP 请求定向至 HTTPS 的重写规则导致请求在负载均衡器上为 HTTPS 流量使用端口 443。
2. 负载均衡器仍然通过端口 80 将请求发送至后端 Web 服务器。
3. 后端 Web 服务器将这些请求重定向至负载均衡器上的端口 443。

这导致负载均衡器和后端 Web 服务器之间形成重定向的无限循环，请求永远都不会送达。

#### 解决

使用 HTTP 请求的 [X-Forwarded-Proto](https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/x-forwarded-headers.html#x-forwarded-proto)标头，将 Web 服务器的重写规则更改为仅在客户端的协议为 HTTP 时适用。忽视客户端用于所有其他协议的重写规则。

这样，如果客户端使用 HTTP 来访问您的网站，它们会被重定向至一个 HTTPS URL，如果客户端使用 HTTPS，Web 服务器会直接服务它们。

注意：本文提供了 Apache、Nginx 和 IIS Web 服务器的示例。

#### Apache

在虚拟主机或 .htaccess 文件中使用 mod_rewrite 规则。作为最佳实践，我们建议将虚拟主机规则用于重定向规则。

##### 虚拟主机文件 (推荐)

重写规则必须包含在配置文件的虚拟主机部分中。例如，Apache httpd 服务器应编辑 /etc/httpd/conf/httpd.conf 文件，Apache 2.4 应编辑 /etc/apache2/sites-enabled/ 文件夹中的 conf 文件。

```
<VirtualHost *:80>

RewriteEngine On
RewriteCond %{HTTP:X-Forwarded-Proto} =http
RewriteRule .* https://%{HTTP:Host}%{REQUEST_URI} [L,R=permanent]

</VirtualHost>
```

或者可以写成如下形式（Dr.Cleaner）

```
<VirtualHost *:80>
    RewriteEngine On
    RewriteCond %{HTTP:X-Forwarded-Proto} !https
    RewriteRule ^.*$ https://%{SERVER_NAME}%{REQUEST_URI}

    <IfModule mod_setenvif.c>
        SetEnvIf X-Forwarded-Proto "^https$" HTTPS
    </IfModule>
</VirtualHost>
```


##### .htaccess 文件

注意：不建议使用 .htaccess，而应仅在您没有主配置文件的访问权限时使用。

如要使用 .htaccess，您必须利用目录指令从 Apache 配置文件启用它。例如，Apache httpd 服务器应编辑 /etc/httpd/conf/httpd.conf 文件。Apache 2.4 应编辑/etc/apache2/sites-enabled/ 文件夹中的 conf 文件。

```
<Directory "/var/www/html">
    Options Indexes FollowSymLinks
    AllowOverride All
    Require all granted
</Directory>
```

.htaccess 文件中的重写规则类似于如下：

```
RewriteEngine On
RewriteCond %{HTTP:X-Forwarded-Proto} =http
RewriteRule .* https://%{HTTP:Host}%{REQUEST_URI} [L,R=permanent]
```

#### Nginx

ngnix.conf 文件中的 Nginx 后端重写规则类似于如下：

注意： 适用于版本 nginx/1.10.3 (Ubuntu) 和 nginx/1.12.1 (Amazon Linux)。

```
server {
    listen   80;
    server_name    www.example.org;   
    if ($http_x_forwarded_proto = 'http') {
         return 301 https://$server_name$request_uri;   
    }
}
```

#### IIS

在修改 web.config 文件前，您必须从 Microsoft IIS 下载安装 URL 重写模块。

IIS 后端的重写规则位于 web.config 文件中的 部分下，类似于如下： 

注意：仅适用于 Microsoft Windows Server 2012 R2 和 2016 Base。

```
<rewrite> 
<rules> 
<rule name="Rewrite HTTP to HTTPS” stopProcessing=”true”> 
<match url="^(.*)$" /> 
<conditions logicalGrouping=”MatchAny”> 
<add input="{HTTP_X_FORWARDED_PROTO}" pattern="^http$" />
</conditions> 
<action type="Redirect" url="https://{HTTP_HOST}{REQUEST_URI}" /> 
</rule> 
</rules> 
</rewrite>
```

打开 IIS Manager，然后刷新默认网站。规则应当在“URL Rewrite”部分显示。重新启动网站，然后进行测试。

From: [如何将我服务器的 HTTP 流量重定向至我负载均衡器上的 HTTPS？](https://aws.amazon.com/cn/premiumsupport/knowledge-center/redirect-http-https-elb/)