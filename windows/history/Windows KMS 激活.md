## Windows KMS 激活

### 一句命令激活windows/office

一般来说，只要确保的下载的是VL批量版本并且没有手动安装过任何key，

你只需要使用管理员权限运行cmd执行一句命令就足够：

```
slmgr /skms kms.03k.org
```

这句命令的意思是，把kms服务器地址设置为（set kms）为kms.03k.org。：

然后去计算机属性或者控制面板其他的什么的地方点一下激活就好了。

当然，如果你懒得点，可以多打一句命令手动激活：

```
slmgr /ato
```

这句命令的意思是，马上对当前设置的key和服务器地址等进行尝试激活操作。

kms激活的前提是你的系统是批量授权版本，即VL版，一般企业版都是VL版，专业版有零售和VL版，家庭版旗舰版OEM版等等那就肯定不能默认直接用kms激活。

### KMS Server资源

##### myanaloglife/py-kms

https://github.com/myanaloglife/py-kms

##### SystemRage/py-kms

https://github.com/SystemRage/py-kms

##### lixuy/vlmcsd

https://github.com/lixuy/vlmcsd

### Reference

[2018年11月最新可用KMS激活服务器地址](https://blog.csdn.net/weixin_42588262/article/details/81120403)

[本站上线KMS服务~一句命令激活windows/office](https://03k.org/kms.html)