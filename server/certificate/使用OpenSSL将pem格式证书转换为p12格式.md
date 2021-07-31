# 使用OpenSSL将pem格式证书转换为p12格式

今天一个问题，我们的SSL证书只有pem格式，而Apple要求提交p12格式。

一般情况下pem证书是由cert.pem和key.pem组成，2个pem文件成对儿存在，例如：apiclient_cert.pem和apiclient_key.pem

在命令提示符下输入命令：

```
openssl pkcs12 -export -in apiclient_cert.pem -inkey apiclient_key.pem -out apiclient_cert.p12
```

如果我们只有证书apiclient_cert.pem，而没有对应的证书的私钥apiclient_key.pem的话，可以使用如下命令进行转换

```
openssl pkcs12 -export -nokeys -in apiclient_cert.pem -out apiclient_cert.p12
```

如果我们有多个证书需要放到一个p12文件中（比如证书链），那么我们可以把多个PEM的证书合并成一个，然后再运行上述命令。


## 查看p12文件内容

p12文件内容为二进制格式，Windows上默认没有很好的查看工具，可以使用如下命令转回PEM文本格式：

```
openssl pkcs12 -in xxx.p12 -out xxx.pem -nodes
```

pem文件可以直接用文本工具打开

Reference:

[How can I create a .p12 or .pfx file without a private key?](https://stackoverflow.com/questions/23935820/how-can-i-create-a-p12-or-pfx-file-without-a-private-key)

[Load multiple certificates into PKCS12 with openssl](https://stackoverflow.com/questions/19704950/load-multiple-certificates-into-pkcs12-with-openssl)

[如何查看p12文件的信息](https://jason5.cn/blog/ru-he-cha-kan-p12wen-jian-de-xin-xi.html)

[mac下查看.mobileprovision文件及钥匙串中证书.cer文件](https://www.cnblogs.com/chuanwei-zhang/p/8058254.html)
