
Android [广播概览](https://developer.android.com/guide/components/broadcasts?hl=zh-cn) 文档中描述

> 系统软件包管理器会在应用安装时注册接收器。然后，该接收器会成为应用的一个独立入口点，这意味着如果应用当前未运行，系统可以启动应用并发送广播。

> 系统会创建新的 `BroadcastReceiver` 组件对象来处理它接收到的每个广播。此对象仅在调用 `onReceive(Context, Intent)` 期间有效。一旦从此方法返回代码，系统便会认为该组件不再活跃。

这里有个疑问，如果应用当前未运行，系统可以启动应用并发送广播。那么系统启动应用时，到底应用的那些代码会被运行呢？

1. 应用的Application类会完成初始化
2. 应用的Launcher Activity并不会初始化

下面是测试的过程：

##### 1. 创建测试接收静态广播应用`broadcaststudy`

```
package com.study.android.broadcaststudy;

import android.app.Application;
import android.content.Context;

import com.elvishew.xlog.LogConfiguration;
import com.elvishew.xlog.LogLevel;
import com.elvishew.xlog.XLog;
import com.elvishew.xlog.flattener.ClassicFlattener;
import com.elvishew.xlog.printer.AndroidPrinter;
import com.elvishew.xlog.printer.Printer;
import com.elvishew.xlog.printer.file.FilePrinter;
import com.elvishew.xlog.printer.file.backup.NeverBackupStrategy;
import com.elvishew.xlog.printer.file.clean.FileLastModifiedCleanStrategy;
import com.elvishew.xlog.printer.file.naming.DateFileNameGenerator;


public class MyApplication extends Application {
    @Override
    public void onCreate() {
        super.onCreate();
        
        LogConfiguration config = new LogConfiguration.Builder()
                .logLevel(BuildConfig.DEBUG ? LogLevel.ALL             // Specify log level, logs below this level won't be printed, default: LogLevel.ALL
                        : LogLevel.ALL)
                .tag("MY_TAG")                                         // Specify TAG, default: "X-LOG"
                .enableThreadInfo()                                    // Enable thread info, disabled by default
                .enableStackTrace(3)                                   // Enable stack trace info with depth 2, disabled by default
                .build();

        Printer androidPrinter = new AndroidPrinter(true);         // Printer that print the log using android.util.Log
        Printer filePrinter = new FilePrinter                      // Printer that print(save) the log to file
                .Builder(getApplicationContext().getDir("path-to-logs-dir", Context.MODE_PRIVATE).getAbsolutePath())                         // Specify the directory path of log file(s)
                .fileNameGenerator(new DateFileNameGenerator())        // Default: ChangelessFileNameGenerator("log")
                .backupStrategy(new NeverBackupStrategy())             // Default: FileSizeBackupStrategy(1024 * 1024)
                .cleanStrategy(new FileLastModifiedCleanStrategy(7 * 24 * 3600000))     // Default: NeverCleanStrategy()
                .flattener(new ClassicFlattener())  // By default, FilePrinter use a DefaultFlattener, which just simply concat the timestamp and message together.
                .build();

        XLog.init(                     // Initialize XLog
                config,                // Specify the log configuration, if not specified, will use new LogConfiguration.Builder().build()
                androidPrinter,        // Specify printers, if no printer is specified, AndroidPrinter(for Android)/ConsolePrinter(for java) will be used.
                filePrinter);
        XLog.d("Application Start!!!!");
    }

    @Override
    public void onTerminate() {
        XLog.d("Application end!!!!");
        super.onTerminate();
    }
}
```

##### 2. 创建broadcast接收类`MyReceiver`

```
package com.study.android.broadcaststudy;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.widget.Toast;

import com.elvishew.xlog.XLog;

public class MyReceiver extends BroadcastReceiver {

    @Override
    public void onReceive(Context context, Intent intent) {
        XLog.d("on receive !!!!" + intent.getAction());
        Toast.makeText(context, "检测到意图。", Toast.LENGTH_LONG).show();
    }
}
```

##### 3. 在LAUNCHER Activity中添加日志打印语句

```
package com.study.android.broadcaststudy;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;

import com.elvishew.xlog.XLog;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        XLog.d("MainActivity is created !!!!");
    }
}
```

##### 4. 测试接收静态广播应用`AndroidManifest.xml`文件如下

```
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.study.android.broadcaststudy">

    <application
        android:name=".MyApplication"
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.BroadcastStudy">
        <receiver
            android:name=".MyReceiver"
            android:enabled="true"
            android:exported="true">
            <intent-filter>
                <action android:name="com.study.broadcaststudy.test" />
            </intent-filter>
        </receiver>
        <activity android:name=".MainActivity">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />

                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
```

##### 5. 随意在另一应用中，运行如下测试代码

```
    Intent intent = new Intent();
    intent.setAction("com.study.broadcaststudy.test");
    intent.setComponent(new ComponentName("com.study.broadcaststudy","com.study.broadcaststudy.MyReceiver"));//显示指定组件名称
    sendBroadcast(intent);
```

##### 6. 在接收静态广播应用未启动的情况下，运行另一个App中发送广播的代码，可以看到如下日志

```
2021-10-12 16:49:40.671 D/MY_TAG: Thread: main
	├ com.trendmicro.tmws.android.broadcaststudy.MyApplication.onCreate(MyApplication.java:54)
	├ android.app.Instrumentation.callApplicationOnCreate(Instrumentation.java:1192)
	└ android.app.ActivityThread.handleBindApplication(ActivityThread.java:6712)
Application Start!!!!
2021-10-12 16:49:40.696 D/MY_TAG: Thread: main
	├ com.trendmicro.tmws.android.broadcaststudy.MyReceiver.onReceive(MyReceiver.java:16)
	├ android.app.ActivityThread.handleReceiver(ActivityThread.java:4032)
	└ android.app.ActivityThread.access$1400(ActivityThread.java:237)
on receive !!!!com.trendmicro.tmws.android.broadcaststudy.test
```

说明静态广播的确是启动了测试应用的进程，并执行了对应的`onReceive`代码。

