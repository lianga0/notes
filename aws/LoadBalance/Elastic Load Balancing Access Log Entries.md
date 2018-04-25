### Access Logs for Your Classic Load Balancer

Elastic Load Balancing provides access logs that capture detailed information about requests sent to your load balancer. Each log contains information such as the time the request was received, the client's IP address, latencies, request paths, and server responses. You can use these access logs to analyze traffic patterns and to troubleshoot issues.

Access logging is an optional feature of Elastic Load Balancing that is disabled by default. After you enable access logging for your load balancer, Elastic Load Balancing captures the logs and stores them in the Amazon S3 bucket that you specify. You can disable access logging at any time.

There is no additional charge for access logs. You will be charged storage costs for Amazon S3, but will not be charged for the bandwidth used by Elastic Load Balancing to send log files to Amazon S3. 

#### Access Log Files

The load balancer can deliver multiple logs for the same period. This usually happens if the site has high traffic, multiple load balancer nodes, and a short log publishing interval.

The file names of the access logs use the following format:

```
bucket[/prefix]/AWSLogs/aws-account-id/elasticloadbalancing/region/yyyy/mm/dd/aws-account-id_elasticloadbalancing_region_load-balancer-name_end-time_ip-address_random-string.log
```

bucket

> The name of the S3 bucket.

prefix

> The prefix (logical hierarchy) in the bucket. If you don't specify a prefix, the logs are placed at the root level of the bucket.

aws-account-id

> The AWS account ID of the owner.

region

> The region for your load balancer and S3 bucket.

yyyy/mm/dd

> The date that the log was delivered.

load-balancer-name

> The name of the load balancer.

end-time

> The date and time that the logging interval ended. For example, an end time of 20140215T2340Z contains entries for requests made between 23:35 and 23:40 if the publishing interval is 5 minutes.

ip-address

> The IP address of the load balancer node that handled the request. For an internal load balancer, this is a private IP address.

random-string

> A system-generated random string.

The following is an example log file name:

```
s3://my-loadbalancer-logs/my-app/AWSLogs/123456789012/elasticloadbalancing/us-west-2/2014/02/15/123456789012_elasticloadbalancing_us-west-2_my-loadbalancer_20140215T2340Z_172.160.001.192_20sg8hgm.log
```

You can store your log files in your bucket for as long as you want, but you can also define Amazon S3 lifecycle rules to archive or delete log files automatically. 

#### Access Log Entries

Elastic Load Balancing logs requests sent to the load balancer, including requests that never made it to the back-end instances. For example, if a client sends a malformed request, or there are no healthy instances to respond, the requests are still logged.

**Important**

> Elastic Load Balancing logs requests on a best-effort basis. We recommend that you use access logs to understand the nature of the requests, not as a complete accounting of all requests.

##### Syntax

Each log entry contains the details of a single request made to the load balancer. All fields in the log entry are delimited by spaces. Each entry in the log file has the following format:

```
timestamp elb client:port backend:port request_processing_time backend_processing_time response_processing_time elb_status_code backend_status_code received_bytes sent_bytes "request" "user_agent" ssl_cipher ssl_protocol
```

The following table describes the fields of an access log entry.

<table id="w260aac21b9c13b7b9">
<tbody><tr>
 <th>Field</th>
 <th>Description</th>
</tr>
<tr>
<td>
    <p>timestamp</p>
</td>
<td>
    <p>The time when the load balancer received the request from the client, in ISO 8601
       format.
    </p>
</td>
</tr>
<tr>
 <td>
    <p>elb</p>
 </td>
 <td>
    <p>The name of the load balancer</p>
 </td>
</tr>
<tr>
 <td>
    <p>client:port</p>
 </td>
 <td>
    <p>The IP address and port of the requesting client.</p>
 </td>
</tr>
<tr>
 <td>
    <p>backend:port</p>
 </td>
 <td>
    <p>The IP address and port of the registered instance that processed this request.</p>
    <p>If the load balancer can't send the request to a registered instance, or if the instance
        closes the connection before a response can be sent, this value is set to <code class="code">-</code>.
    </p>
    <p>This value can also be set to <code class="code">-</code> if the registered instance does not respond 
        before the idle timeout.
    </p>
 </td>
</tr>
<tr>
 <td>
    <p>request_processing_time</p>
 </td>
 <td>
    <p>[HTTP listener] The total time elapsed, in seconds, from the time the load balancer
       received the request
        until the time it sent it to a registered instance.
    </p>
    <p>[TCP listener] The total time elapsed, in seconds, from the time the load balancer
       accepted a
        TCP/SSL connection from a client to the time the load balancer sends the first
       byte of data to
        a registered instance.
    </p>
    <p>This value is set to <code class="code">-1</code> if the load balancer can't dispatch the request
        to a registered instance. This can happen if the registered instance closes
       the connection 
        before the idle timeout or if the client sends a malformed request. Additionally,
       for TCP
        listeners, this can happen if the client establishes a connection with the
       load balancer
        but does not send any data.
    </p>
    <p>This value can also be set to <code class="code">-1</code> if the registered instance does not respond before the idle timeout.
    </p>
 </td>
</tr>
<tr>
 <td>
    <p>backend_processing_time</p>
 </td>
 <td>
    <p>[HTTP listener] The total time elapsed, in seconds, from the time the load balancer
        sent the request to a registered instance until the instance started to send
       the response headers.
    </p>
    <p>[TCP listener] The total time elapsed, in seconds, for the load balancer to successfully
       
        establish a connection to a registered instance.
    </p>
    <p>This value is set to <code class="code">-1</code> if the load balancer can't dispatch the request
        to a registered instance. This can happen if the registered instance closes
       the connection 
        before the idle timeout or if the client sends a malformed request.
    </p>
    <p>This value can also be set to <code class="code">-1</code> if the registered instance does not respond before the idle timeout.
    </p>
 </td>
</tr>
<tr>
 <td>
    <p>response_processing_time</p>
 </td>
 <td>
    <p>[HTTP listener] The total time elapsed (in seconds) from the time the load balancer
       received the
        response header from the registered instance until it started to send the response
       to the client. 
        This includes both the queuing time at the load balancer and the connection
       acquisition time from 
        the load balancer to the client.
    </p>
    <p>[TCP listener] The total time elapsed, in seconds, from the time the load balancer
       received the
        first byte from the registered instance until it started to send the response
       to the client.
    </p>
    <p>This value is set to <code class="code">-1</code> if the load balancer can't dispatch the request
        to a registered instance. This can happen if the registered instance closes
       the connection 
        before the idle timeout or if the client sends a malformed request.
    </p>
    <p>This value can also be set to <code class="code">-1</code> if the registered instance does not respond before the idle timeout.
    </p>
 </td>
</tr>
<tr>
 <td>
    <p>elb_status_code</p>
 </td>
 <td>
    <p>[HTTP listener] The status code of the response from the load balancer.</p>
 </td>
</tr>
<tr>
 <td>
    <p>backend_status_code</p>
 </td>
 <td>
    <p>[HTTP listener] The status code of the response from the registered instance.</p>
 </td>
</tr>
<tr>
 <td>
    <p>received_bytes</p>
 </td>
 <td>
    <p>The size of the request, in bytes, received from the client (requester).</p> 
    <p>[HTTP listener] The value includes the request body but not the headers.</p>
    <p>[TCP listener] The value includes the request body and the headers.</p>
 </td>
</tr>
<tr>
 <td>
    <p>sent_bytes</p>
 </td>
 <td>
    <p>The size of the response, in bytes, sent to the client (requester).</p> 
    <p>[HTTP listener] The value includes the response body but not the headers.</p>
    <p>[TCP listener] The value includes the request body and the headers.</p>
 </td>
</tr>
<tr>
 <td>
    <p>request</p>
 </td>
 <td>
    <p>The request line from the client enclosed in double quotes and logged in the following
        format: HTTP Method + Protocol://Host header:port + Path + HTTP version.
    </p>
    <p>[TCP listener] The URL is three dashes, each separated by a space, and ending with
       a space ("- - - ").
    </p>
 </td>
</tr>
<tr>
 <td>
    <p>user_agent</p>
 </td>
 <td>
    <p>[HTTP/HTTPS listener] A User-Agent string that identifies the client that originated
       the request. 
        The string consists of one or more product identifiers, product[/version].
       If the string is longer
        than 8 KB, it is truncated.
    </p>
 </td>
</tr>
<tr>
 <td>
    <p>ssl_cipher</p>
 </td>
 <td>
    <p>[HTTPS/SSL listener] The SSL cipher. This value is recorded only if the incoming SSL/TLS
       connection
        was established after a successful negotiation. Otherwise, the value is set
       to <code class="code">-</code>.
    </p>
 </td>
</tr>
<tr>
 <td>
    <p>ssl_protocol</p>
 </td>
 <td>
    <p>[HTTPS/SSL listener] The SSL protocol. This value is recorded only if the incoming
       SSL/TLS connection
        was established after a successful negotiation. Otherwise, the value is set
       to <code class="code">-</code>.
    </p>
 </td>
</tr>
</tbody></table>


##### Example HTTP Entry

The following is an example log entry for an HTTP listener (port 80 to port 80):

```
2015-05-13T23:39:43.945958Z my-loadbalancer 192.168.131.39:2817 10.0.0.1:80 0.000073 0.001048 0.000057 200 200 0 29 "GET http://www.example.com:80/ HTTP/1.1" "curl/7.38.0" - -
```

##### Example HTTPS Entry

The following is an example log entry for an HTTPS listener (port 443 to port 80):

```
2015-05-13T23:39:43.945958Z my-loadbalancer 192.168.131.39:2817 10.0.0.1:80 0.000086 0.001048 0.001337 200 200 0 57 "GET https://www.example.com:443/ HTTP/1.1" "curl/7.38.0" DHE-RSA-AES128-SHA TLSv1.2
```

#### 下载S3日志目录到本地命令

支持本地或S3目录的同步

```
aws s3 sync 源目录路径 目的目录路径
```

例如，将4月23号的ELB log同步到当前目录如下：

```
aws s3 sync s3://drs-ti-kinesis-firehose-beta-s3/beanstalk-beta-lb/AWSLogs/944809154377/elasticloadbalancing/ap-northeast-1/2018/04/23 .
```

#### 将日期目录多个文本文件合并为一个文件

```
ls | xargs cat > ../elb_22.txt
```

#### goaccess 解析ELB Log的格式化字符串

```
goaccess -f elb_log.txt -o report.html --date-format %Y-%m-%d  --time-format %H:%M:%S --log-format "%dT%t.%^ %^ %h:%^ %^ %T %^ %^ %^ %s %^ %b \"%r\" \"%u\"" > abc.html
```
or

```
goaccess -f elb_log.txt -o report.html --no-global-config --date-format %Y-%m-%d  --time-format  %H:%M:%S  --log-format "%dT%t.%^ %^ %h:%^ %^ %^ %T %^ %s %^ %b %^ \"%r\" \"%^\" %^ %^" > 5.html
```


From: [Access Logs for Your Classic Load Balancer](https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/access-log-collection.html)