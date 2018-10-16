## python decorator装饰器

概括的讲，装饰器的作用就是为已经存在的函数或对象添加额外的功能。 Python中的装饰器仅仅是@语法糖，简化代码的书写形式，提高代码可读性。

装饰器本质上是一个Python函数，它可以让其他函数在不需要做任何代码变动的前提下增加额外功能，装饰器的返回值也是一个函数对象。它经常用于有切面需求的场景，比如：插入日志、性能测试、事务处理、缓存、权限校验等场景。装饰器是解决这类问题的绝佳设计，有了装饰器，我们就可以抽离出大量与函数功能本身无关的雷同代码并继续重用。

### decorator

A function returning another function, usually applied as a function transformation using the `@wrapper syntax`. Common examples for decorators are `classmethod()` and `staticmethod()`.

**The decorator syntax is merely syntactic sugar**, the following two function definitions are semantically equivalent:

```
def f(...):
    ...
f = staticmethod(f)

@staticmethod
def f(...):
    ...
```

The same concept exists for classes, but is less commonly used there.

注意：
> 装饰器仅仅是简单的@语法糖，遵循简单的函数替换原则，如上述示例。如果装饰器带有参数，例如@logging(level='INFO')，那么也遵循简单的foo = logging(level='INFO')(foo)原则

定义一个带参数和不带参数的装饰器，如下：

```
def firstDecorator(para):
    print("invoke first decorator")
    print("first decorator parameter is %s" % para)

    def wrapper(func):
        print("invoke first decorator wrapper")

        def inner_wrapper(*args, **kwargs):
            print("invoke first decorator inner_wrapper")
            return func(*args, **kwargs)
        print("exit first decorator wrapper")
        return inner_wrapper
    print("exit first decorator")
    return wrapper


def secondDecorator(func):
    print("invoke second decorator")

    def wrapper(*args, **kwargs):
        print("invoke second decorator wrapper")
        return func(*args, **kwargs)

    print("exit second decorator")
    return wrapper


```


#### 对于不带参数的装饰器，下面两种方式是等效的

```
@secondDecorator
def foo():
    print("===test===")

foo()
```

等效于

```
def foo():
    print("===test===")
foo = secondDecorator(foo)

foo()
```

测试输出结果均为：

```
invoke second decorator
exit second decorator
invoke second decorator wrapper
===test===
```

#### 对于带参数的装饰器，下面两个方式是等效的

```
@firstDecorator(1)
def foo():
    print("===test===")
foo()
```

等效于

```
@firstDecorator(1)
def foo():
    print("===test===")
foo = firstDecorator(1)(foo)
foo()
```

测试输出结果均为：

```
invoke first decorator
first decorator parameter is 1
exit first decorator
invoke first decorator wrapper
exit first decorator wrapper
invoke first decorator inner_wrapper
===test===
```

### 同时使用多个装饰器时，应当注意调用顺序（影响执行结果）

#### 两个装饰器，同时使用情况1：

```
@firstDecorator(1)
@secondDecorator
def foo():
    print("===test===")

foo()
foo()
```

等效于

```
foo = firstDecorator(1)(secondDecorator(foo))

foo()
foo()

```

测试输出结果均为：

```
invoke first decorator
first decorator parameter is 1
exit first decorator
invoke second decorator
exit second decorator
invoke first decorator wrapper
exit first decorator wrapper
invoke first decorator inner_wrapper
invoke second decorator wrapper
===test===
invoke first decorator inner_wrapper
invoke second decorator wrapper
===test===
```

#### 两个装饰器，同时使用情况2：

```
@secondDecorator
@firstDecorator(1)
def foo():
    print("===test===")

foo()
foo()
```

等效于

```
foo = secondDecorator(firstDecorator(1)(foo))

foo()
foo()
```

测试输出结果均为：

```
invoke first decorator
first decorator parameter is 1
exit first decorator
invoke first decorator wrapper
exit first decorator wrapper
invoke second decorator
exit second decorator
invoke second decorator wrapper
invoke first decorator inner_wrapper
===test===
invoke second decorator wrapper
invoke first decorator inner_wrapper
===test===
```

注意：
> python函数调用类似数组，同样为从左到右。例如 foo(1)(2)，python先执行foo(1)，然后再执行(foo(1))(2)。

### 如何优化你的装饰器

嵌套的装饰函数不太直观，我们可以使用第三方包类改进这样的情况，让装饰器函数可读性更好。

#### decorator.py 

decorator.py 是一个非常简单的装饰器加强包。你可以很直观的先定义包装函数`wrapper()`，再使用`decorate(func, wrapper)`方法就可以完成一个装饰器。

```
from decorator import decorate

def wrapper(func, *args, **kwargs):
    """print log before a function."""
    print "[DEBUG] {}: enter {}()".format(datetime.now(), func.__name__)
    return func(*args, **kwargs)

def logging(func):
    return decorate(func, wrapper)  # 用wrapper装饰func
```

你也可以使用它自带的`@decorator`装饰器来完成你的装饰器。

```
from decorator import decorator

@decorator
def logging(func, *args, **kwargs):
    print "[DEBUG] {}: enter {}()".format(datetime.now(), func.__name__)
    return func(*args, **kwargs)
```

decorator.py实现的装饰器能完整保留原函数的name，doc和args，唯一有问题的就是`inspect.getsource(func)`返回的还是装饰器的源代码，你需要改成`inspect.getsource(func.__wrapped__)`。

#### wrapt

wrapt是一个功能非常完善的包，用于实现各种你想到或者你没想到的装饰器。使用wrapt实现的装饰器你不需要担心之前inspect中遇到的所有问题，因为它都帮你处理了，甚至`inspect.getsource(func)`也准确无误。

```
import wrapt

# without argument in decorator
@wrapt.decorator
def logging(wrapped, instance, args, kwargs):  # instance is must
    print "[DEBUG]: enter {}()".format(wrapped.__name__)
    return wrapped(*args, **kwargs)

@logging
def say(something): pass
```

使用`wrapt`你只需要定义一个装饰器函数，但是函数签名是固定的，必须是`(wrapped, instance, args, kwargs)`，注意第二个参数instance是必须的，就算你不用它。当装饰器装饰在不同位置时它将得到不同的值，比如装饰在类实例方法时你可以拿到这个类实例。根据instance的值你能够更加灵活的调整你的装饰器。另外，args和kwargs也是固定的，注意前面没有星号。在装饰器内部调用原函数时才带星号。

如果你需要使用wrapt写一个带参数的装饰器，可以这样写。

```
def logging(level):
    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        print "[{}]: enter {}()".format(level, wrapped.__name__)
        return wrapped(*args, **kwargs)
    return wrapper

@logging(level="INFO")
def do(work): pass
```

关于wrapt的使用，建议查阅官方文档，在此不在赘述。

http://wrapt.readthedocs.io/en/latest/quick-start.html

[详解Python的装饰器](https://www.cnblogs.com/cicaday/p/python-decorator.html)

[12步轻松搞定python装饰器](http://python.jobbole.com/81683/)
