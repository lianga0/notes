### Managing Transaction Logs

> By Gail Shaw, 2012/01/03 (first published: 2008/10/31)

##### Introduction

The transaction log and how SQL uses it seems to be one of the most misunderstood topics among newcomers to the DBA role. I’m going to see if I can shed a little light on what the transaction log is, why SQL uses it, how to manage it and what not to do to it.

##### What is the Transaction Log?

At its simplest, the transaction log is a record of all transactions run against a database and all database modifications made by those transactions. The transaction log is a critical part of the database’s architecture.

The transaction log is not an audit log. It’s not there so that the DBA can see who did what to the database. It’s also not a data recovery tool.  There are third-party tools that can get audit or data-recovery info from the log, but that is not its primary purpose.

The transaction log is predominantly used by the SQL engine to ensure database integrity, to allow transaction rollbacks and for database recovery. 

##### How does SQL use the log?

When changes are made to a database, whether it be in an explicit transaction or an auto-committed transaction, those changes are first written (hardened) to the log file and the data pages are changed in memory. Once the record of the changes is in the log, the transaction is considered complete. The data pages will be written to the data file on disk at a later time either by the lazy writer or by the checkpoint process.

If transactions are rolled back, either by an explicit ROLLBACK TRANSACTION, by an error if XACT_ABORT is on, or due to a loss of connection to the client, the transaction log is used to undo the modifications made by that transaction and leave the database as though the transaction had never occurred. In a similar way, the log is used to undo the effects of single statements that fail, whether in an explicit transaction or not.

When a server is restarted, SQL uses the transaction log to see if, at the point the server shut down there were any transactions that had completed but whose changes may not have been written to disk, or any transactions that had not completed. If there are, then the modifications that may not have been written to disk are replayed (rolled forward) and any that had not completed are rolled back. This is done to ensure that the database is in a consistent state after a restart and that any transactions that had committed remain a part of the permanent database state (the Durability requirement of ACID)

Lastly, backups made of the transaction log can be used to recover a database to a point-in-time in case of a failure.

The transaction log is also used to support replication, database mirroring and change data capture. I won’t be going into how they affect the log here. 

##### Recovery models and the Transaction Log

The database recovery model does not (with the exception of bulk operations) affect what is written to the transaction log. Rather it affects how long log entries remain in the log. This is just a very basic look at the recovery models. For more detail, see my article “Recovery Models".

###### Simple Recovery Model

In the simple recovery model, the transaction log entries are kept only to allow for transaction rollbacks and crash recovery, not for the purpose of restoring a database. Once the data pages have been written to disk and the transaction is complete; then, in the absence of replication or other things that need the log, the log records are considered inactive and can be marked as reusable. This marking of portions of the log as reusable is done by the checkpoint process.

This is the simplest recovery mode in terms of log management as the log manages itself. The downside of simple recovery is that (because transaction log backups cannot be made) a restore of the database can only be done to the time of the latest full or differential database backup. With a busy database, this can result in unacceptable data loss.

###### Full Recovery model

In full recovery model transaction log entries cannot be overwritten until they have been backed up by a transaction log backup. Simply having the transaction committed and data pages written to disk is not enough

Full recovery can be more difficult to manage as the log can grow beyond what is expected if transaction log backups don’t occur, or if there’s an increase in the amount of database activity that occurs between log backups.

Without any log backups running (an all-too common occurrence seeing that new databases will default to full recovery model unless the recovery model of the Model database has been changed), the transaction log will grow until it reaches its configured maximum file size (2TB unless otherwise specified) or until it fills the disk. No amount of full or differential backups will allow the log space to be reused as neither marks log space as reusable.

What can be even worse is that a database in full recovery model does not behave like this from the moment created. When created, a database in full recovery model will behave in a manner sometimes called pseudo-simple recovery model. This occurs because no database backup has yet been taken, and a database backup is needed to start a log chain. While in pseudo-simple recovery, the database behaves as though it really is in simple recovery model, truncating the log (marking space as reusable) every time a checkpoint occurs. This state remains until the first full backup is taken of the database. That full backup starts the log chain and from that point on the log will no longer be marked reusable by the checkpoint process and, if there are no log backups, the log will begin to grow.

Because log records are not overwritten until they have been backed up, a database in full recovery mode can be recovered to any time using a combination of full, differential and log backups, assuming a starting full backup exists and none of the log backups since have been deleted.

###### Bulk-logged recovery model

Bulk-logged is very similar to full recovery, except that in bulk-logged, bulk operations are minimally logged.  When operations are minimally logged, much less information is written to the transaction log compared to when the operation is fully logged.

The advantage of bulk-logged recovery is that if there are bulk operations occurring, the impact those operations have on the transaction log is less than it would be if the database was in full recovery mode. However the transaction log backups may be much larger than the transaction log itself since the log backups include all data pages modified by bulk operations since the previous log backup.

I'm not going to discuss bulk-logged recovery model further than this in the current article. For the purposes of log management, bulk-logged recovery model can be treated much like full recovery.

##### Managing transaction logs

Managing your transaction log requires you to think about your recovery model, log backups, and various other details regarding the log files.

###### Picking a recovery model

The key to effectively managing transaction logs is to know what the availability and recovery requirements are for the database. The choice of recovery model should not be chosen because of performance issues or space concerns.

If there is no requirement for point-in-time recovery and it is acceptable, in the case of a disaster, to restore the database to the last full/differential backup, then simple recovery model can be used. In reality, it’s not that common to have a database where the loss of several hours of data is acceptable, so in general simple recovery model should be limited to development or testing environments or databases that can be completely recreated from a source if they fail.

If there is a requirement for point-in-time recovery and minimal or no data loss in the case of a disaster, then the database should be in full or bulk-logged recovery model. This, along with proper storage and retention for the backup files can allow the database to be restored to the point of failure or near to the point of failure in most situations.

If the database is in full or bulk-logged recovery model then log backups must be done. Without log backups the log entries will never be discarded from the log and the log file will grow until it fills the drive. Since one of the main reasons for having a database in full or bulk-logged recovery model is to allow the database to be restored without data loss in the case of a disaster, it’s important to have an unbroken log chain to allow a restore to the point of failure if such a restore becomes necessary. This means that no log backups can be lost or discarded and the database cannot be switched to simple recovery model.

###### Frequency of log backups

The frequency that log backups should be done is dependent on two considerations:

The maximum amount of data that can be lost in the case of a disaster
1. The size to which the log can grow.
2. The first consideration is by far the most important.

When in full recovery model a disaster that destroys or damages the database can be recovered from without data loss, providing the transaction log file is available. If the log file is not available then the best that can be done, assuming that the log backups are stored separately from the database files and are available, is a restore to the last log backup taken, losing all data after that point. From this it should be clear that the interval between log backups should be carefully chosen based on the RPO (recovery point objective) requirements for that database. If the mandate is that no more than 20 minutes of data can be lost, then scheduling log backups hourly is a risk, as a disaster can result in losing up to 60 minutes of data if the transaction log file is lost or damaged.

If (once the log backups have been setup and scheduled based on the database's RPO) the log is growing larger than is acceptable, then the log backup frequency can be increased in order to keep the size down. This is by no means guaranteed to have the desired effect as the log must be large enough to accommodate the largest single transaction run against the database (which is usually an index rebuild).

##### Log chains
A log chain is an unbroken set of log backups starting with a full or differential backup and reaching to the point where the database needs to be restored. When a log chain is broken, the database cannot be restored to any point past the point at which the log chain was broken until a full or differential backup is taken to restart the log chain.

Switching a database to simple recovery model immediately breaks the log chain and prevents further log backups. Log backups cannot be taken until the database is switched back to full or bulk-logged recovery and a full or differential backup is taken. The database can't be restored to any point between the last log backup prior to the switch to simple recovery and the full or differential backup that re-established the log chain.

Deleting or losing a log backup file breaks the log chain, although SQL doesn't know that the log chain is broken in that case and allows log backups to still be taken. Regardless, if a log backup file is missing the log chain is broken and point-in-time restores can't be done to any point within or after the time range covered by the missing log backup. As with the case of switching to simple recovery model, a full or differential backup must be taken to start a new log chain.

It is important to note that while a full or differential backup starts a log chain, full and differential backups don't break the log chain. If, for example, full backups were taken every 4 hours and transaction log backups hourly and a restore was needed to 5pm, then all of these would be valid, working options

1. Restore 4pm full backup, 5pm log backup
2. Restore midday full backup, log backups from 1pm-5pm
3. Restore 8am full backup, log backups from 9am-5pm
4. Etc.

##### Log size

The question of how big a log file should be given a data file of a particular size is a common one, and one almost impossible to easily answer.

There is no single formula that calculates how large a log file should be based on the data file size. The size that the log file needs to be is based on activity (specifically database changes) and, in full and bulk-logged recovery, on the interval between log backups. This is not easy to calculate without performing a load-test of the database with both production-level data volumes and production-level transaction volumes.

At a minimum, the log must be large enough to hold the log records for the largest transaction that will be run against the database. In full recovery that will likely be the index rebuild of the largest clustered index in the database. So, with no other considerations, a reasonable place to start would be around 150% of the size of the largest table in the database with a reasonable growth increment based on the initial size, assuming that the largest table will have its clustered index rebuilt in full recovery model. This may need to be increased based on a number of considerations, including but not limited to

- Largest size of the database mirroring send queue
- Transaction volume during a full or differential backup
- Latency and transaction volume of transactional replication or CDC.

A large log file will not cause performance problems for queries in the database. It is possible that a very large number of Virtual Log Files will result in slower than expected log backups and other operations that read the log, but that's not a problem of large log, that's a result of growing the log file in small intervals

##### Number of log files

The answer to the question of how many log files a database should have is a simple one. One log file only. SQL uses log files sequentially, not in any form of parallel or Round-Robin mechanism. Hence, if there are multiple log files, SQL will only ever be writing to one at a time.

The one time where there may be a use for a second log file is when unusual database activity needs a total amount of log space larger than what is available on any particular drive or larger than the 2TB limit in the size of a log file. In these circumstances it may be necessary to create a second log file to increase the amount of available log space. This is purely about available log space, not about performance.

##### Shrinking the log

In general, the transaction log should not be shrunk. It certainly should never be shrunk on a regular basis in a job or maintenance plan.

The only time a log should be shrunk is if some abnormal database activity (or failed log backups) has resulted in the log growing far beyond the size it needs to be for the database activity. In this situation, the log can be shrunk as a once-off operation, reducing it back to the size that it was before the abnormal activity.

Shrinking the log on a regular basis will have just one effect - the log growing again once regular activity on the database requires the old size. Transaction log grow operations are not fast, they cannot take advantage of instant initialisation and hence the new portion of the log will always have to be zeroed out. The other effect of the log repeatedly growing is that unless the auto-grow setting has been carefully chosen, the growth of the log will result in log fragmentation - excessive VLFs that can degrade the performance of backups, restores, crash recovery, replication and anything else that reads the log.

Don't shrink the log regularly. Shrink only if something has blown the size of the log far beyond what it needs to be.

##### Log fragmentation and VLFs

Internally, the log is divided into sections called Virtual Log Files (VLF). A log will always contain at least 2 VLFs and will usually contain far more. When the log is truncated (checkpoint in simple recovery or log backup in full recovery), only entire VLFs can be marked reusable. SQL can't mark individual log records or log blocks as reusable. A single log record that's part of an open transaction or otherwise needed prevents the entire VLF from being marked as reusable.

When the log is created or the log grows the specified size results in a specific number of VLFs of specific sizes. More details on the exact algorithm can be found on Kimberly Tripp's blog. If the log was improperly sized initially and auto-grew to a huge size, the log can have vast numbers of VLFs (tens of thousands have been seen in production systems). The problem with excessive VLFs is that it can have a massive impact on operations that read the log. These include, but are not limited to, database and log backups, restores, crash recovery, transactional replication, change data capture.

There's no exact number of VLFs that are good or bad. If there are thousands, it's probably bad. Tens of thousands is definitely very bad. Hundreds?  That depends on the size of the log. The number of VLFs should be high enough that SQL doesn't have to keep huge portions of the log active but low enough that reading all the VLF headers doesn't take too long.

The fix for excessive VLFs is to shrink the log to 0 and then regrow it in reasonable chunks to its previous size. This obviously has to be done while the database is idle. The size of the grow increments determines how many VLFs will be in the new file, see Kimberly’s blog post on log throughput for details, as well as the previously mentioned blog post: http://www.sqlskills.com/blogs/kimberly/post/8-Steps-to-better-Transaction-Log-throughput.aspx.

The growth increment must not be an exact multiple of 4GB. There's a bug in SQL if that exact size is used. Any other size works as expected.

##### Log mismanagement

There's a huge amount of advice on various forums and blogs as to management of logs. Unfortunately much of it is incorrect or outright dangerous. To end this article I'll touch on a couple of particularly bad forms and explain why they're so bad.

###### Detach the database, delete the log file, and reattach the database.

This one's particularly terrible as it can cause unexpected downtime and potentially could even result in the complete loss of the database. SQL cannot always recreate the log if a database is attached without one. A log can only be recreated if the database was shut down cleanly. That means no uncommitted transactions, sufficient time to perform a checkpoint and sufficient log space to perform a checkpoint.

If the database is detached and the log deleted and SQL could not cleanly shut the database down beforehand, the database will fail to reattach necessitating a restore from backup or hacking the database back in and doing an emergency mode repair. Said repair can fail and if it does with no available backup, the database is essentially lost without hope of recovery.

###### Set the recovery model to Simple, shrink the log to 0 and then set the recovery model back to full

This one's nasty for two reasons.

The switch to simple recovery breaks the log chain, which means that there is no possibility for point-in-time recovery past this point until another full or differential backup is taken to restart the log chain (something most people recommending this don't mention). Even if a full backup is taken immediately after switching back to full recovery, breaking the log chain reduces the options available for restoring. If a full backup taken after the point the log chain was broken is damaged, a full backup from before can't be used without potentially significant data loss.

The other reason is that shrinking the log to 0 will immediately force it to grow. When the log grows it has to be zero-initialised and hence can slow down all data modifications occurring. It can also result in a huge number of VLFs if the auto grow increments are not properly chosen.

##### Conclusion

The transaction log is a crucial piece of a database and a good understanding of basic log management is an essential skill for any DBA. In this article I've briefly covered what the log is used for and how the recovery models affect that.  I've also touched on how the log should and shouldn’t be managed and some other considerations that exist for dealing with the transaction log of a SQL Server database.


##### Acknowledgements

Thanks to Jason and Rémi for proof-reading and picking up all sorts of ridiculous auto-correct errors.

Reference: [Managing Transaction Logs](http://www.sqlservercentral.com/articles/Administration/64582/)