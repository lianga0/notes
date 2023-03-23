## How can I list all the deleted files in a git repository?

> 如何在git存储库中列出所有已删除的文件？

> 2023-03-21 13:26:18

> From: https://www.codenong.com/6017987/


git会存储文件何时被删除的信息，我应该能够检查各个提交以查看哪些文件已被删除。

但是，可以使用下面一个命令显示在存储库的生命周期内生成每个已删除文件的列表？

```
git log --diff-filter=D --summary

```

如果您不想要有关删除它们的提交的所有信息，您只需在其中添加grep delete即可。

```
git log --diff-filter=D --summary | grep delete

```

你也可以仅保留删除文件的文件名，命令如下

```
git log --all --pretty=format: --name-only --diff-filter=D
```

执行命令发现可能存在少量空文件名行，可以使用如下命令进行进一步过滤

```
git log --all --pretty=format: --name-only --diff-filter=D | grep -v '^$'
```

