## Iterate a Cursor in the mongo Shell 在查询结果集上迭代或分页（性能）

> https://docs.mongodb.com/manual/tutorial/iterate-a-cursor/

### `db.collection.find()`会自动返回一个游标

The `db.collection.find()` method returns a cursor. To access the documents, you need to iterate the cursor. **However, in the mongo shell, if the returned cursor is not assigned to a variable using the var keyword, then the cursor is automatically iterated up to 20 times to print up to the first 20 documents in the results.**

### Manually Iterate the Cursor

In the mongo shell, when you assign the cursor returned from the find() method to a variable using the var keyword, the cursor does not automatically iterate.

You can call the cursor variable in the shell to iterate up to 20 times and print the matching documents, as in the following example:

```
var myCursor = db.users.find( { type: 2 } );

myCursor
```

You can also use the cursor method next() to access the documents, as in the following example:

```
var myCursor = db.users.find( { type: 2 } );

while (myCursor.hasNext()) {
   print(tojson(myCursor.next()));
}
```

You can use the cursor method forEach() to iterate the cursor and access the documents, as in the following example:

```
var myCursor =  db.users.find( { type: 2 } );

myCursor.forEach(printjson);
```

### Iterator Index 会先加载所有数据，如果查询结果集比较大，那很可能需要加载非常长时间，最后OOM

In the mongo shell, you can use the `toArray()` method to iterate the cursor and return the documents in an array, as in the following:

```
var myCursor = db.inventory.find( { type: 2 } );
var documentArray = myCursor.toArray();
var myDocument = documentArray[3];
```

The `toArray()` method loads into RAM all documents returned by the cursor; **the `toArray()` method exhausts the cursor**.

Additionally, some drivers provide access to the documents by using an index on the cursor (i.e. `cursor[index]`). This is a shortcut for first calling the `toArray()` method and then using an index on the resulting array.

Consider the following example:

```
var myCursor = db.users.find( { type: 2 } );
var myDocument = myCursor[1];
```

The `myCursor[1]` is equivalent to the following example:

```
myCursor.toArray() [1];
```

所以，如果想分页，或者直接跳过某些记录，可以使用`cursor.skip()`方法。这样可以避免传输不需要的数据，从而提高性能。但`cursor.skip()`方法仍然需要MongoDB从头开始扫描需要返回的结果集，当offset值较大时，需要的时间较长。当offset值较大时，使用在带有唯一索引的field上的条件查询（Range Queries），会比使用`cursor.skip()`更快。

### cursor.skip(<offset>)

Call the `cursor.skip()` method on a cursor to control where MongoDB begins returning results. This approach may be useful in implementing paginated results.

> You must apply `cursor.skip()` to the cursor before retrieving any documents from the database.

如果，你希望使用cursor.skip，那么必须在获取任何数据之前，调用 `cursor.skip()`。

The following JavaScript function uses `cursor.skip()` to paginate a collection in natural order:

```
function printStudents(pageNumber, nPerPage) {
  print( "Page: " + pageNumber );
  db.students.find()
             .skip( pageNumber > 0 ? ( ( pageNumber - 1 ) * nPerPage ) : 0 )
             .limit( nPerPage )
             .forEach( student => {
               print( student.name );
             } );
}
```

**The `cursor.skip()` method requires the server to scan from the beginning of the input results set before beginning to return results. As the offset increases, `cursor.skip()` will become slower.**

### Using Range Queries

Range queries can use **indexes** to avoid scanning unwanted documents, typically yielding better performance as the offset grows compared to using `cursor.skip()` for pagination.

#### Descending Order

Use this procedure to implement pagination with range queries:

- Choose a field such as `_id` which generally changes in a consistent direction over time and has a **unique index** to prevent duplicate values,
- Query for documents whose field is less than the start value using the `$lt` and `cursor.sort()` operators, and
- Store the last-seen field value for the next query.

For example, the following function uses the above procedure to print pages of student names from a collection, sorted approximately in order of newest documents first using the `_id` field (that is, in descending order):

```
function printStudents(startValue, nPerPage) {
  let endValue = null;
  db.students.find( { _id: { $lt: startValue } } )
             .sort( { _id: -1 } )
             .limit( nPerPage )
             .forEach( student => {
               print( student.name );
               endValue = student._id;
             } );

  return endValue;
}
```

You may then use the following code to print all student names using this pagination function, using `MaxKey` to start from the largest possible key:

```
let currentKey = MaxKey;
while (currentKey !== null) {
  currentKey = printStudents(currentKey, 10);
}
```

> NOTE

**While ObjectId values should increase over time, they are not necessarily monotonic. This is because they:**

- Only contain one second of temporal resolution, so ObjectId values created within the same second do not have a guaranteed ordering, and
- Are generated by clients, which may have differing system clocks.


### Cursor Behaviors

#### Closure of Inactive Cursors

By default, the server will automatically close the cursor after 10 minutes of inactivity, or if client has exhausted the cursor. To override this behavior in the mongo shell, you can use the cursor.noCursorTimeout() method:

```
var myCursor = db.users.find().noCursorTimeout();
```

After setting the `noCursorTimeout option`, you must either close the cursor manually with `cursor.close()`` or by exhausting the cursor’s results.

#### Cursor Isolation

As a cursor returns documents, other operations may interleave with the query. For the MMAPv1 storage engine, intervening write operations on a document may result in a cursor that returns a document more than once if that document has changed. 

#### Cursor Batches

The MongoDB server returns the query results in batches. The amount of data in the batch will not exceed the maximum BSON document size( 16 megabytes.). To override the default size of the batch, see `batchSize()` and `limit()`.

`find()` and `aggregate()` operations have an initial batch size of 101 documents by default. Subsequent `getMore` operations issued against the resulting cursor have no default batch size, so they are limited only by the 16 megabyte message size.

**For queries that include a sort operation without an index, the server must load all the documents in memory to perform the sort before returning any results.**

As you iterate through the cursor and reach the end of the returned batch, if there are more results, `cursor.next()` will perform a getMore operation to retrieve the next batch. To see how many documents remain in the batch as you iterate the cursor, you can use the `objsLeftInBatch()` method, as in the following example:

```
var myCursor = db.inventory.find();

var myFirstDocument = myCursor.hasNext() ? myCursor.next() : null;

myCursor.objsLeftInBatch();
```

#### Cursor Information

The `db.serverStatus()` method returns a document that includes a metrics field. The metrics field contains a metrics.cursor field with the following information:

- number of timed out cursors since the last server restart
- number of open cursors with the option DBQuery.Option.noTimeout set to prevent timeout after a period of inactivity
- number of “pinned” open cursors
- total number of open cursors

Consider the following example which calls the `db.serverStatus()` method and accesses the metrics field from the results and then the cursor field from the metrics field:

```
db.serverStatus().metrics.cursor
```


Reference: https://docs.mongodb.com/manual/tutorial/iterate-a-cursor/

https://docs.mongodb.com/manual/reference/method/cursor.skip/