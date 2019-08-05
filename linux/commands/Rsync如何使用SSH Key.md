## Rsync如何使用SSH Key?

> 2018-07-17

`rsync`是linux下的“同步”神器，`rsync`的命令格式:

```
rsync [OPTION]... SRC DEST
```

推荐在 SSH 的基础上使用rsync。可以事先在`~/.ssh/config`中加入配置，这样远端可以写作`SSH配置名:路径`。

目录`SRC`是否以斜杠结尾，会影响同步的结果：

- 以斜杠结尾：目录`DEST`里面有 [目录`SRC`本身]
- 不以斜杠结尾：目录`DEST`里面有 [目录`SRC`里面的文件]
    
目录`DEST`是否以斜杠结尾，对同步的结果没有任何影响。

### 1. 直接指定SSH Key

如果不使用`~/.ssh/config`配置的换，也可以直接使用`rsync`的`-e`参数来指定SSH Key，使用的命令如下所示：

```
rsync -Pav -e "ssh -i $HOME/.ssh/somekey" username@hostname:/from/dir/ /to/dir/
```

### 2. 使用SSH `~/.ssh/config` 配置

设置SSH Host后，可以很方便的指定远程主机资源。

```
Host hostname
    User username
    IdentityFile ~/.ssh/somekey
```

例如上述`-e`参数指定SSH Key，在配置完`~/.ssh/config`后，命令可以简化为如下：

```
rsync -Pav hostname:/from/dir/ /to/dir/
```

### 3. 使用`ssh-agent`

通过SSH的`ssh-agent`可以帮助使用rsync采用公钥完成验证。命令如下：

```
eval `ssh-agent -s`
# or 
$ ssh-agent bash
# or
$ ssh-agent tcsh
# (or another shell you use).
ssh-add /path/to/mykey
```

添加公钥后，后续使用rsync命令同步远程主机时，就不再需要额外指定SSH密码或公钥了。

rsync命令更详细的使用方法可以参考[rsync 的使用方法](https://segmentfault.com/a/1190000015669114)文章。

rsync 全部参数：

```
-v, --verbose          详细模式输出。
-q, --quiet            精简输出模式。
-c, --checksum         打开校验开关，强制对文件传输进行校验。
-a, --archive          归档模式，表示以递归方式传输文件，并保持所有文件属性，等于-rlptgoD。
-r, --recursive        对子目录以递归模式处理。
-R, --relative         使用相对路径信息。
-b, --backup           创建备份，也就是对于目的已经存在有同样的文件名时，将老的文件重新命名为~filename。可以使用 --suffix 选项来指定不同的备份文件前缀。
--backup-dir           将备份文件（~filename）存放在在目录下。
-suffix=SUFFIX         定义备份文件前缀。
-u, --update           仅仅进行更新，也就是跳过所有已经存在于 DST，并且文件时间晚于要备份的文件。（不覆盖更新的文件。）
-l, --links            保留软链结。
-L, --copy-links       想对待常规文件一样处理软链结。
--copy-unsafe-links    仅仅拷贝指向 SRC 路径目录树以外的链结。
--safe-links           忽略指向 SRC 路径目录树以外的链结。
-H, --hard-links       保留硬链结。
-p, --perms            保持文件权限。
-o, --owner            保持文件属主信息。
-g, --group            保持文件属组信息。
-D, --devices          保持设备文件信息。
-t, --times            保持文件时间信息。
-S, --sparse           对稀疏文件进行特殊处理以节省 DST 的空间。
-n, --dry-run          显示哪些文件将被传输（新增、修改和删除）。
-W, --whole-file       拷贝文件，不进行增量检测。
-x, --one-file-system  不要跨越文件系统边界。
-B, --block-size=SIZE  检验算法使用的块尺寸，默认是 700 字节。
-e, --rsh=COMMAND      指定使用 rsh, ssh 方式进行数据同步。
--rsync-path=PATH      指定远程服务器上的 rsync 命令所在路径信息。
-C, --cvs-exclude      使用和CVS一样的方法自动忽略文件，用来排除那些不希望传输的文件。
--existing             仅仅更新那些已经存在于 DST 的文件，而不备份那些新创建的文件。
--delete               删除那些 DST 中 SRC 没有的文件。
--delete-excluded      同样删除接收端那些被该选项指定排除的文件。
--delete-after         传输结束以后再删除。
--ignore-errors        即使出现 IO 错误也进行删除。
--max-delete=NUM       最多删除 NUM 个文件。
--partial              保留那些因故没有完全传输的文件，以便实现断点续传。
--force                强制删除目录，即使不为空。
--numeric-ids          不将数字的用户和组 ID 匹配为用户名和组名。
--timeout=TIME         IP 超时时间，单位为秒。
-I, --ignore-times     不跳过那些有同样的时间和长度的文件。
--size-only            当决定是否要备份文件时，仅仅察看文件大小而不考虑文件时间。
--modify-window=NUM    决定文件是否时间相同时使用的时间戳窗口，默认为 0。
-T --temp-dir=DIR      在 DIR 中创建临时文件。
--compare-dest=DIR     同样比较 DIR 中的文件来决定是否需要备份。
--progress             显示传输过程。
-P                     等同于 -partial -progress。
-z, --compress         对备份的文件在传输时进行压缩处理。
--exclude=PATTERN      指定排除不需要传输的文件模式。
--include=PATTERN      指定不排除而需要传输的文件模式。
--exclude-from=FILE    排除 FILE 中指定模式的文件。
--include-from=FILE    不排除 FILE 指定模式匹配的文件。
--version              打印版本信息。
--address              绑定到特定的地址。
--config=FILE          指定其他的配置文件，不使用默认的 rsyncd.conf 文件。
--port=PORT            指定其他的 rsync 服务端口。
--blocking-io          对远程 shell 使用阻塞 IO。
--stats                给出某些文件的传输状态。
--log-format=formAT    指定日志文件格式。
--password-file=FILE   从 FILE 中得到密码。
--bwlimit=KBPS         限制 I/O 带宽，KBytes per second。
-h, --help             显示帮助信息。
```

Reference：

[rsync 的使用方法](https://segmentfault.com/a/1190000015669114)

[Specify identity file (id_rsa) with rsync](https://unix.stackexchange.com/questions/127352/specify-identity-file-id-rsa-with-rsync)