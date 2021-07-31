# curl: (58) unable to set private key file: 'server.key' type PEM

> https://michaelheap.com/curl-58-unable-to-set-private-key-file-server-key-type-pem/

This took me far too long to work out.

I kept getting the following error whilst trying to sign a cURL request:

```
curl: (58) unable to set private key file: 'server.key' type PEM
```

Google kept sending me to [this StackOverflow page](https://stackoverflow.com/questions/16624704/unable-to-set-private-key-file-cert-pem-type-pem) which is correct, but was not the issue that I was having. I tried placing both key and cert in one file and using --cert, and using separate files and sending `--cert` and `--key`. The actual issue is that I was sending the wrong certificate file. This meant that cURL was looking for a private key that belongs to that certificate and couldn't find it (leading the to above error)

To ensure that your certificate and key match, you can use the following commands:

```
$ openssl x509 -noout -modulus -in server.crt | openssl md5
$ openssl rsa -noout -modulus -in server.key | openssl md5
```

You should see something that looks like the following:

```
(stdin)= 47f0c86371b31432504f195357cf2947
```

If the two values don't match, you're not using the correct combination.
