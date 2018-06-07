## How can I execute `date` inside of a cron tab job?

I want to create a log file for a cron script that has the current hour in the log file name. This is the command I tried to use:

```
0 * * * * echo hello >> ~/cron-logs/hourly/test`date "+%d"`.log
```

Unfortunately I get this message when that runs:

```
/bin/sh: -c: line 0: unexpected EOF while looking for matching ``'
/bin/sh: -c: line 1: syntax error: unexpected end of file
```

I have tried escaping the `date` part in various ways, but without much luck. Is it possible to make this happen in-line in a crontab file or do I need to create a shell script to do this?

##### Short answer:

Try this:

```
0 * * * * echo hello >> ~/cron-logs/hourly/test`date "+\%d"`.log
```

Note the backslash escaping the % sign.

##### Long answer:

The error message suggests that the shell which executes your command doesn't see the second back tick character:

> ```/bin/sh: -c: line 0: unexpected EOF while looking for matching ``'```

This is also confirmed by the second error message your received when you tried one of the other answers:

> ```/bin/sh: -c: line 0: unexpected EOF while looking for matching `)'```

The [crontab manpage](https://linux.die.net/man/5/crontab) confirms that the command is read only up to the first unescaped % sign:

> ```The "sixth" field (the rest of the line) specifies the command to be run. The entire command portion of the line, up to a newline or % character, will be executed by /bin/sh or by the shell specified in the SHELL variable of the cronfile. Percent-signs (%) in the command, unless escaped with backslash (\), will be changed into newline charac- ters, and all data after the first % will be sent to the command as standard input.```

FROM: https://unix.stackexchange.com/questions/29578/how-can-i-execute-date-inside-of-a-cron-tab-job
