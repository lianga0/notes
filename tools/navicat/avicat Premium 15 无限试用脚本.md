## Navicat Premium 15 无限试用脚本

> xiaosemei 2020-07-23 20:33:11   

> From: https://blog.csdn.net/xiaosemei/article/details/107547168

```
@echo off
 
echo\
echo\
echo 适用于 Navicat 12.0.29
echo 正在清除试用信息。。。
 
for /f %%i in ('reg query HKCU\Software\Classes\CLSID') do call:checkDelCLSID %%i
 
reg delete HKCR\NavicatProfileBackup /f 1>nul 2>nul 
reg delete HKCR\NavicatProfileBatchJob /f 1>nul 2>nul
reg delete HKCR\NavicatProfileDataSync /f 1>nul 2>nul
reg delete HKCR\NavicatProfileExport /f 1>nul 2>nul
reg delete HKCR\NavicatProfileImport /f 1>nul 2>nul
reg delete HKCR\NavicatProfileModel /f 1>nul 2>nul
reg delete HKCR\NavicatProfileStructureSync /f 1>nul 2>nul
reg delete HKCR\NavicatProfileTransfer /f 1>nul 2>nul
reg delete HKCU\Software\PremiumSoft /f 1>nul 2>nul
 
rmdir /S /Q C:\Users\XXXX\Documents\Navicat
rmdir /S /Q C:\Users\XXXX\AppData\Local\Temp\NavicatCloud
 
echo\
echo\
echo 清除试用信息成功！
echo 请重新运行Navicat。
echo\
pause
exit
 
 
:checkDelCLSID
echo filtering %1
echo %1|findstr "{CAFEEFAC-" 1>nul 2>nul
set result=%errorlevel%
if %result%==0 goto:eof
 
echo checking %1
reg query %1\Info 1>nul 2>nul
set result=%errorlevel%
if %result%==1 goto:eof
 
echo deleteing %1
reg delete %1 /f 1>nul 2>nul
 
goto:eof
```


1.新建文本文档，建上面语句放入文本中

2.更改文件名后缀为 .bat

3.执行文件
