## Understanding the SSH Encryption and Connection Process

> Justin Ellingwood October 22, 2014

> https://www.digitalocean.com/community/tutorials/understanding-the-ssh-encryption-and-connection-process

### Introduction

SSH, or secure shell, is a secure protocol and the most common way of safely administering remote servers. Using a number of encryption technologies, SSH provides a mechanism for establishing a cryptographically secured connection between two parties, authenticating each side to the other, and passing commands and output back and forth.

In this guide, we will be examining the underlying encryption techniques that SSH employs and the methods it uses to establish secure connections. This information can be useful for understanding the various layers of encryption and the different steps needed to form a connection and authenticate both parties.

### Symmetric Encryption, Asymmetric Encryption, and Hashes

In order to secure the transmission of information, SSH employs a number of different types of data manipulation techniques at various points in the transaction. These include forms of symmetrical encryption, asymmetrical encryption, and hashing.

#### Symmetrical Encryption

The relationship of the components that encrypt and decrypt data determine whether an encryption scheme is symmetrical or asymmetrical.

Symmetrical encryption is a type of encryption where one key can be used to encrypt messages to the opposite party, and also to decrypt the messages received from the other participant. This means that anyone who holds the key can encrypt and decrypt messages to anyone else holding the key.

This type of encryption scheme is often called "shared secret" encryption, or "secret key" encryption. There is typically only a single key that is used for all operations, or a pair of keys where the relationship is easy to discover and it is trivial to derive the opposite key.

Symmetric keys are used by SSH in order to encrypt the entire connection. Contrary to what some users assume, public/private asymmetrical key pairs that can be created are only used for authentication, not the encrypting the connection. The symmetrical encryption allows even password authentication to be protected against snooping.

The client and server both contribute toward establishing this key, and the resulting secret is never known to outside parties. The secret key is created through a process known as a key exchange algorithm. This exchange results in the server and client both arriving at the same key independently by sharing certain pieces of public data and manipulating them with certain secret data. This process is explained in greater detail later on.

The symmetrical encryption key created by this procedure is session-based and constitutes the actual encryption for the data sent between server and client. Once this is established, the rest of the data must be encrypted with this shared secret. **This is done prior to authenticating a client.**

SSH can be configured to utilize a variety of different symmetrical cipher systems, including AES, Blowfish, 3DES, CAST128, and Arcfour. The server and client can both decide on a list of their supported ciphers, ordered by preference. The first option from the client's list that is available on the server is used as the cipher algorithm in both directions.

On Ubuntu 14.04, both the client and the server are defaulted like this: `aes128-ctr`, `aes192-ctr`, `aes256-ctr`, `arcfour256`, `arcfour128`, `aes128-gcm@openssh.com`, `aes256-gcm@openssh.com`, `chacha20-poly1305@openssh.com`, `aes128-cbc`, `blowfish-cbc`, `cast128-cbc`, `aes192-cbc`, `aes256-cbc`, `arcfour`.

This means that if two Ubuntu 14.04 machines are connecting to each other (without overriding the default ciphers through configuration options), they will always use the aes128-ctr cipher to encrypt their connection.

#### Asymmetrical Encryption

Asymmetrical encryption is different from symmetrical encryption in that to send data in a single direction, two associated keys are needed. One of these keys is known as the **private key**, while the other is called the **public key**.

The public key can be freely shared with any party. It is associated with its paired key, but the private key **cannot** be derived from the public key. The mathematical relationship between the public key and the private key allows the public key to encrypt messages that can only be decrypted by the private key. This is a one-way ability, meaning that the public key has no ability to decrypt the messages it writes, nor can it decrypt anything the private key may send it.

> 注：这里作者讲的one-way ability是指在SSH中的应用。**理论上讲，私钥加密的数据是可以用公钥解密的。**但是因为公钥是公开的，任何人都可以获得，所以这里，作者讲不能使用私钥加密数据，然后再使用公钥解密密文。因为，这种操作丧失了加密的意义。但是，私钥加密数据，然后采用公钥解密的操作还是有实际的应用价值，例如数字签名就是一个典型的应用案例。

The private key should be kept entirely secret and should never be shared with another party. This is a key requirement for the public key paradigm to work. The private key is the only component capable of decrypting messages that were encrypted using the associated public key. By virtue of this fact, any entity capable decrypting these messages has demonstrated that they are in control of the private key.

**SSH utilizes asymmetric encryption in a few different places.** During the initial key exchange process used to set up the symmetrical encryption (used to encrypt the session), asymmetrical encryption is used. In this stage, both parties produce temporary key pairs and exchange the public key in order to produce the shared secret that will be used for symmetrical encryption.

The more well-discussed use of asymmetrical encryption with SSH comes from SSH key-based authentication. SSH key pairs can be used to authenticate a client to a server. The client creates a key pair and then uploads the public key to any remote server it wishes to access. This is placed in a file called `authorized_keys` within the `~/.ssh` directory in the user account's home directory on the remote server.

After the symmetrical encryption is established to secure communications between the server and client, the client must authenticate to be allowed access. The server can use the public key in this file to encrypt a challenge message to the client. If the client can prove that it was able to decrypt this message, it has demonstrated that it owns the associated private key. The server then can set up the environment for the client.

#### Hashing

Another form of data manipulation that SSH takes advantage of is cryptographic hashing. Cryptographic hash functions are methods of creating a succinct "signature" or summary of a set of information. Their main distinguishing attributes are that they are never meant to be reversed, they are virtually impossible to influence predictably, and they are practically unique.

Using the same hashing function and message should produce the same hash; modifying any portion of the data should produce an entirely different hash. A user should not be able to produce the original message from a given hash, but they should be able to tell if a given message produced a given hash.

Given these properties, hashes are mainly used for data integrity purposes and to verify the authenticity of communication. The main use in SSH is with HMAC, or hash-based message authentication codes. These are used to ensure that the received message text is intact and unmodified.

As part of the symmetrical encryption negotiation outlined above, a message authentication code (MAC) algorithm is selected. The algorithm is chosen by working through the client's list of acceptable MAC choices. The first one out of this list that the server supports will be used.

Each message that is sent after the encryption is negotiated must contain a MAC so that the other party can verify the packet integrity. The MAC is calculated from the symmetrical shared secret, the packet sequence number of the message, and the actual message content.

The MAC itself is sent outside of the symmetrically encrypted area as the final part of the packet. Researchers generally recommend this method of encrypting the data first, and then calculating the MAC.

### How Does SSH Work?

You probably already have a basic understanding of how SSH works. The SSH protocol employs a client-server model to authenticate two parties and encrypt the data between them.

The server component listens on a designated port for connections. It is responsible for negotiating the secure connection, authenticating the connecting party, and spawning the correct environment if the credentials are accepted.

The client is responsible for beginning the initial TCP handshake with the server, negotiating the secure connection, verifying that the server's identity matches previously recorded information, and providing credentials to authenticate.

**An SSH session is established in two separate stages. The first is to agree upon and establish encryption to protect future communication. The second stage is to authenticate the user and discover whether access to the server should be granted.**

### Negotiating Encryption for the Session

When a TCP connection is made by a client, the server responds with the protocol versions it supports. If the client can match one of the acceptable protocol versions, the connection continues. The server also provides its public host key, which the client can use to check whether this was the intended host.

At this point, both parties negotiate a session key using a version of something called the Diffie-Hellman algorithm. This algorithm (and its variants) make it possible for each party to combine their own private data with public data from the other system to arrive at an identical secret session key.

**The session key will be used to encrypt the entire session. The public and private key pairs used for this part of the procedure are completely separate from the SSH keys used to authenticate a client to the server.**

The basis of this procedure for classic Diffie-Hellman is:

1. Both parties agree on a large prime number, which will serve as a seed value.

2. Both parties agree on an encryption generator (typically AES), which will be used to manipulate the values in a predefined way.

3. Independently, each party comes up with another prime number which is kept secret from the other party. This number is used as the private key for this interaction (different than the private SSH key used for authentication).

4. The generated private key, the encryption generator, and the shared prime number are used to generate a public key that is derived from the private key, but which can be shared with the other party.

5. Both participants then exchange their generated public keys.

6. The receiving entity uses their own private key, the other party's public key, and the original shared prime number to compute a shared secret key. Although this is independently computed by each party, using opposite private and public keys, it will result in the same shared secret key.

7. The shared secret is then used to encrypt all communication that follows.

The shared secret encryption that is used for the rest of the connection is called binary packet protocol. The above process allows each party to equally participate in generating the shared secret, which does not allow one end to control the secret. It also accomplishes the task of generating an identical shared secret without ever having to send that information over insecure channels.

The generated secret is a symmetric key, meaning that the same key used to encrypt a message can be used to decrypt it on the other side. The purpose of this is to wrap all further communication in an encrypted tunnel that cannot be deciphered by outsiders.

After the session encryption is established, the user authentication stage begins.

### Authenticating the User's Access to the Server

The next stage involves authenticating the user and deciding access. There are a few different methods that can be used for authentication, based on what the server accepts.

The simplest is probably password authentication, in which the server simply prompts the client for the password of the account they are attempting to login with. The password is sent through the negotiated encryption, so it is secure from outside parties.

Even though the password will be encrypted, this method is not generally recommended due to the limitations on the complexity of the password. Automated scripts can break passwords of normal lengths very easily compared to other authentication methods.

The most popular and recommended alternative is the use of SSH key pairs. SSH key pairs are asymmetric keys, meaning that the two associated keys serve different functions.

The public key is used to encrypt data that can only be decrypted with the private key. The public key can be freely shared, because, although it can encrypt for the private key, there is no method of deriving the private key from the public key.

Authentication using SSH key pairs begins after the symmetric encryption has been established as described in the last section. The procedure happens like this:

1. The client begins by sending an ID for the key pair it would like to authenticate with to the server.

2. The server check's the `authorized_keys` file of the account that the client is attempting to log into for the key ID.

3. If a public key with matching ID is found in the file, the server generates a random number and uses the public key to encrypt the number.

4. The server sends the client this encrypted message.

5. If the client actually has the associated private key, it will be able to decrypt the message using that key, revealing the original number.

6. The client combines the decrypted number with the shared session key that is being used to encrypt the communication, and calculates the MD5 hash of this value.

7. The client then sends this MD5 hash back to the server as an answer to the encrypted number message.

8. The server uses the same shared session key and the original number that it sent to the client to calculate the MD5 value on its own. It compares its own calculation to the one that the client sent back. If these two values match, it proves that the client was in possession of the private key and the client is authenticated.

> 注：这里作者并没解释key ID具体是怎么产生的。考虑到，私钥可以推出公钥，客户端和服务器分别计算公私秘钥的ID还是很简单的事情。例如，下面解释的计算RSA key fingerprint的方法。

As you can see, the asymmetry of the keys allows the server to encrypt messages to the client using the public key. The client can then prove that it holds the private key by decrypting the message correctly. The two types of encryption that are used (symmetric shared secret, and asymmetric public-private keys) are each able to leverage their specific strengths in this model.

### Conclusion

Learning about the connection negotiation steps and the layers of encryption at work in SSH can help you better understand what is happening when you login to a remote server. Hopefully, you now have a better idea of relationship between various components and algorithms, and understand how all of these pieces fit together.

#### [comments] guntbert October 30, 2014

> Let me point out an error regarding asymmetric encryption: 

> "This is a one-way ability, meaning that the public key has no ability to decrypt the messages it writes, nor can it decrypt anything the private key may send it."

> The first part is correct: You cannot use any of those two keys to decrypt a message encrypted with the same key.

> The second part is wrong: You can use either of those keys to decrypt a message encrypted with the other one.

>> [comments] jellingwood October 30, 2014

>> First off, I'm not sure if your point is correct.

>> In asymmetric key systems, the public key should always encrypt to the private key, and not the other way around. The private key can be used to sign messages, but should not be used to encrypt them, due to the one-to-many relationship that exists with single ownership of the private key and distributed ownership of the public key. If a message was encrypted with the private key, any entity with the public key could decrypt it. This is why the asymmetric keys are only used for authentication and not the bulk of the communication in an SSH session.

>> These sources seem to confirm my understanding:

>> [Wikipedia's public key cryptography article](https://en.wikipedia.org/wiki/Public-key_cryptography#Description)

>> Let me know if you have any sources that suggest otherwise.

>>> [comments] guntbert November 1, 2014

>>> we are almost on the same side :-)

>>> Your comment is really correct, my concern was with the way you said it in your article.

>>> To clarify: The private key can be used to sign messages, but should not be used to encrypt them - thats exactly correct. 
But: signing a message is done by encrypting a hash of it with your private key, so that everyone can verify your authorship by decrypting the hash with your public key and comparing that decrypted hash with a hash of the received message.

>>> Since only you should be able to use your private key the message can be tied to you.


>>> So we really need both directions


>>> - encrypting with my partner's public key to protect the message from being read by others

>>> - encrypting with my own private key to prove that the message is mine (and hasn't been altered on the way)

>>> P.S. Of course I didn't read your article to discover errors but to learn from it - which I did, thank you :-))

#### [comments] Lajamerr December 7, 2014

> Very nice article, this is really well-written. Helped me understand the distinction between the various cryptographic techniques that go into securing SSH.

> I was hoping for some clarification on asymmetric keys. You use the public key to encrypt and the private key to decrypt. But can the opposite happen. Can you encrypt using the private key and decrypt it with the public key using the same key pair for both scenarios.

>> [comments] jellingwood December 8, 2014 

>> Asymmetric keys generally do not provide for encrypting with the private key because the public key is shared and publicly available. This means that anyone with the public key could decrypt the message, regardless of the intended recipient.

>> What the private key can do is sign messages to prove the authenticity of the message. This means that any holder of a public key can verify the origins of a signed message as having been sent by the holder of the private key.

>> If you wish to send messages between two parties using a public key system, you have a few options. The first is to use two sets of public and private keys, one for each party. The participants exchange public keys using a secure and trusted method where they can personally verify the identity of the opposite party.

>> Messages can then be sent to each other by encrypting using the other user's public key. I would send a message to you encrypted with your public key. You would decrypt it using your private key and encrypt a message back using my public key. This is the method that systems like PGP/GPG use.

>> The other way of sending messages in both directions is to not actually use asymmetrical encryption for the communication. We only rely on the asymmetrical keys to authenticate and we establish a symmetrical encryption channel for the actual communication encryption. This is what SSH does. It establishes a symmetric key encryption channel using the Diffie-Hellman (or a related) algorithm. Afterwards, it uses the asymmetric keys to authenticate the user.

>> Hope this helps.

《完》

## Calculate RSA key fingerprint

> https://stackoverflow.com/questions/9607295/calculate-rsa-key-fingerprint

> asked Mar 7 '12 at 18:48

I need to do the SSH key audit for GitHub, but I am not sure how do find my RSA key fingerprint. I originally followed a guide to generate an SSH key on Linux.

What is the command I need to enter to find my current RSA key fingerprint?

### Answer 1

Run the following command to retrieve the SHA256 fingerprint of your SSH key (`-l` means "list" instead of create a new key, `-f` means "filename"):

```
$ ssh-keygen -lf /path/to/ssh/key
```

So for example, on my machine the command I ran was (using RSA public key or private key is all OK):

```
$ ssh-keygen -lf id_rsa
2048 SHA256:zUmXeardRLigLe31/XTLPwhn9IAjHtZxCCM4AmxQmDg dr@Ubuntu (RSA)

$ ssh-keygen -lf id_rsa.pub
2048 SHA256:zUmXeardRLigLe31/XTLPwhn9IAjHtZxCCM4AmxQmDg dr@Ubuntu (RSA)
```

Use the following command, if you do not want the standard sha256 output.

To get the GitHub (MD5) fingerprint format with newer versions of ssh-keygen, run:

```
$ ssh-keygen -E md5 -lf <fileName>
```

Bonus information:

ssh-keygen -lf also works on `known_hosts` and `authorized_keys` files.

### Answer 2

A key pair (the private and public keys) will have the same fingerprint; so in the case you can't remember which private key belong to which public key, find the match by comparing their fingerprints.

The most voted answer by Marvin Vinto provides the fingerprint of a public SSH key file. The fingerprint of the corresponding private SSH key can also be queried.

1. Load the SSH agent, if you haven't done so. The easiest way is to invoke

```
$ ssh-agent bash
# or
$ ssh-agent tcsh
# (or another shell you use).
```

2. Load the private key you want to test:

```
$ ssh-add /path/to/your-ssh-private-key
```

3. You will be asked to enter the passphrase if the key is password-protected.

Now, as others have said, type

```
$ ssh-add -l
2048 SHA256:zUmXeardRLigLe31/XTLPwhn9IAjHtZxCCM4AmxQmDg id_rsa (RSA)

$ ssh-add -l -E md5
2048 MD5:9c:0b:06:9e:92:03:b5:f7:09:c7:d8:22:5d:6c:07:70 id_rsa (RSA)
```

the output is the fingerprint you are after. If there are multiple keys, multiple lines will be printed, and the last line contains the fingerprint of the last loaded key.

If you want to stop the agent (i.e., if you invoked step 1 above), then simply type `exit' on the shell, and you'll be back on the shell prior to the loading of ssh agent.

《完》

## Simplify Your Life With an SSH Config File

> Mar 17, 2011 • Joël Perras

If you're anything like me, you probably log in and out of a half dozen remote servers (or these days, local virtual machines) on a daily basis. And if you're even more like me, you have trouble remembering all of the various usernames, remote addresses and command line options for things like specifying a non-standard connection port or forwarding local ports to the remote machine.

### Shell Aliases

Let's say that you have a remote server named `dev.example.com`, which has not been set up with public/private keys for password-less logins. The username to the remote account is fooey, and to reduce the number of scripted login attempts, you've decided to change the default SSH port to 2200 from the normal default of 22. This means that a typical command would look like:

```
$ ssh fooey@dev.example.com -p 22000
password: *************
```

Not too bad.

We can make things simpler and more secure by using a public/private key pair; I highly recommend using `ssh-copy-id` for moving your public keys around. It will save you quite a few folder/file permission headaches.

```
$ ssh fooey@dev.example.com -p 22000
# Assuming your keys are properly setup…
```

Now this doesn't seem all that bad. To cut down on the verbosity you could create a simple alias in your shell as well:

```
$ alias dev='ssh fooey@dev.example.com -p 22000'
$ dev # To connect
```

This works surprisingly well: Every new server you need to connect to, just add an alias to your `.bashrc` (or `.zshrc` if you hang with the cool kids), and voilà.

### ~/.ssh/config

However, there's a much more elegant and flexible solution to this problem. Enter the SSH config file:

```
# contents of $HOME/.ssh/config
Host dev
    HostName dev.example.com
    Port 22000
    User fooey
```

This means that I can simply `$ ssh dev`, and the options will be read from the configuration file. Easy peasy. Let's see what else we can do with just a few simple configuration directives.

Personally, I use quite a few public/private keypairs for the various servers and services that I use, to ensure that in the event of having one of my keys compromised the damage is as restricted as possible. For example, I have a key that I use uniquely for my Github account. Let's set it up so that that particular private key is used for all my github-related operations:

```
Host dev
    HostName dev.example.com
    Port 22000
    User fooey
Host github.com
    IdentityFile ~/.ssh/github.key
```

The use of `IdentityFile` allows me to specify exactly which private key I wish to use for authentification with the given host. You can, of course, simply specify this as a command line option for "normal" connections:

```
$ ssh -i ~/.ssh/blah.key username@host.com
```

but the use of a config file with `IdentityFile` is pretty much your only option if you want to specify which identity to use for any git commands. This also opens up the very interesting concept of further segmenting your github keys on something like a per-project or per-organization basis:

```
Host github-project1
    User git
    HostName github.com
    IdentityFile ~/.ssh/github.project1.key
Host github-org
    User git
    HostName github.com
    IdentityFile ~/.ssh/github.org.key
Host github.com
    User git
    IdentityFile ~/.ssh/github.key
```

Which means that if I want to clone a repository using my organization credentials, I would use the following:

```
$ git clone git@github-org:orgname/some_repository.git
```

### Going further

As any security-conscious developer would do, I set up firewalls on all of my servers and make them as restrictive as possible; in many cases, this means that the only ports that I leave open are 80/443 (for webservers), and port 22 for SSH (or whatever I might have remapped it to for obfuscation purposes). On the surface, this seems to prevent me from using things like a desktop MySQL GUI client, which expect port 3306 to be open and accessible on the remote server in question. The informed reader will note, however, that a simple local port forward can save you:

```
$ ssh -f -N -L 9906:127.0.0.1:3306 coolio@database.example.com
# -f puts ssh in background
# -N makes it not execute a remote command
```

This will forward all local port 9906 traffic to port 3306 on the remote `database.example.com` server, letting me point my desktop GUI to localhost (127.0.0.1:9906) and have it behave exactly as if I had exposed port 3306 on the remote server and connected directly to it.

Now I don't know about you, but remembering that sequence of flags and options for SSH can be a complete pain. Luckily, our config file can help alleviate that:


```
Host tunnel
    HostName database.example.com
    IdentityFile ~/.ssh/coolio.example.key
    LocalForward 9906 127.0.0.1:3306
    User coolio
```

Which means I can simply do:

```
$ ssh -f -N tunnel
```

And my local port forwarding will be enabled using all of the configuration directives I set up for the tunnel host. Slick.

There are quite a few configuration options that you can specify in `~/.ssh/config`, and I highly suggest consulting the [online documentation](https://linux.die.net/man/5/ssh_config) or the `ssh_config` man page. Some interesting/useful things that you can do include: change the default number of connection attempts, specify local environment variables to be passed to the remote server upon connection, and even the use of * and ? wildcards for matching hosts.

You can also reference the nixCraft blog: [OpenSSH Config File Examples](https://www.cyberciti.biz/faq/create-ssh-config-file-on-linux-unix/).

I hope that some of this is useful to a few of you. Leave a note in the comments if you have any cool tricks for the SSH config file; I'm always on the lookout for fun hacks.

## Reference:

https://stackoverflow.com/questions/9607295/calculate-rsa-key-fingerprint

[Simplify Your Life With an SSH Config File](https://nerderati.com/2011/03/17/simplify-your-life-with-an-ssh-config-file/)

[OpenSSH Config File Examples](https://www.cyberciti.biz/faq/create-ssh-config-file-on-linux-unix/)

