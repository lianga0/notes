## Start up DRS service with uwsgi

### Installing uWSGI with Python support

uWSGI is a (big) C application, so you need a C compiler (like gcc or clang) and the Python development headers.

On a Debian-based distro an

```
sudo apt-get install build-essential python3-dev
```

via pip

```
sudo pip3 install uwsgi
```

Install uwsgi plugin for python3

```
sudo apt install uwsgi-plugin-python3
```

注意：

使用pip安装完uwsgi后，使用如下命令启用HTTP服务，如果出错，那么一般是忘记安装python plugin或者plugin配置不正确。

```
[root@localhost webserver]# uwsgi --http-socket :8080 --wsgi-file testuwsgi.py 
```

错误信息：

```
uwsgi: unrecognized option '--wsgi-file' 
getopt_long() error
```

使用命令安装python plugin后，再使用`uwsgi --http-socket :8001 --plugin python --wsgi-file testuwsgi.py`命令启动服务。

如果还不行，可以试试添加`plugin-dir`参数

```
uwsgi --http-socket :8001 --plugin-dir /usr/lib/uwsgi/plugins/ --plugin python --wsgi-file testuwsgi.py
```

Reference:

[uWSGI Options](https://uwsgi-docs.readthedocs.io/en/latest/Options.html)