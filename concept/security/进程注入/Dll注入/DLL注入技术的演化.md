Windows中DLL注入存在多种技术方式，常见如下所示：

- 从外部促使目标进程调用`kernel32.dll`动态链接库中的`LoadLibrary()`API
- 使用用注册表`.APPInit_DLLs`项目注册`User32.dll`动态链接库加载时会自动加载的用户自定义dll清单
- 使用消息钩取`SetWindowsHookEx()`API

其中，第一种从外部促使目标进程调用`kernel32.dll`动态链接库中的`LoadLibrary()`API，常见的方法为远程线程创建(`CreateRemoteThread()`)，直接执行`LoadLibrary()`加载指定路径的dll。

##  **MemoryModule** 内存加载（不落盘）

由于Windows中的`LoadLibrary()`函数加载的指定DLL文件必须是磁盘文件，2004年Joachim Bauch发布了一个可以不使用`LoadLibrary()`，直接从内存加载DLL的方法，称之为[MemoryModule](https://www.joachim-bauch.de/2012/04/09/memorymodule-0-0-3-released/)。2012年代码更新至0.0.3版本，源代码可以从https://github.com/fancycode/MemoryModule中下载。

> The default windows API functions to load external libraries into a program (`LoadLibrary`, `LoadLibraryEx`) only work with files on the filesystem. It's therefore impossible to load a DLL from memory.

> But sometimes, you need exactly this functionality (e.g. you don't want to distribute a lot of files or want to make disassembling harder). Common workarounds for this problems are to write the DLL into a temporary file first and import it from there. When the program terminates, the temporary file gets deleted.

> **MemoryModule** is a library that can be used to load a DLL completely from memory - without storing on the disk first.

若进程中使用**MemoryModule**，该模块并不在需要加载的DLL内部（被加载DLL与MemoryModule无任何特殊关系）。也就是说，它使用VS studio编译出来的普通DLL文件即可完成注入。使用此工具，可以很容易实现向进程自身注入DLL，但向远程进程注入就比较困难。

## **Reflective DLL injection**反射DLL注入(RDI)

上述**MemoryModule**允许注入器程序方便的向自身进程注入DLL文件，但是向远程进程注入会有些麻烦。

2009年 Stephen Fewer 发布 [Reflective DLL Injection](https://github.com/stephenfewer/ReflectiveDLLInjection) 项目，方便进行远程进程注入。 与常规远程线程创建(`CreateRemoteThread()`)，直接执行`LoadLibrary()`的注入方法不同，它不需要 `LoadLibrary()` 这个函数来加载 dll，而是通过 DLL 内部的一个（自定义的ReflectiveLoader）函数来自己把自己加载起来，这么说可能会有一点抽象，总之这个函数会负责解析DLL文件的头信息、导入函数的地址、处理重定位等初始化操作。我们的注入器进程只需要将这个DLL文件写入目标进程的虚拟空间中，然后通过Reflective DLL的导出表找到这个ReflectiveLoader函数并调用它，我们的任务就完成了。

由于这个ReflectiveLoader函数执行的时候 DLL 还没有被加载，这个函数的编写也会受到诸多限制，比如说无法正常使用全局变量，还有我们的函数必须编写成与地址无关的函数，就像 shellcode 那样，无论加载到了内存中的哪一个位置都要保证成功加载。


[Reflective DLL Injection](https://github.com/stephenfewer/ReflectiveDLLInjection) library is responsible for loading itself by implementing a minimal Portable Executable (PE) file loader. 

The process of remotely injecting a library into a process is two fold. Firstly, the library you wish to inject must be written into the address space of the target process (Herein referred to as the host process). Secondly the library must be loaded into that host process in such a way that the library's run time expectations are met, such as resolving its imports or relocating it to a suitable location in memory.

Assuming we have code execution in the host process and the library we wish to inject has been written into an arbitrary location of memory in the host process, Reflective DLL Injection works as follows.

- Execution is passed, either via `CreateRemoteThread()` or a tiny bootstrap shellcode, to the library's ReflectiveLoader function which is an exported function found in the library's export table.
- As the library's image will currently exists in an arbitrary location in memory the ReflectiveLoader will first calculate its own image's current location in memory so as to be able to parse its own headers for use later on.
- The ReflectiveLoader will then parse the host processes kernel32.dll export table in order to calculate the addresses of three functions required by the loader, namely LoadLibraryA, GetProcAddress and VirtualAlloc.
- The ReflectiveLoader will now allocate a continuous region of memory into which it will proceed to load its own image. The location is not important as the loader will correctly relocate the image later on.
- The library's headers and sections are loaded into their new locations in memory.
- The ReflectiveLoader will then process the newly loaded copy of its image's import table, loading any additional library's and resolving their respective imported function addresses.
- The ReflectiveLoader will then process the newly loaded copy of its image's relocation table.
- The ReflectiveLoader will then call its newly loaded image's entry point function, DllMain with DLL_PROCESS_ATTACH. The library has now been successfully loaded into memory.
- Finally the ReflectiveLoader will return execution to the initial bootstrap shellcode which called it, or if it was called via `CreateRemoteThread`, the thread will terminate.

可以看出使用该技术编译出来的DLL，格式上仍然是正常的PE文件，并且有导入导出表。只不过它有一个特殊的导出函数`ReflectiveLoader`，该函数全部采用类似shellcode的地址无关代码实现，所以注入器可以直接找到该函数的起始地址，然后直接执行即可完成DLL的导入工作。

[Reflective DLL Injection](https://github.com/stephenfewer/ReflectiveDLLInjection) library 的另外一个测试版本 [RflDllOb - Bambini](https://github.com/oldboy21/RflDllOb) 有更详细的介绍文档[反射DLL注入原理解析](https://www.cnblogs.com/fdxsec/p/18300826) 和 [All I Want for Christmas is Reflective DLL Injection](https://oldboy21.github.io/posts/2023/12/all-i-want-for-christmas-is-reflective-dll-injection/)。


> The assumption of **reflective DLL injection** is that calling the entry point of the DLL is sufficient to execute the full functionality of the DLL. However, this is often not the case. **In fact, Microsoft advises developers to minimize the amount of work done in DllMain**, and to do “lazy initialization”, avoiding loading additional libraries or creating new threads. The main entry point then, would be in another function that would be called separately after the DLL was loaded.

In 2015, Dan Staples released an important update to RDI, called [“Improved Reflective DLL Injection“](https://disman.tl/2015/01/30/an-improved-reflective-dll-injection-technique.html). This aimed to allow an additional function to be called after “DLLMain” and support the passing of user arguments into said additional function. Some shellcode trickery and a bootstrap placed before the call to ReflectiveLoader accomplished just that. RDI is now functioning more and more like the legitimate LoadLibrary. We can now load a DLL, call it’s entry point, and then pass user data to another exported function. 

此技术存在的不便之处在于，我必须把`ReflectiveLoader`函数的实现代码和原本实现功能的DLL源码合并编译，无法直接使用已经编译好的DLL包装一下转为RDI。另一种可行方式为 **Reflective DLL injection** + **MemoryModule** + 原始业务DLL。

为克服这个问题sRDI项目，可以直接把一个普通DLL转为位置无关的SHELLCODE（“You can now convert any DLL to position independent shellcode at any time, on the fly.”）


## [sRDI – Shellcode Reflective DLL Injection](https://www.netspi.com/blog/technical-blog/adversary-simulation/srdi-shellcode-reflective-dll-injection/)

sRDI是一个Shellcode Reflective DLL Injection的工具，它可以将DLL文件转换为位置无关的shellcode。它具有完整的PE加载器功能，支持正确的节权限、TLS回调和健全性检查。可以将其视为一个绑定了打包的DLL的Shellcode PE加载器。

相对于标准 RDI，使用 sRDI 的一些优点：

- 你可以转换任何 DLL为无位置依赖的 shellcode，并且可以使用标准的 shellcode 注入技术来使用它。
- 你的 DLL 中不需要写任何反射加载器代码，因为反射加载器是在 DLL 外部的 shellcode 中实现的。
- 合理使用权限，没有大量的 RWX 权限数据。
- 还可以根据选项，抹掉 PE 头特征。

使用案例＃1 - 隐蔽的持久性


◆使用服务器端的Python代码（sRDI）将RAT转换为shellcode

◆然后将shellcode写入注册表

◆设置定时任务来执行一个基本的加载器DLL

◆该加载器DLL将读取shellcode并进行注入（不超过20行的C代码）。



优点：您的RAT或加载器都不需要理解RDI或使用RDI进行编译。加载器可以保持小巧简单，以避免被杀毒软件检测。



使用案例＃2 - 侧加载


◆让您的RAT在内存中运行

◆编写DLL以执行额外的功能

◆将DLL转换为shellcode（使用sRDI）并进行本地注入

◆使用GetProcAddressR来查找导出函数

◆无需重新加载DLL，执行额外功能X次



优点：使您的初始工具更轻巧，并根据需要添加功能。只需加载一次DLL，就可以像使用其他任何DLL一样使用它。



使用案例＃3 - 依赖项


◆从磁盘读取现有的合法API DLL

◆将DLL转换为shellcode（使用sRDI）并加载到内存中

◆使用GetProcAddress来查找所需的函数



优点：避免监控工具检测LoadLibrary调用。在不泄漏信息的情况下访问API函数。（例如WinInet、PSApi、TlHelp32、GdiPlus）

