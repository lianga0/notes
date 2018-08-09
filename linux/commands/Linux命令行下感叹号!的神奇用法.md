## Linux命令行下感叹号!的神奇用法

### 1. 从历史记录中使用命令号来运行命令

通过命令 history 的输出中的命令序号来执行一条命令。

```
!100
```

### 2.执行指定的之前执行过的命令

你可以运行 `!-1`， `!-2` 或者 `!-7` 等命令来执行你记录序列中的倒数第一条命令、倒数第二条命令已经倒数第七条等等。。。

不过执行之前，你最后使用history命令，看看之前执行过的命令是不是特别危险的指令。

### 3.向一条新命令传递旧命令的参数避免重复输入

比如说我需要列出 ‘/home/$USER/Binary/firefox’ 这个目录。

```
$ ls /home/$USER/Binary/firefox
```

但是这个时候我又想用 `ls-l` 查看这个目录下的具体信息，那么我需要重新输入上面的命令吗？当然不需要，你只要用下面这个命令：

```
$ ls -l !$
```

### 4.如何用 ! 处理两个以上的参数?

例如我在桌面上创建了一个 1.txt 文件

```
$ touch /home/avi/Desktop/1.txt
```

然后使用CP命令把它复制到 home/avi/Downloads 目录

```
$ cp /home/avi/Desktop/1.txt /home/avi/downloads
```

这样我们就向CP命令传递了两个参数。第一个是 /home/avi/Desktop/1.txt ，第二个是/home/avi/Downloads，为了区分它们，我们 使用 echo 来打印每个参数。

```
$ echo "1st Argument is : !^"
$ echo "2nd Argument is : !cp:2"
```

可以注意到第一个参数可以使用 `!^` 来表示，剩下的参数就可以使用 `命令名：参数序号` 这种方式来表示，比如 `!cp:2`。

再举个例子，如果你执行的某个命令为 “xyz”，命令，后面有5个参数而你想调用第四个参数，就可以使用 `!xyz:4` 来调用它。**当然，你可以使用 `!* ` 来表示所有参数**。

### 5.通过关键词来执行之前的命令

我们可以通过执行关键词来执行之前的命令。可以按照下面的命令来理解：

```
$ ls -al xxx
$ cat xxx
```

上面两个命令分别有自己的参数，那么我们可以通过下面命令来实现重复执行之前的命令

```
$ !ls
ls -al xxx
ls: cannot access 'xxx': No such file or directory
$ !cat
cat xxx
cat: xxx: No such file or directory
```

### 6.非常实用的 !! 操作符

You can run/alter your last run command using `!!`. It will call the last run command with alter/tweak in the current command. Lets show you the scenario

昨天我运行了一个获取IP的Shell命令：

```
$ ip addr show | grep inet | grep -v 'inet6'| grep -v '127.0.0.1' | awk '{print $2}' | cut -f1 -d/
```

突然我意识到需要将结果重定向到 `ip.txt` 中，这时你应该想到用 `UP` 键恢复上一个命令再加上 `>ip.txt` 命令来重定向进去：

```
$ ip addr show | grep inet | grep -v 'inet6'| grep -v '127.0.0.1' | awk '{print $2}' | cut -f1 -d/ > ip.txt
```

感谢这次救命的 `UP` 键。那么再考虑下这个场景，如果我需要运行下面的这个脚本：

```
ifconfig | grep "inet addr:" | awk '{print $2}' | grep -v '127.0.0.1' | cut -f2 -d:
```

当我运行它的时候突然报出了"bash:ifconfig:command not found"错误，我意识到可能是我设定了这个命令需要root权限来运行它。那么现在怎么办？需要重新登录root账号来执行它么？这种情况下使用 `UP` 键也并不管用。所以这里我们使用 `!!` 命令来选择调用这条命令。

```
$ su -c !! root
```

显而易见的是 su 是用来选择执行用户的， -c 是用来表示执行具体命令的，最重要的部分 `!!` 代替了你最后一次运行的命令。然后输入你的root密码即可运行它了。

### 7.使用 !(文件名) 的方式来避免命令对某个文件的影响

这里的 `!` 符号相当于逻辑否定来使用，用来避免对加了 `!` 前缀的文件产生影响。

A.从目录中删除除 2.txt 外的所有文件:

```
$ rm !(2.txt)
```

B.从目录中删除 pdf 为后缀以外的文件（请忽略下图中多出来的一个$）:

```
$ $ rm !(*.pdf)
```

### 8.检查某个目录是否存在，如果存在就将其打印

这里使用 `! -d`  命令来判断目录是否为空，同时使用 `&&` 和 `||` 命令来打印判断目录是否存在：

```
$ [ ! -d /home/avi/Tecmint ] && printf '\nno such /home/avi/Tecmint directory exist\n' || printf '\n/home/avi/Tecmint directory exist\n'
```

From: [Linux命令行下”!”的十个神奇用法](https://www.cnblogs.com/shuaihe/articles/8550108.html)

[10 Amazing and Mysterious Uses of (!) Symbol or Operator in Linux Commands](https://www.tecmint.com/mysterious-uses-of-symbol-or-operator-in-linux-commands/)

[shell中的括号（小括号，中括号，大括号）](https://blog.csdn.net/tttyd/article/details/11742241)