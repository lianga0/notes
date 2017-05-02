### How to: Prevent a fork bomb by limiting user process

> November 27, 2007 in Categories CentOS, Debian Linux, Howto, Linux, RedHat/Fedora Linux, Security last updated September 4, 2015

Earlier, I wrote about a [fork bomb](https://www.cyberciti.biz/faq/understanding-bash-fork-bomb/). A few readers like to know about getting protection against a fork bomb:

How do I protect my system from a fork bomb under a Linux system? How to stop a fork bomb on a RHEL or CentOS Linux?

**Limiting user processes** is important for running a stable system. To limit user process just add user name or group or all users to `/etc/security/limits.conf` file and impose process limitations.

##### Understanding /etc/security/limits.conf file

Each line describes a limit for a user in the form:

```
<domain> <type> <item> <value>
Where:

<domain> can be:
	an user name
	a group name, with @group syntax
	the wildcard *, for default entry
	the wildcard %, can be also used with %group syntax, for maxlogin limit
<type> can have the two values:
	“soft” for enforcing the soft limits
	“hard” for enforcing hard limits
<item> can be one of the following:
	core – limits the core file size (KB)
<value> can be one of the following:
	core – limits the core file size (KB)
	data – max data size (KB)
	fsize – maximum filesize (KB)
	memlock – max locked-in-memory address space (KB)
	nofile – max number of open files
	rss – max resident set size (KB)
	stack – max stack size (KB)
	cpu – max CPU time (MIN)
	nproc – max number of processes
	as – address space limit
	maxlogins – max number of logins for this user
	maxsyslogins – max number of logins on the system
	priority – the priority to run user process with
	locks – max number of file locks the user can hold
	sigpending – max number of pending signals
	msgqueue – max memory used by POSIX message queues (bytes)
	nice – max nice priority allowed to raise to
	rtprio – max realtime priority
	chroot – change root to directory (Debian-specific)
```

> **Warning**: This will have no effect on the root user or any process with the `CAP_SYS_ADMIN` or `CAP_SYS_RESOURCE` [capabilities](http://man7.org/linux/man-pages/man7/capabilities.7.html) are not affected by this kind of limitation on a Linux based system.

##### Configuration

Login as the root and open configuration file:

```
# vi /etc/security/limits.conf
```

Following will prevent a “fork bomb”:

```
vivek hard nproc 300
@student hard nproc 50
@faculty soft nproc 100
@pusers hard nproc 200
```

Above will prevent anyone in the student group from having more than 50 processes, faculty and pusers group limit is set to 100 and 200. Vivek can create only 300 process. Please note that KDE and Gnome desktop system can launch many process.

##### Test it again

Save and close the file. Test your new system by dropping a fork bomb:

```
$ :(){ :|:& };:
```

`:(){ :|:& };:` is nothing but a bash function. This function get executed recursively. It is often used by sys admin to test user process limitations. Linux process limits can be configured via `/etc/security/limits.conf` and PAM.

Once a successful fork bomb has been activated in a system it may not be possible to resume normal operation without rebooting the system as the only solution to a fork bomb is to destroy all instances of it.

> **Warning examples may crash your computerWARNING! These examples may crash your computer if executed.**

##### Understanding `:(){ :|:& };:` fork() bomb code

`:()` – Defined the function called `:`. This function accepts no arguments. The syntax for bash function is as follows:

```
foo(){
 arg1=$1
 arg2=$2
 echo 'Bar..'
 #do_something on $arg argument
}
```

fork() bomb is defined as follows:

```
:(){
 :|:&
};:
```

`:|:` – Next it will call itself using programming technique called recursion and pipes the output to another call of the function `:`. The worst part is function get called two times to bomb your system.

`&` – Puts the function call in the background so child cannot die at all and start eating system resources.

`;` – Terminate the function definition

`:` – Call (run) the function aka set the fork() bomb.

Here is more human readable code:

```
bomb() { 
 bomb | bomb &
}; bomb
```

Properly configured Linux / UNIX box should not go down when fork() bomb sets off.

From:[How to: Prevent a fork bomb by limiting user process](https://www.cyberciti.biz/tips/linux-limiting-user-process.html)

Reference:
[Understanding Bash fork() Bomb ~ :(){ :|:& };:](https://www.cyberciti.biz/faq/understanding-bash-fork-bomb/)

[CAPABILITIES](http://man7.org/linux/man-pages/man7/capabilities.7.html)