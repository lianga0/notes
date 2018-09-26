## Git在Windows平台配置使用beyond compare作为difftool

git作为分布式版本管理工具，各种强大之处不言自明，但在Windows上，我还是更习惯使用beyond compare作为可视化的diff工具。这里简单记录下配置过程

### 安装beyond compare

beyond compare默认安装于`C:\Program Files\Beyond Compare 4\`路径下。

### 创建启动defftool的脚本

找到Git在Windows上的安装路径，默认为`C:\Program Files\Git`。并在`C:\Program Files\Git\cmd`目录下，创建`git-difftool-wrapper.sh`文件，并写入下面脚本

```
# place this file in the Windows Git installation directory /cmd folder
# be sure to add the ../cmd folder to the Path environment variable

# diff is called by git with 7 parameters:
# path old-file old-hex old-mode new-file new-hex new-mode

"C:\Program Files\Beyond Compare 4\BComp.exe" "$1" "$2" | cat

```

### 修改Git配置文件

Windows中`.gitconfig`文件默认路径为“用户”目录。找到`.gitconfig文`件，添加以下内容。

```
[diff]
    tool = difftool
[difftool "difftool"]
    cmd = git-difftool-wrapper.sh "$LOCAL" "$REMOTE"
[difftool]
    prompt = false
```

### git difftool

修改完上述配置后，运行git difftool命令，即可看到熟悉的beyond compare diff的界面了。
这个Mac平台上的配置稍微有些不同，Mac平台可以配置diff节点的external属性（然后就可以直接用git diff命令）。我在Windows平台尝试配置不成功。

Reference： https://blog.csdn.net/u010232305/article/details/51767887

[自定义-Git-配置-Git](https://git-scm.com/book/zh/v2/%E8%87%AA%E5%AE%9A%E4%B9%89-Git-%E9%85%8D%E7%BD%AE-Git)
