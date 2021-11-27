# Android中的Thread, Looper和Handler

> From: https://hit-alibaba.github.io/interview/Android/basic/Android-handler-thread-looper.html#thread%EF%BC%8Clooper%E5%92%8Chandler%E7%9A%84%E5%85%B3%E7%B3%BB

## Thread，Looper和Handler的关系

与Windows系统一样，Android也是消息驱动型的系统。引用一下消息驱动机制的四要素：

- 接收消息的“消息队列”
- 阻塞式地从消息队列中接收消息并进行处理的“线程”
- 可发送的“消息的格式”
- “消息发送函数”

与之对应，Android中的实现对应了

- 接收消息的“消息队列” ——【MessageQueue】
- 阻塞式地从消息队列中接收消息并进行处理的“线程” ——【Thread+Looper】
- 可发送的“消息的格式” ——【Message】
- “消息发送函数”——【Handler的post和sendMessage】

一个Looper类似一个消息泵。它本身是一个死循环，不断地从MessageQueue中提取Message或者Runnable。而Handler可以看做是一个Looper的暴露接口，向外部暴露一些事件，并暴露sendMessage()和post()函数。

在安卓中，除了UI线程/主线程以外，普通的线程(先不提HandlerThread)是不自带Looper的。想要通过UI线程与子线程通信需要在子线程内自己实现一个Looper。开启Looper分三步走：

1. 判定是否已有Looper并Looper.prepare()
2. 做一些准备工作(如暴露handler等)
3. 调用Looper.loop()，线程进入阻塞态

由于每一个线程内最多只可以有一个Looper，所以一定要在Looper.prepare()之前做好判定，否则会抛出`java.lang.RuntimeException: Only one Looper may be created per thread`。为了获取Looper的信息可以使用两个方法：

1. Looper.myLooper()
2. Looper.getMainLooper()

Looper.myLooper()获取当前线程绑定的Looper，如果没有返回null。Looper.getMainLooper()返回主线程的Looper,这样就可以方便的与主线程通信。注意：在Thread的构造函数中调用Looper.myLooper只会得到主线程的Looper，因为此时新线程还未构造好

