##### SIGHUP - (signal hang up)

On POSIX-compliant platforms, **SIGHUP** ("signal hang up") is a signal sent to a process when its controlling terminal is closed. (It was originally designed to notify the process of a serial line drop). SIGHUP is a **symbolic constant** defined in the header file `signal.h`.

###### History

Access to computer systems for many years consisted of connecting a terminal to a mainframe system via a serial line and the RS-232 protocol. For this reason, when a system of software interrupts, called signals, were being developed, a signal was designated for use on "Hangup".

SIGHUP would be sent to programs when the serial line was dropped, often because the connected user terminated the connection by hanging up the modem. The system would detect the line was dropped via the lost Data Carrier Detect (DCD) signal.

<img src="img/hungup.jpg" />

> A hangup was often the result of a connected user physically hanging up the modem

Signals have always been a convenient method of inter-process communication (IPC), but in early implementations there were no user-definable signals (such as the later additions of SIGUSR1 and SIGUSR2) that programs could intercept and interpret for their own purposes. For this reason, applications that did not require a controlling terminal, such as daemons, would re-purpose SIGHUP as a signal to re-read configuration files, or reinitialize. This convention survives to this day in packages such as Apache and Sendmail.

###### Modern usage

With the decline of access via serial line, the meaning of SIGHUP has changed somewhat on modern systems, often meaning a controlling pseudo or virtual terminal has been closed (i.e. a command is executed inside a terminal window and the terminal window is closed while the command process is still running).

If the process receiving SIGHUP is a Unix shell, then as part of job control it will often intercept the signal and ensure that all stopped processes are continued before sending the signal to child processes (more precisely, process groups, represented internally by the shell as a "job"), which by default terminates them.

This can be circumvented in two ways. Firstly, the Single UNIX Specification describes a shell utility called nohup, which can be used as a wrapper to start a program and make it ignore SIGHUP by default. Secondly, child process groups can be "disowned" by invoking disown with the job id, which removes the process group from the shell's job table (so they will not be sent SIGHUP), or (optionally) keeps them in the job table but prevents them from receiving SIGHUP on shell termination.

Different shells also have other methods of controlling and managing SIGHUP, such as the disown facility of ksh. Most modern Linux distributions documentation specify using `kill -HUP <processID>` to send the SIGHUP signal.

Daemon programs sometimes use SIGHUP as a signal to restart themselves, the most common reason for this being to re-read a configuration file that has been changed.

###### Details

Symbolic signal names are used because signal numbers can vary across platforms, but XSI-conformant systems allow the use of the numeric constant 1 to be used to indicate a SIGHUP, which the vast majority of systems in fact use.

SIGHUP can be handled. That is, programmers can define the action they want to occur upon receiving a SIGHUP, such as calling a function, ignoring it, or restoring the default action.

The default action on POSIX-compliant systems is an abnormal termination.

From Wikipedia:[SIGHUP](https://en.wikipedia.org/wiki/SIGHUP)