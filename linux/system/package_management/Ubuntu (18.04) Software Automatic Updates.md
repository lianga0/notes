## Ubuntu (18.04) Software Automatic Updates

> 2018.12.11

大早上收到服务器5xx过多报警，查看日志发现web应用无法连接redis服务器。因为，确定没有任何人动过服务器，一时间都有点怀疑服务器是不是被人搞了。

在redis服务器上，可以通过localhost连接，而无法通过服务器IP连接。查看redis运行信息，发现redis使用了默认配置文件，而不是我们自己指定的配置文件。

进而查看redis日志文件，发现redis有过一次重启，日志信息如下：

```
18723:C 11 Dec 01:15:39.017 * RDB: 3 MB of memory used by copy-on-write
27761:M 11 Dec 01:15:39.118 * Background saving terminated with success
27761:signal-handler (1544491003) Received SIGTERM scheduling shutdown...
27761:M 11 Dec 01:16:43.927 # User requested shutdown...
27761:M 11 Dec 01:16:43.927 * Saving the final RDB snapshot before exiting.
27761:M 11 Dec 01:16:45.853 * DB saved on disk
27761:M 11 Dec 01:16:45.853 * Removing the pid file.
27761:M 11 Dec 01:16:45.853 # Redis is now ready to exit, bye bye...
```

Google发现可能是redis自动升级导致redis重启，因为我们没有使用默认的redis配置文件，重启后redis回落到`/etc/redis/redis.conf`文件，导致web服务器无法访问redis。

查看Ubuntu软件包的安装和更新时间日志文件`/var/log/dpkg.log`，发现如下日志印证了我们的想法：

```
$ tail -50 /var/log/dpkg.log
2018-12-07 17:33:32 status installed openssl:amd64 1.0.2g-1ubuntu4.14
2018-12-07 17:33:32 trigproc libc-bin:amd64 2.23-0ubuntu10 <none>
2018-12-07 17:33:32 status half-configured libc-bin:amd64 2.23-0ubuntu10
2018-12-07 17:33:32 status installed libc-bin:amd64 2.23-0ubuntu10
2018-12-07 17:33:32 startup packages configure
2018-12-11 01:16:37 startup archives unpack
2018-12-11 01:16:42 upgrade redis-server:amd64 2:3.0.6-1ubuntu0.2 2:3.0.6-1ubuntu0.3
2018-12-11 01:16:42 status half-configured redis-server:amd64 2:3.0.6-1ubuntu0.2
2018-12-11 01:16:45 status unpacked redis-server:amd64 2:3.0.6-1ubuntu0.2
2018-12-11 01:16:45 status half-installed redis-server:amd64 2:3.0.6-1ubuntu0.2
2018-12-11 01:16:45 status triggers-pending man-db:amd64 2.7.5-1
2018-12-11 01:16:46 status triggers-pending systemd:amd64 229-4ubuntu21.10
2018-12-11 01:16:46 status triggers-pending ureadahead:amd64 0.100.0-19
2018-12-11 01:16:46 status half-installed redis-server:amd64 2:3.0.6-1ubuntu0.2
2018-12-11 01:16:46 status unpacked redis-server:amd64 2:3.0.6-1ubuntu0.3
2018-12-11 01:16:46 status unpacked redis-server:amd64 2:3.0.6-1ubuntu0.3
2018-12-11 01:16:46 upgrade redis-tools:amd64 2:3.0.6-1ubuntu0.2 2:3.0.6-1ubuntu0.3
2018-12-11 01:16:46 status half-configured redis-tools:amd64 2:3.0.6-1ubuntu0.2
2018-12-11 01:16:46 status unpacked redis-tools:amd64 2:3.0.6-1ubuntu0.2
2018-12-11 01:16:46 status half-installed redis-tools:amd64 2:3.0.6-1ubuntu0.2
2018-12-11 01:16:46 status half-installed redis-tools:amd64 2:3.0.6-1ubuntu0.2
2018-12-11 01:16:46 status unpacked redis-tools:amd64 2:3.0.6-1ubuntu0.3
2018-12-11 01:16:46 status unpacked redis-tools:amd64 2:3.0.6-1ubuntu0.3
2018-12-11 01:16:46 trigproc man-db:amd64 2.7.5-1 <none>
2018-12-11 01:16:46 status half-configured man-db:amd64 2.7.5-1
2018-12-11 01:16:47 status installed man-db:amd64 2.7.5-1
2018-12-11 01:16:47 trigproc systemd:amd64 229-4ubuntu21.10 <none>
2018-12-11 01:16:47 status half-configured systemd:amd64 229-4ubuntu21.10
2018-12-11 01:16:47 status installed systemd:amd64 229-4ubuntu21.10
2018-12-11 01:16:47 trigproc ureadahead:amd64 0.100.0-19 <none>
2018-12-11 01:16:47 status half-configured ureadahead:amd64 0.100.0-19
2018-12-11 01:16:47 status installed ureadahead:amd64 0.100.0-19
2018-12-11 01:16:47 startup packages configure
2018-12-11 01:16:47 configure redis-tools:amd64 2:3.0.6-1ubuntu0.3 <none>
2018-12-11 01:16:47 status unpacked redis-tools:amd64 2:3.0.6-1ubuntu0.3
2018-12-11 01:16:47 status half-configured redis-tools:amd64 2:3.0.6-1ubuntu0.3
2018-12-11 01:16:47 status installed redis-tools:amd64 2:3.0.6-1ubuntu0.3
2018-12-11 01:16:47 configure redis-server:amd64 2:3.0.6-1ubuntu0.3 <none>
2018-12-11 01:16:47 status unpacked redis-server:amd64 2:3.0.6-1ubuntu0.3
2018-12-11 01:16:47 status unpacked redis-server:amd64 2:3.0.6-1ubuntu0.3
2018-12-11 01:16:47 status unpacked redis-server:amd64 2:3.0.6-1ubuntu0.3
2018-12-11 01:16:47 status unpacked redis-server:amd64 2:3.0.6-1ubuntu0.3
2018-12-11 01:16:47 status unpacked redis-server:amd64 2:3.0.6-1ubuntu0.3
2018-12-11 01:16:47 status unpacked redis-server:amd64 2:3.0.6-1ubuntu0.3
2018-12-11 01:16:47 status unpacked redis-server:amd64 2:3.0.6-1ubuntu0.3
2018-12-11 01:16:47 status unpacked redis-server:amd64 2:3.0.6-1ubuntu0.3
2018-12-11 01:16:47 status unpacked redis-server:amd64 2:3.0.6-1ubuntu0.3
2018-12-11 01:16:47 status half-configured redis-server:amd64 2:3.0.6-1ubuntu0.3
2018-12-11 01:16:48 status installed redis-server:amd64 2:3.0.6-1ubuntu0.3
2018-12-11 01:16:48 startup packages configure

```

这下坐实是Ubuntu自动更新的锅了，之前从未考虑过自动更新的影响。鉴于这次事故，特意研究了下Ubuntu下的软件自动更新机制。了解机制后，禁用自动更新就很容易了（当然，并非一定要禁用自动更新）。

## Automatic Security Updates

There are always some security risks involved in running software upgrades without supervision, but there are also benefits. 

There are several options for enabling automatic updates:

- Use the GNOME Update Manager
- Use the `unattended-upgrades` package
- Write your own cron script that calls aptitude
- Use cron-apt

`unattended-upgrades` is one of the best practices of having automatic updates, especially for headless machines or servers!

Generally, Ubuntu already installed `unattended-upgrades` and been configured. If not, you can set up `unattended-upgrades` pretty easily by typing this in a terminal:

```
sudo apt-get install unattended-upgrades
sudo dpkg-reconfigure unattended-upgrades
```
The second command `sudo dpkg-reconfigure --priority=low unattended-upgrades`
is an interactive dialog which will create `/etc/apt/apt.conf.d/20auto-upgrades` with the following contents:

```
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Unattended-Upgrade "1";
```

Details about what these values mean may be found in the header of the `/etc/cron.daily/apt` file. Note:

1. When the apt job starts, it will sleep for a random period between 0 and `APT::Periodic::RandomSleep` seconds. The default value is "1800" so that the script will stall for up to 30 minutes (1800 seconds) so that the mirror servers are not crushed by everyone running their updates all at the same time. Only set this to 0 if you use a local mirror and don't mind the load spikes. Note that while the apt job is sleeping it will cause the execution of the rest of your cron.daily jobs to be delayed.

2. If you want the script to generate more verbose output set `APT::Periodic::Verbose "1"`;

3. If you want the script to automatically reboot when needed, you not only need to set `Unattended-Upgrade::Automatic-Reboot` "true", but you also need to have the "update-notifier-common" package installed. On minimal installations this is not installed by default and without it the automatic updater will never reboot and will not even tell you that you need to reboot manually if you have email notifications configured!


### `unattended-upgrades`

The purpose of `unattended-upgrades` is to keep the computer current with the latest security (and other) updates automatically.

The `unattended-upgrades` package can be used to automatically install updated packages, and can be configured to update all packages or just install security updates.

If you plan to use it, you should have some means to monitor your systems, such as installing the `apt-listchanges` package and configuring it to send you emails about updates. And there is always `/var/log/dpkg.log`, or the files in `/var/log/unattended-upgrades/`.

**As of Debian 9 (Stretch) both the `unattended-upgrades` and `apt-listchanges` packages are installed by default and upgrades are enabled with the GNOME desktop. Rudimentary configuration is accessible via the "Software & Updates" application**

The default configuration file for the unattended-upgrades package is at `/etc/apt/apt.conf.d/50unattended-upgrades`. The defaults will work fine, but you should read it and make changes as needed.

You should at least uncomment the following line:

```
Unattended-Upgrade::Mail "root";
```

#### Automatic call via `/etc/apt/apt.conf.d/20auto-upgrades`

To activate `unattended-upgrades`, you need to ensure that the apt configuration stub `/etc/apt/apt.conf.d/20auto-upgrades` contains at least the following lines:

```
# editor /etc/apt/apt.conf.d/20auto-upgrades
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Unattended-Upgrade "1";
```

The file `/etc/apt/apt.conf.d/20auto-upgrades` can be created manually or by running the following command as root:

```
# dpkg-reconfigure -plow unattended-upgrades
```


#### Automatic call via `/etc/apt/apt.conf.d/02periodic`

Alternatively, you can also create the apt configuration file `/etc/apt/apt.conf.d/02periodic` to activate `unattended-upgrades`:

```
# editor /etc/apt/apt.conf.d/02periodic
```


#### Manual run (for debugging)

To aid debugging you may need to run unattended-upgrades manually thus:

```
sudo unattended-upgrade -d
```

### Using GNOME Update Manager

If you are using GNOME, go to the "System" menu, then "Administration", then "Update Manager", then "Settings".

Open up the "Updates" tab and in the "Automatic updates" section select "Install security updates without confirmation".

### Determining the current `unattended-upgrades` configuration

The current configuration can be queried by running:

```
apt-config dump APT::Periodic::Unattended-Upgrade
```

Which will produce output like:

```
APT::Periodic::Unattended-Upgrade "1";
```

In this example, Unattended Upgrade will run every 1 day. If the number is "0" then unattended upgrades are disabled.

The files in `/etc/apt/apt.conf.d/` are evaluated in lexicographical order with each file capable of overriding values set in earlier files. This makes it insufficient to view the setting in `/etc/apt/apt.conf.d/20auto-upgrades` and why it is recommended to use `apt-config`.

## Disable Automatic Updates on Ubuntu 18.04 Bionic Beaver Linux

> Warning: Disabling automatic updates comes with a security risk. Once automatic updates are disabled, use `sudo apt update` and `sudo apt upgrade` to keep your system updated manually. 

### Disable Automatic Updates from Command Line

Edit `/etc/apt/apt.conf.d/20auto-upgrades` to disable automatic updates from the command line. Once you have the file opened, switch off the `Update-Package-Lists` directive from 1 to 0 as shown below on Line 1:

```
APT::Periodic::Update-Package-Lists "0";
APT::Periodic::Unattended-Upgrade "1";
```

### Disable Automatic Updates from Graphical User Interface


You can also disable automatic updates on your Ubuntu 18.04 desktop using the graphical user interface.

Use your search menu to open `Software & updates` windows. Click on `Updates` tab and select *Never* from `Automatically check for updates drop down` menu.

Once you enter your administrative password the automatic updates feature will be disabled.


Reference:

[怎么查询Ubuntu/Debian软件包的安装和更新时间](http://blog.topspeedsnail.com/archives/2709)

[AutomaticSecurityUpdates](https://help.ubuntu.com/community/AutomaticSecurityUpdates)

[Automatic Updates](https://help.ubuntu.com/lts/serverguide/automatic-updates.html.en)

[UnattendedUpgrades](https://wiki.debian.org/UnattendedUpgrades)

[Disable Automatic Updates on Ubuntu 18.04 Bionic Beaver Linux](https://linuxconfig.org/disable-automatic-updates-on-ubuntu-18-04-bionic-beaver-linux)