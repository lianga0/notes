## What's the difference between MySQLdb, mysqlclient and MySQL connector/Python?

> 2018.10.19

Most languages have several database adapter layers of varying levels of sophistication, support and quality. 

### MySQLdb

[MySQLdb](http://mysql-python.sourceforge.net/MySQLdb.html) is a thin python wrapper around C module which implements API for MySQL database.

You can install this package use the following command. But MySQLdb is not support python3 and the last updated time is Jan 2, 2014.

```
pip install MySQL-python
```

> MySQLdb is a C module that links against the MySQL protocol implementation in the libmysqlclient library. It is faster, but requires the library in order to work.

There was [MySQLDb1](https://github.com/farcepest/MySQLdb1) version of wrapper used some time ago and now it is considered to be a legacy. As MySQLDb1 started evolving to [MySQLDb2](https://github.com/farcepest/moist) with bug fixes and Python3 support, a MySQLDb1 was forked and here is how [mysqlclient](https://github.com/PyMySQL/mysqlclient-python) appeared, with bugfixes and Python3 support. Sum up, so now we have MySQLDb2 which is not ready for production use(last update is in 25 Sep 2012, it's outdated and nobody maintain), MySQLDb1 as an outdated driver and a community supported [mysqlclient](https://github.com/PyMySQL/mysqlclient-python) with bug fixes and Python3 support.

Now, to solve that mess, MySQL provides their own version of MySQL adapter - [mysql connector](https://dev.mysql.com/doc/connector-python/en/connector-python-introduction.html), an all-in python module that uses MySQL API with no C modules dependencies and only standard python modules used.

So now the question comes down to: mysqlclient vs mysql connector.

As for me, I would go with officially supported library, however mysqlclient should be a good choice as well. Both of them are being actively updated with fixes and new features which you can see by active commits in last days.

#### Installation and Dependencies

##### mysqlclient

As a fork of C wrapper it requires C modules to work with MySQL which adds python header files to build these extensions. Installation depends on the system you use, just make sure you aware of package names and can install them.

##### mysql connector

Connector/Python implements the MySQL client/server protocol two ways:

- As pure Python. This implementation of the protocol does not require any other MySQL client libraries or other components.

- As a C Extension that interfaces with the MySQL C client library. This implementation of the protocol is dependent on the client library, but can use the library provided by either MySQL Connector/C or MySQL Server packages (see MySQL C API Implementations). The C Extension is available as of Connector/Python 2.1.1.

Neither implementation of the client/server protocol has any third-party dependencies. However, if you need SSL support, verify that your Python installation has been compiled using the OpenSSL libraries.

### mysqlclient

mysqlclient - By far the fastest MySQL connector for CPython. Requires the mysql-connector-c C library to work.

mysqlclient-python is much faster than PyMySQL. You can install mysqlclient using command `pip install mysqlclient`. But you should install the dependencies frist.

When to use PyMySQL is:

- You can't use libmysqlclient for some reason
- You want to use monkeypatched socket of gevent or eventlet
- You wan't to hack mysql protocol

### mysql-connector-python

mysql-connector-python, MySQL driver written in Python which does not depend on MySQL C client libraries and implements the DB API v2.0 specification (PEP-249).

### PyMySQL

This package contains a pure-Python MySQL client library, based on [PEP 249](https://www.python.org/dev/peps/pep-0249/).

Most public APIs are compatible with mysqlclient and MySQLdb.

NOTE: PyMySQL doesn’t support low level APIs \_mysql provides like *data_seek*, *store_result*, and *use_result*. You should use high level APIs defined in [PEP 249](https://www.python.org/dev/peps/pep-0249/). But some APIs like *autocommit* and *ping* are supported because [PEP 249](https://www.python.org/dev/peps/pep-0249/) doesn’t cover their usecase.

### 总结：

mysqlclient是C模块`libmysqlclient`的封装，目前仍在维护，网上通常认为性能要比纯Python实现的mysql-connector-python和PyMySQL性能要好。但是mysql-connector-python是Oracle维护的，并且也提供binary形式的安装包，支持 MySQL C 客户端库的封装（类似mysqlclient的模式）。

综上，建议使用官方mysql-connector-python包。

As of Connector/Python 2.1.1, binary distributions are available that include a C Extension that interfaces with the MySQL C client library. Some packaging types have a single distribution file that includes the pure-Python Connector/Python code together with the C Extension. (Windows MSI and macOS Disk Image packages fall into this category.) Other packaging types have two related distribution files: One that includes the pure-Python Connector/Python code, and one that includes only the C Extension. For packaging types that have separate distribution files, install either one or both packages. The two files have related names, the difference being that the one that contains the C Extension has “cext” in the distribution file name.

Binary distributions that provide the C Extension are either statically linked to MySQL Connector/C or link to an already installed C client library provided by a Connector/C or MySQL Server installation. For those distributions that are not statically linked, you must install Connector/C or MySQL Server if it is not already present on your system. 

#### Connector/Python C Extension

Installations of Connector/Python from version 2.1.1 on support a `use_pure` argument to `mysql.connector.connect()` that indicates whether to use the pure Python interface to MySQL or the C Extension that uses the MySQL C client library:

By default, `use_pure` (use the pure Python implementation) is False as of MySQL 8 and defaults to True in earlier versions. If the C extension is not available on the system then `use_pure` is True.

On Linux, the C and Python implementations are available as different packages. You can install one or both implementations on the same system. On Windows and macOS, the packages include both implementations.
【在Ubuntu中如果仅安装C Extension包，那么会出现无法导入mysql包的错误。因为Ubuntu的C Extension包仅仅包含二进制的C library文件，还需要安装纯python版的Connector，然后通过`use_pure`参数控制或直接使用`_mysql_connector`。】

For Connector/Python installations that include both implementations, it can optionally be toggled it by passing `use_pure=False` (to use C implementation) or `use_pure=True` (to use the Python implementation) as an argument to `mysql.connector.connect()`.

If you need to check whether your Connector/Python installation is aware of the C Extension, test the `HAVE_CEXT` value. There are different approaches for this. Suppose that your usual arguments for `mysql.connector.connect()` are specified in a dictionary:

```
config = {
  'user': 'scott',
  'password': 'password',
  'host': '127.0.0.1',
  'database': 'employees',
}
```

The following example illustrates one way to add use_pure to the connection arguments:

```
import mysql.connector

if mysql.connector.__version_info__ > (2, 1) and mysql.connector.HAVE_CEXT:
  config['use_pure'] = False
```

If `use_pure=False` and the C Extension is not available, then Connector/Python will automatically fall back to the pure Python implementation.

[What's the difference between MySQLdb, mysqlclient and MySQL connector/Python?](https://stackoverflow.com/questions/43102442/whats-the-difference-between-mysqldb-mysqlclient-and-mysql-connector-python)

[Python MySQLdb vs mysql-connector query performance](http://charlesnagy.info/it/python/python-mysqldb-vs-mysql-connector-query-performance)

[Welcome to PyMySQL’s documentation!](https://pymysql.readthedocs.io/en/latest/index.html)

[mysqlclient](https://github.com/PyMySQL/mysqlclient-python)

[Chapter 4 Connector/Python Installation](https://dev.mysql.com/doc/connector-python/en/connector-python-installation.html)

[4.2 Installing Connector/Python from a Binary Distribution](https://dev.mysql.com/doc/connector-python/en/connector-python-installation-binary.html)

[Chapter 8 The Connector/Python C Extension](https://dev.mysql.com/doc/connector-python/en/connector-python-cext.html)

[8.1 Application Development with the Connector/Python C Extension](https://dev.mysql.com/doc/connector-python/en/connector-python-cext-development.html)