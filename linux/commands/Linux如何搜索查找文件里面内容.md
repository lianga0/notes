### Linux如何搜索查找文件里面内容

> From: [潇湘隐者](http://www.cnblogs.com/kerrycode/p/5802420.html)
 
在Linux系统当中，搜索、查找文件当中的内容，一般最常用的是grep命令，另外还有egrep。 vi命令也能搜索文件里面内容，只不过没有grep命令功能那么方便、强大。

grep命令搜索指定文件中包含指定PATTERN的行，如果用户没有指定文件名或指定文件名为“-”，那么grep将搜索标准输入。grep默认仅输出PATTERN匹配的行。

另外，常见的egrep, fgrep 和 rgrep变种程序同grep -E, grep -F, 和 grep -r相同。（In addition, the variant programs egrep, fgrep and rgrep are the same as grep -E, grep -F, and grep -r, respectively.  These variants are deprecated, but are provided for backward compatibility.）

1. 搜索某个文件里面是否包含指定字符串

```
grep "search content" filename1
```

2. 搜索多个文件是否包含某个字符串

```
grep "search content" filename1 filename2
grep "search content" *.txt
```

3. 如果搜索时需要忽略大小写问题，可以使用参数 `-i`


4. 使用正则表达式进行搜索可以使用参数 `-e`


5. 如果需要显示搜索文本在文件中的行数，可以使用参数 `-n`


6. 搜索命中内容上下文方式显示方式

```
-A NUM, --after-context=NUM
-B NUM, --before-context=NUM
-C NUM, -NUM, --context=NUM
```

7. 最多命中行数，可以使用参数 `-m NUM, --max-count=NUM`

8. 从指定文件中加载搜索的pattern，可以使用参数 `-f`

9. 搜索、查找匹配的行数，可以使用参数 `-c`

10. 从文件内容查找不匹配指定字符串的行

```
grep -v "search content" filename1
```

11. 递归搜索某个目录以及子目录下的所有文件，可以使用参数 `-r` 或 `-R`

12. 如果我们只想获取那些文件包含搜索的内容，那么可以使用下命令

```
grep -H -r "pattern" /folder/path/ | cut -d: -f1
```

<完>