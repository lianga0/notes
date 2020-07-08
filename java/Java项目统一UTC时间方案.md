## Java项目统一UTC时间方案

> From: https://www.cnblogs.com/gods/p/4288926.html

### 引言

近期团队的个别项目在进行框架升级后，部分时间值存在8小时误差，原因是错误的将数据库中的时间数据理解成了UTC时间（旧版本认为是北京时间）

考虑到未来项目对于时间理解的一致性，决定将项目统一为使用UTC时间。

### mysql数据库时区及时间时间类型说明

#### 数据库时区

mysql数据库拥有时区设置，默认使用系统时区

可通过如下语句查询当前时区

```
show variables like '%time_zone%';
```

#### 时间类型说明

##### datetime

实际格式储存（Just stores what you have stored and retrieves the same thing which you have stored.）

与时区无关（It has nothing to deal with the TIMEZONE and Conversion.）

##### timestamp

值以UTC毫秒数保存（ it stores the number of milliseconds）

存储及检索时根据当前时区设置，对时间数值做转换


由于timestamp与时区相关，且线上数据库时区设置为北京时间（即UTC+8:00）。因此，当数据库中使用了timestamp列，若使用不当，统一UTC格式时间改造将很可能会引入错误！

### Java 设置默认时区为UTC

第一行代码也可设置，二选一

```
System.setProperty("user.timezone", "UTC");
TimeZone.setDefault(TimeZone.getTimeZone("Asia/Tokyo"));
System.out.println("TimeZone : " + TimeZone.getDefault().getID());
//System.setProperty("user.timezone","Asia/Tokyo");

```

# Reference

## How can I get the current date and time in UTC or GMT in Java?

> https://stackoverflow.com/questions/308683/how-can-i-get-the-current-date-and-time-in-utc-or-gmt-in-java

Question: When I create a new Date object, it is initialized to the current time but in the local timezone. How can I get the current date and time in GMT?

Answer:
`java.util.Date` has no specific time zone, although its value is most commonly thought of in relation to UTC. What makes you think it's in local time?

To be precise: the value within a `java.util.Date` is the number of milliseconds since the Unix epoch, which occurred at midnight January 1st 1970, UTC. The same epoch could also be described in other time zones, but the traditional description is in terms of UTC. As it's a number of milliseconds since a fixed epoch, the value within `java.util.Date` is the same around the world at any particular instant, regardless of local time zone.

I suspect the problem is that you're displaying it via an instance of Calendar which uses the local timezone, or possibly using `Date.toString()` which also uses the local timezone, or a SimpleDateFormat instance, which, by default, also uses local timezone.

其他参照：

[Java处理GMT时间和UTC时间](https://blog.csdn.net/FX_SKY/article/details/50462922)