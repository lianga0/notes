# fcntl.h 头文件简介

fcntl是 “file control”的缩写，意为“文件控制”。因此 fcntl.h 可以理解为“文件控制相关定义的头文件”。fcntl.h 头文件在 Windows 系统中的情况与 Unix/Linux 系统有显著差异。

在 POSIX/Unix 中 `fcntl.h` 是 Unix/Linux 系统中的标准头文件，主要用于文件描述符控制和文件属性管理。它定义了文件控制函数 `fcntl()` 的原型、相关操作命令以及文件访问模式等宏。

在 Windows 上，<fcntl.h> 的作用依赖你的工具链。

1. MSVC/Visual C++ 提供的是“C 运行时（CRT）版”的 <fcntl.h>（`C:\Program Files (x86)\Windows Kits\10\Include\10.0.26100.0\ucrt\fcntl.h`），主要定义打开/控制文件的标志常量，配合 _open/_sopen/_setmode 等函数使用，但不提供 POSIX 的 fcntl() 函数。

2. MinGW/Cygwin/MSYS 等类 Unix 环境在 Windows 上也有 <fcntl.h>，更接近 POSIX，包含 fcntl()、open() 及 O_* 标志。

> MSVC/Visual C++ 下的 <fcntl.h>提供文件访问模式与状态标志，供 CRT 的低级 I/O 使用（_open、_sopen、_setmode、_pipe 等）。但没有 POSIX 的 `fcntl()；`需要 Win32 原生文件 API 时用 `<Windows.h>` 的 `CreateFile/SetFileInformation`等。

> MinGW/Cygwin 等的 <fcntl.h>通过兼容层在 Windows 上实现 POSIX 语义（可能有差异或限制）。
