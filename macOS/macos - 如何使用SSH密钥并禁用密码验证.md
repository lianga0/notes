## macos - 如何使用SSH密钥并禁用密码验证

> How to use SSH keys and disable password authentication
> 2016.01.27
> https://apple.stackovernet.com/cn/q/57112

I'm trying to access a Mac remotely (I do have physical access to this Mac) through SSH from a Linux client computer. Now I want to set up SSH keys.

How do I set up my `/etc/ssh/sshd_config` to so that it doesn't ask for the password and only accepts SSH keys? 

> MacOS中`/etc`目录链接到`/private/etc`。所以，有些blog中也讲编辑`/private/etc/ssh/sshd_config`文件。

change the configure items in `/etc/ssh/sshd_config` as following:

```
PermitRootLogin no  # (or without-password)
PasswordAuthentication no 
PermitEmptyPasswords no 
ChallengeResponseAuthentication no
```

To stop and start SSHD:

```
sudo launchctl stop com.openssh.sshd
sudo launchctl start com.openssh.sshd
```

《完》