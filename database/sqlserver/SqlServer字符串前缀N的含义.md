### SqlServer字符串前缀N的含义

在MSSQL中，字符串前加上 N 代表存入数据库时以 Unicode 格式存储。

Unicode 字符串的格式与普通字符串相似，但它前面有一个 N 标识符（N 代表 SQL-92 标准中的国际语言 (National Language)）。N 前缀必须是大写字母。例如，'Michél' 是字符串常量而 N'Michél' 则是 Unicode 常量。

例如，N'string'  表示string是个Unicode字符串。

但有时候加与不加都一样，又是什么原因呢？这是由于自动转换造成的。
 
比如：

```
declare @status nvarchar(20)
select @status = N'stopped'
select @status = 'stopped'
```

实际上上述两句赋值的结果是一样的，因为变量类型就是 nvarchar(Unicode 类型)。

而有些地方（比如：`sp_executesql` 的参数）不能自动转换，所以需要加 N 了。

Unicode 常量被解释为 Unicode 数据，并且不使用代码页进行计算。Unicode 常量确实有排序规则，主要用于控制比较和区分大小写。为 Unicode 常量指派当前数据库的默认排序规则，除非使用 COLLATE 子句为其指定了排序规则。

Reference：

[T-SQL字符串前加N是什么意思](http://www.2cto.com/database/201301/181440.html)

[sql server中，N''表示什么意思？](https://zhidao.baidu.com/question/85830038.html)