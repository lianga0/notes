# node.js 笔记

### 1. node.js install

macOS Using Homebrew:

```
brew install node
```

https://nodejs.org/en/download/

https://nodejs.org/en/download/package-manager/

https://github.com/nodesource/distributions/blob/master/README.md

ubuntu install Node.js v13.x:

```
curl -sL https://deb.nodesource.com/setup_13.x | sudo -E bash -
sudo apt-get install -y nodejs
```

Windows platform installation use Windows Installer directly from the [nodejs.org](https://nodejs.org/en/#home-downloadhead) web site.

### 2. What are callbacks?

https://nodejs.org/en/knowledge/getting-started/control-flow/what-are-callbacks/

The general idea is that the callback is the last parameter. The callback gets called after the function is done with all of its operations. Traditionally, the first parameter of the callback is the `error` value. If the function hits an error, then they typically call the callback with the first parameter being an Error object. If it cleanly exits, then they will call the callback with the first parameter being null and the rest being the return value(s).

### 3. What are the error conventions?

https://nodejs.org/en/knowledge/errors/what-are-the-error-conventions/

### 4. Overview of Blocking vs Non-Blocking

https://nodejs.org/en/docs/guides/blocking-vs-non-blocking/

