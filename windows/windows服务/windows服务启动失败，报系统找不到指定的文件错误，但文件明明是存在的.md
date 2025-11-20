# Windows服务启动失败，报系统找不到指定的文件错误，但文件明明是存在的

```
D:\> sc start ObCallbackTest type= kernel
[SC] StartService 失败 2:

系统找不到指定的文件。

D:\> sc query ObCallbackTest
SERVICE_NAME: ObCallbackTest
        TYPE               : 1  KERNEL_DRIVER
        STATE              : 1  STOPPED
        WIN32_EXIT_CODE    : 2  (0x2)
        SERVICE_EXIT_CODE  : 0  (0x0)
        CHECKPOINT         : 0x0
        WAIT_HINT          : 0x0
```

## 原因

ERROR_FILE_NOT_FOUND(=2) 有时并不是指 ImagePath 路径对应文件不存在，也有可能是驱动加载过程内部依赖的某个文件没找到，比如它静态依赖的DLL、SYS也不存在，也会报错误码 2。

驱动主函数不规范、入口异常或者初始化失败，也可能表现为此错误。尝试更换简单不会出错的测试驱动，排除代码因素。
