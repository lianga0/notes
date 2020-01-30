## 时间格式 yyyy-MM-dd'T'HH:mm:ss.SSSZ 中的T和Z表示什么

> From: [残花织梦 最后发布于2019-06-17 17:10:13 ](https://blog.csdn.net/qq_39141723/article/details/92655240)

下面来着重认识一下yyyy-MM-dd'T'HH:mm:ss.SSSZ 中的T和Z所表示的含义:

### Date Time String Format

ECMAScript defines a string interchange format for date-times based upon a simplification of the ISO 8601 Extended Format. The format is as follows: `YYYY-MM-DDTHH:mm:ss.sssZ`

Where the fields are as follows:

<table cellspacing="0"> 
  <tbody>
    <tr>
     <td><code>YYYY</code></td> 
     <td>is the decimal digits of the year 0000 to 9999 in the Gregorian calendar.</td> 
    </tr>
    <tr>
     <td><code>-</code></td> 
     <td><code>&quot;-&quot;</code>&nbsp;(hyphen) appears literally twice in the string.</td> 
    </tr>
    <tr>
     <td><code>MM</code></td> 
     <td>is the month of the year from 01 (January) to 12 (December).</td> 
    </tr>
    <tr>
     <td><code>DD</code></td> 
     <td>is the day of the month from 01 to 31.</td> 
    </tr>
    <tr>
     <td><span><code>T</code></span></td> 
     <td><span><code>&quot;T&quot;</code>&nbsp;appears literally in the string, to indicate the beginning of the time element.</span></td> 
    </tr>
    <tr>
     <td><code>HH</code></td> 
     <td>is the number of complete hours that have passed since midnight as two decimal digits from 00 to 24.</td> 
    </tr>
    <tr>
     <td><code>:</code></td> 
     <td><code>&quot;:&quot;</code>&nbsp;(colon) appears literally twice in the string.</td> 
    </tr>
    <tr>
     <td><code>mm</code></td> 
     <td>is the number of complete minutes since the start of the hour as two decimal digits from 00 to 59.</td> 
    </tr>
    <tr>
     <td><code>ss</code></td> 
     <td>is the number of complete seconds since the start of the minute as two decimal digits from 00 to 59.</td> 
    </tr>
    <tr>
     <td><code>.</code></td> 
     <td><code>&quot;.&quot;</code>&nbsp;(dot) appears literally in the string.</td> 
    </tr>
    <tr>
     <td><code>sss</code></td> 
     <td>is the number of complete milliseconds since the start of the second as three decimal digits.</td> 
    </tr>
    <tr>
     <td><span><code>Z</code></span></td> 
     <td><span>is the time zone offset specified as&nbsp;<code>&quot;Z&quot;</code>&nbsp;(for UTC) or either&nbsp;<code>&quot;+&quot;</code>&nbsp;or&nbsp;<code>&quot;-&quot;</code>&nbsp;followed by a time expression&nbsp;<code>HH:mm</code></span></td> 
    </tr> 
  </tbody>
</table>

因为北京处于东八区.我们北京时间UTC+8 , 所以Updated Date:2017-10-20T02:59:25Z  转换成北京时间就是 2017-10-20 10:59:25

Creation Date:2015-08-03T07:21:33Z 转换成北京时间就是 2015-08-03 15:21:33

参考网址: http://www.ecma-international.org/ecma-262/6.0/#sec-date-time-string-format 