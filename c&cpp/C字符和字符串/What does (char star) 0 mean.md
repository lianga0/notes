# What does (char*) 0 mean?

> https://stackoverflow.com/questions/36931022/what-does-char-0-mean

`(char *) 0` is not a "pointer to a character at address 0". In C `(char *) 0` is treated in a special way - it is guaranteed to produce a *null-pointer value* of type `char *`. Formally it does not point to any `char` object. Its actual numerical value (the "address") is implementation-defined and can correspond to any address, not necessarily `0`. E.g. numerically `(char *) 0` can produce a pointer that "points" to address `0xFFFFFFFF`, for one example, if the given platform reserves this address for null-pointer value of `char *` type. But again, from the language point of view, a null-pointer value does not really point anywhere.

`(char *) 9` does not have such special meaning. The pointer that `(char *) 9` produces is also implementation-dependent. In most implementations it will indeed produce a `char *` pointer to address `9`.

In order to work around that special treatment of `(char *) 0` you can try something like

```
int i = 0;
(char *) i;
```

The above` (char *) i` (albeit implementation-dependent too) will usually produce a `char *` pointer to address 0. The key moment here that disables the special treatment is the fact that 0 in the expression is no longer a constant.

> It's important to know that a null-pointer doesn't actually have to be a pointer to address `0`, a null-pointer is actually system dependent. *However*, the integer zero when casted to a pointer (any pointer really) is converted by the compiler to the system-dependent *null-pointer*. 




# [What does char *p=(char *) 0 mean?](https://www.quora.com/What-does-char-*p-char-*-0-mean)

It means someone thinks they’re being clever, or they’re lazy. They’re initializing `p` to what they think is a `NULL` pointer value.

`NULL` is defined in several system header files, including `stdio.h` and `stddef.h.`

There are environments where `stdio.h` may not be usable, but `stddef.h` should always be “safe”, even in embedded environments where you may not have the standard library available.


That said, this initialization should be “OK” - even if stylistically awful - as in the vast majority of C environments, `NULL` is some type of pointer-casted `0`.

A more common situation where `NULL` is implied to be `0` by initialization is something like this

```
typedef struct big_hairy_struct { 
 void *pointer1; 
 void *pointer2; 
 int arrayint[50]; 
 /* lots o' random stuff */ 
 somestruct *structptr1; 
 anotherstruct *structptr2; 
 /* more stuff */ 
} BigHairyStruct; 
 
BigHairyStruct *s = (BigHairyStruct *) malloc(sizeof(BigHairyStruct)); 
 
memset(s, 0, sizeof(BigHairyStruct)); 
```

I’ve seen (and, to be honest, written) code that assumes that the pointers in something like “s” to be set to `NULL` after the `memset`…

Yes, environments do exist where `NULL` is not a `0`, but unless you’re working on very ancient legacy code running on an ancient system, you’re unlikely to ever encounter such an environment: [Null Pointers](http://c-faq.com/null/).

In most implementations, the C declaration of `NULL` in standard header files looks like (E.g. Visual Studio)

```
C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Tools\MSVC\14.29.30133\include\vcruntime.h

#ifndef NULL
    #ifdef __cplusplus
        #define NULL 0
    #else
        #define NULL ((void *)0)
    #endif
#endif
```