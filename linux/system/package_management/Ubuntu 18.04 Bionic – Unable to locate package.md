## Ubuntu 18.04 Bionic – Unable to locate package when installing in command line

> From: https://handyman.dulare.com/ubuntu-18-04-bionic-unable-to-locate-package-when-installing-in-command-line/

I just started to install Ubuntu Server 18.04 Bionic Beaver on new servers. I noticed an interesting thing – once the server is installed, I typically install additional software such as phpmyadmin or autossh. Surprisingly I was not able to install even such popular things no matter if I was using apt or apt-get…

```
$ sudo apt-get update
[...]
no errors
[...]
$ sudo apt-get install phpmyadmin
Reading package lists... Done
Building dependency tree       
Reading state information... Done
E: Unable to locate package phpmyadmin
```

The thing is that it looks like the default list of code sources stored in `/etc/apt/sources.list` is rather short:

```
deb http://archive.ubuntu.com/ubuntu/ bionic main
deb http://archive.ubuntu.com/ubuntu/ bionic-updates main
deb http://security.ubuntu.com/ubuntu bionic-security main
```

To be able to install things I needed, I had to change the contents of the `/etc/apt/sources.list` to the following:

```
deb http://archive.ubuntu.com/ubuntu/ bionic main restricted
deb http://archive.ubuntu.com/ubuntu/ bionic-updates main restricted
deb http://archive.ubuntu.com/ubuntu/ bionic universe
deb http://archive.ubuntu.com/ubuntu/ bionic-updates universe
deb http://archive.ubuntu.com/ubuntu/ bionic multiverse
deb http://archive.ubuntu.com/ubuntu/ bionic-updates multiverse
deb http://archive.ubuntu.com/ubuntu/ bionic-backports main restricted universe multiverse
deb http://security.ubuntu.com/ubuntu bionic-security main restricted
deb http://security.ubuntu.com/ubuntu bionic-security universe
deb http://security.ubuntu.com/ubuntu bionic-security multiverse
```

Once the list was updated, I executed apt update and I was good to go with my usual software list.

> Side note: the sources on the list above contains also software which is not supported by Ubuntu team and may not be under a free license. This means that you have to take care of the security and licensing on your own. The list above also contains the software which may not have been tested as extensively as that contained in the main release.

