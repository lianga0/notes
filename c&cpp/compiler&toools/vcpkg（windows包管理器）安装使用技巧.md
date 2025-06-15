# 一、vcpkg 简介

vcpkg 是一个用于管理 C++库的开源工具，由微软推出。它可以帮助开发者轻松地获取、构建和安装大量的 C++开源库，解决了在不同平台上编译和管理第三方库的复杂性问题，尤其在 Windows 平台下优势明显。

# 二、vcpkg 的安装

## 下载 vcpkg

从 vcpkg 的 GitHub 仓库（https://github.com/microsoft/vcpkg）下载最新版本的 vcpkg。你可以使用 Git 克隆仓库，命令如下：

```
git clone https://github.com/microsoft/vcpkg
```


## 编译 vcpkg

在 Windows 系统中，建议使用 PowerShell 进行编译。打开 PowerShell，导航到 vcpkg 目录，例如：


```powershell
cd D:\vcpkg
```


### 运行编译脚本：


```powershell
.\bootstrap-vcpkg.bat -disableMetrics
```

编译完成后，会在当前目录下生成`vcpkg.exe`文件。


### 配置环境变量（可选）

为了能够更方便地使用 vcpkg 命令，可以将 vcpkg 的安装目录添加到系统环境变量 Path 中。具体操作如下：


- 右键点击“此电脑”选择“属性”。

- 点击“高级系统设置”。

- 在“系统属性”窗口中，点击“环境变量”按钮。

- 在“系统变量”中，找到 Path 变量，点击“编辑”。

- 在变量值中添加 vcpkg 的安装路径，例如`D:\vcpkg\vcpkg\scripts`。

- 点击“确定”保存设置。


## vcpkg 的使用技巧

### 查看支持的库列表

运行以下命令，查看 vcpkg 支持的所有库：

```powershell
.\vcpkg search
```

### 安装库

以安装 `gtest` 为例，运行以下命令：

```
vcpkg install gtest
Computing installation plan...
A suitable version of cmake was not found (required v3.30.1).
Downloading https://github.com/Kitware/CMake/releases/download/v3.30.1/cmake-3.30.1-windows-i386.zip -> cmake-3.30.1-windows-i386.zip
Successfully downloaded cmake-3.30.1-windows-i386.zip
Extracting cmake...
A suitable version of 7zip was not found (required v24.9.0).
Downloading https://github.com/ip7z/7zip/releases/download/24.09/7z2409.exe -> 7z2409.7z.exe
Successfully downloaded 7z2409.7z.exe
Extracting 7zip...
A suitable version of 7zr was not found (required v24.9.0).
Downloading https://github.com/ip7z/7zip/releases/download/24.09/7zr.exe -> 44d8504a-7zr.exe
Successfully downloaded 44d8504a-7zr.exe
The following packages will be built and installed:
    gtest:x64-windows@1.16.0#1
  * vcpkg-cmake:x64-windows@2024-04-23
  * vcpkg-cmake-config:x64-windows@2024-05-23
Additional packages (*) will be modified to complete this operation.
Detecting compiler hash for triplet x64-windows...
A suitable version of git was not found (required v2.7.4).
Downloading https://github.com/git-for-windows/git/releases/download/v2.47.1.windows.2/PortableGit-2.47.1.2-64-bit.7z.exe -> PortableGit-2.47.1.2-64-bit.7z.exe
Successfully downloaded PortableGit-2.47.1.2-64-bit.7z.exe
Extracting git...
-- Using %HTTP(S)_PROXY% in environment variables.
A suitable version of powershell-core was not found (required v7.2.24).
Downloading https://github.com/PowerShell/PowerShell/releases/download/v7.2.24/PowerShell-7.2.24-win-x64.zip -> PowerShell-7.2.24-win-x64.zip
Successfully downloaded PowerShell-7.2.24-win-x64.zip
Extracting powershell-core...
Compiler found: C:/Program Files/Microsoft Visual Studio/2022/Community/VC/Tools/MSVC/14.41.34120/bin/Hostx64/x64/cl.exe
Restored 0 package(s) from C:\Users\zlo20\AppData\Local\vcpkg\archives in 173 us. Use --debug to see more details.
Installing 1/3 vcpkg-cmake:x64-windows@2024-04-23...
Building vcpkg-cmake:x64-windows@2024-04-23...
-- Installing: C:/app/vcpkg/packages/vcpkg-cmake_x64-windows/share/vcpkg-cmake/vcpkg_cmake_configure.cmake
-- Installing: C:/app/vcpkg/packages/vcpkg-cmake_x64-windows/share/vcpkg-cmake/vcpkg_cmake_build.cmake
-- Installing: C:/app/vcpkg/packages/vcpkg-cmake_x64-windows/share/vcpkg-cmake/vcpkg_cmake_install.cmake
-- Installing: C:/app/vcpkg/packages/vcpkg-cmake_x64-windows/share/vcpkg-cmake/vcpkg-port-config.cmake
-- Installing: C:/app/vcpkg/packages/vcpkg-cmake_x64-windows/share/vcpkg-cmake/copyright
-- Performing post-build validation
Starting submission of vcpkg-cmake:x64-windows@2024-04-23 to 1 binary cache(s) in the background
Elapsed time to handle vcpkg-cmake:x64-windows: 112 ms
vcpkg-cmake:x64-windows package ABI: 42db87fc471accbd768b4aaff4272591b2d31f1847e8778a9b91f168fa63bbdb
Installing 2/3 vcpkg-cmake-config:x64-windows@2024-05-23...
Building vcpkg-cmake-config:x64-windows@2024-05-23...
-- Installing: C:/app/vcpkg/packages/vcpkg-cmake-config_x64-windows/share/vcpkg-cmake-config/vcpkg_cmake_config_fixup.cmake
-- Installing: C:/app/vcpkg/packages/vcpkg-cmake-config_x64-windows/share/vcpkg-cmake-config/vcpkg-port-config.cmake
-- Installing: C:/app/vcpkg/packages/vcpkg-cmake-config_x64-windows/share/vcpkg-cmake-config/copyright
-- Skipping post-build validation due to VCPKG_POLICY_EMPTY_PACKAGE
Starting submission of vcpkg-cmake-config:x64-windows@2024-05-23 to 1 binary cache(s) in the background
Elapsed time to handle vcpkg-cmake-config:x64-windows: 92 ms
vcpkg-cmake-config:x64-windows package ABI: 4bda0a54af1522aa5080aa93f5465f1b28a82b63e896048d3d602d1fd844fa41
Completed submission of vcpkg-cmake:x64-windows@2024-04-23 to 1 binary cache(s) in 55.2 ms
Installing 3/3 gtest:x64-windows@1.16.0#1...
Building gtest:x64-windows@1.16.0#1...
Downloading https://github.com/google/googletest/archive/v1.16.0.tar.gz -> google-googletest-v1.16.0.tar.gz
Successfully downloaded google-googletest-v1.16.0.tar.gz
-- Extracting source C:/app/vcpkg/downloads/google-googletest-v1.16.0.tar.gz
-- Applying patch 001-fix-UWP-death-test.patch
-- Applying patch clang-tidy-no-lint.patch
-- Applying patch fix-main-lib-path.patch
-- Using source at C:/app/vcpkg/buildtrees/gtest/src/v1.16.0-a2e0b328c1.clean
-- Configuring x64-windows
-- Building x64-windows-dbg
-- Building x64-windows-rel
-- Installing: C:/app/vcpkg/packages/gtest_x64-windows/src/gtest.cc
-- Installing: C:/app/vcpkg/packages/gtest_x64-windows/src/gtest_main.cc
-- Installing: C:/app/vcpkg/packages/gtest_x64-windows/src/gtest-all.cc
-- Installing: C:/app/vcpkg/packages/gtest_x64-windows/src/gtest-assertion-result.cc
-- Installing: C:/app/vcpkg/packages/gtest_x64-windows/src/gtest-death-test.cc
-- Installing: C:/app/vcpkg/packages/gtest_x64-windows/src/gtest-filepath.cc
-- Installing: C:/app/vcpkg/packages/gtest_x64-windows/src/gtest-internal-inl.h
-- Installing: C:/app/vcpkg/packages/gtest_x64-windows/src/gtest-matchers.cc
-- Installing: C:/app/vcpkg/packages/gtest_x64-windows/src/gtest-port.cc
-- Installing: C:/app/vcpkg/packages/gtest_x64-windows/src/gtest-printers.cc
-- Installing: C:/app/vcpkg/packages/gtest_x64-windows/src/gtest-test-part.cc
-- Installing: C:/app/vcpkg/packages/gtest_x64-windows/src/gtest-typed-test.cc
-- Fixing pkgconfig file: C:/app/vcpkg/packages/gtest_x64-windows/lib/pkgconfig/gmock.pc
-- Fixing pkgconfig file: C:/app/vcpkg/packages/gtest_x64-windows/lib/pkgconfig/gmock_main.pc
-- Fixing pkgconfig file: C:/app/vcpkg/packages/gtest_x64-windows/lib/pkgconfig/gtest.pc
-- Fixing pkgconfig file: C:/app/vcpkg/packages/gtest_x64-windows/lib/pkgconfig/gtest_main.pc
Downloading msys2-mingw-w64-x86_64-pkgconf-1~2.3.0-1-any.pkg.tar.zst, trying https://mirror.msys2.org/mingw/mingw64/mingw-w64-x86_64-pkgconf-1~2.3.0-1-any.pkg.tar.zst
Successfully downloaded msys2-mingw-w64-x86_64-pkgconf-1~2.3.0-1-any.pkg.tar.zst
Downloading msys2-msys2-runtime-3.5.4-2-x86_64.pkg.tar.zst, trying https://mirror.msys2.org/msys/x86_64/msys2-runtime-3.5.4-2-x86_64.pkg.tar.zst
Successfully downloaded msys2-msys2-runtime-3.5.4-2-x86_64.pkg.tar.zst
-- Using msys root at C:/app/vcpkg/downloads/tools/msys2/21caed2f81ec917b
-- Fixing pkgconfig file: C:/app/vcpkg/packages/gtest_x64-windows/debug/lib/pkgconfig/gmock.pc
-- Fixing pkgconfig file: C:/app/vcpkg/packages/gtest_x64-windows/debug/lib/pkgconfig/gmock_main.pc
-- Fixing pkgconfig file: C:/app/vcpkg/packages/gtest_x64-windows/debug/lib/pkgconfig/gtest.pc
-- Fixing pkgconfig file: C:/app/vcpkg/packages/gtest_x64-windows/debug/lib/pkgconfig/gtest_main.pc
-- Installing: C:/app/vcpkg/packages/gtest_x64-windows/share/gtest/copyright
-- Installing: C:/app/vcpkg/packages/gtest_x64-windows/share/gtest/usage
-- Performing post-build validation
Starting submission of gtest:x64-windows@1.16.0#1 to 1 binary cache(s) in the background
Elapsed time to handle gtest:x64-windows: 37 s
gtest:x64-windows package ABI: 335535219304e273a29db1a9d3404a45eae1c596edeceb017c3fd160d19fdc05
Total install time: 37 s
The package gtest is compatible with built-in CMake targets:

    enable_testing()

    find_package(GTest CONFIG REQUIRED)
    target_link_libraries(main PRIVATE GTest::gtest GTest::gtest_main GTest::gmock GTest::gmock_main)

    add_test(AllTestsInMain main)

Completed submission of vcpkg-cmake-config:x64-windows@2024-05-23 to 1 binary cache(s) in 55.7 ms
Waiting for 1 remaining binary cache submissions...
Completed submission of gtest:x64-windows@1.16.0#1 to 1 binary cache(s) in 1.6 s (1/1)
```


### 移除已安装的库

如果需要移除某个库，可以使用 remove 命令：

```powershell
.\vcpkg remove jsoncpp
```

### 列出已安装的库

运行以下命令，查看已安装的库：

```powershell
.\vcpkg list
```

### 更新库

查看可更新的库：

```powershell
.\vcpkg update
```

更新所有库：

```powershell
.\vcpkg upgrade
```


## 与 Visual Studio 集成


### 全局集成：将 vcpkg 集成到全局环境，适用于所有 Visual Studio 项目：


```powershell
.\vcpkg integrate install
```
执行样例如下：
```
PS C:\Users\x> vcpkg integrate install
Applied user-wide integration for this vcpkg root.
CMake projects should use: "-DCMAKE_TOOLCHAIN_FILE=C:/app/vcpkg/scripts/buildsystems/vcpkg.cmake"

All MSBuild C++ projects can now #include any installed libraries. Linking will be handled automatically. Installing new libraries will make them instantly available.
```

集成后，Visual Studio 会自动识别 vcpkg 安装的库，无需手动配置头文件和库路径。


### 移除全局集成：


```powershell
.\vcpkg integrate remove
```

## 与 CMake 集成


• 在 CMake 项目中使用 vcpkg 管理的库，需要在 CMake 配置中添加 vcpkg 的工具链文件。假设你已经安装并配置了 vcpkg，可以在 CMake 中使用`-DCMAKE_TOOLCHAIN_FILE`参数来指定 vcpkg 的工具链文件：


```bash
cmake -DCMAKE_TOOLCHAIN_FILE=C:/path/to/vcpkg/scripts/buildsystems/vcpkg.cmake ..
```

• 在 CMakeLists.txt 文件中使用`find_package()`来查找并链接库。例如，如果你安装了 Boost：


```cmake
find_package(Boost REQUIRED)
target_link_libraries(my_target Boost::Boost)
```

# 注意事项

- 确保你的系统已经安装了必要的编译器和工具，例如在 Windows 上安装 Visual Studio 的 MSVC 编译器。

- 在使用 vcpkg 时，可能会遇到网络问题导致下载库失败。可以尝试使用代理

```
set HTTP_PROXY=http://10.15.1.2:8080
set HTTPS_PROXY=http://10.15.1.2:8080
```


原文链接：https://blog.csdn.net/qq_40685088/article/details/145741701
