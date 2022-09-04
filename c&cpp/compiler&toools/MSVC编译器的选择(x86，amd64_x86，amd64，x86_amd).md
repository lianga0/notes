# MSVC编译器的选择(x86，amd64_x86，amd64，x86_amd64)

`x86`：编译器为x86版本，输出文件为x86。

`amd64_x86`：编译器为amd64版本，输出文件为x86。

`amd64`：编译器为amd64版本，输出文件为amd64。

`x86_amd64`：编译器为x86版本，输出文件为amd64。

## Explanation `amd64_x86` and `x86_amd64` cross compilers in MSVC

MSVC contains cross compilers. They run on one architecture and produce code for another. Three architectures are supported, x86 (32-bit Intel/AMD), amd64 (64-bit Intel/AMD, aka x64) and arm. So:

`x86_amd64`: contains a 32-bit compiler and linker that generate x64 code. Could be useful on a build server that boots a 32-bit operating system.

`amd64_x86`: contains a 64-bit compiler and linker that generate x86 code. Can be useful to tackle very large source code files that make a 32-bit compiler run out of memory. Not the kind of code that a human ever writes, but not unlikely to go wrong with auto-generated code.

`x86_arm` and `amd64_arm`: respectively a 32-bit and 64-bit compiler that generate ARM code. Note how targeting an ARM device always requires a cross-compiler. Also the reason there are no arm_x86 and arm_amd64 subdirs, your dev machine doesn't have an ARM processor.

## When compiling x64 code, what's the difference between "x86_amd64" and "amd64"?

When compiling code with VC++, MSDN gives you the option between using the x86_amd64 toolset or the amd64 toolset (when calling vcvarsall.bat).

How do I choose between those two when compile x64 code? Will the amd64 option churn out more efficient x64 machine code than the cross compiler?

> 2010.08.18

It has nothing to do with efficiency. The native and cross-compiler will both generate the same machine code. You will however gain some benefits by running a native 64-bit compiler process on a 64-bit workstation (larger registers, larger memory space, etc...).

The native compiler will only run on an 64-bit copy of Windows, so if your workstation is 32-bit this compiler won't even run.

The cross-compiler is meant to run on x86 machines even though it will run on a 64-bit copy of Windows via WoW; however, there is no reason to do this.

The page you link says it quite well:

> x64 on x86 (x64 cross-compiler)
> Allows you to create output files for x64. This version of cl.exe runs as a 32-bit process, native on an x86 machine and under WOW64 on a 64-bit Widows operating system.

> x64 on x64
> Allows you to create output files for x64. This version of cl.exe runs as a native process on an x64 machine.

> Thanks to Brian R. Bondy for the quote formatting

Reference: https://stackoverflow.com/questions/3508173/when-compiling-x64-code-whats-the-difference-between-x86-amd64-and-amd64
