## git获取某次commit的指定信息（作者，时间，message等）

> 2019-04-12 13:26:18

> From: https://blog.csdn.net/liurizhou/article/details/89234032

### 获取某个commit的作者:

```
$ git log --pretty=format:"%an" b29b8b608b4d00f85b5d08663120b286ea657b4a -1
liurizhou
```

### 获取某个commit的时间：

```
git log --pretty=format:"%cd" b29b8b608b4d00f85b5d08663120b286ea657b4a -1
Wed Apr 3 10:12:33 2019 +0800
```

### 获取某个commit的提交message：

```
$ git log --pretty=format:"%s" b29b8b608b4d00f85b5d08663120b286ea657b4a -1
Change the length of the pre label string.
```

其中--pretty=format:"%xx"可以指定需要的信息，其常用的选项有：

```
%H 提交对象（commit）的完整哈希字串 
%h 提交对象的简短哈希字串 
%T 树对象（tree）的完整哈希字串 
%t 树对象的简短哈希字串 
%P 父对象（parent）的完整哈希字串 
%p 父对象的简短哈希字串 
%an 作者（author）的名字 
%ae 作者的电子邮件地址 
%ad 作者修订日期（可以用 -date= 选项定制格式） 
%ar 作者修订日期，按多久以前的方式显示 
%cn 提交者(committer)的名字 
%ce 提交者的电子邮件地址 
%cd 提交日期 
%cr 提交日期，按多久以前的方式显示 
%s 提交说明
```

附更多选项：

```

%H: commit hash
%h: 缩短的commit hash
%T: tree hash
%t: 缩短的 tree hash
%P: parent hashes
%p: 缩短的 parent hashes
%an: 作者名字
%aN: mailmap的作者名字 (.mailmap对应，详情参照git-shortlog(1)或者git-blame(1))
%ae: 作者邮箱
%aE: 作者邮箱 (.mailmap对应，详情参照git-shortlog(1)或者git-blame(1))
%ad: 日期 (--date= 制定的格式)
%aD: 日期, RFC2822格式
%ar: 日期, 相对格式(1 day ago)
%at: 日期, UNIX timestamp
%ai: 日期, ISO 8601 格式
%cn: 提交者名字
%cN: 提交者名字 (.mailmap对应，详情参照git-shortlog(1)或者git-blame(1))
%ce: 提交者 email
%cE: 提交者 email (.mailmap对应，详情参照git-shortlog(1)或者git-blame(1))
%cd: 提交日期 (--date= 制定的格式)
%cD: 提交日期, RFC2822格式
%cr: 提交日期, 相对格式(1 day ago)
%ct: 提交日期, UNIX timestamp
%ci: 提交日期, ISO 8601 格式
%d: ref名称
%e: encoding
%s: commit信息标题
%f: sanitized subject line, suitable for a filename
%b: commit信息内容
%N: commit notes
%gD: reflog selector, e.g., refs/stash@{1}
%gd: shortened reflog selector, e.g., stash@{1}
%gs: reflog subject
%Cred: 切换到红色
%Cgreen: 切换到绿色
%Cblue: 切换到蓝色
%Creset: 重设颜色
%C(...): 制定颜色, as described in color.branch.* config option
%m: left, right or boundary mark
%n: 换行
%%: a raw %
%x00: print a byte from a hex code
%w([[,[,]]]): switch line wrapping, like the -w option of git-shortlog(1).
```

————————————————

版权声明：本文为CSDN博主「liurizhou」的原创文章，遵循 CC 4.0 BY-SA 

版权协议，转载请附上原文出处链接及本声明。

原文链接：https://blog.csdn.net/liurizhou/article/details/89234032
