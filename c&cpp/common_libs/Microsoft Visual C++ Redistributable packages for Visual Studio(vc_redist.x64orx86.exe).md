# Microsoft Visual C++ Redistributable packages 版本不兼容导致的Crash问题

使用VS2022发布release版本可执行文件时，未匹配旧版本Win10导致如下获取锁代码运行直接Crash

```
std::ofstream log_file_stream{};
std::mutex log_file_mutex;

static int write_to_log_file(const char* msg) {
	std::lock_guard<std::mutex> lock(log_file_mutex);
	if (!log_file_stream.is_open()) {
............
```

上述代码运行报错：

```
0x75795383 (msvcp140.dll) (Beacon.exe.2168.dmp 中)处有未经处理的异常: 0xC0000005: 读取位置 0x00000000 时发生访问冲突。
```
VS2022分析dump文件，异常发生在如下Windows提供锁代码中

```
    void lock() {
        if (_Mtx_lock(_Mymtx()) != _Thrd_result::_Success) {
            // undefined behavior, only occurs for plain mutexes (N4950 [thread.mutex.requirements.mutex.general]/6)
            _STD _Throw_Cpp_error(_RESOURCE_DEADLOCK_WOULD_OCCUR);
        }

        if (!_Verify_ownership_levels()) {
            // only occurs for recursive mutexes (N4950 [thread.mutex.recursive]/3)
            // POSIX specifies EAGAIN in the corresponding situation:
            // https://pubs.opengroup.org/onlinepubs/9699919799/functions/pthread_mutex_lock.html
            _STD _Throw_Cpp_error(_RESOURCE_UNAVAILABLE_TRY_AGAIN);
        }
    }
```

函数代码中第一行报上述提到的错误，但std::mutex为全局变量，它的值肯定不为空。
错误原因为VC版本运行库不兼容问题造成的。下载最新的[Microsoft Visual C++ Redistributable packages for Visual Studio 2015, 2017, 2019, and 2022.](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170)如下安装文件，安装在Windows 10中即可解决上述问题。

```
VC_redist.x64.exe
VC_redist.x86.exe
```

微软官网如下文档描述，Microsoft Visual C++ Redistributable packages for Visual Studio的版本必须不能低于VS的编译版本，且目标机器必须在安装应用前完成安装操作。

```
The Visual C++ Redistributable installs Microsoft C and C++ (MSVC) runtime libraries. Many applications built using Microsoft C and C++ tools require these libraries. If your app uses those libraries, a Microsoft Visual C++ Redistributable package must be installed on the target system before you install your app. The Redistributable package architecture must match your app's target architecture. The Redistributable version must be at least as recent as the MSVC build toolset used to build your app. We recommend you use the latest Redistributable available for your version of Visual Studio, with some exceptions noted later in this article.
```