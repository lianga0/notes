# Postgres JSON object operation

## [Postgres query to return JSON object keys as array](https://dba.stackexchange.com/questions/127228/postgres-query-to-return-json-object-keys-as-array)

Is it possible to return a JSON object keys as an array of values in PostgreSQL?

```
CREATE TABLE test (
    id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    data jsonb NOT NULL
);
```

Sure, with `json_object_keys()`. This returns a set. Feed the set to an `ARRAY constructor` to transform it:

```
select id, jsonb_object_keys(data) from test;
SELECT id, ARRAY(SELECT jsonb_object_keys(data)) AS keys FROM test;
```

Or use `jsonb_object_keys()` for `jsonb`.

**This returns an array of keys per row (not for the whole table).**

A more verbose form would be to spell out a `LATERAL` join instead of the correlated subquery:

```
SELECT t.id, k.keys
FROM   test t
LEFT JOIN LATERAL (SELECT ARRAY(SELECT * FROM jsonb_object_keys(t.data)) AS keys) k ON true;
```

