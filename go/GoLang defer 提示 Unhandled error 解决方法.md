# GoLand defer 提示 Unhandled error 解决方法

## Handling errors in defer

> 2019.08.13

> https://stackoverflow.com/questions/57740428/handling-errors-in-defer

I have a function which open db connection and return it. Or error, if something happened:

```
OpenDbConnection(connectionString string, logSql bool) (*gorm.DB, error) 
```

In this function I am using logger:

```
logger := zap.NewExample().Sugar()
defer logger.Sync()
```

Method `Sync()` returns error and I am ignoring this error.

What is the best strategy in this case ?

I can rewrite my code to avoid linter error, but I am still ignore error:

```
logger := zap.NewExample().Sugar()
defer func() {
    _ = logger.Sync()
}()
```

I can return error, but I am have correct db connection and I need to analyze this error in the calling function to understand what to do.

## Answer

You can name your returning error variable and initialize anywhere inside the function.

```
OpenDbConnection(connectionString string, logSql bool) (db *gorm.DB, err error) {

    logger := zap.NewExample().Sugar()
    defer func() {
        err = logger.Sync()
    }()

    // some logic here

    return db, err

}
```

The flaw in this as written is that if there is an error set inside the `// some logic here section` (e.g., `if ... { err := errors.New("bad"); return nil, err; }`) you will overwrite it with the result of `logger.Sync`. This may result in returning no error, if `logger.Sync` succeeds, even though the actual open failed.


you are right. to bypass this situation we can return an array of errors `errs []error` containing both deferred and logical errors. Or you can check the error returned by `logger.Sync()` in the defer and only overwrite the err variable if it's not nil.

## GoLand defer 提示 Unhandled error 解决方法

> https://www.zhangbj.com/p/651.html

> 2020-10-24

代码处理

```
defer func() {
    err := db.Close()
    if err != nil {
        fmt.Println(err)
        return
    }
}()
```

也可以不关心错误

```
defer func() {
    _ = db.Close()
}()
```

编辑器处理： 在设置中`Editor`下的`Inspections`搜索框中搜索`Unhandler error`，取消勾选即可。
