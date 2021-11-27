# Android Studio查看Debug日志

logcat是android中的一个命令行工具，可以用于得到程序的log信息。在Android Studio的Logcat窗格中，不仅能看到`android.util.Log`输出的log信息，而且可以看到`System.out.println()`和`e.printStackTrace()`函数输出的信息。显示信息分别如下：

```
2021-08-08 16:50:18.234 11235-11327/com.trendmicro.wifiprotection.us W/System.err: java.lang.NoSuchFieldException: responseError
2021-08-08 16:50:18.234 11235-11327/com.trendmicro.wifiprotection.us W/System.err:     at java.lang.Class.getField(Class.java:1604)
2021-08-08 16:50:18.234 11235-11327/com.trendmicro.wifiprotection.us W/System.err:     at com.trendmicro.service.ProtocolJsonParser.parseResponse(ProtocolJsonParser.java:675)
2021-08-08 16:50:18.234 11235-11327/com.trendmicro.wifiprotection.us W/System.err:     at com.trendmicro.service.GetPopupByDeviceV2Request.processResponseBody(GetPopupByDeviceV2Request.java:109)
2021-08-08 16:50:18.234 11235-11327/com.trendmicro.wifiprotection.us W/System.err:     at com.trendmicro.service.HTTPPostJob.internalExcute(HTTPPostJob.java:228)
2021-08-08 16:50:18.234 11235-11327/com.trendmicro.wifiprotection.us W/System.err:     at com.trendmicro.service.HTTPPostJob.excute(HTTPPostJob.java:82)
2021-08-08 16:50:18.234 11235-11327/com.trendmicro.wifiprotection.us W/System.err:     at com.trendmicro.service.NetworkBaseJob.run(NetworkBaseJob.java:166)
2021-08-08 16:50:18.234 11235-11327/com.trendmicro.wifiprotection.us W/System.err:     at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1167)
2021-08-08 16:50:18.234 11235-11327/com.trendmicro.wifiprotection.us W/System.err:     at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:641)
2021-08-08 16:50:18.235 11235-11327/com.trendmicro.wifiprotection.us W/System.err:     at java.lang.Thread.run(Thread.java:923)
```

```
2021-08-08 16:50:01.520 11235-11383/com.trendmicro.wifiprotection.us I/System.out: Client: Start connecting
```

在stackoverlow看到一个人问在Android中用`e.printStackTrace()`是不是一个bad idea。

然后后面回答it is a bad idea。适当的操作方法：

```
catch (Exception e) {
    Log.e(TAG,Log.getStackTraceString(e));
}
```

或者

```
android.util.Log.e("mytag", "mymessage", exception);
```

这样就能在LogCat中输出调用堆栈信息，并且也是可以点击函数跳转到错误行。

Reference：[Android Studio查看System.out.print的内容](https://blog.csdn.net/Jessicababy1994/article/details/86544182)

[Is it a bad idea to use printStackTrace() for caugt Exceptions?](https://stackoverflow.com/questions/3855187/is-it-a-bad-idea-to-use-printstacktrace-for-caugt-exceptions)

