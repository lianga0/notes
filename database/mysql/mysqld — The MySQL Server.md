### mysqld — The MySQL Server

[mysqld](https://dev.mysql.com/doc/refman/5.5/en/mysqld.html), also known as MySQL Server, is the main program that does most of the work in a MySQL installation. MySQL Server manages access to the MySQL data directory that contains databases and tables. The data directory is also the default location for other information such as log files and status files.

When MySQL server starts, it listens for network connections from client programs and manages access to databases on behalf of those clients.

The mysqld program has many options that can be specified at startup. For a complete list of options, run this command:

```
shell> mysqld --verbose --help
```

MySQL Server also has a set of system variables that affect its operation as it runs. System variables can be set at server startup, and many of them can be changed at runtime to effect dynamic server reconfiguration. MySQL Server also has a set of status variables that provide information about its operation. You can monitor these status variables to access runtime performance characteristics.

##### max_connections

<table>
<tr>
    <td>Command-Line Format</td>
    <td colspan="2">--max-connections=#</td>
</tr>

<tr>
    <td rowspan="3">System Variable</td>
    <td>Name</td>
    <td>max_connections</td>
</tr>
<tr>
    <td>Variable Scope</td>
    <td>Global</td>
</tr>
<tr>
    <td>Dynamic Variable</td>
    <td>Yes</td>
</tr>

<tr>
    <td rowspan="4">Permitted Values</td>
    <td>Type</td>
    <td>integer</td>
</tr>
<tr>
    <td>Default</td>
    <td>151</td>
</tr>
<tr>
    <td>Min Value</td>
    <td>1</td>
</tr>
<tr>
    <td>Max Value</td>
    <td>100000</td>
</tr>
</table>

The maximum permitted number of simultaneous client connections. By default, this is 151.  See [Section B.5.2.7, “Too many connections”](https://dev.mysql.com/doc/refman/5.5/en/too-many-connections.html), for more information.

**Increasing this value increases the number of file descriptors that mysqld requires.** See [Section 8.4.3.1, “How MySQL Opens and Closes Tables”](https://dev.mysql.com/doc/refman/5.5/en/table-cache.html), for comments on file descriptor limits.

mysqld actually permits `max_connections+1` clients to connect. The extra connection is reserved for use by accounts that have the `SUPER` privilege. By granting the `SUPER` privilege to administrators and not to normal users (who should not need it), an administrator can connect to the server and use `SHOW PROCESSLIST` to diagnose problems even if the maximum number of unprivileged clients are connected.

##### open-files-limit

<table>
<tr>
    <td>Command-Line Format</td>
    <td colspan="2">--open-files-limit=#</td>
</tr>

<tr>
    <td rowspan="3">System Variable</td>
    <td>Name</td>
    <td>max_connections</td>
</tr>
<tr>
    <td>Variable Scope</td>
    <td>Global</td>
</tr>
<tr>
    <td>Dynamic Variable</td>
    <td>No</td>
</tr>

<tr>
    <td rowspan="4">Permitted Values</td>
    <td>Type</td>
    <td>integer</td>
</tr>
<tr>
    <td>Default</td>
    <td>0</td>
</tr>
<tr>
    <td>Min Value</td>
    <td>0</td>
</tr>
<tr>
    <td>Max Value</td>
    <td>platform dependent</td>
</tr>
</table>

Changes the number of file descriptors available to mysqld. You should try increasing the value of this option if mysqld gives you the error `Too many open files`. mysqld uses the option value to reserve descriptors with `setrlimit()`. Internally, the maximum value for this option is the maximum unsigned integer value, but the actual maximum is platform dependent. If the requested number of file descriptors cannot be allocated, mysqld writes a warning to the error log.

mysqld may attempt to allocate more than the requested number of descriptors (if they are available), using the values of `max_connections` and `table_open_cache` to estimate whether more descriptors will be needed.

On Unix, the value cannot be set less than ulimit -n.

##### Too many connections

If you get a `Too many connections error` when you try to connect to the mysqld server, this means that all available connections are in use by other clients.

The number of connections permitted is controlled by the `max_connections` system variable. The default value is 151 to improve performance when MySQL is used with the Apache Web server. (Previously, the default was 100.) If you need to support more connections, you should set a larger value for this variable.

mysqld actually permits `max_connections+1` clients to connect. The extra connection is reserved for use by accounts that have the `SUPER` privilege. By granting the `SUPER` privilege to administrators and not to normal users (who should not need it), an administrator can connect to the server and use `SHOW PROCESSLIST` to diagnose problems even if the maximum number of unprivileged clients are connected.

The maximum number of connections MySQL supports depends on the quality of the thread library on a given platform, the amount of RAM available, how much RAM is used for each connection, the workload from each connection, and the desired response time. Linux or Solaris should be able to support at least 500 to 1000 simultaneous connections routinely and as many as 10,000 connections if you have many gigabytes of RAM available and the workload from each is low or the response time target undemanding. Windows is limited to `(open tables × 2 + open connections) < 2048` due to the Posix compatibility layer used on that platform.

Increasing `open-files-limit` may be necessary.

##### How MySQL Opens and Closes Tables

When you execute a mysqladmin status command, you should see something like this:

```
Uptime: 426 Running threads: 1 Questions: 11082
Reloads: 1 Open tables: 12
```

The Open tables value of 12 can be somewhat puzzling if you have only six tables.

MySQL is multi-threaded, so there may be many clients issuing queries for a given table simultaneously. To minimize the problem with multiple client sessions having different states on the same table, the table is opened independently by each concurrent session. This uses additional memory but normally increases performance. With `MyISAM` tables, one extra file descriptor is required for the data file for each client that has the table open. (By contrast, the index file descriptor is shared between all sessions.)

The `table_open_cache` and `max_connections` system variables affect the maximum number of files the server keeps open. **If you increase one or both of these values, you may run up against a limit imposed by your operating system on the per-process number of open file descriptors.** Many operating systems permit you to increase the open-files limit, although the method varies widely from system to system. Consult your operating system documentation to determine whether it is possible to increase the limit and how to do so.

`table_open_cache` is related to `max_connections`. For example, for 200 concurrent running connections, specify a table cache size of at least `200 * N`, where N is the maximum number of tables per join in any of the queries which you execute. You must also reserve some extra file descriptors for temporary tables and files.

Make sure that your operating system can handle the number of open file descriptors implied by the `table_open_cache` setting. If `table_open_cache` is set too high, MySQL may run out of file descriptors and refuse connections, fail to perform queries, and be very unreliable.

You should also take into account the fact that the `MyISAM` storage engine needs two file descriptors for each unique open table. For a partitioned MyISAM table, two file descriptors are required for each partition of the opened table. (Note further that when `MyISAM` opens a partitioned table, it opens every partition of this table, whether or not a given partition is actually used. See [`MyISAM` and partition file descriptor usage](https://dev.mysql.com/doc/refman/5.5/en/partitioning-limitations.html#partitioning-limitations-myisam-file-descriptors).) You can increase the number of file descriptors available to MySQL using the `--open-files-limit` startup option to mysqld. See [Section B.5.2.18, “File Not Found and Similar Errors”](https://dev.mysql.com/doc/refman/5.5/en/not-enough-file-handles.html).

The cache of open tables is kept at a level of table_open_cache entries. The default value is 400; this can be changed with the --table_open_cache option to mysqld. Note that MySQL may temporarily open more tables than this to execute queries.

Refrence:
[mysqld — The MySQL Server](https://dev.mysql.com/doc/refman/5.5/en/mysqld.html)

[server-options](https://dev.mysql.com/doc/refman/5.5/en/server-options.html#option_mysqld_open-files-limit)

[Server System Variables](https://dev.mysql.com/doc/refman/5.5/en/server-system-variables.html#sysvar_max_connections)

[Too many connections](https://dev.mysql.com/doc/refman/5.5/en/too-many-connections.html)

[How MySQL Opens and Closes Tables](https://dev.mysql.com/doc/refman/5.5/en/table-cache.html)
