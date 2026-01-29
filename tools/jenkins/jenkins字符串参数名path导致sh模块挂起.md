# jenkins字符串参数名path导致sh模块挂起

## 问题描述

Jenkins Version 2.412中设置一个pipleline任务，添加一个构建参数，名称为path。测试脚本如下

```
pipeline {
	agent any
    options {
        timestamps()
        disableConcurrentBuilds()
    }
    parameters {
        string(name: 'path', defaultValue: '/home/local_md_create/1_Local_Change', description: '手动修改HASH库文件保存路径')
    }
    stages {
        stage('执行本地变更脚本') {
			agent {
                label 'ptn'
            }
            options {
                timeout(time: 20, unit: 'SECONDS')
            }
            steps {
                script {
                    echo "开始执行：python3 -u /home/local_md_create/1_Get_Local_Change.py --path=${params.path}"
                    // 分步输出，确保控制台有日志且可见退出码
                    sh '''
                            set +e
                            pwd
                            set -e
                    '''
                }
            }
        }
    }
}
```

pipleline任务首次执行，即构建号为1的任务，很快就可以执行成功。

后续构建号为2的任务，执行到sh模块时，挂起，没有任何输出。任务无法继续，直到超时结束。

猜测原因为，path参数覆盖了sh模块的path变量，导致sh模块无法正常执行。

修改path参数名为path1，则可以正常执行。

看来jenkins的参数名称也不能随便乱起，Jenkins内部处理机制不够完善啊。
