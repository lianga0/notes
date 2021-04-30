# 通配符 DNS 服务

- nip.io

- sslip.io

- xip.io



## Dead simple wildcard DNS for any IP Address

Stop editing your `etc/hosts` file with custom hostname and IP address mappings.

nip.io allows you to do that by mapping any IP Address to a hostname using the following formats:

Without a name:

10.0.0.1.nip.io maps to 10.0.0.1
192-168-1-250.nip.io maps to 192.168.1.250
0a000803.nip.io maps to 10.0.8.3

With a name:

app.10.8.0.1.nip.io maps to 10.8.0.1
app-116-203-255-68.nip.io maps to 116.203.255.68
app-c0a801fc.nip.io maps to 192.168.1.252
customer1.app.10.0.0.1.nip.io maps to 10.0.0.1
customer2-app-127-0-0-1.nip.io maps to 127.0.0.1
customer3-app-7f000101.nip.io maps to 127.0.1.1

nip.io maps `<anything>[.-]<IP Address>.nip.io` in "dot", "dash" or "hexadecimal" notation to the corresponding `<IP Address>`:

dot notation: magic.127.0.0.1.nip.io
dash notation: magic-127-0-0-1.nip.io
hexadecimal notation: magic-7f000001.nip.io

The "dash" and "hexadecimal" notation is especially useful when using services like LetsEncrypt as it's just a regular sub-domain of nip.io
