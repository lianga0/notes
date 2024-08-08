# 在Windows中安装OpenSHH服务

Get the latest build from github.com/PowerShell/Win32-OpenSSH/

Extract contents of the latest build to `C:\Program Files\OpenSSH`

Install ssh 

```
cd "C:\Program Files\OpenSSH"
powershell.exe -ExecutionPolicy Bypass -File install-sshd.ps1
```

Open the firewall for sshd.exe to allow inbound SSH connections 

```
netsh advfirewall firewall add rule name=sshd dir=in action=allow protocol=TCP localport=22
```

start the sshd service

```
net start sshd
```

Edit %programdata%/ssh/sshd_config

```
PasswordAuthenticcation yes
AuthorizedKeysFile .ssh/authorized_keys
Comment out these two lines
# Match Group administrators
# AuthorizedKeysFile __PROGRAMDATA__/ssh/administrators_authorized_keys
```

net stop sshd

net start sshd
