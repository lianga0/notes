# openssl升级导致加密文件解密失败

> 2021.07.20

一个旧项目中的解密脚本在新版本的Linux系统中突然不能正常工作，找到其中openssl命令参数，单独运行结果如下：

```
openssl aes-256-cbc -d -a -in uat_certs_production.tgz.enc -out beta.tgz
enter aes-256-cbc decryption password:
*** WARNING : deprecated key derivation used.
Using -iter or -pbkdf2 would be better.
bad decrypt
140586010125632:error:06065064:digital envelope routines:EVP_DecryptFinal_ex:bad decrypt:../crypto/evp/evp_enc.c:610:
```

搜索一圈后发现，原来是因为：在Openssl 1.1.0中，默认摘要已从MD5更改为SHA256。所以解密时需要显示的指定为旧版本的MD5。命令如下：

```
openssl enc -d -aes-256-cbc -a -md md5 -in uat_certs_production.tgz.enc -out beta.tgz
```
命令行： [openssl enc](https://www.openssl.org/docs/man1.1.1/man1/enc.html)采用以下形式：

```
openssl enc -ciphername [-in filename] [-out filename] [-pass arg]
[-e] [-d] [-a/-base64] [-A] [-k password] [-kfile filename] 
[-K key] [-iv IV] [-S salt] [-salt] [-nosalt] [-z] [-md] [-p] [-P] 
[-bufsize number] [-nopad] [-debug] [-none] [-engine id]
```

Reference: [如何使用OpenSSL加密/解密文件？](https://qastack.cn/programming/16056135/how-to-use-openssl-to-encrypt-decrypt-files)