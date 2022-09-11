# c gets() is risky to use

> https://www.geeksforgeeks.org/gets-is-risky-to-use/

Consider the below program. 

```
void read()
{
   char str[20];
   gets(str);
   printf("%s", str);
   return;
}
```

The code looks simple, it reads string from standard input and prints the entered string, but it suffers from Buffer Overflow as `gets()` doesn’t do any array bound testing. `gets()` keeps on reading until it sees a newline character. 

To avoid Buffer Overflow, `fgets()` should be used instead of `gets()` as `fgets()` makes sure that not more than `MAX_LIMIT` characters are read.

```
#define MAX_LIMIT 20
void read()
{
   char str[MAX_LIMIT];
   fgets(str, MAX_LIMIT, stdin);
   printf("%s", str);
 
   getchar();
   return;
}
```

NOTE: `fgets()` stores the `\n` character if it is read, so removing that has to be done explicitly by the programmer. It is hence, generally advised that your str can store at least (`MAX_LIMIT + 1`) characters if your intention is to keep the newline character. This is done so there is enough space for the null terminating character `\0` to be added at the end of the string.

If keeping the newline character is not intended, then one can simply do the following-

```
int len = strlen(str);
 
// Remove the '\n' character and replace it with '\0'
str[len - 1] = '\0';
```

C 库函数 `char *fgets(char *str, int n, FILE *stream)` 从指定的流 `stream` 读取一行，并把它存储在 `str` 所指向的字符串内。当读取 `(n-1)` 个字符时，或者读取到换行符时，或者到达文件末尾时，它会停止，具体视情况而定。也就是说如果读取过程中没有发生错误，那么它一定会在字符串的末尾添加一个`\n`。

### fgets() 函数的声明

```
char *fgets(char *str, int n, FILE *stream)
```

### 参数

```
str -- 这是指向一个字符数组的指针，该数组存储了要读取的字符串。
n -- 这是要读取的最大字符数（包括最后的空字符）。通常是使用以 str 传递的数组长度。
stream -- 这是指向 FILE 对象的指针，该 FILE 对象标识了要从中读取字符的流。
```

### 返回值

如果成功，该函数返回相同的 str 参数。如果到达文件末尾或者没有读取到任何字符，str 的内容保持不变，并返回一个空指针。

如果发生错误，返回一个空指针。

例如如下代码，定义缓冲区大小为1个字节数组，那么程序会直接返回，并不会等待用户输入内容。

```
int main(void)
{
    #define MAX_LIMIT 1
    char str[MAX_LIMIT];
    fgets(str, MAX_LIMIT, stdin);
    printf("String:%s\n", str);
    printf("%d\n", str[0]);
    printf("Done\n");
    return 0;
}
```

输出：

```
String:
0
Done
```


# fgets() and gets() in C language

> https://www.geeksforgeeks.org/fgets-gets-c-language/

For reading a string value with spaces, we can use either `gets()` or `fgets()` in C programming language. Here, we will see what is the difference between `gets()` and `fgets()`.

## `fgets()`

It reads a line from the specified stream and stores it into the string pointed to by str. It stops when either `(n-1)` characters are read, the newline character is read, or the end-of-file is reached, whichever comes first.


### Syntax :

```
char *fgets(char *str, int n, FILE *stream)

str : Pointer to an array of chars where the string read is copied.

n : Maximum number of characters to be copied into str 
(including the terminating null-character).

*stream : Pointer to a FILE object that identifies an input stream.
stdin can be used as argument to read from the standard input.

returns : the function returns str
```

- It follow some parameter such as Maximum length, buffer, input device reference.
- It is **safe** to use because it checks the array bound.
- It keep on reading until new line character encountered or maximum limit of character array.

Example : Let’s say the maximum number of characters are 15 and input length is greater than 15 but still `fgets()` will read only 15 character and print it.


```
// C program to illustrate
// fgets()
#include <stdio.h>
#define MAX 15
int main()
{
    char buf[MAX];
    fgets(buf, MAX, stdin);
    printf("string is: %s\n", buf);
  
    return 0;
}
Since fgets() reads input from user, we need to provide input during runtime.
```

Input:

```
Hello and welcome to GeeksforGeeks
```

Output:

```
Hello and welc
```

## gets()

Reads characters from the standard input (stdin) and stores them as a C string into str until a newline character or the end-of-file is reached.

### Syntax:

```
char * gets ( char * str );
str :Pointer to a block of memory (array of char) 
where the string read is copied as a C string.
returns : the function returns str
```

- It is **not safe** to use because it does not check the array bound.
- It is used to read string from user until newline character not encountered.

Example : Suppose we have a character array of 15 characters and input is greater than 15 characters, `gets()` will read all these characters and store them into variable.Since, `gets()` do not check the maximum limit of input characters, so at any time compiler may return buffer overflow error.

```
// C program to illustrate
// gets()
#include <stdio.h>
#define MAX 15
  
int main()
{
    char buf[MAX];
  
    printf("Enter a string: ");
    gets(buf);
    printf("string is: %s\n", buf);
  
    return 0;
}
Since gets() reads input from user, we need to provide input during runtime.
```

Input:

```
Hello and welcome to GeeksforGeeks
```

Output:

```
Hello and welcome to GeeksforGeeks
```
