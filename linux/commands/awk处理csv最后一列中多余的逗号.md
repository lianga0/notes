# awk 处理非正式产生的CSV文件

正常的CSV文件使用逗号分割各个列，若列中值包含逗号时需要用引号包含该值。

## awk合并CSV列

目前有一个自己手动拼接的CSV文件，文件最后一列为文件名，因为文件名中可能包含逗号，但是该值未用双引号包含。样例数据如下：

```
8a90ef3ea9858aef984928c0985a9839,10752,7,5,Win32 DLL,I:\\Program Files\Common Files\microsoft shared\ink\ar-SA\tipresx.dll.mui
```

因为前几列不会出错，所以可以使用AWK删除最后一列多余的逗号，如下：

```
awk -F , '{print $1","$2","$3","$4","$5","$6$7$8}' file.csv
```

也就是把第6到8列合并为一列。

## 追加文件名到最后一列

如果有多个文件，我们还可以把文件名加到最后一列，如下：

```
awk -F , '{print $1","$2","$3","$4","$5","$6$7$8","FILENAME}' file*.csv
```

## 处理Windows平台换行问题

因为该CSV文件来自windows平台，所以它的换行符为`\r\n`，这导致awk处理后把`\r`字符带到了输出中（显示为^M）。这里使用awk将所有`\r`直接删除掉。

```
awk -F , 'gsub(/\r/,""){print $1","$2","$3","$4","$5","$6$7$8","FILENAME}' file*.csv
```

## iconv命令

有时候拿到的文件名可能存在错误编码，导致有些程序不能正确解码，这时候可以使用`iconv`转换编码，并剔除错误编码。

```
iconv -f utf-8 -t utf-8 -c file.csv > final.csv
```

## 合并多个CSV文件并过滤错误编码

```
awk -F , 'gsub(/\r/,""){print $1","$2","$3","$4","$5","$6 $7 $8","FILENAME}' file*.csv | iconv -f utf-8 -t utf-8 -c > final.csv
```

> 测试发现`iconv`命令有Bug，输出文件中有非法的UTF-8编码的字节序列（比如invalid byte sequence for encoding "UTF8": 0xf6 0xb4 0xb0 0xbf)。所以又找了一个新的工具`uconv`，不过你需要自己安装一下（`sudo apt install icu-devtools`）。

修正后命令格式如下

```
awk -F , 'gsub(/\r/,""){print $1","$2","$3","$4","$5","$6 $7 $8","FILENAME}' file*.csv | uconv -i -f utf-8 -t utf-8 -c > final.csv
```

合并完成后，可以使用`wc`命令看看文件中行数是否一致。

```
wc -l file*.csv
wc -l final.csv
```

Reference: [How to remove non UTF-8 characters from text file](https://stackoverflow.com/questions/12999651/how-to-remove-non-utf-8-characters-from-text-file)

[在Linux上删除Windows换行符（sed和awk）](http://zgserver.com/linuxwindowssedawk.html)
