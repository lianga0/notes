### What Happens if I Drop a Clustered Index?

> by Kimberly L.  2010 Apr 22

Q: I’ve heard that the clustered index is “the data,” but I don’t fully understand what that means. If I drop a clustered index, will I lose the data?

A: I get asked this question a lot, and I find that index structures tend to confuse people; indexes seem mysterious and, as a result, are unintentionally thought of as very complicated. A table can be stored internally with or without a clustered index. **If a table doesn’t have a clustered index, it’s called a heap.** If the table has a clustered index, it’s often referred to as a clustered table. When a clustered index is created, SQL Server will temporarily duplicate and sort the data from the heap into the clustered index key order (because the key defines the ordering of the data) and remove the original pages associated with the heap. From this point forward, SQL Server will maintain order logically through a doubly-linked list and a B+ tree that’s used to navigate to specific points within the data.

In addition, a clustered index helps you quickly navigate to the data when queries make use of nonclustered indexes—the other main type of index that SQL Server allows. A nonclustered index provides a way to efficiently look up data in the table using a different key from the clustered index key. For example, if you create a clustered index on EmployeeID in the Employee table, then the EmployeeID will be duplicated in each nonclustered index record and used for navigation from the nonclustered indexes to retrieve columns from the clustered index data row. (This process is often known as a bookmark lookup or a Key Lookup.)

However, all of these things change if you drop the clustered index on a table. The data isn’t removed, just the maintenance of order (i.e., the index/navigational component of the clustered index). However, nonclustered indexes use the clustering key to look up the corresponding row of data, so when a clustered index is dropped, the nonclustered indexes must be modified to use another method to lookup the corresponding data row because the clustering key no longer exists.

The only way to jump directly to a record in the table without a clustered index is to use its physical location in the database (i.e., a particular record number on a particular data page in a particular data file, known as a row identifier—RID), and this physical location must be included in the nonclustered indexes now that the table is no longer clustered. So when a clustered index is dropped, all the nonclustered indexes must be rebuilt to use RIDs to look up the corresponding row within the heap.

Rebuilding all the nonclustered indexes on a table can be very expensive. And, if the clustered index is also enforcing a relational key (primary or unique), it might also have foreign key references. Before you can drop a primary key, you need to first remove all the referencing foreign keys. So although dropping a clustered index doesn’t remove data, you still need to think very carefully before dropping it.

I have a huge queue of index-related questions, so I’m sure indexing best practices will be a topic frequently covered in this column. I’ll tackle another indexing question next to keep you on the right track.

Reference：[What Happens if I Drop a Clustered Index?](http://sqlmag.com/blog/what-happens-if-i-drop-clustered-index)