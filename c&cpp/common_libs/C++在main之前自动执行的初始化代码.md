# C++在main之前自动执行的初始化代码

```
#  define __constructor__(f)                                      \
    static void __CDECL f(void);                            \
    __declspec(allocate(".CRT$XCU"))                              \
    void (__CDECL * __init_##f)(void) = f;                  \
    static void __CDECL f(void)
```

这是一段在 Windows/MSVC 环境下实现“构造函数”（在 main 之前自动执行的初始化代码）的宏。它的用途是让你在 C（或 C++）里定义一个不带参数的函数，并把该函数指针放到 MSVC C 运行库预定义的初始化段 `.CRT$XCU` 中，使得该函数会在程序启动阶段、main 被调用之前（或 DLL 加载时）被 CRT 自动调用。

作用类似于 GCC/Clang 的 `attribute((constructor))`。

宏的每一部分含义：

`static void __CDECL f(void);`：先声明一个使用 `__cdecl` 调用约定的静态函数 f。

`__declspec(allocate(".CRTXCU")) void (__CDECL * __init_##f)(void) = f;`：把一个指向 f 的函数指针变量 __init_f 放到名为 `.CRTXCU` 的段里。MSVC 的 C 运行库在启动时会遍历该段中的函数指针并逐一调用。

`static void __CDECL f(void)`：真正定义函数体，供你书写初始化逻辑。

使用示例：

```
#define __CDECL __cdecl
#  define __constructor__(f)                                      \
    static void __CDECL f(void);                                  \
    __declspec(allocate(".CRT$XCU"))                              \
    void (__CDECL * __init_##f)(void) = f;                        \
    static void __CDECL f(void)
// 定义一个会在程序启动时自动执行的初始化函数
__constructor__(my_init)
{
    // 这里写你的初始化代码，例如注册、日志、环境检测等
    // 注意不要依赖尚未初始化完成的全局状态
}
```

关键点与注意事项：

- 仅适用于 MSVC/Windows（PE/COFF）环境，属于非可移植技巧。跨平台时应改用对应编译器的构造器机制（如 GCC/Clang 的 attribute((constructor))）。

- 函数必须是无参、返回 void，并使用 `__cdecl` 调用约定，符合 CRT 期望的签名。

- 执行时机：

    - 在 EXE 中：在 main 之前、且在 C 运行库完成基础初始化之后调用。

    - 在 DLL 中：在 DLL 进程附加阶段，由 CRT 在调用用户 DllMain 之前（或与 C++ 全局构造一起）进行调用，具体顺序取决于版本与段内排序。

- 初始化函数的调用顺序不严格可控。MSVC 会按段名和对象内符号布局进行遍历，.CRT$XCA … .CRT$XCZ 进行字典序分层，但也要谨慎。

- 链接器剔除问题：

    - 在目标文件直接参与链接时，放入 .CRT$XCU 的符号通常会保留并执行。

    - 如果该代码位于静态库（.lib）中，且没有其它被引用的符号，链接器可能不会把含有该构造器的对象文件拉入最终可执行文件，导致初始化函数不运行。解决办法：

         - 强制链接该符号：`#pragma comment(linker, "/include:__init_my_init")`（注意需要去名修饰匹配，C++ 需 extern "C" 或用修饰名）。

         - 或对库使用 `/WHOLEARCHIVE（MSVC：/WHOLEARCHIVE:yourlib.lib）`。

- 与 C++ 全局对象构造的关系：.CRT$XCU 是 CRT 遍历的“构造器数组”之一，常与 C++ 全局对象的构造一起被调用。若你的代码依赖某些全局对象已构造完毕，需验证顺序是否满足；否则应在 my_init 中只做独立、轻量的初始化。

- 对应的“析构器”（程序结束时自动调用）机制不同，通常使用 atexit 注册或放入终止段（如 .CRT$XT?），该宏未提供销毁钩子。

总结：这个宏是一个在 MSVC 上为 C 代码提供“启动前自动执行钩子”的实现手段，常用于注册模块、初始化日志/插件系统、执行一次性检查等，无需在 main 或 DllMain 手工调用。
