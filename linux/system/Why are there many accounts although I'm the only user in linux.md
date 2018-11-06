## Why are there many accounts? I'm the only user in Linux

> 2015.4.19 at 19:15

### Q: 

I am running an Ubuntu 12.04 desktop system. So far I have only installed some programs (I have sudo rights).

- When I check the list of users on the system, I see a long list, like more than 20 users—when were these users created (e.g. daemon, sys, sync, games, pulse, etc.)? How are these related to new programs being installed?

- If I run a program on my system, it should run with my UID. But on doing a ps, I see many other programs running with different UID (like root, daemon, avahi, syslog, colord etc.) — how were these programs started with different UIDs?

### A:

**User accounts are used not only for actual, human users, but also to run system services and sometimes as owners of system files**. This is done because the separation between human users' resources (processes, files, etc.) and the separation between system services' resources requires the same mechanisms under the hood.

The programs that you run normally run with your user ID. It's only system daemons that run under their own account. *Either the configuration file that indicates when to run the daemon also indicates what user should run it, or the daemon switches to an unprivileged account after starting*. Some daemons require full administrative privileges, so they run under the `root` account. Many daemons only need access to a specific hardware device or to specific files, so they run under a dedicated user account. This is done for security: that way, even if there's a bug or misconfiguration in one of these services, it can't lead to a full system attack, because the attacker will be limited to what this service can do and won't be able to overwrite files, spy on processes, etc.

Under Ubuntu, user IDs in the range 0–99 are created at system installation. 0 is root; many of the ones in the range 1–99 exist only for historical reasons and are only kept for backward compatibility with some local installations that use them (a few extra entries don't hurt). User IDs in the range 100–999 are created and removed dynamically when services that need a dedicated user ID are installed or removed. The range from 1000 onwards is for human users or any other account created by the system administrator. The same goes for groups.

#### Another Answer:

> 2015.4.19 - dimo414 

Think about it another way: when the computer first boots you're not logged in yet, and the programs have to run as somebody. They could all run as root, but that's insecure, as most of these programs are only responsible for a small part of the computer's operation. Once you're logged in, most programs you run directly will be run as you.

> 2015.4.19 - Federico Poloni

Ultimately, it is a hack. A widely used one, but a hack nevertheless. UNIX distributions abuse the "user" concept in order to work around an old and incomplete security model.

### How were these programs started with different UIDs?

Under Unix and Linux, a process running under the aegis of the superuser can change its user account to something else and continue running the same program, but the reverse is not permitted. (One must use the set-UID mechanism.)

There are a bunch of ways for a process to change its own EUID.

```
setuid() - as a side-effect sets EUID when used by a process with EUID of 0
seteuid()
setreuid()
```

Depending on the effective UID of the program, and whether there is a saved UID, you may be able to switch between two EUID values in a non-root program. With a root privileged program, you have to be careful - you have to decide whether the change should be irreversible, and use the correct function for the job. (Using `setuid()` as root is irreversible.)

## How to use special permissions: the setuid, setgid and sticky bits

> 20 November 2017  - Egidio Docile

**Normally, on a unix-like operating system, the ownership of files and directories is based on the default `uid` (user-id) and `gid` (group-id) of the user who created them. The same thing happens when a process is launched: it runs with the effective user-id and group-id of the user who started it, and with the corresponding privileges. This behavior can be modified by using special permissions.**

### The `setuid` bit

**When the `setuid` bit is used, the behavior described above is modified so that when an executable is launched, it does not run with the privileges of the user who launched it, but with that of the file owner instead.** So, for example, if an executable has the `setuid` bit set on it, and it's owned by root, when launched by a normal user, it will run with root privileges. It should be clear why this represents a potential security risk, if not used correctly. 

An example of an executable with the `setuid` permission set is `passwd`, the utility we can use to change our login password. We can verify that by using the `ls` command:

```
ls -l /bin/passwd
-rwsr-xr-x. 1 root root 27768 Feb 11  2017 /bin/passwd
```

How to identify the `setuid` bit? As you surely have noticed looking at the output of the command above, the `setuid` bit is represented by an `s` in place of the `x` of the executable bit. The `s` implies that the executable bit is set, otherwise you would see a capital `S`. This happens when the setuid or setgid bits are set, but the executable bit is not, showing the user an inconsistency: the `setuid` and `setgid` bits have no effect if the executable bit is not set. The setuid bit has no effect on directories.

### The `setgid` bit

Unlike the `setuid` bit, the `setgid` bit has effect on both files and directories. In the first case, the file which has the `setgid` bit set, when executed, instead of running with the privileges of the group of the user who started it, runs with those of the group which owns the file: in other words, the group ID of the process will be the same of that of the file. 

When used on a directory, instead, the `setgid` bit alters the standard behavior so that the group of the files created inside directory, will not be that of the user who created them, but that of the parent directory itself. This is often used to ease the sharing of files (files will be modifiable by all the users that are part of group). Just like the `setuid`, the `setgid` bit can easily be spotted (in this case on a test directory):

```
ls -ld test
drwxrwsr-x. 2 egdoc egdoc 4096 Nov  1 17:25 test
```

This time the `s` is present in place of the executable bit on the group sector.

### The sticky bit

The sticky bit works in a different way: while it has no effect on files, when used on a directory, all the files in the directory will be modifiable only by their owners. A typical case in which it is used, involves the `/tmp` directory. Typically this directory is writable by all users on the system, so to make impossible for one user to delete the files of another one, the sticky bit is set:

```
$ ls -ld /tmp
drwxrwxrwt. 14 root root 300 Nov  1 16:48 /tmp
```

In this case the owner, the group, and all other users, have full permissions on the directory (read, write and execute). The sticky bit is identifiable by a `t` which is reported where normally the executable `x` bit is shown, in the "other" section. Again, a lowercase `t` implies that the executable bit is also present, otherwise you would see a capital `T`.

### How to set special bits

Just like normal permissions, the special bits can be assigned with the `chmod` command, using the numeric or the `ugo/rwx` format. In the former case the `setuid`, `setgid`, and `sticky` bits are represented respectively by a value of 4, 2 and 1. So for example if we want to set the `setgid` bit on a directory we would execute:

```
$ chmod 2775 test
```

With this command we set the `setgid` bit on the directory, (identified by the first of the four numbers), and gave full privileges on it to it's owner and to the user that are members of the group the directory belongs to, plus read and execute permission for all the other users (remember the execute bit on a directory means that a user is able to `cd` into it). 

The other way we can set the special permissions bits is to use the `ugo/rwx` syntax:

```
$ chmod g+s test
```

To apply the `setuid` bit to a file, we would have run:

```
$ chmod u+s file
```

While to apply the sticky bit:

```
$ chmod o+t test
```

The use of special permissions can be very useful in some situations, but if not used correctly the can introduce serious vulnerabilities, so think twice before using them.

[Why are there many accounts? I'm the only user](https://unix.stackexchange.com/questions/197124/why-are-there-many-accounts-im-the-only-user)

[setuid - set user identity](http://man7.org/linux/man-pages/man2/setuid.2.html)

[Change EUID of running process](https://superuser.com/questions/56884/change-euid-of-running-process)

[Changing the owner of an existing process in Linux](https://stackoverflow.com/questions/428920/changing-the-owner-of-an-existing-process-in-linux)

[How to use special permissions: the setuid, setgid and sticky bits](https://linuxconfig.org/how-to-use-special-permissions-the-setuid-setgid-and-sticky-bits)