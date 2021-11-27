# Android Studio gradle takes too long to build

> 2021.08.08

> https://stackoverflow.com/questions/29391421/android-studio-gradle-takes-too-long-to-build


My Android Studio project used to build faster but now it takes a long time to build. Any ideas what could be causing the delays? I haven't any Anti virus running which could interrupt the builds. My app is not that big in size as well (around 5MB) and it used to build within few seconds but not sure what has changed.

```
10:03:51 Gradle build finished in 4 min 0 sec  
10:04:03 Session 'app': running  
10:10:11 Gradle build finished in 3 min 29 sec  
10:10:12 Session 'app': running  
10:20:24 Gradle build finished in 3 min 42 sec  
10:28:18 Gradle build finished in 3 min 40 sec  
10:28:19 Session 'app': running  
10:31:14 Gradle build finished in 2 min 56 sec   
10:31:14 Session 'app': running  
10:38:37 Gradle build finished in 3 min 30 sec  
10:42:17 Gradle build finished in 3 min 40 sec  
10:45:18 Gradle build finished in 3 min 1 sec  
10:48:49 Gradle build finished in 3 min 30 sec  
10:53:05 Gradle build finished in 3 min 22 sec  
10:57:10 Gradle build finished in 3 min 19 sec  
10:57:11 Session 'app': running  
```

## Answers

In Android Studio go to File -> Settings -> Build, Execution, Deployment -> Build Tools -> Gradle

(if on mac) Android Studio -> preferences... -> Build, Execution, Deployment -> Build Tools -> Gradle

Check the 'Offline work' under 'Global Gradle settings'

Note: In newer version of Android studio, View->Tool Windows->Gradle->Toggle button of online/offline

It will reduce 90% gradle build time.

Note: If you just added a new dependency in your gradle you will have to uncheck the **offline work** or gradle will not be able to resolve the dependencies. After the complete resolving then you you can check the **offline work** for a faster build


## 用于切换 Gradle 离线模式的新位置

如需启用或停用 Gradle 离线模式，请先从菜单栏中依次选择 View > Tool Windows > Gradle。然后，在 Gradle 窗口顶部附近，点击 Toggle Offline Mode 图标。

Reference：https://developer.android.com/studio/releases#3.6-gradle-offline-ui
