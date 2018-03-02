### shadowsocks Command-line Client

shadowsocks提供Python实现的Command-line版客户端，可以在windows、linux以及MAC OS平台上使用。当不能使用图形界面时，是一个不错的选择，可以使用下面命令进行安装：

```
pip install shadowsocks
```

安装完成后，使用`sslocal`可以启动shadowsocks客户端。可以使用 `-c`参数指定包含服务器地址、密码等参数的配置文件路径。配置文件格式如下：

```
{
    "server":"my_server_ip",
    "server_port":8388,
    "local_port":1080,
    "password":"barfoo!",
    "timeout":600,
    "method":"chacha20-ietf-poly1305"
}
```

- server: your hostname or server IP (IPv4/IPv6).
- server_port: server port number.
- local_port: local port number.
- password: a password used to encrypt transfer.
- timeout: connections timeout in seconds.
- method: encryption method.


Stream ciphers provide only confidentiality. Data integrity and authenticity is not guaranteed. Users should use AEAD ciphers whenever possible.

The following stream ciphers provide reasonable confidentiality.

|Name    |Key Size   |IV Length|
|--------|-----------|--------|
|aes-128-ctr         |16  |16|
|aes-192-ctr         |24  |16|
|aes-256-ctr         |32  |16|
|aes-128-cfb         |16  |16|
|aes-192-cfb         |24  |16|
|aes-256-cfb         |32  |16|
|camellia-128-cfb    |16  |16|
|camellia-192-cfb    |24  |16|
|camellia-256-cfb    |32  |16|
|chacha20-ietf       |32  |12|


`AEAD` stands for Authenticated Encryption with Associated Data. `AEAD` ciphers simultaneously provide confidentiality, integrity, and authenticity. They have excellent performance and power efficiency on modern hardware. Users should use AEAD ciphers whenever possible.

The following AEAD ciphers are recommended. Compliant Shadowsocks implementations must support AEAD_CHACHA20_POLY1305. Implementations for devices with hardware AES acceleration should also implement AEAD_AES_128_GCM, AEAD_AES_192_GCM, and AEAD_AES_256_GCM.

|Name    |Alias      |Key Size    |Salt Size   |Nonce Size  |Tag Size|
|--------|-----------|------------|------------|------------|--------|
|AEAD_CHACHA20_POLY1305|  chacha20-ietf-poly1305 |32 | 32 | 12 | 16|
|AEAD_AES_256_GCM      |   aes-256-gcm           |32 | 32 | 12 | 16|
|AEAD_AES_192_GCM      |   aes-192-gcm           |24 | 24 | 12 | 16|
|AEAD_AES_128_GCM      |   aes-128-gcm           |16 | 16 | 12 | 16|

<完>|

Reference：[Quick Guide](https://shadowsocks.org/en/config/quick-guide.html)

[Stream Ciphers](https://shadowsocks.org/en/spec/Stream-Ciphers.html)

[AEAD Ciphers](https://shadowsocks.org/en/spec/AEAD-Ciphers)