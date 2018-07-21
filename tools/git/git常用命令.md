git常用命令

### 修改最后一次提交
$ git commit –amend

这种方法不仅可以修改commit message，也可以修改提交内容。这种方式在还没有推送到远端的情况下可以比较方便的保持原有的Change-Id，推荐使用（若已经推送到远端，Change-Id则会修改掉）。

### 将多个commit在另一个分支上合并一个提交
$ git merge --squash another_branch
$ git commit -m "message here"

--squash 选项的含义是：本地文件内容与不使用该选项的合并结果相同，但是不提交、不移动HEAD，因此需要一条额外的commit命令。其效果相当于将another分支上的多个commit合并成一个，放在当前分支上，原来的commit历史则没有拿过来。

判断是否使用--squash选项最根本的标准是，待合并分支上的历史是否有意义。

如果在开发分支上提交非常随意，甚至写成微博体，那么一定要使用--squash选项。版本历史记录的应该是代码的发展，而不是开发者在编码时的活动。

### 拣选指令，实现提交在新的分支上"重放"
git cherry-pick commit-id

### 删除分支
git branch -d branch-name

### 强制覆盖远程分支
git push -f remote-name branch-name