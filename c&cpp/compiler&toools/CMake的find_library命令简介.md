CMake的find_library命令简介

## 用途概览

find_library用于在文件系统中查找某个库文件的完整路径，并把它保存到一个变量中。它只找到“库文件路径”（例如 /usr/lib/libssl.so、C:\lib\zlib.lib），不创建目标，也不解析依赖。

最简单用法：

```
find_library(MyLib z)    # 查找名为“z”的库，变量 MyLib 保存结果
```

完整用法参考文档：https://cmake.org/cmake/help/latest/command/find_library.html

```
find_library (
          <VAR>
          name | NAMES name1 [name2 ...] [NAMES_PER_DIR]
          [HINTS [path | ENV var]...]
          [PATHS [path | ENV var]...]
          [REGISTRY_VIEW (64|32|64_32|32_64|HOST|TARGET|BOTH)]
          [PATH_SUFFIXES suffix1 [suffix2 ...]]
          [VALIDATOR function]
          [DOC "cache documentation string"]
          [NO_CACHE]
          [REQUIRED|OPTIONAL]
          [NO_DEFAULT_PATH]
          [NO_PACKAGE_ROOT_PATH]
          [NO_CMAKE_PATH]
          [NO_CMAKE_ENVIRONMENT_PATH]
          [NO_SYSTEM_ENVIRONMENT_PATH]
          [NO_CMAKE_SYSTEM_PATH]
          [NO_CMAKE_INSTALL_PREFIX]
          [CMAKE_FIND_ROOT_PATH_BOTH |
           ONLY_CMAKE_FIND_ROOT_PATH |
           NO_CMAKE_FIND_ROOT_PATH]
         )
```

Prior to searching, `find_library` checks if variable `<VAR>` is defined. If the variable is not defined, the search will be performed. 
If the variable is defined and its value is `NOTFOUND`, or ends in `-NOTFOUND`, the search will be performed. 
If the variable contains any other value the search is not performed.


## 返回值与缓存行为

- 如果找到：`<VAR>` 被设为库的绝对路径（例如 /usr/lib/x86_64-linux-gnu/libz.so）。

- 如果没找到：`<VAR>` 被设为 `<VAR>-NOTFOUND`。

- 会创建一个缓存条目（CMakeCache.txt）。后续运行通常直接使用缓存值，不再搜索。若环境改变（库位置或工具链改变），请在 GUI/ccmake 清理该缓存条目，或者用 `unset(<VAR> CACHE)` 再次搜索。


## 库命名解析与平台差异

你在 NAMES 中提供的是“逻辑库名”，CMake会根据平台的常见前缀/后缀去尝试具体文件：

- Linux/Unix：`lib<name>.so`、`lib<name>.a `等

- macOS：`lib<name>.dylib`、`lib<name>.a` 等

- Windows：`<name>.lib`（可能是静态库或导入库），以及较少情况的 `<name>.a`（MinGW）

影响后缀顺序的变量：`CMAKE_FIND_LIBRARY_SUFFIXES`

例如在 Linux 上可临时修改以“偏好静态库”：

```
# 注意：这会全局影响本目录之后的查找顺序
set(CMAKE_FIND_LIBRARY_SUFFIXES ".a" ".so")
find_library(MyLib NAMES z)
```


## 搜索顺序（简化与实用视角） 

CMake 的查找路径比较复杂，遵循下列大致顺序（受选项和变量影响）：

1. HINTS 指定的目录（优先级高）

2. 环境变量（如 LIB、PATH 等，除非使用 NO_SYSTEM_ENVIRONMENT_PATH）

3. PATHS 指定的目录

4. 默认路径集合（除非使用 NO_DEFAULT_PATH），包括但不限于：

    - CMAKE_PREFIX_PATH、CMAKE_LIBRARY_PATH

    - CMAKE_INSTALL_PREFIX

    - CMAKE_SYSTEM_PREFIX_PATH（系统前缀，比如 /usr、/usr/local、Program Files 等）

    - 平台/发行版特有的多架构路径（例如 lib/x86_64-linux-gnu）

    - 包注册表（除非 NO_CMAKE_PACKAGE_REGISTRY）

    - CMAKE_FIND_ROOT_PATH（跨编译/SDK 根路径，受 CMAKE_FIND_ROOT_PATH_MODE_LIBRARY 控制）

5. PATH_SUFFIXES 会附加到每个候选目录（例如给出 lib、lib64，CMake会尝试 `<dir>/lib、<dir>/lib64）`



# 实战

在CMakeLists.txt中，使用find_library命令查找hs库，并将结果保存到变量HYPERSCAN_LIBRARY中。

```
find_library(HYPERSCAN_LIBRARY NAMES hs)
```

生成VS2022工程后，Debug版本可以正常编译链接，但是Release版本链接报错，错误信息如下：

```
默认库“MSVCRTD”与其他库的使用冲突；请使用 /NODEFAULTLIB:library

无法解析的外部符号 __imp__calloc_dbg，函数 "public: __cdecl std::_Compressed_pair<struct ue2::`anonymous namespace'::FloodComparator,class std::_Compressed_pair<class std::allocator<struct std::_Tree_node<struct std::pair<struct FDRFlood const ,class ue2::CharReach>,void *> >,class std::_Tree_val<struct std::_Tree_simple_types<struct std::pair<struct FDRFlood const ,class ue2::CharReach> > >,1>,1>::_Compressed_pair<struct ue2::`anonymous namespace'::FloodComparator,class std::_Compressed_pair<class std::allocator<struct std::_Tree_node<struct std::pair<struct FDRFlood const ,class ue2::CharReach>,void *> >,class std::_Tree_val<struct std::_Tree_simple_types<struct std::pair<struct FDRFlood const ,class ue2::CharReach> > >,1>,1><struct ue2::`anonymous namespace'::FloodComparator const &,struct std::_Zero_then_variadic_args_t>(struct std::_One_then_variadic_args_t,struct ue2::`anonymous namespace'::FloodComparator const &,struct std::_Zero_then_variadic_args_t &&)" (??$?0AEBUFloodComparator@?A0x69e95c48@ue2@@U_Zero_then_variadic_args_t@std@@@?$_Compressed_pair@UFloodComparator@?A0x69e95c48@ue2@@V?$_Compressed_pair@V?$allocator@U?$_Tree_node@U?$pair@$$CBUFDRFlood@@VCharReach@ue2@@@std@@PEAX@std@@@std@@V?$_Tree_val@U?$_Tree_simple_types@U?$pair@$$CBUFDRFlood@@VCharReach@ue2@@@std@@@std@@@2@$00@std@@$00@std@@QEAA@U_One_then_variadic_args_t@1@AEBUFloodComparator@?A0x69e95c48@ue2@@$$QEAU_Zero_then_variadic_args_t@1@@Z) 中引用了该符号
```

原因在于，CMake生成的VS2022工程中，Debug配置连接的库路径为`C:\app\vcpkg\installed\x64-windows\debug\lib\hs.lib`，而Release也使用该路径，导致链接报错。
Release正确的路径应该修改为`C:\app\vcpkg\installed\x64-windows\lib\hs.lib`。

工程“属性”页 -> “链接器” -> “输入” -> “附加依赖项”，修改为正确的路径。

上述问题本质在于：VS2022 是“多配置”生成器（Debug/Release 并存），而你用了一次 find_library 得到一个“单一”路径变量，它被缓存成 Debug 目录的库，于是 Release 也用同一个路径，造成链接错误。

解决方案推荐：使用 vcpkg 提供的 `find_package` 导入目标，vcpkg 的端口一般都导出配置包和导入目标，会自动处理 Debug/Release 库路径。但是在 vcpkg 中，有些端口不导出 CMake Config 包，这种情况下 `find_package` 无法使用，需要改为手动查找库并区分 `Debug/Release`。

比如， `find_package(hyperscan CONFIG REQUIRED)`没有在 vcpkg 的安装树中找到 hyperscan 的 CMake 配置文件（hyperscan-config.cmake）。会报如下错误：

```
CMake Error at C:/app/vcpkg/scripts/buildsystems/vcpkg.cmake:893 (_find_package):
  Could not find a package configuration file provided by "hyperscan" with
  any of the following names:

    hyperscanConfig.cmake
    hyperscan-config.cmake

  Add the installation prefix of "hyperscan" to CMAKE_PREFIX_PATH or set
  "hyperscan_DIR" to a directory containing one of the above files.  If
  "hyperscan" provides a separate development package or SDK, be sure it has
  been installed.
Call Stack (most recent call first):
  CMakeLists.txt:7 (find_package)


-- Configuring incomplete, errors occurred!
```

可以按下面两条路径解决：

方案 A：如果 hyperscan端口导出了配置包-先确认 vcpkg 是否安装了 hyperscan 对应的三方包：

`vcpkg list - vcpkg install hyperscan:x64-windows` 检查是否存在配置文件：
`C:\app\vcpkg\installed\x64-windows\share\hyperscan\hyperscan-config.cmake` 如果存在，显式设置配置目录再调用 find_package：

```
set(hyperscan_DIR "C:/app/vcpkg/installed/x64-windows/share/hyperscan")
find_package(hyperscan CONFIG REQUIRED)

add_executable(app main.cpp)
# 根据 usage 文件或配置中的导入目标名链接（示例，实际名称以包为准）
target_link_libraries(app PRIVATE hyperscan::hyperscan)
```

如果该 share/hyperscan目录不存在或里面没有 config 文件，说明该端口不导出配置（在很多版本的 vcpkg 中确实如此），转到方案 B。

方案 B：不使用 `find_package`，手动区分 `Debug/Release` 查找库并创建导入目标。由于 VS 是多配置生成器，必须分别为 Debug 和 Release 查找库，不能用一个变量混用，否则缓存会污染。

```
# 假设 vcpkg 根在 C:/app/vcpkgset(VCPKG_ROOT "C:/app/vcpkg")
set(VCPKG_TRIPLET "x64-windows")
set(VCPKG_INSTALLED "${VCPKG_ROOT}/installed/${VCPKG_TRIPLET}")

# 分别查找 Release 和 Debug 的导入库（hs.lib）
find_library(HS_RELEASE NAMES hs PATHS "${VCPKG_INSTALLED}"
 PATH_SUFFIXES lib NO_DEFAULT_PATH REQUIRED DOC "Hyperscan release import library"
)

find_library(HS_DEBUG NAMES hs PATHS "${VCPKG_INSTALLED}"
 PATH_SUFFIXES debug/lib NO_DEFAULT_PATH REQUIRED DOC "Hyperscan debug import library"
)

# 如果需要包含目录（通常是 include）
set(HS_INCLUDE_DIR "${VCPKG_INSTALLED}/include")

# 可选：创建一个导入目标，自动根据配置切换库路径add_library(hyperscan::hs UNKNOWN IMPORTED)
set_target_properties(hyperscan::hs PROPERTIES IMPORTED_LOCATION_RELEASE "${HS_RELEASE}"
 IMPORTED_LOCATION_RELWITHDEBINFO "${HS_RELEASE}"
 IMPORTED_LOCATION_MINSIZEREL "${HS_RELEASE}"
 IMPORTED_LOCATION_DEBUG "${HS_DEBUG}"
 INTERFACE_INCLUDE_DIRECTORIES "${HS_INCLUDE_DIR}"
)

add_executable(app main.cpp)
target_link_libraries(app PRIVATE hyperscan::hs)

# 如果 vcpkg 使用动态库（x64-windows 默认常为 DLL），需要确保运行时 hs.dll 被复制到可执行文件旁# 可在构建后复制 DLL（示例，实际 DLL 路径请在 ${VCPKG_INSTALLED}/bin 或 debug/bin 中确认）
# add_custom_command(TARGET app POST_BUILD# COMMAND ${CMAKE_COMMAND} -E copy_if_different# "${VCPKG_INSTALLED}/bin/hs.dll" $<TARGET_FILE_DIR:app>
# )
# add_custom_command(TARGET app POST_BUILD# COMMAND ${CMAKE_COMMAND} -E copy_if_different# "${VCPKG_INSTALLED}/debug/bin/hs.dll" $<TARGET_FILE_DIR:app>
# )
```

不创建导入目标也可以，直接用生成器表达式链接（两者等价）：

```
add_executable(app main.cpp)
target_link_libraries(app PRIVATE $<$<CONFIG:Debug>:${HS_DEBUG}>
 $<$<CONFIG:Release,RelWithDebInfo,MinSizeRel>:${HS_RELEASE}>
)
```

完整测试工程cmake文件如下所示

```
cmake_minimum_required(VERSION 3.14)

set(VCPKG_ROOT "C:\\app\\vcpkg")
set(CMAKE_TOOLCHAIN_FILE "${VCPKG_ROOT}\\scripts\\buildsystems\\vcpkg.cmake")
set(VCPKG_TRIPLET "x64-windows")
set(VCPKG_INSTALLED "${VCPKG_ROOT}/installed/${VCPKG_TRIPLET}")

project(hyperscantest)

# 创建可执行文件
add_executable(main simplegrep.c)

# 分别查找 Release 和 Debug 的导入库（hs.lib）
find_library(HYPERSCAN_RELEASE_LIBRARY NAMES hs PATHS "${VCPKG_INSTALLED}"
 PATH_SUFFIXES lib NO_DEFAULT_PATH REQUIRED DOC "Hyperscan release import library"
)

find_library(HYPERSCAN_DEBUG_LIBRARY NAMES hs PATHS "${VCPKG_INSTALLED}"
 PATH_SUFFIXES debug/lib NO_DEFAULT_PATH REQUIRED DOC "Hyperscan debug import library"
)

# 查找hs.lib导入库的头文件
find_path(HYPERSCAN_INCLUDE_DIR hs/hs.h)

target_include_directories(main PUBLIC ${HYPERSCAN_INCLUDE_DIR})

if(NOT HYPERSCAN_INCLUDE_DIR OR NOT HYPERSCAN_DEBUG_LIBRARY OR NOT HYPERSCAN_RELEASE_LIBRARY)
  message(FATAL_ERROR "Could not find Hyperscan library/headers")
endif()

target_link_libraries(main PRIVATE $<$<CONFIG:Debug>:${HYPERSCAN_DEBUG_LIBRARY}>
 $<$<CONFIG:Release,RelWithDebInfo,MinSizeRel>:${HYPERSCAN_RELEASE_LIBRARY}>
)
```
