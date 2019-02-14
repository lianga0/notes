## "General Network error", "Communication link failure", or "A transport-level error" message when an application connects to SQL Server

> From : https://support.microsoft.com/en-us/help/942861/general-network-error-communication-link-failure-or-a-transport-level

### Scalable Network Pack(SNP)

The SNP is a set of high-speed networking features that were introduced as part of Windows Server 2003 Service Pack 2 (SP2). These features also were included as part of Windows Server 2008 and later versions.

Note Because these features are part of the base TCP/IP stack in Windows Server 2008 and later versions, they are no longer known as Scalable Networking Pack features.

The important SNP features relevant to this article are as follows:

- TCP Chimney Offload: This feature transfers TCP/IP protocol processing from the CPU to a network adapter during network data transfer.

- Receive Side Scaling: This feature enables the network load from a network adapter to be distributed across multiple CPUs in a multiprocessor computer.

- NetDMA: This feature provides services for offloading the memory copy operation that is performed by the networking subsystem to a dedicated direct memory access (DMA) engine when receiving network packets.

#### Error messages when an application connects to SQL Server

You may receive one or more of the following error messages when your network hardware is incompatible with SNP features.

Note You may receive one or more of these error messages when one of the following conditions is true:

- The computer on which the hardware is installed hosts the instance of SQL Server.

- An application connects to the instance of SQL Server by using TCP/IP.

Error message 1

```
[Microsoft][ODBC SQL Server Driver][DBNETLIB] General Network error. Check your network documentation
```

Error message 2

```
ERROR [08S01] [Microsoft][SQL Native Client]Communication link failure
```

Error message 3

```
System.Data.SqlClient.SqlException: A transport-level error has occurred when sending the request to the server. (provider: TCP Provider, error: 0 - An existing connection was forcibly closed by the remote host.)
```

**You may also receive one of these error messages when the network load on SQL Server is high.** For example, you may receive one of these error messages when you replicate databases in SQL Server. Or, you may receive one of these error messages when a multiple-user application accesses databases in SQL Server.

Python2.x中的pyodbc库抛出的错误信息（SQL Server服务器负载过高的情况）如下：

```
'[01000] [Microsoft][ODBC SQL Server Driver][DBNETLIB]ConnectionRead (recv()). (65534) (SQLExecDirectW); [08S01] [Microsoft][ODBC SQL Server Driver][DBNETLIB]General network error. Check your network documentation. (11)'
```

#### Verify the current configuration

To display the current TCP global parameters, at a command prompt, type the following command, and then press Enter:

```
Netsh int tcp show global
```

The output of this command resembles the following:

```
TCP Global Parameters
----------------------------------------------
Receive-Side Scaling State          : enabled
Chimney Offload State               : disabled
NetDMA State                        : disabled
Direct Cache Access (DCA)           : disabled
Receive Window Auto-Tuning Level    : normal
Add-On Congestion Control Provider  : default
ECN Capability                      : enabled
RFC 1323 Timestamps                 : disabled
Initial RTO                         : 3000
Receive Segment Coalescing State    : enabled
Non Sack Rtt Resiliency             : disabled
Max SYN Retransmissions             : 2
TCP Fast Open                       : disabled
```

To display the network adapters that have the TCP Chimney Offload feature enabled, at a command prompt, type the following command, and then press Enter:

```
Netsh int tcp show chimneystats
```

The output of this command resembles the following:

```
Your System Administrator has disabled TCP Chimney.
```

### TCP Chimney Offload

> 09/12/2018 Windows Server 2016

TCP Chimney Offload, also known as TCP Engine Offload (TOE), is a technology that allows the host to offload all TCP processing to the NIC. Because the Windows Server TCP stack is almost always more efficient than the TOE engine, using TCP Chimney Offload is not recommended.

> Important

TCP Chimney Offload is a deprecated technology. We recommend you do not use TCP Chimney Offload as Microsoft might stop supporting it in the future.

From: [Software and hardware (SH) integrated features and technologies](https://docs.microsoft.com/en-us/windows-server/networking/technologies/hpn/hpn-software-hardware-features)

Reference: [Networking Deployment Guide: Deploying High-speed Networking Features](https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2008-R2-and-2008/gg162681(v=ws.10))

["General Network error", "Communication link failure", or "A transport-level error" message when an application connects to SQL Server](https://support.microsoft.com/en-us/help/942861/general-network-error-communication-link-failure-or-a-transport-level)

[High-performance networking (HPN)](https://docs.microsoft.com/en-us/windows-server/networking/technologies/hpn/hpn-top)