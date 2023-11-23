## Python单元测试unittest

> From: 尘世风 https://www.cnblogs.com/feng0815/p/8045850.html

Python中有一个自带的单元测试框架是unittest模块，用它来做单元测试，它里面封装好了一些校验返回的结果方法和一些用例执行前的初始化操作。

在说unittest之前，先说几个概念：

- TestCase 也就是测试用例

- TestSuite 多个测试用例集合在一起，就是TestSuite

- TestLoader是用来加载TestCase到TestSuite中的

- TestRunner是来执行测试用例的,测试的结果会保存到TestResult实例中，包括运行了多少测试用例，成功了多少，失败了多少等信息

下面写一个简单的单元测试用例

```
import unittest

class MyTest(unittest.TestCase):  # 继承unittest.TestCase
    def tearDown(self):
        # 每个测试用例执行之后做操作
        print('111')

    def setUp(self):
        # 每个测试用例执行之前做操作
        print('22222')

    @classmethod
    def tearDownClass(self):
    # 必须使用 @ classmethod装饰器, 所有test运行完后运行一次
         print('4444444')
    @classmethod
    def setUpClass(self):
    # 必须使用@classmethod 装饰器,所有test运行前运行一次
        print('33333')

    def test_a_run(self):
        self.assertEqual(1, 1)  # 测试用例
        
    def test_b_run(self):
        self.assertEqual(2, 2)  # 测试用例
        
if __name__ == '__main__':
    unittest.main()#运行所有的测试用例
```

下面是一些常用的断言，也就是校验结果

```
assertEqual(a, b)     a == b      
assertNotEqual(a, b)     a != b      
assertTrue(x)     bool(x) is True      
assertFalse(x)     bool(x) is False      
assertIsNone(x)     x is None     
assertIsNotNone(x)     x is not None   
assertIn(a, b)     a in b    
assertNotIn(a, b)     a not in b
```

那如何生成一个测试报告呢，需要加入另外一个模块了，HtmlTestRunner，这个模块需要自己使用命令`pip install html-testRunner`安装，使用执行测试用例就会生成一个html的测试报告，里面会有每个测试用例的执行结果，代码如下：

```
        import HtmlTestRunner        
        import unittest
        class MyTest(unittest.TestCase):#继承unittest.TestCase
            def tearDown(self):
                #每个测试用例执行之后做操作
                print('111')
            def setUp(self):
                #每个测试用例执行之前做操作
                print(22222)
            def test_run(self):
                # self.assertEqual(1,1)
                self.assertIs(1,1)
                #测试用例
            def test_run2(self):
                # self.assertEqual(1,1)
                self.assertIs(1,1)
                #测试用例
            def test_run3(self):
                # self.assertEqual(1,1)
                self.assertIs(1,1)
                #测试用例
            def test_run1(self):
                # self.assertEqual(1,1)
                self.assertIs(1,1)
                #测试用例
        if __name__ == '__main__':
            test_suite = unittest.TestSuite()#创建一个测试集合
            test_suite.addTest(MyTest('test_run1'))#测试套件中添加测试用例
            #test_suite.addTest(unittest.makeSuite(MyTest))#使用makeSuite方法添加所有的测试方法
            fp = open('res.html','wb')#打开一个保存结果的html文件
            runner = HtmlTestRunner.HTMLTestRunner("", stream=fp)
            #生成执行用例的对象
            runner.run(test_suite)
            #执行测试套件
```

如果我们有很多个模块，每个模块下面都写了很多python文件，每个python文件里面都有测试用例，那怎么把这个目录下的用例都执行了呢，就要先找到这个目录下的所有python文件，然后找到里面的测试用例，逐个执行，代码如下：

```
        import unittest,HtmlTestRunner
        suite = unittest.TestSuite()#创建测试套件
        all_cases = unittest.defaultTestLoader.discover('.','test_*.py')
        #找到某个目录下所有的以test开头的Python文件里面的测试用例
        for case in all_cases:
            suite.addTests(case)#把所有的测试用例添加进来
        fp = open('res.html','wb')
        runner = HtmlTestRunner.HTMLTestRunner("", stream=fp)
        runner.run(suite)
        #运行测试
```

我们在后续进行持续集成的时候，要让代码自动运行，就会用到Jenkins了，但是上面产生的测试报告都是html格式的，Jenkins不认识，就在Jenkins里面显示不出来。那咱们就要产生一些Jenkins认识的测试报告，Jenkins认识xml格式的报告，那咱们就产生xml格式的呗，就需要用一个新的模块，xmlrunner，安装直接`pip install xmlrunner`即可，代码如下：

```
import unittest
import xmlrunner
#导入这个模块
class My(unittest.TestCase):
 
    def test1(self,a,b,c):
        self.assertEqual(a+b,c)
 
if __name__=='__main__':
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(My))
    runner = xmlrunner.XMLTestRunner(output='report')#指定报告放的目录
    runner.run(test_suite)
```

Reference：

[unittest — Unit testing framework](https://docs.python.org/3/library/unittest.html)

[unittest.mock — mock object library](https://docs.python.org/3/library/unittest.mock.html)

[pytest: helps you write better programs](https://github.com/pytest-dev/pytest/)

[4 Techniques for Testing Python Command-Line (CLI) Apps](https://realpython.com/python-cli-testing/)

[Testing](https://github.com/vinta/awesome-python#testing)
