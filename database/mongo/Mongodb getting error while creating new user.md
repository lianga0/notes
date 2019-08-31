### Mongodb getting error while creating new user

> https://stackoverflow.com/questions/51149455/mongodb-getting-error-while-creating-new-user

I just installed a fresh mongodb on Ubuntu server and when I try to adduser I am getting error:

```
use admin;
db.createUser({user:"user_name",pwd:"password",roles:["root"], mechanisms:[ "SCRAM-SHA-1", "SCRAM-SHA-256"]})
```

```
Failed to execute script.

Error: couldn't add user: Use of SCRAM-SHA-256 requires undigested passwords :
_getErrorWithCode@src/mongo/shell/utils.js:25:13
DB.prototype.createUser@src/mongo/shell/db.js:1290:15
@(shell):1:1

```

### Answer:

If you use [User Management Methods](https://docs.mongodb.com/manual/reference/method/db.createUser/) you have to set param passwordDigestor. This works for me:

```
use admin;
db.createUser({user:"user_name",pwd:"password",roles:["root"], mechanisms:[ "SCRAM-SHA-1", "SCRAM-SHA-256"], passwordDigestor :"server"})
db.createUser({user:"user_name",pwd:"password",roles:["readAnyDatabase"], mechanisms:[ "SCRAM-SHA-1", "SCRAM-SHA-256"], passwordDigestor :"server"})
```

