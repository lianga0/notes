# linux文件编码转换命令iconv

`iconv`命令 是用来转换文件的编码方式的，比如它可以将UTF8编码的转换成GB18030的编码，反过来也行。

```
iconv -f encoding [-t encoding] [inputfile]...
```

* `-f` encoding :把字符从encoding编码开始转换。

* `-t` encoding :把字符转换到encoding编码。

* `-l` :列出已知的编码字符集合

* `-o` file :指定输出文件

* `-c` :忽略输出的非法字符

* `-s` :禁止警告信息，但不是错误信息

* `–verbose` :显示进度

* `-f`和`-t`所能指定的合法字符在-l选项的命令里面都列出来了。
