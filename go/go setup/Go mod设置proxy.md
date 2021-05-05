# Go mod设置proxy

> 2020.02.06

## 开启Go module并设置proxy

Go 1.11和1.12版

将下面两个设置添加到系统的环境变量中

```
GO111MODULE=on
GOPROXY=https://goproxy.io
```

Go 1.13版本之后

需要注意的是这种方式并不会覆盖之前的配置，有点坑，你需要先把系统的环境变量里面的给删掉再设置

```
go env -w GO111MODULE=on
go env -w GOPROXY=https://goproxy.cn,https://goproxy.io,direct
```

## go get使用

使用go module之后，go get 拉取依赖的方式就发生了变化。下载项目依赖

```
go get
```

From: https://zhuanlan.zhihu.com/p/103534192
