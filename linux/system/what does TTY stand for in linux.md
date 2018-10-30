## What does “TTY” stand for?

> 2014.06.24

Q:

On the [Wikipedia's article (Computer terminal)](https://en.wikipedia.org/wiki/Computer_terminal) under the [hard copy terminals](https://en.wikipedia.org/wiki/Computer_terminal#Hard-copy_terminals) section of the article it says this "Early user terminals connected to computers were electromechanical teleprinters or teletypewriters (TeleTYpewriter, TTY)..."

So does TTY stand for teletypewriters? But it doesn't make any sense for me because I have never seen it.

A:

Early user terminals connected to computers were electromechanical teleprinters or teletypewriters (TeleTYpewriter, TTY), and since then TTY has continued to be used as the name for the text-only console although now this text-only console is a virtual console not a physical console.

There are 6 virtual consoles in Ubuntu accessed by the keyboard shortcuts `Ctrl+Alt+F1` to `Ctrl+Alt+F6`. You can move away from a virtual console (move the console to the background) by using the keyboard shortcut `Ctrl+Alt+F7`.

## What is the difference between /dev/ttyS and /dev/tty device files?

`/dev/tty` are used by the kernel to interface with built in devices such as monitor, keyboard or console terminal.

`/dev/ttyS` are files for terminals (devices) connected through the serial.

another description:

`/dev/tty` are the loginshells on your computer (/dev/tty1-6 representing alt+F1-6)

`/dev/ttyS0-n` on the other hand are the seriel ports on you computer (Typically known as com 1-4 on a windows machine)


From: 

[What does “TTY” stand for?](https://askubuntu.com/questions/481906/what-does-tty-stand-for)

[What is the difference between /dev/ttyS and /dev/tty device files?](https://www.quora.com/What-is-the-difference-between-dev-ttyS-and-dev-tty-device-files)

# Gettys on Serial Consoles (and Elsewhere)

> 2012.10.13

> TL;DR: To make use of a serial console, just use console=ttyS0 on the kernel command line, and systemd will automatically start a getty on it for you.

While physical RS232 serial ports have become exotic in today's PCs they play an important role in modern servers and embedded hardware. They provide a relatively robust and minimalistic way to access the console of your device, that works even when the network is hosed, or the primary UI is unresponsive. VMs frequently emulate a serial port as well.

Of course, Linux has always had good support for serial consoles, but with systemd we tried to make serial console support even simpler to use. In the following text I'll try to give an overview how serial console gettys on systemd work, and how TTYs of any kind are handled.

Let's start with the key take-away: in most cases, to get a login prompt on your serial prompt you don't need to do anything. systemd checks the kernel configuration for the selected kernel console and will simply spawn a serial getty on it. That way it is entirely sufficient to configure your kernel console properly (for example, by adding console=ttyS0 to the kernel command line) and that's it. But let's have a look at the details:

In systemd, two template units are responsible for bringing up a login prompt on text consoles:

1. `getty@.service` is responsible for virtual terminal (VT) login prompts, i.e. those on your VGA screen as exposed in /dev/tty1 and similar devices.

2. `serial-getty@.service` is responsible for all other terminals, including serial ports such as /dev/ttyS0. It differs in a couple of ways from `getty@.service`: among other things the $TERM environment variable is set to vt102 (hopefully a good default for most serial terminals) rather than linux (which is the right choice for VTs only), and a special logic that clears the VT scrollback buffer (and only work on VTs) is skipped.

### Virtual Terminals

Let's have a closer look how `getty@.service` is started, i.e. how login prompts on the virtual terminal (i.e. non-serial TTYs) work. Traditionally, the init system on Linux machines was configured to spawn a fixed number login prompts at boot. In most cases six instances of the getty program were spawned, on the first six VTs, tty1 to tty6.

In a systemd world we made this more dynamic: in order to make things more efficient login prompts are now started on demand only. As you switch to the VTs the getty service is instantiated to `getty@tty2.service`, `getty@tty5.service` and so on. Since we don't have to unconditionally start the getty processes anymore this allows us to save a bit of resources, and makes start-up a bit faster. This behaviour is mostly transparent to the user: if the user activates a VT the getty is started right-away, so that the user will hardly notice that it wasn't running all the time. If he then logs in and types ps he'll notice however that getty instances are only running for the VTs he so far switched to.

By default this automatic spawning is done for the VTs up to VT6 only (in order to be close to the traditional default configuration of Linux systems)[1]. Note that the auto-spawning of gettys is only attempted if no other subsystem took possession of the VTs yet. More specifically, if a user makes frequent use of fast user switching via GNOME he'll get his X sessions on the first six VTs, too, since the lowest available VT is allocated for each session.

Two VTs are handled specially by the auto-spawning logic: firstly tty1 gets special treatment: if we boot into graphical mode the display manager takes possession of this VT. If we boot into multi-user (text) mode a getty is started on it -- unconditionally, without any on-demand logic[2].

Secondly, tty6 is especially reserved for auto-spawned gettys and unavailable to other subsystems such as X[3]. This is done in order to ensure that there's always a way to get a text login, even if due to fast user switching X took possession of more than 5 VTs.

### Serial Terminals

Handling of login prompts on serial terminals (and all other kind of non-VT terminals) is different from that of VTs. By default systemd will instantiate one serial-getty@.service on the main kernel[4] console, if it is not a virtual terminal. The kernel console is where the kernel outputs its own log messages and is usually configured on the kernel command line in the boot loader via an argument such as `console=ttyS0`[5]. This logic ensures that when the user asks the kernel to redirect its output onto a certain serial terminal, he will automatically also get a login prompt on it as the boot completes[6]. systemd will also spawn a login prompt on the first special VM console (that's `/dev/hvc0`, `/dev/xvc0`, `/dev/hvsi0`), if the system is run in a VM that provides these devices. This logic is implemented in a generator called systemd-getty-generator that is run early at boot and pulls in the necessary services depending on the execution environment.

In many cases, this automatic logic should already suffice to get you a login prompt when you need one, without any specific configuration of systemd. However, sometimes there's the need to manually configure a serial getty, for example, if more than one serial login prompt is needed or the kernel console should be redirected to a different terminal than the login prompt. To facilitate this it is sufficient to instantiate `serial-getty@.service` once for each serial port you want it to run on[7]:

```
# systemctl enable serial-getty@ttyS2.service
# systemctl start serial-getty@ttyS2.service
```

And that's it. This will make sure you get the login prompt on the chosen port on all subsequent boots, and starts it right-away too.

Sometimes, there's the need to configure the login prompt in even more detail. For example, if the default baud rate configured by the kernel is not correct or other agetty parameters need to be changed. In such a case simply copy the default unit template to /etc/systemd/system and edit it there:

```
# cp /usr/lib/systemd/system/serial-getty@.service /etc/systemd/system/serial-getty@ttyS2.service
# vi /etc/systemd/system/serial-getty@ttyS2.service
 .... now make your changes to the agetty command line ...
# ln -s /etc/systemd/system/serial-getty@ttyS2.service /etc/systemd/system/getty.target.wants/
# systemctl daemon-reload
# systemctl start serial-getty@ttyS2.service

```

This creates a unit file that is specific to serial port ttyS2, so that you can make specific changes to this port and this port only.

And this is pretty much all there's to say about serial ports, VTs and login prompts on them. I hope this was interesting, and please come back soon for the next installment of this series!

#### Footnotes

[1] You can easily modify this by changing NAutoVTs= in logind.conf.

[2] Note that whether the getty on VT1 is started on-demand or not hardly makes a difference, since VT1 is the default active VT anyway, so the demand is there anyway at boot.

[3] You can easily change this special reserved VT by modifying ReserveVT= in logind.conf.

[4] If multiple kernel consoles are used simultaneously, the main console is the one listed first in /sys/class/tty/console/active, which is the last one listed on the kernel command line.

[5] See kernel-parameters.txt for more information on this kernel command line option.

[6] Note that agetty -s is used here so that the baud rate configured at the kernel command line is not altered and continued to be used by the login prompt.

[7] Note that this systemctl enable syntax only works with systemd 188 and newer (i.e. F18). On older versions use ln -s /usr/lib/systemd/system/serial-getty@.service /etc/systemd/system/getty.target.wants/serial-getty@ttyS2.service ; systemctl daemon-reload instead.

From: [systemd for Administrators, Part XVI](http://0pointer.de/blog/projects/serial-console.html)
