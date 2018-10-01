## Linux man 帮助文档约定格式

From: [详解Linux shell命令帮助格式](https://blog.csdn.net/littlewhite1989/article/details/54425071)

> 2017年01月14日 09:29:24

对于Linux初学者，比较艰苦的一个工作就是寻找合适的文档。Linux自带的文档，可以通过man查看各个命令的帮助文档。下面介绍man文档的一些约定格式：

man帮助文档一般分为：NAME、SYNOPSIS、DESCRIPTION、EXAMPLES、OVERVIEW等章节。其中SYNOPSIS章节直接给出命令支持的参数格式，其中特殊字符含义如下：

```
没有任何修饰符参数 : 原生参数
<>  : 占位参数
[]  : 可选组合
()  : 必选组合
|   : 互斥参数
... : 可重复指定前一个参数
--  : 标记后续参数类型
```

下面结合git命令的帮助文档，来解释每种特殊字符的含义。

```
SYNOPSIS
       git [--version] [--help] [-C <path>] [-c <name>=<value>]
           [--exec-path[=<path>]] [--html-path] [--man-path] [--info-path]
           [-p|--paginate|--no-pager] [--no-replace-objects] [--bare]
           [--git-dir=<path>] [--work-tree=<path>] [--namespace=<name>]
           [--super-prefix=<path>]
           <command> [<args>]

       git commit [-a | --interactive | --patch] [-s] [-v] [-u<mode>] [--amend]
                  [--dry-run] [(-c | -C | --fixup | --squash) <commit>]
                  [-F <file> | -m <msg>] [--reset-author] [--allow-empty]
                  [--allow-empty-message] [--no-verify] [-e] [--author=<author>]
                  [--date=<date>] [--cleanup=<mode>] [--[no-]status]
                  [-i | -o] [-S[<keyid>]] [--] [<file>...]

       git reset [-q] [<tree-ish>] [--] <paths>...
       git reset (--patch | -p) [<tree-ish>] [--] [<paths>...]
       git reset [--soft | --mixed [-N] | --hard | --merge | --keep] [-q] [<commit>]
```

### 参数类型解读

#### 原生参数:

说明文档里的字符即为命令需要使用的字符，这种参数在使用时必需指定，且和说明文档里的一致。

如，上述的`git`

### 占位参数

表示方式：`<>`

和原生参数类似，都是必需指定的，只不过占位参数的实际字符是在使用时指定的，同时为了方便阅读会用一个描述词汇来表示，并以`<>`包围，比如`<command>`表示git的子命令，使用时可以指定为具体的子命令，而command只是起一个说明作用，有些帮助说明里也会用大写来表示占位参数，比如将以上参数说明写成COMMAND

### 可选组合

表示方式： `[]`

括号里的参数为可选参数，比如`[--version]`，则`--version`为可选参数。

可选项和占位参数也可以同时使用，如`[<args>]`

### 必选组合

表示方式: `()`

括号里的参数必需指定，通常里面会是一些互斥参数，比如`(-c | -C | --fixup | --squash)`表示这四个参数必需指定一个。

必选组合也有可能使用大括号`{choice1,choice2}`的形式表示。参考[Beginners Guide to man Pages](http://www.tfug.org/helpdesk/general/man.html)

```
Some options will have a limited list of choices. A list of choices will be comma seperated and put between braces.

    {choice1,choice2}
    {yes,no}
```

### 互斥参数

表示方式: `|`

互斥参数一般都在`()`和`[]`里，表示该参数只能指定其中一个，比如`(-c | -C | --fixup | --squash)`

### 重复参数

表示方式: `...`

表示前一个参数可以被指定多个，比如`<file>...`。

`<file>`是一个占位参数，使用时必需指定为文件，`...`并表示可以指定多个路径。重复参数的一个典型使用场景就是移动文件，将多个文件移动到一个目录下，比如如下命令

```
git mv [<options>] <source>... <destination>
```


我们可以这样使用`git mv -f a.cpp b.py dir`
此时options对应为-f参数，source对应为a.cpp b.py，destination对应为dir

### 标记后续参数类型

表示方式: `--`

表示后续参数的某种类型，比如这里如果使用如下命令

```
git reset -p -- xx
```

对比git reset命令，这里的xx对应的应该是`<paths>`参数，当我们指定`--`之后，则git会认为xx就是一个路径，那怕它是特殊符号或者路径并不存在。这是shell命令的一个通用方式，比如我们有一个文件名为`-h`，如果想删除这个文件，执行

```
rm -h
```

肯定是无法删除的，因为这时`-h`会被认为是`rm`的一个参数选项，应该使用

```
rm -- -h
```

这时shell会将`-h`解释为一个文件名传递给`rm`命令

上述这些约定可以在man命令的帮助文档的DESCRIPTION中看到，但是并不是特别完整。

```
A manual page consists of several sections.

Conventional  section  names include NAME, SYNOPSIS, CONFIGURATION, DESCRIPTION, OPTIONS, EXIT STATUS, RETURN VALUE, ERRORS, ENVIRONMENT, FILES, VERSIONS, CON‐FORMING TO, NOTES, BUGS, EXAMPLE, AUTHORS, and SEE ALSO.

The following conventions apply to the SYNOPSIS section and can be used as a guide in other sections.

       bold text          type exactly as shown.
       italic text        replace with appropriate argument.
       [-abc]             any or all arguments within [ ] are optional.
       -a|-b              options delimited by | cannot be used together.
       argument ...       argument is repeatable.
       [expression] ...   entire expression within [ ] is repeatable.

Exact rendering may vary depending on the output device.  For instance, man will usually not be able to render italics when running in  a  terminal,  and  will typically use underlined or coloured text instead.

The  command  or  function illustration is a pattern that should match all possible invocations.  In some cases it is advisable to illustrate several exclusive invocations as is shown in the SYNOPSIS section of this manual page.
```

更具体的内容可以参考一下连接：

[Beginners Guide to man Pages](http://www.tfug.org/helpdesk/general/man.html)

[The Open Group Base Specifications Issue 7, 2018 edition
IEEE Std 1003.1-2017 (Revision of IEEE Std 1003.1-2008) - Utility Conventions](http://pubs.opengroup.org/onlinepubs/9699919799/)
