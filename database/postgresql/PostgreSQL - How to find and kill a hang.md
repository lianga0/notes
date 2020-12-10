## PostgreSQL - How to find and kill a hanging query?

> https://tableplus.com/blog/2018/08/postgresql-how-to-find-and-kill-hanging-query.html

First, check all the processes that are running:

```
SELECT * FROM pg_stat_activity WHERE state = 'active';
```

So you can identify the PID of the hanging query you want to terminate, run this:

```
SELECT pg_cancel_backend(PID);
```

This query might take a while to kill the query, so if you want to kill it the hard way, run this instead:

```
SELECT pg_terminate_backend(PID);
```

