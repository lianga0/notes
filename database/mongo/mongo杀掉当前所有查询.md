## 杀掉mongodb目前的所有查询进程

> 2018年07月16日 10:46:29
> From: https://blog.csdn.net/newjueqi/article/details/81061297

把下面的脚本保存为/tmp/kill.js

```
var ops = db.currentOp().inprog;
 
for(i = 0; i < ops.length; i++){
        var opid = ops[i].opid;
        db.killOp(opid);
        print("Stopping op #"+opid)
}
```

用法：

```
mongo 10.9.1.1:27107/admin -u root -p '1111'< /tmp/kill.js
```
