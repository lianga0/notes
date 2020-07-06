## Running Airflow with systemd

Airflow can integrate with `systemd` based systems. This makes watching your daemons easy as `systemd` can take care of restarting a daemon on failures.

In the [scripts/systemd](https://github.com/apache/airflow/tree/master/scripts/systemd) directory, you can find unit files that have been tested on Redhat based systems. These files can be used as-is by copying them over to `/usr/lib/systemd/system`.

The following **assumptions** have been made while creating these unit files:

- Airflow runs as the following user:group airflow:airflow.

- Airflow runs on a Redhat based system.

If this is not the case, **appropriate changes** will need to be made.

Please note that environment configuration is picked up from `/etc/sysconfig/airflow`.

You can also define configuration at `AIRFLOW_HOME` or `AIRFLOW_CONFIG`.

为了简单起见，我将airflow webserver的监听端口配置为80，所以需要root权限启动该服务。
所以，简单起见，直接用了root用户。配置文件如下(注意可执行文件的路径)：

### /usr/lib/systemd/system/airflow-webserver.service


```
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

[Unit]
Description=Airflow webserver daemon
After=network.target postgresql.service mysql.service redis.service rabbitmq-server.service
Wants=postgresql.service mysql.service redis.service rabbitmq-server.service

[Service]
Environment="AIRFLOW_HOME=/home/ubuntu/airflow"
User=root
Group=root
Type=simple
ExecStart=/usr/local/bin/airflow webserver --pid /run/airflow/webserver.pid
Restart=on-failure
RestartSec=5s
PrivateTmp=true

[Install]
WantedBy=multi-user.target

```


### /usr/lib/systemd/system/airflow-scheduler.service

```
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

[Unit]
Description=Airflow scheduler daemon
After=network.target postgresql.service mysql.service redis.service rabbitmq-server.service
Wants=postgresql.service mysql.service redis.service rabbitmq-server.service

[Service]
# Environment="AIRFLOW_HOME=/home/ubuntu/airflow"
EnvironmentFile=/etc/sysconfig/airflow
User=root
Group=root
Type=simple
ExecStart=/usr/local/bin/airflow scheduler
Restart=always
RestartSec=5s

[Install]
WantedBy=multi-user.target
```
需要手动创建文件`/etc/sysconfig/airflow`，文件内容如下：

```
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

# This file is the environment file for Airflow. Put this file in /etc/sysconfig/airflow per default
# configuration of the systemd unit files.
#
# AIRFLOW_CONFIG=
AIRFLOW_HOME=/home/ubuntu/airflow

```

From: http://airflow.apache.org/docs/stable/howto/run-with-systemd.html


## Web Authentication - Password

> http://airflow.apache.org/docs/stable/security.html

One of the simplest mechanisms for authentication is requiring users to specify a password before logging in. Password authentication requires the used of the password subpackage in your requirements file. Password hashing uses bcrypt before storing passwords.

```
[webserver]
authenticate = True
auth_backend = airflow.contrib.auth.backends.password_auth
```

When password auth is enabled, an initial user credential will need to be created before anyone can login. An initial user was not created in the migrations for this authentication backend to prevent default Airflow installations from attack. Creating a new user has to be done via a Python REPL on the same machine Airflow is installed.

Navigate to the airflow installation directory

```
$ cd ~/airflow
$ python
Python 2.7.9 (default, Feb 10 2015, 03:28:08)
Type "help", "copyright", "credits" or "license" for more information.
>>> import airflow
>>> from airflow import models, settings
>>> from airflow.contrib.auth.backends.password_auth import PasswordUser
>>> user = PasswordUser(models.User())
>>> user.username = 'new_user_name'
>>> user.email = 'new_user_email@example.com'
>>> user.password = 'set_the_password'
>>> session = settings.Session()
>>> session.add(user)
>>> session.commit()
>>> session.close()
>>> exit()
```

注意：上述创建的用户为普通用户，如果想创建管理员用户，需要额外指定一个参数：

```
user.superuser = 1 //赋予管理员权限，如果是普通用户就不需要这个
```
或者也可以自己去Airflow的数据库中修改user表中记录。