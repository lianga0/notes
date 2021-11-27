# Android Layout XML 命名空间


android中xml中有些控件的属性里面有 "app:***" ，此处的app:是什么意思？和一般的android:有什么区别？


区别是：这两个是声明的不同的命名空间，android的是系统的，app是自定义的。

Android自定义控件的属性，在xml中使用自己自定义的attr的时候，其中有一步就是要自定义一个xml的命名空间后然后再给自定义属性赋值，现在可以统一用

```
xmlns:app="http://schemas.android.com/apk/res-auto"
```

而不是原来的:

```
xmlns:app="http://schemas.android.com/apk/App的Package名"
```

Reference: https://blog.csdn.net/lilin_emcc/article/details/50675467

https://zhidao.baidu.com/question/394670552939034365.html
