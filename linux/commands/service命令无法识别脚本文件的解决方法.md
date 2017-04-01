## linux service or bash can't run '/etc/init.d/xxx': No such file or directory解决方法

自己写service启动脚本时，遇到了can't run '/etc/init.d/xxx': No such file or directory的问题，可是这个文件确实是存在的。

问题产生的原因：

在windows下编辑xxx文件，然后复制到linux中，文本文件中换行等符号为windows平台默认格式，而service命令仅能识别unix格式，所以出现上述问题。


解决办法：

将文件格式转为unix格式。使用`dos2unix`命令即可很方便的完成转换。

Reference:
[can't run '/etc/init.d/rcS': No such file or directory解决方法](http://blog.csdn.net/yuanzhi7/article/details/64923842)