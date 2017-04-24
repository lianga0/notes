##### mysql连接自动关闭

MySQL服务器所支持的最大连接数是有上限的，因为每个连接的建立都会消耗内存，因此我们希望客户端在连接到MySQL Server处理完相应的操作后，应该断开连接并释放占用的内存。如果你的MySQL Server有大量的闲置连接，他们不仅会白白消耗内存，而且如果连接一直在累加而不断开，最终肯定会达到MySQL Server的连接上限数，这会报'too many connections'的错误。

###### 1. interactive_timeout:

<table>
<tr>
    <td>Command-Line Format</td>
    <td colspan="2">--interactive-timeout=#</td>
</tr>

<tr>
    <td rowspan="3">System Variable</td>
    <td>Name</td>
    <td>interactive_timeout</td>
</tr>
<tr>
    <td>Variable Scope</td>
    <td>Global, Session</td>
</tr>
<tr>
    <td>Dynamic Variable</td>
    <td>Yes</td>
</tr>

<tr>
    <td rowspan="3">Permitted Values</td>
    <td>Type</td>
    <td>integer</td>
</tr>
<tr>
    <td>Default</td>
    <td>28800</td>
</tr>
<tr>
    <td>Min Value</td>
    <td>1</td>
</tr>
</table>

The number of seconds the server waits for activity on an interactive connection before closing it. An interactive client is defined as a client that uses the `CLIENT_INTERACTIVE` option to `mysql_real_connect()`. 

参数含义：服务器关闭交互式连接前等待活动的秒数。交互式客户端定义为在mysql_real_connect()中使用CLIENT_INTERACTIVE选项的客户端。

参数默认值：28800秒（8小时）

###### 2. wait_timeout:

<table>
<tr>
    <td>Command-Line Format</td>
    <td colspan="2">--wait-timeout=#</td>
</tr>
<tr>
    <td rowspan="3">System Variable</td>
    <td>Name</td>
    <td>wait_timeout</td>
</tr>
<tr>
    <td>Variable Scope</td>
    <td>Global, Session</td>
</tr>
<tr>
    <td>Dynamic Variable</td>
    <td>Yes</td>
</tr>
<tr>
    <td rowspan="4">Permitted Values (Windows)</td>
    <td>Type</td>
    <td>integer</td>
</tr>
<tr>
    <td>Default</td>
    <td>28800</td>
</tr>
<tr>
    <td>Min Value</td>
    <td>1</td>
</tr>
<tr>
    <td>Max Value</td>
    <td>2147483</td>
</tr>
<tr>
    <td rowspan="4">Permitted Values (Other)</td>
    <td>Type</td>
    <td>integer</td>
</tr>
<tr>
    <td>Default</td>
    <td>28800</td>
</tr>
<tr>
    <td>Min Value</td>
    <td>1</td>
</tr>
<tr>
    <td>Max Value</td>
    <td>31536000</td>
</tr>
</table>

The number of seconds the server waits for activity on a noninteractive connection before closing it.

参数含义：服务器关闭非交互连接之前等待活动的秒数。

参数默认值：28800秒（8小时）

On thread startup, the session wait_timeout value is initialized from the global wait_timeout value or from the global interactive_timeout value, depending on the type of client (as defined by the `CLIENT_INTERACTIVE` connect option to `mysql_real_connect()`). 

在线程启动时，根据全局wait_timeout值或全局interactive_timeout值初始化会话wait_timeout值。参数选取取决于客户端连接类型(由`mysql_real_connect()`的连接选项`CLIENT_INTERACTIVE定义`)。

Reference：
[MySQL中的配置参数interactive_timeout和wait_timeout(可能导致过多sleep进程的两个参数)](http://www.cnblogs.com/jiunadianshi/articles/2475475.html)

[Server System Variables](https://dev.mysql.com/doc/refman/5.7/en/server-system-variables.html#sysvar_wait_timeout)