### python sys.argv 参数详解

sys.argv用来获取命令行中的参数，sys.argv的值为数组。

数组第一元素的值sys.argv[0]表示代码本身文件路径（文件名），该值可能为相对路径，也可能是绝对路径。

如下代码：

```
#!/usr/bin/env python
import sys
print sys.argv
```

Linux平台输出如下：

```
$ ./test.py 1 2 3
['./test.py', '1', '2', '3']

$ python test.py 1 2 3
['test.py', '1', '2', '3']
```
Windows平台输出如下：

```
C:\Users\zhang\Desktop>test.py 1 2 3
['C:\\Users\\zhang\\Desktop\\test.py', '1', '2', '3']

C:\Users\zhang\Desktop>python test.py 1 2 3
['test.py', '1', '2', '3']

C:\Users\zhang\Desktop>python ..\Desktop\test.py 1 2 3
['..\\Desktop\\test.py', '1', '2', '3']
```