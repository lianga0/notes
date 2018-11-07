### Python性能分析器cProfile、line_profiler和memory_profiler

> 2018.3.31


Python中常见的三个性能分析工具有：cProfile、line_profiler、memory_profiler

- cProfile是python内置包，它主要用来统计函数调用以及每个函数所占的cpu时间。
- line_profiler可以帮你一行一行分析函数性能。
- memory_profiler帮你一行一行分析函数内存消耗。

#### 1. cProfile

cProfile是标准库内建的三个分析工具之一，另外两个是profile和hotshot。此外，还有一个辅助模块stats。这些模块提供了对Python程序的确定性分析功能，同时也提供了相应的报表生成工具，方便用户快速地检查和分析结果。

 这三个性能分析模块的介绍如下：

- cProfile：基于lsprof的用C语言实现的扩展应用，运行开销比较合理，适合分析运行时间较长的程序，推荐使用这个模块；

- profile：纯Python实现的性能分析模块，接口和cProfile一致。但在分析程序时增加了很大的运行开销。不过，如果你想扩展profiler的功能，可以通过继承这个模块实现；

- hotshot：一个试验性的C模块，减少了性能分析时的运行开销，但是需要更长的数据后处理的次数。目前这个模块不再被维护，有可能在新版本中被弃用。


由于hotshot基本不再使用，而profile和cProfile的用法基本一致，所以下面就只介绍一下cProfile的用法。

cProfile模块存在两种使用方式，一种是不需要修改待测Python文件，通过命令启动cProfile模块并将代分析文件作为参数。另外一种是，在代码内导入cProfile模块模块，然后使用cProfile模块提供的方法还有针对的测试自己的代码。


##### 1.1 命令行模块方式运行


```
python -m cProfile -s cumulative performance_testing_file.py
```


其中，-s cumulative开关告诉cProfile对每个函数累计花费的时间进行排序，这能让我们看到代码最慢的部分。cProfile会将输出直接打印到屏幕：

```
         154675 function calls (150154 primitive calls) in 23.437 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
    271/1    0.027    0.000   23.438   23.438 {built-in method builtins.exec}
        1    0.000    0.000   23.438   23.438 ttt.py:1(<module>)
        1    0.000    0.000   21.057   21.057 api.py:61(get)
        1    0.000    0.000   21.057   21.057 api.py:16(request)
        1    0.000    0.000   21.056   21.056 sessions.py:441(request)
        1    0.000    0.000   21.037   21.037 sessions.py:589(send)
        1    0.000    0.000   21.037   21.037 adapters.py:388(send)
        1    0.000    0.000   21.036   21.036 connectionpool.py:447(urlopen)
        1    0.000    0.000   21.036   21.036 connectionpool.py:322(_make_request)
        1    0.000    0.000   21.036   21.036 connectionpool.py:842(_validate_conn)
        1    0.000    0.000   21.036   21.036 connection.py:282(connect)
        1    0.000    0.000   21.036   21.036 connection.py:127(_new_conn)
        1    0.000    0.000   21.035   21.035 connection.py:36(create_connection)
        1   21.001   21.001   21.001   21.001 {method 'connect' of '_socket.socket' objects}
    281/2    0.006    0.000    2.395    1.198 <frozen importlib._bootstrap>:966(_find_and_load)
...............
```

其中，输出每列的具体解释如下：

```
    ncalls：表示函数调用的次数；

    tottime：表示指定函数的总的运行时间，除掉函数中调用子函数的运行时间；

    percall：（第一个percall）等于 tottime/ncalls；

    cumtime：表示该函数及其所有子函数的调用运行的时间，即函数开始调用到返回的时间；

    percall：（第二个percall）即函数运行一次的平均时间，等于 cumtime/ncalls；

    filename:lineno(function)：每个函数调用的具体信息；
```

另外，上面分析的时候，排序方式使用的是函数调用时间(cumulative)，除了这个还有一些其他允许的排序方式：calls, cumulative, file, line, module, name, nfl, pcalls, stdname, time等。具体的结果如何，大家可以试试。

对累计时间排序能告诉我们大部分的执行时间花在了哪，这个时间包括了使用cProfile的开销。需要注意的是cProfile的输出并不以父函数排序，它总结了执行代码块的全部函数。用cProfile很难搞清楚函数内的每一行发生了什么，因为我们只拿到了函数自身调用的分析信息，而不是函数内的每一行。


为了获得对cProfile结果的更多控制，我们可以生成一个统计文件然后通过Python进行分析：

```
python -m cProfile -o profile.stats performance_testing_file.py
```

但是文件内容是以二进制的方式保存的，用文本编辑器打开时乱码。我们可以用Python提供的pstats模块，来分析cProfile输出的文件内容，它会输出跟之前一样的累计时间报告：

```
In [1]: import pstats
In [2]: p = pstats.Stats("profile.stats")
In [3]: p.sort_stats("cumulative")
Out[3]: <pstats.Stats instance at 0x177dcf8>
In [4]: p.print_stats()
Tue Jan 7 21:00:56 2014 profile.stats

        36221992 function calls in 19.983 seconds
...................
```

##### 图形化工具

对于一些比较大的应用程序，如果能够将性能分析的结果以图形的方式呈现，将会非常实用和直观，常见的可视化工具有Gprof2Dot，visualpytune，KCacheGrind等。 


##### 1.2 在Python脚本中实现

```
if __name__ == "__main__":
    import cProfile

    # 直接把分析结果打印到控制台
    cProfile.run("test()")
    # 把分析结果保存到文件中
    cProfile.run("test()", filename="result.out")
    # 增加排序方式
    cProfile.run("test()", filename="result.out", sort="cumulative")
```


#### 2. 使用line_profiler逐行计时和分析执行的频率

罗伯特·克恩有一个不错的项目称为line_profiler, 可以使用它来分析脚本有多快，以及每行代码执行的频率。

为了使用它，你可以通过使用  pip 来安装它：

```
pip install line_profiler
```

安装完成后，你将获得一个新模块称为`line_profiler`和`kernprof.py`可执行脚本。

为了使用这个工具，首先在你想测量的函数上设置`@profile`修饰符。不用担心，为了这个修饰符，你不需要引入任何东西。 `kernprof.py`脚本会在运行时自动注入你的脚本。

```
#primes.py

@profile
def primes(n): 
    if n==2:
        return [2]
    elif n<2:
        return []
    s=range(3,n+1,2)
    mroot = n ** 0.5
    half=(n+1)/2-1
    i=0
    m=3
    while m <= mroot:
        if s[i]:
            j=(m*m-3)/2
            s[j]=0
            while j<half:
                s[j]=0
                j+=m
        i=i+1
        m=2*i+3
    return [2]+[x for x in s if x]
primes(100)
```

一旦你得到了你的设置了修饰符`@profile`的代码，使用`kernprof.py`运行这个脚本。

```
kernprof.py -l -v fib.py
```

`-l`选项告诉`kernprof`把修饰符`@profile`注入你的脚本，`-v`选项告诉`kernprof`一旦你的脚本完成后，你应该可以获得输出结果。

```
Wrote profile results to primes.py.lprof
Timer unit: 1e-06 s

File: primes.py
Function: primes at line 2
Total time: 0.00019 s

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     2                                           @profile
     3                                           def primes(n): 
     4         1            2      2.0      1.1      if n==2:
     5                                                   return [2]
     6         1            1      1.0      0.5      elif n<2:
     7                                                   return []
     8         1            4      4.0      2.1      s=range(3,n+1,2)
     9         1           10     10.0      5.3      mroot = n ** 0.5
    10         1            2      2.0      1.1      half=(n+1)/2-1
    11         1            1      1.0      0.5      i=0
    12         1            1      1.0      0.5      m=3
    13         5            7      1.4      3.7      while m <= mroot:
    14         4            4      1.0      2.1          if s[i]:
    15         3            4      1.3      2.1              j=(m*m-3)/2
    16         3            4      1.3      2.1              s[j]=0
    17        31           31      1.0     16.3              while j<half:
    18        28           28      1.0     14.7                  s[j]=0
    19        28           29      1.0     15.3                  j+=m
    20         4            4      1.0      2.1          i=i+1
    21         4            4      1.0      2.1          m=2*i+3
    22        50           54      1.1     28.4      return [2]+[x for x
```


#### 3. memory_profiler

Fabian Pedregosa仿照Robert Kern的line_profiler实现了一个很好的内存分析器，首先通过 pip 安装它。

```
pip install -U memory_profiler
```

在这里建议安装psutil是因为该包能提升memory_profiler的性能。

```
pip install psutil
```

在代码里，首先添加

```
from memory_profiler import profile
```

然后在需要测试的函数上添加装饰器`@profile`

```
@profile
def primes(n): 
    ...
    ...
```

运行如下命令来显示你的函数使用了多少内存：

```
python -m memory_profiler example.py
```

一旦你的程序退出，你应该就可以看到输出结果。



Reference：

[《Python高性能编程》——2.6　使用cProfile模块](https://yq.aliyun.com/articles/96808/)

[使用cProfile分析Python程序性能](http://xianglong.me/article/analysis-python-application-performance-using-cProfile/)

[Python 性能分析入门指南](http://itindex.net/detail/50507-python-性能分析)
