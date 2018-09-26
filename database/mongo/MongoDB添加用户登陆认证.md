## MongoDB添加用户登陆认证

mongodb存储所有的用户信息在admin 数据库的集合system.users中，保存用户名、密码和数据库信息。mongodb默认不启用授权认证，只要能连接到该服务器，就可连接到mongod。若要启用安全认证，需要更改配置文件参数auth。

### 创建用户和用户角色

添加具有合适权限的用户，以防止出现启用认证后无法修改数据库配置的窘况。

> With access control enabled, ensure you have a user with `userAdmin` or `userAdminAnyDatabase` role in the `admin` database. This user can administrate user and roles such as: create users, grant or revoke roles from users, and create or modify customs roles.

> You can create users either before or after enabling access control. If you enable access control before creating any user, MongoDB provides a localhost exception which allows you to create a user administrator in the admin database. The localhost exception applies only when there are no users created in the MongoDB instance.

这里为了简单起见，我们直接创建root权限的用户和只读用户。

```
use admin

db.createUser(
  {
    user: "dr_writer1",
    pwd: "...........",
    roles: [ { role: "root", db: "admin" } ]
  }
)

db.createUser(
  {
    user: "querier",
    pwd: ".........",
    roles: [ { role: "readAnyDatabase", db: "admin" } ]
  }
)
```

### 重启MongoDB实例启用访问控制

启动mongod实例时添加`--auth`命令行参数或修改配置文件中的security.authorization设置项目。

```
mongod --auth --port 27017 --dbpath /data/db1
```

或修改配置文件（/etc/mongod.conf）

```
security:
  authorization: enabled
```

### 登陆MongoDB数据库

可以在登陆数据库时，进行身份验证

```
mongo --port 27017 -u "myUserAdmin" -p "abc123" --authenticationDatabase "admin"
```

或在连接后验证身份

> Switch to the authentication database (in this case, admin), and use db.auth(<username>, <pwd>) method to authenticate

```
use admin
db.auth("myUserAdmin", "abc123" )
```

Reference：https://docs.mongodb.com/manual/tutorial/enable-authentication/