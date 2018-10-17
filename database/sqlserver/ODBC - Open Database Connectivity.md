### ODBC - Open Database Connectivity

Open Database Connectivity (ODBC) is a standard application programming interface (API) for accessing database management systems (DBMS).The designers of ODBC aimed to make it independent of database systems and operating systems. An application written using ODBC can be ported to other platforms, both on the client and server side, with few changes to the data access code.

ODBC accomplishes DBMS independence by using an ODBC driver as a translation layer between the application and the DBMS. The application uses ODBC functions through an ODBC driver manager with which it is linked, and the driver passes the query to the DBMS. An ODBC driver can be thought of as analogous to a printer driver or other driver, providing a standard set of functions for the application to use, and implementing DBMS-specific functionality. An application that can use ODBC is referred to as "ODBC-compliant". Any ODBC-compliant application can access any DBMS for which a driver is installed. Drivers exist for all major DBMSs, many other data sources like address book systems and Microsoft Excel, and even for text or comma-separated values (CSV) files.

ODBC was originally developed by Microsoft and Simba Technologies during the early 1990s. ODBC 1.0 was released in September 1992. ODBC remains in wide use today, with drivers available for most platforms and most databases. It is not uncommon to find ODBC drivers for database engines that are meant to be embedded, like SQLite, as a way to allow existing tools to act as front-ends to these engines for testing and debugging. However, the rise of thin client computing using HTML as an intermediate format has reduced the need for ODBC. Many web development platforms contain direct links to target databases – MySQL being very common. The virtualization that ODBC offers is no longer a strong requirement, and development of ODBC is no longer as active as it once was.

ODBC(Open Database Connectivity,开放数据库互连)是微软公司开放服务结构中有关数据库的一个组成部分，它建立了一组规范，并提供了一组对数据库访问的标准API（应用程序编程接口）。这些API利用SQL来完成其大部分任务。ODBC本身也提供了对SQL语言的支持，用户可以直接将SQL语句送给ODBC。

一般，应用程序要访问一个数据库，首先必须用“ODBC数据源管理器”注册一个数据源（DSN）。DSN (Data Source Name) 代表 ODBC 连接数据源的信息，它存储数据源的连接详细信息，如数据库名称、 目录、 数据库驱动程序，用户 Id，密码等。这样，应用程序只需要提供给ODBC数据源名，ODBC就能建立起与相应数据库的连接。

此外，应用也可指定连接字符串来访问数据库。在模块中，可以定义用于指定连接信息的带格式连接字符串。连接字符串将连接信息直接传递到 ODBC 驱动程序管理器，不需要系统管理员或用户预先创建 DSN，从而简化应用程序。

“ODBC数据源管理器”提供了三种DSN，分别为用户DSN、系统DSN和文件DSN。**注意：驱动区分32位和64位版本，并且有时提供的功能不能完全一致。例如，Access在win10上可能没有32位的*accdb驱动，而只有64位的。**

<img src="imgs/ODBC Data Source Administrator.png" alt="ODBC Data Source Administrator" />

1. 用户DSN

会把相应的配置信息保存在Windows的注册表中，但是只允许创建该DSN的登录用户使用。

2.系统DSN

同样将有关的配置信息保存在系统注册表中，但是与用户DSN不同的是系统DSN允许所有登录服务器的用户使用。 

3.文件DSN

把具体的配置信息保存在硬盘上的某个具体文件中。文件DSN允许所有登录服务器的用户使用，而且即使在没有任何用户登录的情况下，也可以提供对数据库DSN的访问支持。此外，因为文件DSN被保存在硬盘文件里，所以可以方便地复制到其它机器中（文件可以在网络范围内共享）。这样，用户可以不对系统注册表进行任何改动就可直接使用在其它机器上创建的DSN。用户DSN和系统DSN的区别在于，用户DSN保存在注册表的HKEY_CURRENT_USER下，而系统DSN保存在HKEY_LOCAL_MACHINE下。


参考：

[Open Database Connectivity](https://en.wikipedia.org/wiki/Open_Database_Connectivity)

[【数据库】——ODBC数据源管理器 和 三种DSN](https://blog.csdn.net/z15732621736/article/details/47622357)

[What is a DSN (Data Source Name)?](https://support.microsoft.com/en-us/help/966849/what-is-a-dsn-data-source-name)

[ODBC 程序员'的参考](https://docs.microsoft.com/zh-cn/sql/odbc/reference/odbc-programmer-s-reference?view=sql-server-2017)

[Microsoft ODBC Driver for SQL Server](https://docs.microsoft.com/en-us/sql/connect/odbc/microsoft-odbc-driver-for-sql-server?view=sql-server-2017)