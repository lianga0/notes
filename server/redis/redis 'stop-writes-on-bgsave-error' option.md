### Redis "stop-writes-on-bgsave-error" option

当配置Redis保存数据库快照到硬盘选项时，不管是因为硬盘满还是内存不足等任何因素，导致快照写入硬盘失败后，Redis默认会进入只读模式，此时所有的写操作都会被拒绝。Redis会向用户报告写操作错误信息。

可以通过修改`stop-writes-on-bgsave-error`配置项，来改变Redis的行为。当值设置为no时，即使保存快照出错，Redis也会允许用户继续做更新操作。此配置项的值默认为yes。

当`stop-writes-on-bgsave-error`配置项为yes时，Python的redis-py库表现如下：

```
[pid: 15696] - 25/11/2017 19:16:45.000380 [WARNING]

MISCONF Redis is configured to save RDB snapshots, but it is currently not able to persist on disk. Commands that may modify the data set are disabled, because this instance is configured to report errors during writes if RDB snapshotting fails (stop-writes-on-bgsave-error option). Please check the Redis logs for details about the RDB error. --- logmanager.py(339)

details Traceback (most recent call last):
  File "./api/impl/logmanager.py", line 272, in api_parser_multi_protocol
    parse_code, parse_result = logworker.parse_incrementally(protocol.upper(), user_info, request_json)
  File "./api/impl/logmanager.py", line 501, in parse_incrementally
    return self._iparser.parse_incrementally_log(protocol, session_info, log_content)
  File "./api/impl/parser.py", line 474, in parse_incrementally_log
    result_s = self.merger.merge(req_info_t, device_info_t, protocol, result)
  File "./api/impl/merge_cache.py", line 389, in merge
    lock_id = self.acquire_lock(dev_lock)
  File "./api/impl/merge_cache.py", line 264, in acquire_lock
    if self._redis_conn.set(lock_name, lock_id, ex=lock_timeout, nx=True):
  File "/usr/local/lib/python2.7/dist-packages/redis/client.py", line 1072, in set
    return self.execute_command('SET', *pieces)
  File "/usr/local/lib/python2.7/dist-packages/redis/client.py", line 573, in execute_command
    return self.parse_response(connection, command_name, **options)
  File "/usr/local/lib/python2.7/dist-packages/redis/client.py", line 585, in parse_response
    response = connection.read_response()
  File "/usr/local/lib/python2.7/dist-packages/redis/connection.py", line 582, in read_response
    raise response
ResponseError: MISCONF Redis is configured to save RDB snapshots, but it is currently not able to persist on disk. Commands that may modify the data set are disabled, because this instance is configured to report errors during writes if RDB snapshotting fails (stop-writes-on-bgsave-error option). Please check the Redis logs for details about the RDB error.
 --- logmanager.py(341)
```

下面是Redis自身运行的错误日志信息。可以看出是因为Redis进程申请内存失败，导致redis写硬盘快照时出错。

```
1371:M 17 Sep 06:06:30.039 * 10000 changes in 60 seconds. Saving...
1371:M 17 Sep 06:06:30.088 * Background saving started by pid 5186
5186:C 17 Sep 06:12:04.044 * DB saved on disk
5186:C 17 Sep 06:12:04.719 * RDB: 47 MB of memory used by copy-on-write
1371:M 17 Sep 06:12:04.842 * Background saving terminated with success
1371:M 17 Sep 06:13:05.089 * 10000 changes in 60 seconds. Saving...
1371:M 17 Sep 06:13:05.110 # Can't save in background: fork: Cannot allocate memory
1371:M 17 Sep 06:13:11.052 * 10000 changes in 60 seconds. Saving...
1371:M 17 Sep 06:13:11.052 # Can't save in background: fork: Cannot allocate memory
```

《完》