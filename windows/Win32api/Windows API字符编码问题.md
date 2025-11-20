## Windows API字符编码

Unicode 是 ASCII 字符编码的一个扩展，只不过在 Windows中用2字节其进行编码，因此也被称为宽字符集(Widechars)。Windows NT内核基于Unicode实现，其采用的UTF-16编码通过代理对（Surrogate Pair）机制能够支持四字节字符（即需要32位表示的字符）。
在C++中，宽字符串（wchar_t或char16_t/char32_t）的字符个数计算需区分码元数量和实际字符数量，尤其是处理UTF-16代理对或UTF-32字符时。使用`wcslen`（适用于`wchar_t`）或`std::wstring::length()`，但仅统计16位码元数量，无法正确处理代理对。

Windows NT 系统是使用Unicode 标准字符集重新开发的，其系统核心完全是用 Unicode 函数工作的。如果希望调用一个Windows 函数并向它传递一个 ANSI字符串，系统会先将 ANSI字符串转换成 Unicode 字符串，再将Unicode 字符串传递给操作系统。
相反，如果希望函数返回 ANSI 字符串，系统会先将 Unicode 字符串转换成 ANSI字符串，然后将结果返回应用程序。也就是说，在NT架构下，Win32 API 能接受Unicode 和 ASCI 两种字符集，而其内核只能使用 Unicode 字符集。尽管这些操作对用户来说都是透明的，但字符串的转换需要占用系统资源。

在 Win32 API函数字符集中,“A”表示 ANSI,“W”表示 Widechars(即 Unicode )。前者就是通常使用的单字节方式;后者是宽字节方式，以便处理双字节字符。每个以字符串为参数的 Win32 函数在操作系统中都有这两种方式的版本。
例如，在编程时使用MessageBox函数，而在 USER32.DLI中却没有 32 位 MessageBox 函数的人口。实际上有两个入口，一个名为“MessageBoxA”(ANSI版),另一个名为“MessageBoxW”(宽字符版 )。
幸运的是，程序员通常不必关心这个问题，只需要在编程时使用 MessageBox 函数，开发工具的编译模块就会根据设置来决定是采用 MessageBoxA 还是MessageBoxW了。
再比如，Windows GetModuleFileNameW 函数的原型如下，其中，lpFilename 宽字符串参数是 UTF-16 编码（小端序，即 Little-Endian UTF-16），这是 Windows 系统内部使用的标准 Unicode 编码格式。
```c++
DWORD GetModuleFileNameW(
  [in, optional] HMODULE hModule,
  [out]          LPWSTR  lpFilename,  //A pointer to a buffer that receives the fully qualified path of the module. If the length of the path is less than the size that the nSize parameter specifies, the function succeeds and the path is returned as a null-terminated string. If the length of the path exceeds the size that the nSize parameter specifies, the function succeeds and the string is truncated to nSize characters including the terminating null character.
  [in]           DWORD   nSize
);
``` 
Windows NT 系统的内部路径存储和返回都统一使用 UTF-16 编码，不受系统区域设置、语言环境或用户设置的影响。也就是说，无论系统语言如何变化，GetModuleFileNameW 始终返回 UTF-16 编码的字符串。


## WOW64

WOW64(Windows-on-Windows 64-bit)是64位 Windows 操作系统的子系统，可以使大多数 32位应用程序在不进行修改的情况下运行在 64 位操作系统上。

64位的 Windows，除了带有 64位操作系统应有的系统文件，还带有 32位操作系统应有的系统文件。Windows的 64位系统文件都放在一个叫作“System32”的文件夹中，\Windows\System32 文件夹中包含原生的 64 位映像文件。为了兼容 32 位操作系统，还增加了 \Windows\SysWOW64 文件夹，其中存储了 32位的系统文件。

64位应用程序会加载 System32 目录下 64位的 kernel32.dl、user32.dl 和 ntdll.dl。当 32 位应用程序加载时，WOW64 建立 32 位 ntdll.dll 所要求的启动环境，将 CPU 模式切换至 32 位，并开始执行 32 位加载器，就如同该进程运行在原生的 32 位系统上一样。WOW64 会对 32 位 ntdll.dll 的调用重定向 ntdll.dll(64 位)，而不是发出原生的 32 位系统调用指令。WOW64 转换到原生的 64 位模式捕获与系统调用有关的参数，发出对应的原生64位系统调用。当原生的系统调用返回时，WOW64在返回 32 位模式之前将所有输出参数从64位转换成 32位。

WOW64 既不支持 16 位应用程序的执行(32位 Windows 支持 16 位应用程序的执行 )，也不支持加载 32 位内核模式的设备驱动程序。WOW64进程只能加载32位的 DLL，不能加载原生的64位DLL。类似的，原生的 64 位进程不能加载 32 位的 DLL。


DLL 程序没有“私有”空间，它们总是被映射到其他应用程序的地址空间中，作为其他应用程序的一部分运行。其原因是:如果 DLL不与其他程序处于同一个地址空间，应用程序就无法调用它。

