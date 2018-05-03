## WINS(Windows Internet Name Service)

Windows Internet Name Service (WINS) is the Microsoft implementation of NetBIOS Name Server (NBNS), a name server for NetBIOS names.
NBNS supports resolution of NetBIOS names to IPv4 addresses. The NBNS database is distributed. Networks normally have more than one NBNS server to help improve availability and scalability of NetBIOS name service. The mappings registered by the clients on one server are replicated across all NBNS servers for consistent NetBIOS name resolution.


WINS是Windows Internet Name Service，即Windows网络名称服务。它提供一个分布式数据库，能在路由网络的环境中动态地对IP地址和NETBios名的映射进行注册与查询。 WINS用来登记NetBIOS计算机名，并在需要时将它解析成为IP地址。WINS数据库是动态更新的。

### WINS服务器与DNS服务器有什么区别？

1. WINS实现的是IP地址和计算机名称的映射，DNS实现的是IP地址和域名的映射。
2. WINS作用的范围是某个内部网络，DNS的范围是整个互联网。WINS集中管理计算机名称和IP地址。通常这些计算机名称都是在某个单位内部有效。比如在一个局域网内你可以通过使用计算机名就访问另一台计算机，它有一个查询IP地址的过程，就是通过WINS服务来实现的。


[WINS服务器与DNS服务器有什么区别？](https://zhidao.baidu.com/question/253276076.html)