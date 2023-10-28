# ansible自动化运维工具

ansible是新出现的自动化运维工具，基于Python开发，集合了众多运维工具（puppet、cfengine、chef、func、fabric）的优点，实现了批量系统配置、批量程序部署、批量运行命令等功能。

Ansible架构相对比较简单，是一种agentless(基于ssh)，仅需通过SSH连接客户机执行任务即可。它有以下两个特性：

- 模块化：通过调用相关模块，完成指定任务，且支持任何语言编写的自定义模块

- playbook：剧本，可根据需要一次执行完剧本中的所有任务或某些任务

ansible是基于模块工作的，本身没有批量部署的能力。真正具有批量部署的是ansible所运行的模块，ansible只是提供一种框架。主要包括：

(1)、连接插件connection plugins：负责和被监控端实现通信；

(2)、host inventory：指定操作的主机，是一个配置文件里面定义监控的主机；

(3)、各种模块核心模块、command模块、自定义模块；

(4)、借助于插件完成记录日志邮件等功能；

(5)、playbook：剧本执行多个任务时，非必需可以让节点一次性运行多个任务。


## ansible的基本模块


示例中使用的默认inventory配置文件信息如下：

```
[hostgroup1]
192.168.31.31 ansible_user=root ansible_ssh_pass=1234

[hostgroup2]
192.168.31.32 ansible_user=root
192.168.31.33
```


### 【command】模块

在远程主机上执行命令。

不加 `-m` 选项的时候，默认执行command。

常用相关参数：

- chdir：在此目录下执行命令

- creates：指定文件存在时，不执行

- removes：指定文件不存在时，不执行

示例：

```
ansible hostgroup1 -m command -a "ls"
ansible hostgroup1 -m command -a "chdir=/ ls"
```

上述命令等效于：

```
ansible hostgroup1 -a "ls"
ansible hostgroup1 -a "chdir=/ ls"
```


## Ansible Host Inventory

Ansible 可同时操作属于一个组的多台主机,组和主机之间的关系通过 inventory 文件配置. 默认的文件路径为 `/etc/ansible/hosts`。

除默认文件外，还可以同时使用多个 inventory 文件，也可以从动态源,或云上拉取 inventory 配置信息。

```
ansible hostgroup1 -a "ls" -i inventory.yaml
ansible hostgroup1 -a "chdir=/ ls" -i inventory.yaml
```

如命令`ansible hostgroup* -a "ls"`输出结果如下：

```
192.168.31.33 | UNREACHABLE! => {
    "changed": false,
    "msg": "Failed to connect to the host via ssh: liang@192.168.31.33: Permission denied (publickey,gssapi-keyex,gssapi-with-mic,password).",
    "unreachable": true
}
192.168.31.32 | CHANGED | rc=0 >>
anaconda-ks.cfg
192.168.31.31 | CHANGED | rc=0 >>
anaconda-ks.cfg
```

其中，192.168.31.33未指定ssh登录用户名，使用ansible默认用户名，即当前系统liang用户登录，登录失败。当然你不满意使用默认用户名登录，那么可以使用`-u`额外指定用户名，即`ansible -u root hostgroup2 -a "ls"`。
192.168.31.32指定用户名，使用默认私钥文件登录成功，并执行ls命令。
192.168.31.31指定用户名和密码，使用密码登录成功，并执行ls命令。
