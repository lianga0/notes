# Windows的PPL安全机制

在Windows安全模型中，任何进程运行时所用的令牌只要包含调试权限（例如使用管理员账户运行）即可向计算机上运行的任何其他进程请求所有访问权限。例如’可以读写任意进程内存、注入代码、挂起并恢复线程，以及查询其他进程的信息。诸如Process Explorer和任务管理器等工具需要并会请求这些访问权限，借此向用户提供所需功能。

但是这种逻辑行为（保证了管理员始终可以完整控制系统中运行的代码）与媒体行业对使用计算机操作系统播放先进的高质量数字化内容（例如蓝光光盘）所提出的、保护数字化版权管理机制所需的系统行为相冲突了。为了以可靠、受保护的形式播放此类内容,Windows Vista和Windows Server2008引入了受保护进程这—概念。此类进程能够与普通Windows进程并存，但会对系统中其他进程（哪怕是使用管理员特权运行的进程）向此类进程请求访问权限的过程添加很多限制。

任何应用程序均可创建受保护进程，然而只有映像文件使用一种特殊的Windows Media证书添加了数字签名后，操作系统才会对进程提供保护。

在内核层面上，对受保护进程的支恃分为两方面。首先，为避免注入攻击，大部分进程创建过程是在内核模式下进行的。其次，受保护进程【及其扩展后的“表亲”——受保护进程轻型（Protected Processes Light (PPL)】会在自己的EPROCESS结构中设置一个特殊位，借此修改进程管理器中与安全有关的例程的行为，进而拒绝通常会授予管理员的某些访问权限。实际上，受保护进程仅能获得PROCESS_QUERY/SET_LIMITED_INFORMAIION、PROCESS_TERMINATE和PROCESS_SUSPEND_RESUME访问权限。受保护进程中运行的线程也会被禁止获得某些访问权限。

## 受保护进程轻型（PPL）

受保护进程最初的模型主要围绕数字版权管理（Digital Rights Management, DRM）内容展开。从Windows 8.l和Windows Server 20l2 R2开始，引入了受保护进程模型扩展——受保护进程轻型（Protected Process Light，PPL）。

PPL可以受到与传统受保护进程相同的保护，即用户模式代码（哪怕提权后运行）无法通过注入线程的方式渗透进此类进程，也无法获取有关己加载DLL的详细信息。而PPL模型对可实现的保护增加了一个新的维度——属性值。不同签名方（signer）的信任程度各不相同,因此一个PPL可以实现比其他PPL更严格或更宽松的保护。

随着DRM从单纯的多媒体内容DRM逐渐演化为Windows许可DRM及Windows应用商店DRM，标准的受保护进程机制也要根据签名方值的差异区别对待。最终，各种获得认可的签名方还可定义对于受保护程度较低的进程需要拒绝哪些访问权限。一般来说，唯一允许的访问掩码（access mask）包括PROCESS_QUERY/SET_LIMITED_INFORMATION和PROCESS_SUSPEND_RESUME，某些PPL签名方可以不允许PROCESS_TERMINATE。

## win11样例：使用EnumProcessModulesEx枚举lsass.exe进程

上述进程在现代 Windows 上通常都是受保护进程（Protected Process Light, PPL）。对这类进程，EnumProcessModulesEx 读取其远程内存会被系统阻止，返回 ERROR_NOACCESS 是按设计的安全限制（Windows11测试情况：lsass.exe打开进程即会失败，没有机会执行后续EnumProcessModulesEx枚举模块。LsaIso.exe进程枚举倒是会返回ERROR_NOACCESS错误码，但是它并没有启用PPL）。

针对 `lsass.exe`进程EnumProcessModulesEx 返回 ERROR_NOACCESS 是系统安全策略的结果。正确做法是检测到 PPL 后直接跳过；不存在“通用的正确枚举方法”。在未启用 LSA 保护的环境里，满足权限和位数要求时才可能枚举成功。

- 普通用户态程序（即使管理员并启用 `SeDebugPrivilege`）无法枚举 PPL 进程的模块。在启用了 LSA 保护或 Credential Guard 的系统上，这几乎总是如此。

- 只有在你的代码本身以受保护进程身份运行，且保护级别不低于目标（例如微软/ELAM 签名的 PPL 或内核态受信组件）时，才可能枚举。这对普通开发者不现实，也不推荐尝试绕过。

- 如果系统未启用 LSA 保护（旧系统或明确关闭该保护），并且你的工具是 64 位、具备 `PROCESS_QUERY_INFORMATION | PROCESS_VM_READ`、启用了 `SeDebugPrivilege`，才有可能成功。

正确的“处理方式”不是强行枚举，而是：

- 运行前检测目标是否为 PPL，若是则跳过并提示“受保护进程无法枚举模块”。

- 在非受保护场景下，确保权限、位数匹配、缓冲区足够，再调用 `EnumProcessModulesEx`。

- 位数匹配：用 64 位工具枚举 64 位进程；32 位进程无法看到 64 位模块。

- 权限：需要管理员（UAC 提升）并启用 `SeDebugPrivilege`，且 OpenProcess 至少包含 `PROCESS_QUERY_INFORMATION | PROCESS_VM_READ`。即便如此，PPL 仍会阻止。

- 工具型产品应在枚举前过滤系统关键进程（如 lsass.exe），避免触发安全软件拦截。

- 如果你确实需要这些进程的模块信息，唯一正途是让该信息由进程自身或受信的系统组件提供；不建议从外部用户态进程去读。

参考：深入解析windows操作系统 第3章进程和作业 3.3受保护进程


Windows Credential Guard是一项基于虚拟化的安全功能，旨在防止凭据窃取攻击。它通过隔离和保护敏感凭据（如NTLM密码哈希、Kerberos票证授予票证以及应用程序存储的域凭据），使得只有特权系统软件才能访问它们。

启用Credential Guard后，系统行为会发生显著变化。原本由本地安全机构（LSA）进程lsass.exe管理的凭据，现在会转移到一个名为隔离LSA进程（LSAIso.exe）的受保护环境中运行。LSA进程会通过远程过程调用来与这个隔离的LSA进程进行通信。该机制利用基于虚拟化的安全性（VBS）和虚拟安全模式（VSM），在内存中保护这些机密，并由虚拟机监控程序在运行时进行隔离。在支持TPM 2.0的硬件上，这些受保护的数据还会受到受TPM保护的VSM主密钥的进一步保护。
