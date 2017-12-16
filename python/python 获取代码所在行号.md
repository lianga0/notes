### python 获取代码所在的行数

```
import sys
print "here is :",__file__,sys._getframe().f_lineno
```

上述代码局限性比较大，仅能获取当前代码的信息。如果希望更强大的功能，可以使用inspect模块。

##### inspect模块主要提供了四种用处：

1. 对是否是模块，框架，函数等进行类型检查。

2. 获取源码

3. 获取类或函数的参数的信息

4. 解析堆栈

其中，解析堆栈给我们追踪代码调用关系提供了帮助。例如，下面代码可以自动记录向数组中追加元素的代码信息，可以方便我们调试代码：

```
import os
from inspect import stack

class ListWapper:
    def __init__(self):
        self.__list__ = []

    def append(self, date):
        self.__list__.append(date)
        if not isinstance(date, dict):
            return
        caller_filename = ""
        caller_lineno = ""
        stack_info = stack()
        if len(stack_info) > 1:
            caller_func = stack_info[1]
            # the valid value of caller_func is as following
            # (<frame object at 0x03A81030>, 'tt.py', 6, '<module>', ['a.append("def")\n'], 0)
            if len(caller_func) > 3:
                caller_filename = os.path.basename(caller_func[1])
                caller_lineno = caller_func[2]
            pass
        pass
        date["debug"] = "%s:%s" % (caller_filename, caller_lineno)
    pass

if __name__ == "__main__":
    a = ListWapper()
    a.append("abc")
    a.append({"tt":"123"})

    print a.__list__
```