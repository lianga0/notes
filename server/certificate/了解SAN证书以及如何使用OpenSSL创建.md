# 了解SAN证书以及如何使用OpenSSL创建

> 2020-04-19

> http://www.srcmini.com/57310.html

通过使用SAN证书对多个网站使用单个证书来降低SSL成本和维护

SAN代表“主题备用名称”, 这有助于你为多个CN(通用名称)拥有一个证书。

你可能会以为这是通配符SSL, 但让我告诉你-有点不同。在SAN证书中, 你可以具有多个完整的CN。

例如：

- Geekflare.com

- Bestflare.com

- Usefulread.com

- Chandank.com

SAN的CSR的创建与传统​​的OpenSSL命令略有不同。

登录到已安装OpenSSL的服务器

转到 `/tmp` 或创建任何目录

使用vi(如果在Unix上)使用以下信息创建名为san.cnf的文件

```
[req]
default_bits       = 2048
distinguished_name = req_distinguished_name
req_extensions     = req_ext
prompt             = no

[ req_distinguished_name ]
countryName                 = Country Name (2 letter code)
stateOrProvinceName         = State or Province Name (full name)
localityName               = Locality Name (eg, city)
organizationName           = Organization Name (eg, company)
commonName                 = Common Name (e.g. server FQDN or YOUR name)

[ req_ext ]
subjectAltName = @alt_names

[alt_names]
DNS.1   = bestflare.com
DNS.2   = usefulread.com
DNS.3   = chandank.com
```

> 注意：alt_names部分是你必须更改以用于其他DNS的部分。

保存文件并执行以下OpenSSL命令, 该命令将生成CSR和KEY文件

```
openssl req -out sslcert.csr -newkey rsa:2048 -nodes -keyout private.key -config san.cnf
```

这将在当前工作目录中创建sslcert.csr和private.key。你必须将sslcert.csr发送给证书签署者授权, 以便他们可以为你提供SAN证书。

### 何验证SAN的CSR？

检查你的CSR是否包含SAN(在上面的san.cnf文件中指定)是一个好主意。

```
openssl req -noout -text -in sslcert.csr | grep DNS
```

例如：

```
[[email protected] test]# openssl req -noout -text -in sslcert.csr | grep DNS
               DNS:bestflare.com, DNS:usefulread.com, DNS:chandank.com
[[email protected] test]#
```

你还可以使用在线工具来验证SAN和其他许多参数。
