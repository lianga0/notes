# Nginx配置中try_files和“@”符号得妙用

## `location`

Nginx配置文件中`location`指令：

http://nginx.org/en/docs/http/ngx_http_core_module.html#location

```
Syntax:	location [ = | ~ | ~* | ^~ ] uri { ... }
location @name { ... }
Default:	—
Context:	server, location
```

Sets configuration depending on a request URI.

The matching is performed against a normalized URI, after decoding the text encoded in the “%XX” form, resolving references to relative path components “.” and “..”, and possible [compression](http://nginx.org/en/docs/http/ngx_http_core_module.html#merge_slashes) of two or more adjacent slashes into a single slash.

A location can either be defined by a prefix string, or by a regular expression. Regular expressions are specified with the preceding “~*” modifier (for case-insensitive matching), or the “~” modifier (for case-sensitive matching). To find location matching a given request, nginx first checks locations defined using the prefix strings (prefix locations). Among them, the location with the longest matching prefix is selected and remembered. Then regular expressions are checked, in the order of their appearance in the configuration file. The search of regular expressions terminates on the first match, and the corresponding configuration is used. If no match with a regular expression is found then the configuration of the prefix location remembered earlier is used.

## `try_files`

try_files是nginx中http_core核心模块所带的指令，主要是能替代一些rewrite的指令，提高解析效率。
官网的文档为http://nginx.org/en/docs/http/ngx_http_core_module.html#try_files

```
Syntax:	try_files file ... uri;
try_files file ... =code;
Default:	—
Context:	server, location
```

Checks the existence of files in the specified order and uses the first found file for request processing; the processing is performed in the current context. The path to a file is constructed from the file parameter according to the root and alias directives. It is possible to check directory’s existence by specifying a slash at the end of a name, e.g. `$uri/`. If none of the files were found, an internal redirect to the uri specified in the last parameter is made. For example:

```
location /images/ {
    try_files $uri /images/default.gif;
}

location = /images/default.gif {
    expires 30s;
}
```
