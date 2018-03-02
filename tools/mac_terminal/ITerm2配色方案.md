### ITerm2配色方案

> From: Bill_Wang

iTerm是一款为Mac量身打造的替代原生终端的软件，支持各种个性化定制，当然也包括主题配色。今天下载了iTerm顺便做了下配色，遇到不少波折，还好最终都解决了在此做下记录


##### 设置终端和ls可配色

终端输入`vim ~/.bash_profile`

添加如下export

```
#enables colorin the terminal bash shell export
export CLICOLOR=1

#setsup thecolor scheme for list export
export LSCOLORS=gxfxcxdxbxegedabagacad
 
#sets up theprompt color (currently a green similar to linux terminal)
export PS1='\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;36m\]\w\[\033[00m\]\$'
#enables colorfor iTerm
export TERM=xterm-256color
```


##### 设置vim可配色

终端输入 `vim .vimrc`

设置如下

```
 syntax on
 set number
 set ruler
```


##### 设置Color主题

到[Iterm2-color-schemes](https://github.com/mbadolato/iTerm2-Color-Schemes)下载主题。

iTerm2->Preferences->Profiles->Color选择Color Presets->import到下载好的主题目录下schemes目录下选择你要的主题导入，导入之后别忘记设置成你要的主题。

此时你就能看到变化了(如果还没变化的话请重启下iTerms)。


[ITerm2配色方案](https://www.jianshu.com/p/33deff6b8a63)
