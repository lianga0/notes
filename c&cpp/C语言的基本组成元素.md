# C语言的组成元素（Elements of C）

> https://docs.microsoft.com/en-us/cpp/c-language/elements-of-c?view=msvc-170

This section describes the elements of the C programming language, including the names, numbers, and characters used to construct a C program. The ANSI C syntax labels these components tokens.

This section explains how to define tokens and how the compiler evaluates them.

## Tokens

In a C source program, the basic element recognized by the compiler is the "token." A token is source-program text that the compiler does not break down into component elements.

所以token包含以下的元素：

- keyword

- identifier

- constant

- string-literal

- operator

- punctuator

The keywords, identifiers, constants, string literals, and operators described in this section are examples of tokens. Punctuation characters such as brackets (`[ ]`), braces (`{ }`), parentheses ( `( )` ), and commas (`,`) are also tokens.

## White-Space Characters

Space, tab, line feed (newline), carriage return, form feed, and vertical tab characters are called "white-space characters" because they serve the same purpose as the spaces between words and lines on a printed page — they make reading easier. Tokens are delimited (bounded) by white-space characters and by other tokens, such as operators and punctuation. When parsing code, the C compiler ignores white-space characters unless you use them as separators or as components of character constants or string literals. Use white-space characters to make a program more readable. **Note that the compiler also treats comments as white space.**

## Comments

**Comments(for slash/asterisk `/*` commint) can appear anywhere a white-space character is allowed.** Since the compiler treats a comment as a single white-space character, you cannot include comments within tokens. The compiler ignores the characters in the comment.

While you can use comments to render certain lines of code inactive for test purposes, the **preprocessor directives** `#if` and `#endif` and conditional compilation are a useful alternative for this task. 

## Evaluation of Tokens （Token解析顺序）

**When the compiler interprets tokens, it includes as many characters as possible in a single token before moving on to the next token.** Because of this behavior, the compiler may not interpret tokens as you intended if they are not properly separated by white space. Consider the following expression:

```
i+++j
```

In this example, the compiler first makes the longest possible operator (`++`) from the three plus signs, then processes the remaining plus sign as an addition operator (`+`). Thus, the expression is interpreted as `(i++) + (j)`, not `(i) + (++j)`. In this and similar cases, use white space and parentheses to avoid ambiguity and ensure proper expression evaluation.

> Microsoft Specific

> The C compiler treats a `CTRL+Z` character as an end-of-file indicator. It ignores any text after `CTRL+Z`.

# [C Keywords](https://docs.microsoft.com/en-us/cpp/c-language/c-keywords?view=msvc-170)

**Keywords** are words that have special meaning to the C compiler. In translation phases 7(Translation) and 8(Linkage), an **identifier** can't have the same spelling and case as a C **keyword**. For more information, see [translation phases](https://docs.microsoft.com/en-us/cpp/preprocessor/phases-of-translation?view=msvc-170) in the Preprocessor Reference. 

> Microsoft-specific C keywords

> The ANSI and ISO C standards allow identifiers with two leading underscores to be reserved for compiler implementations. The Microsoft convention is to precede Microsoft-specific keyword names with double underscores. These words can't be used as identifier names.

> Microsoft extensions are enabled by default. To assist in creating portable code, you can disable Microsoft extensions by specifying the `/Za (Disable language extensions)` option during compilation. When you use this option, some Microsoft-specific keywords are disabled.


# [C Identifiers](https://docs.microsoft.com/en-us/cpp/c-language/c-identifiers?view=msvc-170)标识符

"Identifiers" or "symbols" are the names you supply for variables, types, functions, and labels in your program. Identifier names must differ in spelling and case from any keywords. You cannot use keywords (either C or Microsoft) as identifiers; they are reserved for special use. You create an identifier by specifying it in the declaration of a variable, type, or function.

A special kind of identifier, called a statement label, can be used in `goto` statements.

每个C语言中的字要么归为关键字，要么归为标识符。而标识符分为预定义标识符和用户标识符。

预定义标识符是C语言中系统预先定义的标识符，如系统类库名、系统常量名、系统函数名。预定义标识符具有见字明义的特点，如函数“格式输出”（英语全称加缩写：printf）、“格式输入”（英语全称加缩写：scanf）等等。预定义标识符可以作为用户标识符使用，只是这样会失去系统规定的原意，使用不当还会使程序出错。

> Microsoft Specific

> Do not select names for identifiers that begin with two underscores or with an underscore followed by an uppercase letter. The ANSI C standard allows identifier names that begin with these character combinations to be reserved for compiler use. To avoid any naming conflicts, always select identifier names that do not begin with one or two underscores, or names that begin with an underscore followed by an uppercase letter.

An identifier has "scope," which is the region of the program in which it is known, and "linkage," which determines whether the same name in another scope refers to the same identifier. These topics are explained in [Lifetime, Scope, Visibility, and Linkage](https://docs.microsoft.com/en-us/cpp/c-language/lifetime-scope-visibility-and-linkage?view=msvc-170).


## Multibyte and Wide Characters

A multibyte character is a character composed of sequences of one or more bytes. Each byte sequence represents a single character in the extended character set. Multibyte characters are used in character sets such as Kanji.

The C and C++ standard libraries include a number of facilities for dealing with wide characters and strings composed of them. The wide characters are defined using datatype `wchar_t`, which in the original `C90` standard was defined as

> "an integral type whose range of values can represent distinct codes for all members of the largest extended character set specified among the supported locales" (ISO 9899:1990 §4.1.5)

Both C and C++ introduced fixed-size character types `char16_t` and `char32_t` in the 2011 revisions of their respective standards to provide unambiguous representation of `16-bit` and `32-bit` Unicode transformation formats, leaving `wchar_t` implementation-defined. The `ISO/IEC 10646:2003` Unicode standard 4.0 says that:

> "The width of `wchar_t` is compiler-specific and can be as small as 8 bits. Consequently, programs that need to be portable across any C or C++ compiler should not use `wchar_t` for storing Unicode text. The `wchar_t` type is intended for storing compiler-defined wide characters, which may be Unicode characters in some compilers."


# C Constants

A `constant` is a number, character, or character string that can be used as a value in a program. Use constants to represent floating-point, integer, enumeration, or character values that cannot be modified.


# C String Literals

A "string literal" is a sequence of characters from the source character set enclosed in double quotation marks (`" "`). String literals are used to represent a sequence of characters which, taken together, form a null-terminated string. You must always prefix wide-string literals with the letter `L`.

# Punctuation and Special Characters

The punctuation and special characters in the C character set have various uses, from organizing program text to defining the tasks that the compiler or the compiled program carries out. They do not specify an operation to be performed. **Some punctuation symbols are also operators.** The compiler determines their use from context.

punctuator: `one of ( ) [ ] { } * , : = ; ... #`


# C Declarations and Definitions

A "declaration" establishes an association between a particular variable, function, or type and its attributes. [Overview of Declarations](https://docs.microsoft.com/en-us/cpp/c-language/overview-of-declarations?view=msvc-170) gives the ANSI syntax for the declaration nonterminal. A declaration also specifies where and when an identifier can be accessed (the "linkage" of an identifier). See [Lifetime, Scope, Visibility, and Linkage]() for information about linkage.

A "definition" of a variable establishes the same associations as a declaration but also causes storage to be allocated for the variable.

> A "declaration" specifies the interpretation and attributes of a set of identifiers. A declaration that also causes storage to be reserved for the object or function named by the identifier is called a "definition."

> **All definitions are implicitly declarations, but not all declarations are definitions.** For example, variable declarations that begin with the extern storage-class specifier are "referencing," rather than "defining" declarations. If an external variable is to be referred to before it's defined, or if it's defined in another source file from the one where it's used, an extern declaration is necessary. Storage is not allocated by "referencing" declarations, nor can variables be initialized in declarations.

- 变量的定义： 变量的定义用于为变量分配存储空间，还可以为变量指定初始值。在一个程序中，变量有且仅有一个定义。

- 变量的声明： 用于向程序表明变量的类型和名字。程序中变量可以声明多次，但只能定义一次。(定义也是声明，因为当定义变量时我们也向程序表明了它的类型和名字)

Declarations are made up of some combination of `storage-class specifiers`, `type qualifiers`, `type specifiers`, `declarators`, and `initializers`.

The `storage-class-specifier` terminals defined in C include `auto`, `extern`, `register`, `static`, and `typedef`. Microsoft C also includes the storage-class-specifier terminal `__declspec`. 

There are two `type-qualifier` terminals: `const` and `volatile`. 

`type-specifier` gives the data type of the variable. The `type-specifie`r can be a compound, as when the type is modified by `const` or `volatile`. 

The `declarator` gives the name of the variable, the declarator is just an identifier. For more information on declarators, see [Declarators and Variable Declarations](https://docs.microsoft.com/en-us/cpp/c-language/declarators-and-variable-declarations?view=msvc-170).


## Function Declarations and Definitions

Function prototypes establish the name of the function, its return type, and the type and number of its formal parameters. A function definition includes the function body.

> Remarks

> Both function and variable declarations can appear inside or outside a function definition. Any declaration within a function definition is said to appear at the "internal" or "local" level. A declaration outside all function definitions is said to appear at the "external," "global," or "file scope" level. Variable definitions, like declarations, can appear at the internal level (within a function definition) or at the external level (outside all function definitions). Function definitions always occur at the external level. 

> 注解：我认为声明(Declarations)是和语句(statement)并列的概念，而不是类似于表达式(expression)与语句的关系。

> https://docs.microsoft.com/en-us/cpp/c-language/overview-of-functions?view=msvc-170

Functions must have a definition and should have a declaration, although a definition can serve as a declaration if the declaration appears before the function is called. The function definition includes the function body — the code that executes when the function is called.

A function declaration establishes the name, return type, and attributes of a function that is defined elsewhere in the program. A function declaration must precede the call to the function. This is why the header files containing the declarations for the run-time functions are included in your code before a call to a run-time function. If the declaration has information about the types and number of parameters, the declaration is a prototype. See [Function Prototypes](https://docs.microsoft.com/en-us/cpp/c-language/function-prototypes?view=msvc-170) for more information.

A function declaration precedes the function definition and specifies the name, return type, storage class, and other attributes of a function. To be a prototype, the function declaration must also establish types and identifiers for the function's arguments.

在使用函数之前应该先**声明**，事先通知编译器该函数的类型：换句话说，一个声明即是描述一个函数的接口。声明至少应指明函数返回值的类型，如下例所示：

```
int rename();
```

这一行代码声明 `rename()`是一个函数，其返回值的类型是 `int` 类型。因为在默认情况下，函数名是外部可见的标识符，所以上述声明等同于：

```
extern int rename();
```

该声明没有包含关于函数参数的数量和类型等相关信息。因此，编译器无法检查调用该函数时所传入的参数是否正确。如果调用该函数时传入的参数有别于该函数的定义，那么会导致严重的运行错误。

为了避免这样的错误，应该在声明函数时，同时声明函数的参数。换句话说，所声明的应该是一个**函数原型（function prototype）**。例如，标准库函数 `rename()`（它用于修改文件名）的原型如下：

```
int rename( const char *oldname, const char *newname );
```

该函数需要两个参数，类型都是指向 `const char` 的指针。换句话说，此函数使用这两个指针的目的是为了读取 char 对象，所以参数可以是字符串字面量。

在原型声明中，参数的标识符是可选的，可以不写。如果将参数名包含进去，这些名称的作用域也仅限于该原型中。对于编译器来说参数名是没有意义的，它们最多和注释一样告诉程序员该参数的目的。

例如，在函数 `rename()`的原型中，参数名称 oldname 和 newname 用来告诉程序员，在调用函数时，旧的文件名写在前而，新的文件名写在后面。对于编译器来说，上述原型声明等同于没有给出参数名的声明：

```
int rename( const char *, const char * );
```

标准头文件中包含了标准库函数的原型。如果想在程序中调用函数 `rename()`，可以通过在代码中包含头文件 `stdio.h` 的方式来达到声明的效果。

通常，可以将自己所定义的函数原型放在一个头文件中，这样在其他任何源代码文件中，通过 include 命令来包含该头文件，则可以使用这些函数。

# Expression

> https://docs.microsoft.com/en-us/cpp/c-language/operands-and-expressions?view=msvc-170

An "operand" is an entity on which an operator acts. An "expression" is a sequence of operators and operands that performs any combination of these actions:

- Computes a value

- Designates an object or function

- Generates side effects

Operands in C include constants, identifiers, strings, function calls, subscript expressions, member-selection expressions, and complex expressions formed by combining operands with operators or by enclosing operands in parentheses. 

## C primary expressions

> https://docs.microsoft.com/en-us/cpp/c-language/c-primary-expressions?view=msvc-170

Primary expressions are the building blocks of more complex expressions. They may be constants, identifiers, a [Generic selection](https://docs.microsoft.com/en-us/cpp/c-language/generic-selection?view=msvc-170), or an expression in parentheses.

Syntax
```
primary-expression:
    identifier
    constant
    string-literal
    ( expression )
    generic-selection

expression:
    assignment-expression
    expression, assignment-expression
```

# Statement

The statements of a C program control the flow of program execution. In C, as in other programming languages, several kinds of statements are available to perform loops, to select other statements to be executed, and to transfer control.

C statements consist of tokens, expressions, and other statements. A statement that forms a component of another statement is called the "body" of the enclosing statement.
