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


## 从历史提交修改某个删除文件的提交（从历史中删除某个文件的版本）

1. 查找需要删除文件删除是的commit id

```
git log --diff-filter=D --summary
```

可以获取指定的commit ID信息：commit ab44882486092d297307625e7d3abc5c8be443f1


2. 查看对应删除commit的前一个提交id（父commit）

```
git cat-file -p ab44882486092d297307625e7d3abc5c8be443f1
```

可以获取前一个commit ID信息：parent 3271a0d8f9fb1fe57cabc4a4f5adbe79be3f3c77


3. 查看被删除文件对应的blob信息

```
git ls-tree -r 3271a0d8f9fb1fe57cabc4a4f5adbe79be3f3c77
```

可以获取需要删除文件的blob信息
```
100644 blob 96ab444819ac199155982929ef10e033bf0bbb7e    yara_auto_builder/release_V1.9-.1015.zip
100644 blob b05b44317c068cfb882cc79e4ff5acd3c21bdcbc    yara_auto_builder/release_V3.9.1.1111.zip
```


4. 使用git-filter-repo从提交历史中删除指定blob的文件


```
python c:\Python3\git-filter-repo --strip-blobs-with-ids c:\Users\liangao_zhang\Desktop\ids.txt --force
```

其中，git-filter-repo需要自己从https://github.com/newren/git-filter-repo#how-do-i-use-it下载，然后将文件的blob信息放到ids.txt文件中即可。
更多可以参考：https://htmlpreview.github.io/?https://github.com/newren/git-filter-repo/blob/docs/html/git-filter-repo.html
