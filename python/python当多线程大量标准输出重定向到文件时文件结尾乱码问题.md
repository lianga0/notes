# python当多线程标准输出重定向到文件时文件结尾乱码问题

碰到多线程输出到标准输出时，字符串乱行错误问题，运行如下python程序，可以看到直接在标准输出上显示内容无误

```
import threading
def print_hello_world():
    i=0
    while i < 1000:
        i+=1
        print("Hello, World!"*10)
    pass

# 创建线程
threads = []
for i in range(500):
    t = threading.Thread(target=print_hello_world)
    threads.append(t)
    t.start()

# 等待所有线程完成
for t in threads:
    t.join()
```

重定向到文件后，如命令`python a.py > a.txt`可以看到a.txt文件末尾存在一些乱码，并且输出并不足500000行。
这是因为虽然python中print函数线程安全，但是Python的print函数默认是缓冲的，也就是说，它会先把输出存储在一个缓冲区中，当缓冲区满了或者程序结束时，才会把输出写入到文件中。这就可能导致缓冲区数据刷新不匹配的问题，把代码改为如下，再重新运行即可在windows 10平台中解决文件重定向末尾乱码问题


```
import threading
import sys
def print_hello_world():
    i=0
    while i < 1000:
        i+=1
        print("Hello, World!"*10)
    sys.stdout.flush()

# 创建线程
threads = []
for i in range(500):
    t = threading.Thread(target=print_hello_world)
    threads.append(t)
    t.start()

# 等待所有线程完成
for t in threads:
    t.join()
```

或

```
import threading
def print_hello_world():
    i=0
    while i < 1000:
        i+=1
        print("Hello, World!"*10, flush=True)
    pass

# 创建线程
threads = []
for i in range(500):
    t = threading.Thread(target=print_hello_world)
    threads.append(t)
    t.start()

# 等待所有线程完成
for t in threads:
    t.join()
```

Reference：

[python 执行脚本，并将输出打印到文件](https://www.cnblogs.com/zjdxr-up/p/17825940.html)

[How to use printf() in multiple threads](https://stackoverflow.com/questions/23586682/how-to-use-printf-in-multiple-threads)

> Show a code example that illustrates the problem. Like @Duck, I've never seen two printf writes intermingled.

> printf函数在多线程环境中的行为取决于其实现。在POSIX标准中，printf函数被认为是线程安全的。这是因为POSIX规定，所有操作字符流（由FILE*对象表示）的C语言函数和POSIX.1函数都必须以实现重入性的方式实现2。这意味着，理论上，你可以在多个线程中同时调用printf函数，而不会出现数据竞争或其他线程安全问题。

> 多进程同时输出到标准输出乱行问题需要进一步使用进程同步机制进行解决