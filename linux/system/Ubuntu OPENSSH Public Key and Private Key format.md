## Ubuntu OPENSSH Public Key and Private Key format

> 2018.03.11

Ubuntu中安装`openssh-server`包后，sshd服务默认使用`/etc/ssh/sshd_config`配置文件（或者可以使用`-f`命令行参数进行指定）启动。

这个配置文件包含keyword-argument对，每个占一行。空行和以`#`开头的行被解释为注释。

Arguments may optionally be enclosed in double quotes (") in order to represent arguments containing spaces.

Note that the Debian `openssh-server` package sets several options as standard in `/etc/ssh/sshd_config` which are not the default in sshd

### ssh-keygen

`ssh-keygen`命令是用来产生新的SSH公私秘钥对的命令。默认情况下，会在当前用户家目录下的`.ssh`目录中生成一个`id_rsa`和`id_rsa.pub`秘钥对。如下：

```
$ ssh-keygen

Generating public/private rsa key pair.
Enter file in which to save the key (/home/dr/.ssh/id_rsa):
```

当然，你也可以直接在命令行参数中使用`-t`指定key的类型（ecdsa, ed25519或rsa）。使用`-f`参数指定秘钥存储的路径。如下：

```
$ ssh-keygen -t rsa -f ./id_rsa

Generating public/private rsa key pair.
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in ./id_rsa.
Your public key has been saved in ./id_rsa.pub.
The key fingerprint is:
SHA256:TMvt/+CGIlCkMiqS/d2Jz7iLYUmcQZJVNlCBgRsljRU yuliang@Ubuntu4-001
The key's randomart image is:
+---[RSA 2048]----+
|  oOEB*.         |
|  =+o...         |
|   o.o  .        |
|  +..o.+ o       |
| + o+.  S .      |
|= ....   .       |
|o  .+o o ....    |
|   ..o+o+ .o..   |
|    . +=o. .o..  |
+----[SHA256]-----+
```

#### ssh-keygen 公钥文件 id_rsa.pub

`rsa-keygen`生成的公钥文件`id_rsa.pub`，其格式是符合`sshd`使用的`authorized_keys`文件中的每行记录的格式。如下面的`id_rsa.pub`文件，其中`ssh-rsa`表示公钥的类型。 

第一个空格后的是SSH定义的公钥格式中的公钥数据（使用base64编码，RFC7468[Textual Encodings of PKIX, PKCS, and CMS Structures](https://tools.ietf.org/html/rfc7468)）。最后一个空格后的内容为注释，帮助用户理解记忆，`sshd`并不对这个数据做特殊处理。

```
$ cat id_rsa.pub

ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDTw1ey8xdWQgz/Y9aTXhYM8rGJXCj11QZbAYBQ1oGjSoB0meeDfIBjQl4cYRvFR2VogIzZ0c1u0g4D1cXFpXClGnoxqyf1SCb0BgUxijKOV9vImu7CHo8L2CgjwjszIfJAs/S7L8KiZ5kestSrQQG1Wg1Npghdv9T20yQ6M2ZDDt4Yu88p3XH686amT3QVYTdn94qcXn+lF8VWn9mBPXxmVXXGkOmOYIabjs0WExkFKPL4fvN6kbp3EUTOYBRq3VafwgngQii+O08nZIIWk7gLJ8ycilxk/gwTKsN87VNydyXbicliBbk0znjL8zVVDtxQx5SDzYqO8YEfCvlKWeTV dr@Ubuntu4-001
```

Secure Shell (SSH)定义的公钥格式可以参考RFC4716文档[The Secure Shell (SSH) Public Key File Format](https://tools.ietf.org/html/rfc4716)。RFC4716定义的SSH公钥格式如下：

```
---- BEGIN SSH2 PUBLIC KEY ----
Comment: "dr@Ubuntu4-001"
x-command: /home/me/bin/lock-in-guest.sh
AAAAB3NzaC1yc2EAAAADAQABAAABAQDTw1ey8xdWQgz/Y9aTXhYM8rGJXCj11QZbAYBQ1oGjSoB0meeDfIBjQl4cYRvFR2VogIzZ0c1u0g4D1cXFpXClGnoxqyf1SCb0BgUxijKOV9vImu7CHo8L2CgjwjszIfJAs/S7L8KiZ5kestSrQQG1Wg1Npghdv9T20yQ6M2ZDDt4Yu88p3XH686amT3QVYTdn94qcXn+lF8VWn9mBPXxmVXXGkOmOYIabjs0WExkFKPL4fvN6kbp3EUTOYBRq3VafwgngQii+O08nZIIWk7gLJ8ycilxk/gwTKsN87VNydyXbicliBbk0znjL8zVVDtxQx5SDzYqO8YEfCvlKWeTV
---- END SSH2 PUBLIC KEY ----
```

可以看到，`id_rsa.pub`文件的格式和RFC4716定义的SSH公钥格式并不完成相同，不过公钥体的数据部分是相同的。即：

```
         string    certificate or public key format identifier
         byte[n]   key/certificate data
```

通过解码`id_rsa.pub`文件中的公钥体数据，显示如下：

```
$ echo AAAAB3NzaC1yc2EAAAADAQABAAABAQDTw1ey8xdWQgz/Y9aTXhYM8rGJXCj11QZbAYBQ1oGjSoB0meeDfIBjQl4cYRvFR2VogIzZ0c1u0g4D1cXFpXClGnoxqyf1SCb0BgUxijKOV9vImu7CHo8L2CgjwjszIfJAs/S7L8KiZ5kestSrQQG1Wg1Npghdv9T20yQ6M2ZDDt4Yu88p3XH686amT3QVYTdn94qcXn+lF8VWn9mBPXxmVXXGkOmOYIabjs0WExkFKPL4fvN6kbp3EUTOYBRq3VafwgngQii+O08nZIIWk7gLJ8ycilxk/gwTKsN87VNydyXbicliBbk0znjL8zVVDtxQx5SDzYqO8YEfCvlKWeTV | base64 -d | hexdump -C

00000000  00 00 00 07 73 73 68 2d  72 73 61 00 00 00 03 01  |....ssh-rsa.....|
00000010  00 01 00 00 01 01 00 d3  c3 57 b2 f3 17 56 42 0c  |.........W...VB.|
00000020  ff 63 d6 93 5e 16 0c f2  b1 89 5c 28 f5 d5 06 5b  |.c..^.....\(...[|
00000030  01 80 50 d6 81 a3 4a 80  74 99 e7 83 7c 80 63 42  |..P...J.t...|.cB|
00000040  5e 1c 61 1b c5 47 65 68  80 8c d9 d1 cd 6e d2 0e  |^.a..Geh.....n..|
00000050  03 d5 c5 c5 a5 70 a5 1a  7a 31 ab 27 f5 48 26 f4  |.....p..z1.'.H&.|
00000060  06 05 31 8a 32 8e 57 db  c8 9a ee c2 1e 8f 0b d8  |..1.2.W.........|
00000070  28 23 c2 3b 33 21 f2 40  b3 f4 bb 2f c2 a2 67 99  |(#.;3!.@.../..g.|
00000080  1e b2 d4 ab 41 01 b5 5a  0d 4d a6 08 5d bf d4 f6  |....A..Z.M..]...|
00000090  d3 24 3a 33 66 43 0e de  18 bb cf 29 dd 71 fa f3  |.$:3fC.....).q..|
000000a0  a6 a6 4f 74 15 61 37 67  f7 8a 9c 5e 7f a5 17 c5  |..Ot.a7g...^....|
000000b0  56 9f d9 81 3d 7c 66 55  75 c6 90 e9 8e 60 86 9b  |V...=|fUu....`..|
000000c0  8e cd 16 13 19 05 28 f2  f8 7e f3 7a 91 ba 77 11  |......(..~.z..w.|
000000d0  44 ce 60 14 6a dd 56 9f  c2 09 e0 42 28 be 3b 4f  |D.`.j.V....B(.;O|
000000e0  27 64 82 16 93 b8 0b 27  cc 9c 8a 5c 64 fe 0c 13  |'d.....'...\d...|
000000f0  2a c3 7c ed 53 72 77 25  db 89 c9 62 05 b9 34 ce  |*.|.Srw%...b..4.|
00000100  78 cb f3 35 55 0e dc 50  c7 94 83 cd 8a 8e f1 81  |x..5U..P........|
00000110  1f 0a f9 4a 59 e4 d5                              |...JY..|
00000117
```

可以看出`00 00 00 07 73 73 68 2d  72 73 61`十六进制序列表示`string`格式的公钥表示符合ssh-rsa（00 00 00 07表示字符串(string: [5.  Data Type Representations Used in the SSH Protocols](https://tools.ietf.org/html/rfc4251#section-5))的长度为7）。其余公钥体的组成部分可以参照[RFC4253 section-6.6](https://tools.ietf.org/html/rfc4253#section-6.6)。其中，描述的RSA公钥格式如下：

```
   The "ssh-rsa" key format has the following specific encoding:

      string    "ssh-rsa"
      mpint     e
      mpint     n

   Here the 'e' and 'n' parameters form the signature key blob.
```

这里，我们的公钥e=65537(0x010001, 三个字节), n=26732609361384541213316174200406614034201948183651344589062082178500428348244311662800801196886944334589671911919831390497140751758055400426660769753298824880887767136020187542289865603129671255976812058539393143385419594024606720191900899106987584047573643701843366742447817679052082556396601913877853316040358959967709835896762373375048189285864722940254544729109691262220792421052412006183959728271324170851340468766451363362612736157651778910511864849616033016902038784863312121722282906977668702773974210384222096323428592747683046754707399781481530589082529404389492820030364235199271144424382095406835349185749(0x00d3c357b2f31756420cff63d6935e160cf2b1895c28f5d5065b018050d681a34a807499e7837c8063425e1c611bc5476568808cd9d1cd6ed20e03d5c5c5a570a51a7a31ab27f54826f40605318a328e57dbc89aeec21e8f0bd82823c23b3321f240b3f4bb2fc2a267991eb2d4ab4101b55a0d4da6085dbfd4f6d3243a3366430ede18bbcf29dd71faf3a6a64f7415613767f78a9c5e7fa517c5569fd9813d7c665575c690e98e60869b8ecd1613190528f2f87ef37a91ba771144ce60146add569fc209e04228be3b4f2764821693b80b27cc9c8a5c64fe0c132ac37ced53727725db89c96205b934ce78cbf335550edc50c79483cd8a8ef1811f0af94a59e4d5,257个字节)

#### ssh-keygen 私钥文件 id_rsa

`ssh-keygen`默认产生的私钥的格式为: `RSA Private Key file (PKCS#1)`。

> https://tls.mbed.org/kb/cryptography/asn1-key-structures-in-der-and-pem

##### RSA Private Key file (PKCS#1)

The RSA private key PEM file is specific for RSA keys.

It starts and ends with the tags:

```
-----BEGIN RSA PRIVATE KEY-----
BASE64 ENCODED DATA
-----END RSA PRIVATE KEY-----
```

Within the base64 encoded data the following DER structure is present:

```
RSAPrivateKey ::= SEQUENCE {
  version           Version,
  modulus           INTEGER,  -- n
  publicExponent    INTEGER,  -- e
  privateExponent   INTEGER,  -- d
  prime1            INTEGER,  -- p
  prime2            INTEGER,  -- q
  exponent1         INTEGER,  -- d mod (p-1)
  exponent2         INTEGER,  -- d mod (q-1)
  coefficient       INTEGER,  -- (inverse of q) mod p
  otherPrimeInfos   OtherPrimeInfos OPTIONAL
}
```

##### Private Key file (PKCS#8)

Because RSA is not used exclusively inside X509 and SSL/TLS, a more generic key format is available in the form of PKCS#8, that identifies the type of private key and contains the relevant data.

The unencrypted PKCS#8 encoded data starts and ends with the tags:

```
-----BEGIN PRIVATE KEY-----
BASE64 ENCODED DATA
-----END PRIVATE KEY-----
```

Within the base64 encoded data the following DER structure is present:

```
PrivateKeyInfo ::= SEQUENCE {
  version         Version,
  algorithm       AlgorithmIdentifier,
  PrivateKey      OCTET STRING
}

AlgorithmIdentifier ::= SEQUENCE {
  algorithm       OBJECT IDENTIFIER,
  parameters      ANY DEFINED BY algorithm OPTIONAL
}
```

解码私钥数据后，可以看到上述定义数据符合`RSA Private Key file (PKCS#1)`定义的格式：

```
$ echo MIIEpAIBAAKCAQEA08NXsvMXVkIM/2PWk14WDPKxiVwo9dUGWwGAUNaBo0qAdJnng3yAY0JeHGEbxUdlaICM2dHNbtIOA9XFxaVwpRp6Masn9Ugm9AYFMYoyjlfbyJruwh6PC9goI8I7MyHyQLP0uy/ComeZHrLUq0EBtVoNTaYIXb/U9tMkOjNmQw7eGLvPKd1x+vOmpk90FWE3Z/eKnF5/pRfFVp/ZgT18ZlV1xpDpjmCGm47NFhMZBSjy+H7zepG6dxFEzmAUat1Wn8IJ4EIovjtPJ2SCFpO4CyfMnIpcZP4MEyrDfO1Tcncl24nJYgW5NM54y/M1VQ7cUMeUg82KjvGBHwr5Slnk1QIDAQABAoIBAEnBXcg8FsK6WqCQ+2l0eaWk2eUHrlSBD6eezDxbmedvyXHTMOmA8Y6gzPqBcBS0G0PckjJDepPAoZUAXdPLHYLDyA+Il3A84yRW/HQWuCkPvMMQA1ylHBl5/fEGc2wJxMB4bSLNLbM29gPVMXE8QQYTCVMkIwHUEK6vN4z13gY4gvWEy9XB+FAyKG7Pu8EAWOyBd415pd5SOYHB58Y9CNUrEnfOwO3Nll6brNofEcrbz7+eI1zKh9xbKFZC04FNtbaO4jNpj8GKV8K2WpOArkrnx0gg+AZOzz7S6CJcDSWpBPatgEoEeHqBRPpIsGqy1DgNXCkgp23O1XGggUdJDDkCgYEA9vuwvZzQB32jOIrn3/2glZCciGL94c7X7PjY6MrIp6nn4KNBlq2NKV11GS4tzaqk6dqKrj4RI9+g7b9PRn53V30zKe53q0Vg92KYWziZrwciwVvkxNQzeKSdV/cUxsZbVksSy8XmFCSwF4QzicdmamytEQ0FAZ4D1ukvjiJS1usCgYEA2357/cLSFhqXjOSx0Trx4/q5X5eMxGr2hYfL0B6Xp1WVwoFNeeayWDGJ7c0oyfPVRbVW3Tzig0TWjGIANVlrdVGQ3NLFrUgcNPHWNW0Xjl66ZJgwxZ+nRnRK/gwoc+PHiD0QEYLbuC9vP3t/7+I6y0RV3MbrKVY+iRNFDm5Gwz8CgYBWavyNa9fyNwisWRYG7sSIcKAErLZukyREO1ISKhoJaE7E7/qcET+qMJQvalQGeWXYmWoay4bNyYqShXTkko2JZDpJurHOkKj8BliO2oATmOiVRWUHZcRYuyh+xepUHsWIrR33hNgbRjcDE3PBCq8QH9Ryed69kR+Ay/iiv+nCXwKBgQDLpjFYotfVllqiaNXq8SvZgJlZ7fy3iR6tie86bAf9Q9UtoFbIEZnLZjs5Hi8IIWnxwWyU3Ja1gLsniQ30ccDYGxOzLwQl4E/7d55t94fxmkaKawJlednz7pZd2930mJRa/XzZInbGD4zCc82iPl6alg6sRwuNUO24tN5Po1WYdQKBgQCppfdHFoqyDQ8iMq1Ni93sd6uBEilZViI7ovcOR+zHuTy9lY0Ru1mz+kSNRPhFuc3QwfzfF9BVtUlM9Npuj9HYy69smnh3tZQPfLcss+DJrgtRLHKEdK1FOfC+pjfLouZ8jTdVp1/bD6WXgpKudBXCitZRlodNIuoI8us/FHbCGA== | base64 -d | hexdump -C

00000000  30 82 04 a4 02 01 00 02  82 01 01 00 d3 c3 57 b2  |0.............W.|
00000010  f3 17 56 42 0c ff 63 d6  93 5e 16 0c f2 b1 89 5c  |..VB..c..^.....\|
00000020  28 f5 d5 06 5b 01 80 50  d6 81 a3 4a 80 74 99 e7  |(...[..P...J.t..|
00000030  83 7c 80 63 42 5e 1c 61  1b c5 47 65 68 80 8c d9  |.|.cB^.a..Geh...|
00000040  d1 cd 6e d2 0e 03 d5 c5  c5 a5 70 a5 1a 7a 31 ab  |..n.......p..z1.|
00000050  27 f5 48 26 f4 06 05 31  8a 32 8e 57 db c8 9a ee  |'.H&...1.2.W....|
00000060  c2 1e 8f 0b d8 28 23 c2  3b 33 21 f2 40 b3 f4 bb  |.....(#.;3!.@...|
00000070  2f c2 a2 67 99 1e b2 d4  ab 41 01 b5 5a 0d 4d a6  |/..g.....A..Z.M.|
00000080  08 5d bf d4 f6 d3 24 3a  33 66 43 0e de 18 bb cf  |.]....$:3fC.....|
00000090  29 dd 71 fa f3 a6 a6 4f  74 15 61 37 67 f7 8a 9c  |).q....Ot.a7g...|
000000a0  5e 7f a5 17 c5 56 9f d9  81 3d 7c 66 55 75 c6 90  |^....V...=|fUu..|
000000b0  e9 8e 60 86 9b 8e cd 16  13 19 05 28 f2 f8 7e f3  |..`........(..~.|
000000c0  7a 91 ba 77 11 44 ce 60  14 6a dd 56 9f c2 09 e0  |z..w.D.`.j.V....|
000000d0  42 28 be 3b 4f 27 64 82  16 93 b8 0b 27 cc 9c 8a  |B(.;O'd.....'...|
000000e0  5c 64 fe 0c 13 2a c3 7c  ed 53 72 77 25 db 89 c9  |\d...*.|.Srw%...|
000000f0  62 05 b9 34 ce 78 cb f3  35 55 0e dc 50 c7 94 83  |b..4.x..5U..P...|
00000100  cd 8a 8e f1 81 1f 0a f9  4a 59 e4 d5 02 03 01 00  |........JY......|
00000110  01 02 82 01 00 49 c1 5d  c8 3c 16 c2 ba 5a a0 90  |.....I.].<...Z..|
00000120  fb 69 74 79 a5 a4 d9 e5  07 ae 54 81 0f a7 9e cc  |.ity......T.....|
00000130  3c 5b 99 e7 6f c9 71 d3  30 e9 80 f1 8e a0 cc fa  |<[..o.q.0.......|
00000140  81 70 14 b4 1b 43 dc 92  32 43 7a 93 c0 a1 95 00  |.p...C..2Cz.....|
00000150  5d d3 cb 1d 82 c3 c8 0f  88 97 70 3c e3 24 56 fc  |].........p<.$V.|
00000160  74 16 b8 29 0f bc c3 10  03 5c a5 1c 19 79 fd f1  |t..).....\...y..|
00000170  06 73 6c 09 c4 c0 78 6d  22 cd 2d b3 36 f6 03 d5  |.sl...xm".-.6...|
00000180  31 71 3c 41 06 13 09 53  24 23 01 d4 10 ae af 37  |1q<A...S$#.....7|
00000190  8c f5 de 06 38 82 f5 84  cb d5 c1 f8 50 32 28 6e  |....8.......P2(n|
000001a0  cf bb c1 00 58 ec 81 77  8d 79 a5 de 52 39 81 c1  |....X..w.y..R9..|
000001b0  e7 c6 3d 08 d5 2b 12 77  ce c0 ed cd 96 5e 9b ac  |..=..+.w.....^..|
000001c0  da 1f 11 ca db cf bf 9e  23 5c ca 87 dc 5b 28 56  |........#\...[(V|
000001d0  42 d3 81 4d b5 b6 8e e2  33 69 8f c1 8a 57 c2 b6  |B..M....3i...W..|
000001e0  5a 93 80 ae 4a e7 c7 48  20 f8 06 4e cf 3e d2 e8  |Z...J..H ..N.>..|
000001f0  22 5c 0d 25 a9 04 f6 ad  80 4a 04 78 7a 81 44 fa  |"\.%.....J.xz.D.|
00000200  48 b0 6a b2 d4 38 0d 5c  29 20 a7 6d ce d5 71 a0  |H.j..8.\) .m..q.|
00000210  81 47 49 0c 39 02 81 81  00 f6 fb b0 bd 9c d0 07  |.GI.9...........|
00000220  7d a3 38 8a e7 df fd a0  95 90 9c 88 62 fd e1 ce  |}.8.........b...|
00000230  d7 ec f8 d8 e8 ca c8 a7  a9 e7 e0 a3 41 96 ad 8d  |............A...|
00000240  29 5d 75 19 2e 2d cd aa  a4 e9 da 8a ae 3e 11 23  |)]u..-.......>.#|
00000250  df a0 ed bf 4f 46 7e 77  57 7d 33 29 ee 77 ab 45  |....OF~wW}3).w.E|
00000260  60 f7 62 98 5b 38 99 af  07 22 c1 5b e4 c4 d4 33  |`.b.[8...".[...3|
00000270  78 a4 9d 57 f7 14 c6 c6  5b 56 4b 12 cb c5 e6 14  |x..W....[VK.....|
00000280  24 b0 17 84 33 89 c7 66  6a 6c ad 11 0d 05 01 9e  |$...3..fjl......|
00000290  03 d6 e9 2f 8e 22 52 d6  eb 02 81 81 00 db 7e 7b  |.../."R.......~{|
000002a0  fd c2 d2 16 1a 97 8c e4  b1 d1 3a f1 e3 fa b9 5f  |..........:...._|
000002b0  97 8c c4 6a f6 85 87 cb  d0 1e 97 a7 55 95 c2 81  |...j........U...|
000002c0  4d 79 e6 b2 58 31 89 ed  cd 28 c9 f3 d5 45 b5 56  |My..X1...(...E.V|
000002d0  dd 3c e2 83 44 d6 8c 62  00 35 59 6b 75 51 90 dc  |.<..D..b.5YkuQ..|
000002e0  d2 c5 ad 48 1c 34 f1 d6  35 6d 17 8e 5e ba 64 98  |...H.4..5m..^.d.|
000002f0  30 c5 9f a7 46 74 4a fe  0c 28 73 e3 c7 88 3d 10  |0...FtJ..(s...=.|
00000300  11 82 db b8 2f 6f 3f 7b  7f ef e2 3a cb 44 55 dc  |..../o?{...:.DU.|
00000310  c6 eb 29 56 3e 89 13 45  0e 6e 46 c3 3f 02 81 80  |..)V>..E.nF.?...|
00000320  56 6a fc 8d 6b d7 f2 37  08 ac 59 16 06 ee c4 88  |Vj..k..7..Y.....|
00000330  70 a0 04 ac b6 6e 93 24  44 3b 52 12 2a 1a 09 68  |p....n.$D;R.*..h|
00000340  4e c4 ef fa 9c 11 3f aa  30 94 2f 6a 54 06 79 65  |N.....?.0./jT.ye|
00000350  d8 99 6a 1a cb 86 cd c9  8a 92 85 74 e4 92 8d 89  |..j........t....|
00000360  64 3a 49 ba b1 ce 90 a8  fc 06 58 8e da 80 13 98  |d:I.......X.....|
00000370  e8 95 45 65 07 65 c4 58  bb 28 7e c5 ea 54 1e c5  |..Ee.e.X.(~..T..|
00000380  88 ad 1d f7 84 d8 1b 46  37 03 13 73 c1 0a af 10  |.......F7..s....|
00000390  1f d4 72 79 de bd 91 1f  80 cb f8 a2 bf e9 c2 5f  |..ry..........._|
000003a0  02 81 81 00 cb a6 31 58  a2 d7 d5 96 5a a2 68 d5  |......1X....Z.h.|
000003b0  ea f1 2b d9 80 99 59 ed  fc b7 89 1e ad 89 ef 3a  |..+...Y........:|
000003c0  6c 07 fd 43 d5 2d a0 56  c8 11 99 cb 66 3b 39 1e  |l..C.-.V....f;9.|
000003d0  2f 08 21 69 f1 c1 6c 94  dc 96 b5 80 bb 27 89 0d  |/.!i..l......'..|
000003e0  f4 71 c0 d8 1b 13 b3 2f  04 25 e0 4f fb 77 9e 6d  |.q...../.%.O.w.m|
000003f0  f7 87 f1 9a 46 8a 6b 02  65 79 d9 f3 ee 96 5d db  |....F.k.ey....].|
00000400  dd f4 98 94 5a fd 7c d9  22 76 c6 0f 8c c2 73 cd  |....Z.|."v....s.|
00000410  a2 3e 5e 9a 96 0e ac 47  0b 8d 50 ed b8 b4 de 4f  |.>^....G..P....O|
00000420  a3 55 98 75 02 81 81 00  a9 a5 f7 47 16 8a b2 0d  |.U.u.......G....|
00000430  0f 22 32 ad 4d 8b dd ec  77 ab 81 12 29 59 56 22  |."2.M...w...)YV"|
00000440  3b a2 f7 0e 47 ec c7 b9  3c bd 95 8d 11 bb 59 b3  |;...G...<.....Y.|
00000450  fa 44 8d 44 f8 45 b9 cd  d0 c1 fc df 17 d0 55 b5  |.D.D.E........U.|
00000460  49 4c f4 da 6e 8f d1 d8  cb af 6c 9a 78 77 b5 94  |IL..n.....l.xw..|
00000470  0f 7c b7 2c b3 e0 c9 ae  0b 51 2c 72 84 74 ad 45  |.|.,.....Q,r.t.E|
00000480  39 f0 be a6 37 cb a2 e6  7c 8d 37 55 a7 5f db 0f  |9...7...|.7U._..|
00000490  a5 97 82 92 ae 74 15 c2  8a d6 51 96 87 4d 22 ea  |.....t....Q..M".|
000004a0  08 f2 eb 3f 14 76 c2 18                           |...?.v..|
000004a8
```

对于`ssh-keygen`命令产生的私钥，`openssl`命令也可以解析，使用命令`openssl rsa -noout -in id_rsa  -text`可以更方便的查看rsa私钥的各个组件

```
$ openssl rsa -noout -in id_rsa  -text

Private-Key: (2048 bit)
modulus:
    00:d3:c3:57:b2:f3:17:56:42:0c:ff:63:d6:93:5e:
    16:0c:f2:b1:89:5c:28:f5:d5:06:5b:01:80:50:d6:
    81:a3:4a:80:74:99:e7:83:7c:80:63:42:5e:1c:61:
    1b:c5:47:65:68:80:8c:d9:d1:cd:6e:d2:0e:03:d5:
    c5:c5:a5:70:a5:1a:7a:31:ab:27:f5:48:26:f4:06:
    05:31:8a:32:8e:57:db:c8:9a:ee:c2:1e:8f:0b:d8:
    28:23:c2:3b:33:21:f2:40:b3:f4:bb:2f:c2:a2:67:
    99:1e:b2:d4:ab:41:01:b5:5a:0d:4d:a6:08:5d:bf:
    d4:f6:d3:24:3a:33:66:43:0e:de:18:bb:cf:29:dd:
    71:fa:f3:a6:a6:4f:74:15:61:37:67:f7:8a:9c:5e:
    7f:a5:17:c5:56:9f:d9:81:3d:7c:66:55:75:c6:90:
    e9:8e:60:86:9b:8e:cd:16:13:19:05:28:f2:f8:7e:
    f3:7a:91:ba:77:11:44:ce:60:14:6a:dd:56:9f:c2:
    09:e0:42:28:be:3b:4f:27:64:82:16:93:b8:0b:27:
    cc:9c:8a:5c:64:fe:0c:13:2a:c3:7c:ed:53:72:77:
    25:db:89:c9:62:05:b9:34:ce:78:cb:f3:35:55:0e:
    dc:50:c7:94:83:cd:8a:8e:f1:81:1f:0a:f9:4a:59:
    e4:d5
publicExponent: 65537 (0x10001)
privateExponent:
    49:c1:5d:c8:3c:16:c2:ba:5a:a0:90:fb:69:74:79:
    a5:a4:d9:e5:07:ae:54:81:0f:a7:9e:cc:3c:5b:99:
    e7:6f:c9:71:d3:30:e9:80:f1:8e:a0:cc:fa:81:70:
    14:b4:1b:43:dc:92:32:43:7a:93:c0:a1:95:00:5d:
    d3:cb:1d:82:c3:c8:0f:88:97:70:3c:e3:24:56:fc:
    74:16:b8:29:0f:bc:c3:10:03:5c:a5:1c:19:79:fd:
    f1:06:73:6c:09:c4:c0:78:6d:22:cd:2d:b3:36:f6:
    03:d5:31:71:3c:41:06:13:09:53:24:23:01:d4:10:
    ae:af:37:8c:f5:de:06:38:82:f5:84:cb:d5:c1:f8:
    50:32:28:6e:cf:bb:c1:00:58:ec:81:77:8d:79:a5:
    de:52:39:81:c1:e7:c6:3d:08:d5:2b:12:77:ce:c0:
    ed:cd:96:5e:9b:ac:da:1f:11:ca:db:cf:bf:9e:23:
    5c:ca:87:dc:5b:28:56:42:d3:81:4d:b5:b6:8e:e2:
    33:69:8f:c1:8a:57:c2:b6:5a:93:80:ae:4a:e7:c7:
    48:20:f8:06:4e:cf:3e:d2:e8:22:5c:0d:25:a9:04:
    f6:ad:80:4a:04:78:7a:81:44:fa:48:b0:6a:b2:d4:
    38:0d:5c:29:20:a7:6d:ce:d5:71:a0:81:47:49:0c:
    39
prime1:
    00:f6:fb:b0:bd:9c:d0:07:7d:a3:38:8a:e7:df:fd:
    a0:95:90:9c:88:62:fd:e1:ce:d7:ec:f8:d8:e8:ca:
    c8:a7:a9:e7:e0:a3:41:96:ad:8d:29:5d:75:19:2e:
    2d:cd:aa:a4:e9:da:8a:ae:3e:11:23:df:a0:ed:bf:
    4f:46:7e:77:57:7d:33:29:ee:77:ab:45:60:f7:62:
    98:5b:38:99:af:07:22:c1:5b:e4:c4:d4:33:78:a4:
    9d:57:f7:14:c6:c6:5b:56:4b:12:cb:c5:e6:14:24:
    b0:17:84:33:89:c7:66:6a:6c:ad:11:0d:05:01:9e:
    03:d6:e9:2f:8e:22:52:d6:eb
prime2:
    00:db:7e:7b:fd:c2:d2:16:1a:97:8c:e4:b1:d1:3a:
    f1:e3:fa:b9:5f:97:8c:c4:6a:f6:85:87:cb:d0:1e:
    97:a7:55:95:c2:81:4d:79:e6:b2:58:31:89:ed:cd:
    28:c9:f3:d5:45:b5:56:dd:3c:e2:83:44:d6:8c:62:
    00:35:59:6b:75:51:90:dc:d2:c5:ad:48:1c:34:f1:
    d6:35:6d:17:8e:5e:ba:64:98:30:c5:9f:a7:46:74:
    4a:fe:0c:28:73:e3:c7:88:3d:10:11:82:db:b8:2f:
    6f:3f:7b:7f:ef:e2:3a:cb:44:55:dc:c6:eb:29:56:
    3e:89:13:45:0e:6e:46:c3:3f
exponent1:
    56:6a:fc:8d:6b:d7:f2:37:08:ac:59:16:06:ee:c4:
    88:70:a0:04:ac:b6:6e:93:24:44:3b:52:12:2a:1a:
    09:68:4e:c4:ef:fa:9c:11:3f:aa:30:94:2f:6a:54:
    06:79:65:d8:99:6a:1a:cb:86:cd:c9:8a:92:85:74:
    e4:92:8d:89:64:3a:49:ba:b1:ce:90:a8:fc:06:58:
    8e:da:80:13:98:e8:95:45:65:07:65:c4:58:bb:28:
    7e:c5:ea:54:1e:c5:88:ad:1d:f7:84:d8:1b:46:37:
    03:13:73:c1:0a:af:10:1f:d4:72:79:de:bd:91:1f:
    80:cb:f8:a2:bf:e9:c2:5f
exponent2:
    00:cb:a6:31:58:a2:d7:d5:96:5a:a2:68:d5:ea:f1:
    2b:d9:80:99:59:ed:fc:b7:89:1e:ad:89:ef:3a:6c:
    07:fd:43:d5:2d:a0:56:c8:11:99:cb:66:3b:39:1e:
    2f:08:21:69:f1:c1:6c:94:dc:96:b5:80:bb:27:89:
    0d:f4:71:c0:d8:1b:13:b3:2f:04:25:e0:4f:fb:77:
    9e:6d:f7:87:f1:9a:46:8a:6b:02:65:79:d9:f3:ee:
    96:5d:db:dd:f4:98:94:5a:fd:7c:d9:22:76:c6:0f:
    8c:c2:73:cd:a2:3e:5e:9a:96:0e:ac:47:0b:8d:50:
    ed:b8:b4:de:4f:a3:55:98:75
coefficient:
    00:a9:a5:f7:47:16:8a:b2:0d:0f:22:32:ad:4d:8b:
    dd:ec:77:ab:81:12:29:59:56:22:3b:a2:f7:0e:47:
    ec:c7:b9:3c:bd:95:8d:11:bb:59:b3:fa:44:8d:44:
    f8:45:b9:cd:d0:c1:fc:df:17:d0:55:b5:49:4c:f4:
    da:6e:8f:d1:d8:cb:af:6c:9a:78:77:b5:94:0f:7c:
    b7:2c:b3:e0:c9:ae:0b:51:2c:72:84:74:ad:45:39:
    f0:be:a6:37:cb:a2:e6:7c:8d:37:55:a7:5f:db:0f:
    a5:97:82:92:ae:74:15:c2:8a:d6:51:96:87:4d:22:
    ea:08:f2:eb:3f:14:76:c2:18
```

从上述数据可以看到，两个素数构成的rsa秘钥对中，私钥里面的prime1 * prime2 = modulus。

SSH具体的架构可以参考RFC4251：[The Secure Shell (SSH) Protocol Architecture](https://www.ietf.org/rfc/rfc4251.txt)和RFC8308：[Extension Negotiation in the Secure Shell (SSH) Protocol](https://tools.ietf.org/html/rfc8308)。

Reference:

[The Secure Shell (SSH) Public Key File Format](https://tools.ietf.org/html/rfc4716)

[The Secure Shell (SSH) Transport Layer Protocol](https://tools.ietf.org/html/rfc4253#section-6.6)

[ASN.1 key structures in DER and PEM](https://tls.mbed.org/kb/cryptography/asn1-key-structures-in-der-and-pem)

[PKCS #1: RSA Cryptography Specifications Version 2.2](https://tools.ietf.org/html/rfc8017)

[Public-Key Cryptography Standards (PKCS) #8: Private-Key Information Syntax Specification Version 1.2](https://tools.ietf.org/html/rfc5208)