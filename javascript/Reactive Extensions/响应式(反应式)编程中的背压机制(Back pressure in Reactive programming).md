# 响应式（反应式）编程中的背压机制（Back pressure in Reactive programming）

Reactive Programming 对有些人来说可能相对陌生一点。反应式编程是一套完整的编程体系，既有其指导思想，又有相应的框架和库的支持，并且在生产环境中有大量实际的应用。在支持度方面，既有大公司参与实践，也有强大的开源社区的支持。

Reactive Extensions（也称为ReactiveX或Rx ）被移植到多种语言和平台，当然包括 JavaScript、Python、C++、Swift 和 Java。ReactiveX 迅速成为一种跨语言标准，将反应式编程引入行业。RxJava是 Java的ReactiveX端口，主要由 Netflix 的 Ben Christensen 和 David Karnok 创建。RxJava 1.0发布于2014年11月，随后通过RxJava 2.0在2016年十一月是RxJava骨干其他ReactiveX JVM端口，如RxScala， RxKotlin，和RxGroovy。它有成为Android 开发的核心技术，并已进入 Java 后端开发。

## 背压（负压）

响应式编程的重要概念之一是背压或负压（back-pressure），是系统在负载过大时的重要反馈手段。当一个组件的负载过大时，可能导致该组件崩溃。为了避免组件失败，它应该通过负压来通知其上游组件减少负载。负压可能会一直级联往上传递，最终到达用户处，进而影响响应的及时性。

这是在系统整体无法满足过量需求时的自我保护手段，可以保证系统的韧性，不会出现失败的情况。此时系统应该通过增加资源等方式来做出调整。


响应式(反应式)编程的好处是背压Backpressure，可以平衡请求或响应率，这点与异步机制区别所在，也就是说，当响应堵塞时，会同时堵塞请求，因此reactive响应式=异步+同步(背压)。

反应式流（Reactive Streams）是一个反应式编程相关的规范。反应式流为带负压的异步非阻塞流处理提供了标准。

