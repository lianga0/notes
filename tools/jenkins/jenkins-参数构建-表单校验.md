# jenkins-参数构建-表单校验

> https://www.jianshu.com/p/79cdf4e09cff

当jenkins构建需要参数时，往往会需要对输入参数的校验，往往我们会这样做：
在jenkins配置中执行shell脚本进行校验，首先判断是否符合规则，符合则向下执行，否则输出错误日志，报错并退出。

这样实现没有任何问题，但对于使用者还是有一些麻烦的，因为看到构建失败需要打开控制台来查看日志，再返回，很影响效率。为什么不能像web页一样，输入错误有错误提示呢？

这时jenkins插件Validating String Parameter Plugin该闪亮登场了


## Validating String Parameter 插件

该插件会在输入框失去焦点时进行校验提示，在pipeline中使用语法如下：

```
pipeline {
    agent any

    parameters {
        validatingString(name: "test", defaultValue: "", regex: /^abc-[0-9]+$/, failedValidationMessage: "Validation failed!", description: "ABC")
    }

    stages {
        stage("Test") {
            steps {
                echo "${params.test}"
            }
        }
    }
}
```

## 构建触发器中使用触发远程构建会使上述检查失效

因此，即使使用了Validating String Paramete，代码中使用相关值时仍然需要进一步校验。
