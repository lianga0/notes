Android Activity的onDestroy方法不一定任何时候都会执行！！！

> 假装我在飞 2017-07-07 11:02:25

其实activity的生命周期，只有在正常的情况下，才会按顺序执行，如果发生其他状况，则另当别论。

 

正常点击返回键： onDestroy方法一定会执行；

 

从后台强杀分两种情况：

第一种：当前仅有一个activity，这时候，强杀，是会执行onDestroy方法的；

第二种：栈里面的第一个没有销毁的activity会执行ondestroy方法，其他的不会执行。

比如说：从mainactivity跳转到activity-A（或者继续从activity-A再跳转到activity-B），这时候，从后台强杀，只会执行mainactivity的onDestroy方法，activity-A（以及activity-B）的onDestroy方法都不会执行；


From：https://blog.csdn.net/yuzhidao/article/details/74638683

