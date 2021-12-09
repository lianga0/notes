# Chapter 3. Types, Values, and Variables

Computer programs work by manipulating values, such as the number 3.14 or the text “Hello World.” The kinds of values that can be represented and manipulated in a programming language are known as types, and one of the most fundamental characteristics of a programming language is the set of types it supports. 

When a program needs to retain a value for future use, it assigns the value to (or “stores” the value in) a variable. Variables have names, and they allow use of those names in our programs to refer to values. The way that variables work is another fundamental characteristic of any programming language. 

JavaScript types can be divided into two categories: **primitive types**(基本数据类型) and **object types**. 

JavaScript’s primitive types include numbers, strings of text (known as strings), and Boolean truth values (known as booleans). 

The special JavaScript values `null` and `undefined` are primitive values, but they are not numbers, strings, or booleans. Each value is typically considered to be the sole member of its own special type.

ES6 adds a new special-purpose type, known as `Symbol`, that enables the definition of language extensions without harming backward compatibility.

Any JavaScript value that is not a `number`, a `string`, a `boolean`, a `symbol`, `null`, or `undefined` is an `object`. An object (that is, a member of the type `object`) is a collection of properties where each property has a name and a value (either a primitive value or another object). 

An ordinary JavaScript object is an unordered collection of named values. The language also defines a special kind of object, known as an `array`, that represents an ordered collection of numbered values. The JavaScript language includes special syntax for working with arrays, and arrays have some special behavior that distinguishes them from ordinary objects. 

**JavaScript differs from more static languages in that functions and classes are not just part of the language syntax: they are themselves values that can be manipulated by JavaScript programs. Like any JavaScript value that is not a primitive value, functions and classes are a specialized kind of object.**

**JavaScript supports an object-oriented programming style.**
Loosely, this means that rather than having globally defined functions to operate on values of various types, the types themselves define methods for working with values. To sort the elements of an array `a`, for example, we don’t pass `a` to a `sort()` function.  Instead, we invoke the `sort()` method of `a`:

```
a.sort();       // The object-oriented version of sort(a).
```

Technically, it is only JavaScript objects that have methods.
But `numbers`, `strings`, `boolean`, and `symbol` values behave as if they have methods. In JavaScript, `null` and `undefined` are the only values that methods cannot be invoked on.

JavaScript’s object types are `mutable` and its primitive types are `immutable`. A value of a `mutable` type can change: a JavaScript program can change the values of object properties and array elements. `Numbers`, `booleans`, `symbols`, `null`, and `undefined` are immutable.

JavaScript liberally converts values from one type to another. If a program expects a string, for example, and you give it a number, it will automatically convert the number to a string for you.
And if you use a non-boolean value where a boolean is expected, JavaScript will convert accordingly.

JavaScript’s liberal value conversion rules affect its definition of equality, and the `==` equality operator performs type conversions. (In practice, however, the `==` equality operator is deprecated in favor of the strict equality operator `===`, which does no type conversions.)

Constants and variables allow you to use names to refer to values in your programs. Constants are declared with `const` and variables are declared with `let` (or with `var` in older JavaScript code). JavaScript constants and variables are **untyped**: declarations do not specify what kind of values will be assigned.


## Numbers

JavaScript’s primary numeric type, Number, is used to represent integers and to approximate real numbers. 

JavaScript represents numbers using the 64-bit floating-point format defined by the IEEE 754 standard.

The JavaScript number format allows you to exactly represent all integers between −9,007,199,254,740,992 (−2^53^) and 9,007,199,254,740,992 (2^53^), inclusive. If you use integer values larger than this, you may lose precision in the trailing digits. Note, however, that certain operations in JavaScript (such as array indexing and the bitwise operators) are performed with 32-bit integers.

### numeric literal

When a number appears directly in a JavaScript program, it’s called a `numeric literal`. JavaScript supports numeric literals in several formats.

#### Integer Literals

```
10000000   // base-10 integer
0xff       // hexadecimal (base-16) values => 255: (15*16 + 15)
0xBADCAFE  // => 195939070
0b10101    // binary (base 2)  => 21:  (1*16 + 0*8 + 1*4 + 0*2 + 1*1)
0o377      // octal (base 8) => 255: (3*64 + 7*8 + 7*1)
```

#### Floating-Point Literals

```
[digits][.digits][(E|e)[(+|-)]digits]
```

### Arithmetic in JavaScript

JavaScript supports more complex mathematical operations through a set of functions and constants defined as properties of the Math object.

Arithmetic in JavaScript does not raise errors in cases of overflow, underflow, or division by zero.

JavaScript predefines global constants `Infinity` and `NaN` to hold the positive infinity and not-a-number value, and these values are also available as properties of the `Number` object:

```
Infinity                    // A positive number too big to represent
Number.POSITIVE_INFINITY    // Same value
1/0                         // => Infinity
Number.MAX_VALUE * 2        // => Infinity; overflow

-Infinity                   // A negative number too big to represent
Number.NEGATIVE_INFINITY    // The same value
-1/0                        // => -Infinity
-Number.MAX_VALUE * 2       // => -Infinity

NaN                         // The not-a-number value
Number.NaN                  // The same value, written another way
0/0                         // => NaN
Infinity/Infinity           // => NaN

Number.MIN_VALUE/2          // => 0: underflow
-Number.MIN_VALUE/2         // => -0: negative zero
-1/Infinity                 // -> -0: also negative 0
-0
```

The not-a-number value has one unusual feature in JavaScript: it does not compare equal to any other value, including itself. This means that you can’t write `x === NaN` to determine whether the value of a variable x is `NaN`. Instead, you must write `x != x` or `Number.isNaN(x)`. Those expressions will be true if, and only if, x has the same value as the global constant `NaN`.

The global function `isNaN()` is similar to `Number.isNaN()`. It returns true if its argument is `NaN`, or if that argument is a non-numeric value that cannot be converted to a number. 

```
isNaN("abc")         //=> true
Number.isNaN("abc")  //=> false
```

#### negative zero

The negative zero value is also somewhat unusual. It compares equal (even using JavaScript’s strict equality test) to positive zero, which means that the two values are almost indistinguishable, except when used as a divisor:

```
let zero = 0;         // Regular zero
let negz = -0;        // Negative zero
zero === negz         // => true: zero and negative zero are equal
1/zero === 1/negz     // => false: Infinity and -Infinity are not equal
```

#### Binary Floating-Point and Rounding Errors

The IEEE-754 floating-point representation used by JavaScript (and just about every other modern programming language) is a binary representation, which can exactly represent fractions like 1/2, 1/8, and 1/1024. Unfortunately, the fractions we use most commonly (especially when performing financial calculations) are decimal fractions: 1/10, 1/100, and so on. **Binary floating-point representations cannot exactly represent numbers as simple as 0.1.**

avaScript numbers have plenty of precision and can approximate 0.1 very closely. But the fact that this number cannot be represented exactly can lead to problems. Consider this code:

```
let x = .3 - .2;    // thirty cents minus 20 cents
let y = .2 - .1;    // twenty cents minus 10 cents
x === y             // => false: the two values are not the same!
x === .1            // => false: .3-.2 is not equal to .1
y === .1            // => true: .2-.1 is equal to .1
```

Because of rounding error, the difference between the approximations of .3 and .2 is not exactly the same as the difference between the approximations of .2 and .1. It is important to understand that this problem is not specific to JavaScript: it affects any programming language that uses binary floating-point numbers.

#### Arbitrary Precision Integers with `BigInt`

BigInt is a numeric type whose values are integers. The type was added to JavaScript mainly to allow the representation of 64-bit integers, which are required for compatibility with many other programming languages and APIs. 

BigInt literals are written as a string of digits followed by a lowercase letter `n`. By default, the are in base 10, but you can use the 0b, 0o, and 0x prefixes for binary, octal, and hexadecimal BigInts:

```
1234n                // A not-so-big BigInt literal
0b111111n            // A binary BigInt
0o7777n              // An octal BigInt
0x8000000000000000n  // => 2n**63n: A 64-bit integer
```

You can use `BigInt()` as a function for converting regular JavaScript numbers or strings to BigInt values.
None of the functions of the `Math` object accept BigInt operands.


#### Dates and Times

JavaScript defines a simple Date class for representing and manipulating the numbers that represent dates and times. JavaScript Dates are objects, but they also have a numeric representation as a `timestamp` that specifies the number of elapsed milliseconds since January 1, 1970.

## Text

The JavaScript type for representing text is the `string`.  **A string is an immutable ordered sequence of 16-bit values, each of which typically represents a Unicode character.** The length of a string is the number of 16-bit values it contains. JavaScript’s strings (and its arrays) use zero-based indexing: the first 16-bit value is at position 0, the second at position 1, and so on. The empty string is the string of length 0. **JavaScript does not have a special type that represents a single element of a string. To represent a single 16-bit value, simply use a string that has a length of 1**.


JavaScript uses the UTF-16 encoding of the Unicode character set, and JavaScript strings are sequences of unsigned 16-bit values. The most commonly used Unicode characters (those from the “basic multilingual plane”) have codepoints that fit in 16 bits and can be represented by one element of a string. Unicode characters whose codepoints do not fit in 16 bits are encoded using the rules of UTF-16 as a sequence (known as a “surrogate pair”) of two 16-bit values. This means that a JavaScript string of length 2 (two 16-bit values) might represent only a single Unicode character:

```
let euro = "€";
let love = "❤";
euro.length   // => 1: this character has one 16-bit element
love.length   // => 2: UTF-16 encoding of ❤ is "\ud83d\udc99"
```

**Most string-manipulation methods defined by JavaScript operate on 16-bit values, not characters. They do not treat surrogate pairs specially, they perform no normalization of the string, and don’t even ensure that a string is well-formed UTF-16.**

**In ES6, however, strings are iterable, and if you use the `for/of loop` or `...` operator with a string, it will iterate the actual characters of the string, not the 16-bit values.**

### String Literals

To include a string in a JavaScript program, simply enclose the characters of the string within a matched pair of single or double quotes or backticks (' or " or `). 

Strings delimited with backticks are a feature of ES6, and allow JavaScript expressions to be embedded within (or interpolated into) the string literal. 

As of ES5, you can break a string literal across multiple lines by ending each line but the last with a backslash (\\). Neither the backslash nor the line terminator that follow it are part of the string literal. If you need to include a newline character in a single-quoted or double-quoted string literal, use the character sequence `\n` (documented in the next section). The ES6 backtick syntax allows strings to be broken across multiple lines, and in this case, the line terminators are part of the string literal:

```
// A string representing 2 lines written on one line:
'two\nlines'

// A one-line string written on 3 lines:
"one\
 long\
 line"

// A two-line string written on two lines:
`the newline character at the end of this line
is included literally in this string`
```

### Escape Sequences in String Literals

The backslash character (\\) has a special purpose in JavaScript strings. Combined with the character that follows it, it represents a character that is not otherwise representable within the string. For example, `\n` is an escape sequence that represents a newline character.

If the `\` character precedes any character other than predefined in javascript, the backslash is simply ignored (although future versions of the language may, of course, define new escape sequences). For example, `\#` is the same as `#`. Finally, as noted earlier, ES5 allows a backslash before a line break to break a string literal across multiple lines.

### Working with Strings

To determine the length of a string—the number of 16-bit values it contains—use the length property of the string:

```
s.length
```

Strings can also be treated like read-only arrays, and you can access individual characters (16-bit values) from a string using square brackets instead of the `charAt()` method:

```
let s = "hello, world";
s[0]                  // => "h"
s[s.length-1]         // => "d"
```

### Template Literals

In ES6 and later, string literals can be delimited with backticks:

```
let s = `hello world`;
```

This is more than just another string `literal syntax`, however, because these `template literals` can include arbitrary JavaScript expressions. The final value of a string literal in backticks is computed by evaluating any included expressions, converting the values of those expressions to strings and combining those computed strings with the literal characters within the backticks:

```
let name = "Bill";
let greeting = `Hello ${ name }.`;  // greeting == "Hello Bill."
```

Everything between the `${ and the matching }` is interpreted as a JavaScript expression. Everything outside the curly braces is normal string literal text. The expression inside the braces is evaluated and then converted to a string and inserted into the template, replacing the dollar sign, the curly braces, and everything in between them.

### Tagged template literals

A powerful but less commonly used feature of template literals is that, if a function name (or “tag”) comes right before the opening backtick, then the text and the values of the expressions within the template literal are passed to the function. The value of this “tagged template literal” is the return value of the function. 

ES6 has one built-in tag function: `String.raw()`. It returns the text within backticks without any processing of backslash escapes:

```
`\n`.length            // => 1: the string has a single newline character
String.raw`\n`.length  // => 2: a backslash character and the letter n
```

Note that even though the tag portion of a tagged template literal is a function, there are no parentheses used in its invocation. In this very specific case, the backtick characters replace the open and close parentheses.

The ability to define your own template tag functions is a powerful feature of JavaScript. 

### Pattern Matching

JavaScript defines a datatype known as a `regular expression` (or RegExp) for describing and matching patterns in strings of text. RegExps are not one of the fundamental datatypes in JavaScript, but they have a literal syntax like numbers and strings do, so they sometimes seem like they are fundamental.

`RegExps` are powerful and commonly used for text processing, however, this section provides a brief overview.

Text between a pair of slashes constitutes a regular expression literal. The second slash in the pair can also be followed by one or more letters, which modify the meaning of the pattern. For example:

```
/^HTML/;             // Match the letters H T M L at the start of a string
/[1-9][0-9]*/;       // Match a nonzero digit, followed by any # of digits
/\bjavascript\b/i;   // Match "javascript" as a word, case-insensitive
```

## Boolean Values

Any JavaScript value can be converted to a boolean value. The following values convert to, and therefore work like, false:

```
undefined
null
0
-0
NaN
""  // the empty string
```

All other values, including all objects (and arrays) convert to, and work like, `true`. `false`, and the six values that convert to it, are sometimes called `falsy` values, and all other values are called `truthy`. Any time JavaScript expects a boolean value, a `falsy` value works like `false` and a `truthy` value works like `true`.

## null and undefined

`null` is a language keyword that evaluates to a special value that is usually used to indicate the absence of a value. Using the `typeof` operator on `null` returns the string “object”, indicating that `null` can be thought of as a special object value that indicates “no object”. In practice, however, `null` is typically regarded as the sole member of its own type, and it can be used to indicate “no value” for numbers and strings as well as objects. 


JavaScript also has a second value that indicates absence of value. The `undefined` value represents a deeper kind of absence. It is the value of variables that have not been initialized and the value you get when you query the value of an object property or array element that does not exist. The `undefined` value is also the return value of functions that do not explicitly return a value and the value of function parameters for which no argument is passed. `undefined` is a predefined global constant (not a language keyword like `null`, though this is not an important distinction in practice) that is initialized to the `undefined` value. If you apply the `typeof` operator to the `undefined` value, it returns “undefined”, indicating that this value is the sole member of a special type.

## Symbols

Symbols were introduced in ES6 to serve as non-string property names. 

To understand Symbols, you need to know that JavaScript’s fundamental Object type is an unordered collection of properties, where each property has a name and a value. Property names are typically (and until ES6, were exclusively) strings. But in ES6 and later, Symbols can also serve this purpose.

```
let strname = "string name";      // A string to use as a property name
let symname = Symbol("propname"); // A Symbol to use as a property name
typeof strname                    // => "string": strname is a string
typeof symname                    // => "symbol": symname is a symbol
let o = {};                       // Create a new object
o[strname] = 1;                   // Define a property with a string name
o[symname] = 2;                   // Define a property with a Symbol name
o[strname]                        // => 1: access the string-named property
o[symname]                        // => 2: access the symbol-named property
```

The `Symbol` type does not have a literal syntax. To obtain a `Symbol` value, you call the `Symbol()` function. This function never returns the same value twice, even when called with the same argument. This means that if you call `Symbol()` to obtain a Symbol value, you can safely use that value as a property name to add a new property to an object and do not need to worry that you might be overwriting an existing property with the same name. Similarly, if you use symbolic property names and do not share those symbols, you can be confident that other modules of code in your program will not accidentally overwrite your properties.

In practice, Symbols serve as a language extension mechanism. When ES6 introduced the `for/of` loop and iterable objects, it needed to define standard method that classes could implement to make themselves iterable. But standardizing any particular string name for this iterator method would have broken existing code, so a symbolic name was used instead. As we’ll see, `Symbol.iterator` is a `Symbol` value that can be used as a method name to make an object iterable.

The `Symbol()` function takes an optional string argument and returns a unique `Symbol` value. If you supply a string argument, that string will be included in the output of the Symbol’s `toString()` method. Note, however, that calling `Symbol()` twice with the same string produces two completely different Symbol values.

JavaScript defines a global `Symbol` registry. The `Symbol.for()` function takes a string argument and returns a `Symbol` value that is associated with the string you pass. If no `Symbol` is already associated with that string, then a new one is created and returned; otherwise, the already existing `Symbol` is returned. That is, the `Symbol.for()` function is completely different than the `Symbol()` function: `Symbol()` never returns the same value twice, but `Symbol.for()` always returns the same value when called with the same string. The string passed to `Symbol.for()` appears in the output of `toString()` for the returned `Symbol`, and it can also be retrieved by calling `Symbol.keyFor()` on the returned Symbol.

```
let s = Symbol.for("shared");
let t = Symbol.for("shared");
s === t          // => true
s.toString()     // => "Symbol(shared)"
Symbol.keyFor(t) // => "shared"
```

## The Global Object

The `global object` is a regular JavaScript object that serves a very important purpose: the properties of this object are the globally defined identifiers that are available to a JavaScript program. When the JavaScript interpreter starts (or whenever a web browser loads a new page), it creates a new global object and gives it an initial set of roperties that define:

- Global constants like `undefined`, `Infinity`, and `NaN`

- Global functions like `isNaN()`, `parseInt()`, and `eval()`

- Constructor functions like `Date()`, `RegExp()`, `String()`, `Object()`, and `Array()`

- Global objects like Math and JSON

The initial properties of the global object are not reserved words, but they deserve to be treated as if they are. 

In Node, the global object has a property named `global` whose value is the global object itself, so you can always refer to the global object by the name global in Node programs.

In web browsers, the Window object serves as the global object for all JavaScript code contained in the browser window it represents. This global Window object has a self-referential window property that can be used to refer to the global object. The Window object defines the core global properties, but it also defines quite a few other globals that are specific to web browsers and client-side JavaScript. Web worker threads have a different global object than the Window with which they are associated. Code in a worker can refer to its global object as `self`.

ES2020 finally defines `globalThis` as the standard way to refer to the global object in any context. As of early 2020, this feature has been implemented by all modern browsers and by Node.

## Type Conversions

`true` converts to 1, and `false` and the empty string convert to 0.

### Conversions and Equality

JavaScript has two operators that test whether two values are equal. The “strict equality operator,” ===, does not consider its operands to be equal if they are not of the same type, and this is almost always the right operator to use when coding. But because JavaScript is so flexible with type conversions, it also defines the == operator with a flexible definition of equality.

```
null == undefined // => true: These two values are treated as equal.
"0" == 0          // => true: String converts to a number before comparing.
0 == false        // => true: Boolean converts to number before comparing.
"0" == false      // => true: Both operands convert to 0 before comparing!
```

Keep in mind that convertibility of one value to another does not imply equality of those two values. If `undefined` is used where a boolean value is expected, for example, it will convert to false. But this does not mean that `undefined == false`. JavaScript operators and statements expect values of various types and perform conversions to those types. The if statement converts undefined to false, but the == operator never attempts to convert its operands to booleans.

### Explicit Conversions

The simplest way to perform an explicit type conversion is to use the `Boolean()`, `Number()`, and `String()` functions:

```
Number("3")    // => 3
String(false)  // => "false":  Or use false.toString()
Boolean([])    // => true
```

Any value other than `null` or `undefined` has a `toString()` method, and the result of this method is usually the same as that returned by the `String()` function.

Certain JavaScript operators perform implicit type conversions and are sometimes used explicitly for the purpose of type conversion. If one operand of the + operator is a string, it converts the other one to a string. The unary + operator converts its operand to a number. And the unary ! operator converts its operand to a boolean and negates it. These facts lead to the following type conversion idioms that you may see in some code:

```
x + ""   // => String(x)
+x       // => Number(x)
x-0      // => Number(x)
!!x      // => Boolean(x): Note double !
```

If you pass a string to the `Number()` conversion function, it attempts to parse that string as an integer or floating-point literal. That function only works for base-10 integers and does not allow trailing characters that are not part of the literal.

The `parseInt()` and `parseFloat()` functions (these are global functions, not methods of any class) are more flexible. Both `parseInt()` and `parseFloat()` skip leading whitespace, parse as many numeric characters as they can, and ignore anything that follows. If the first nonspace character is not part of a valid numeric literal, they return NaN.

`parseInt()` accepts an optional second argument specifying the radix (base) of the number to be parsed.


### Object to Primitive Conversions

One reason for the complexity of JavaScript’s object-to-primitive conversions is that some types of objects have more than one primitive representation. Date objects, for example, can be represented as strings or as numeric timestamps. The JavaScript specification defines three fundamental algorithms for converting objects to primitive values:

- prefer-string

This algorithm returns a primitive value, preferring a string value, if a conversion to string is possible.

- prefer-number

This algorithm returns a primitive value, preferring a number, if such a conversion is possible.

- no-preference

This algorithm expresses no preference about what type of primitive value is desired, and classes can define their own conversions. 

#### Object-to-boolean conversions

Object-to-boolean conversions are trivial: all objects convert to `true`.  Notice that this conversion does not require the use of the object-to-primitive algorithms described, and that it literally applies to all objects, including empty arrays and even the wrapper object `new Boolean(false)`.

#### Object-to-string conversions

When an object needs to be converted to a string, JavaScript first converts it to a primitive using the prefer-string algorithm, then converts the resulting primitive value to a string.

#### Object-to-number conversions

When an object needs to be converted to a number, JavaScript first converts it to a primitive value using the prefer-number algorithm, then converts the resulting primitive value to a number.


Built-in JavaScript functions and methods that expect numeric arguments convert object arguments to numbers in this way, and most (see the exceptions that follow) JavaScript operators that expect numeric operands convert objects to numbers in this way as well.

#### Special case operator conversions

The + operator in JavaScript performs numeric addition and string concatenation. If either of its operands is an object, JavaScript converts them to primitive values using the `no-preference` algorithm. Once it has two primitive values, it checks their types. If either argument is a string, it converts the other to a string and concatenates the strings. Otherwise, it converts both arguments to numbers and adds them.

The `==` and `!=` operators perform equality and inequality testing in a loose way that allows type conversions. If one operand is an object and the other is a primitive value, these operators convert the object to primitive using the `no-preference` algorithm and then compare the two primitive values.

Finally, the relational operators <, <=, >, and >= compare the order of their operands and can be used to compare both numbers and strings. If either operand is an object, it is converted to a primitive value using the `prefer-number` algorithm. Note, however, that unlike the object-to-number conversion, the primitive values returned by the prefer-number conversion are not then converted to numbers.

#### The `toString()` and `valueOf()` methods

All objects inherit two conversion methods that are used by object-to-primitive conversions, and before we can explain the `prefer-string`, `prefer-number`, and `no-preference` conversion algorithms, we have to explain these two methods.

The first method is `toString()`, and its job is to return a string representation of the object. The default `toString()` method does not return a very interesting value:

```
({x: 1, y: 2}).toString()    // => "[object Object]"
```

The other object conversion function is called `valueOf()`. The job of this method is less well defined: it is supposed to convert an object to a primitive value that represents the object, if any such primitive value exists. Objects are compound values, and most objects cannot really be represented by a single primitive value, so the default `valueOf()` method simply returns the object itself rather than returning a primitive. Wrapper classes such as String, Number, and Boolean define `valueOf()` methods that simply return the wrapped primitive value. Arrays, functions, and regular expressions simply inherit the default method. Calling `valueOf()` for instances of these types simply returns the object itself. 

#### Object-to-primitive conversion algorithms

- The `prefer-string` algorithm first tries the `toString()` method. If the method is defined and returns a primitive value, then JavaScript uses that primitive value (even if it is not a string!). If `toString()` does not exist or if it returns an object, then JavaScript tries the `valueOf()` method. If that method exists and returns a primitive value, then JavaScript uses that value. Otherwise, the conversion fails with a TypeError.

- The `prefer-number` algorithm works like the `prefer-string` algorithm, except that it tries `valueOf()` first and `toString()` second.


- The `no-preference` algorithm depends on the class of the object being converted. If the object is a `Date` object, then JavaScript uses the `prefer-string` algorithm. For any other object, JavaScript uses the `prefer-number` algorithm.

The rules described here are true for all built-in JavaScript types and are the default rules for any classes you define yourself.

## Variable Declaration and Assignment

One of the most fundamental techniques of computer programming is the use of names—or `identifiers`—to represent values. Binding a name to a value gives us a way to refer to that value and use it in the programs we write. When we do this, we typically say that we are assigning a value to a variable. The term “variable” implies that new values can be assigned: that the value associated with the variable may vary as our program runs. If we permanently assign a value to a name, then we call that name a constant instead of a variable.

Before you can use a variable or constant in a JavaScript program, you must declare it. In ES6 and later, this is done with the let and const keywords, which we explain next. Prior to ES6, variables were declared with var, which is more idiosyncratic and is explained later on in this section.

```
let i;
let sum;
let i, sum;
let message = "hello";
let i = 0, j = 0, k = 0;
let x = 2, y = x*x; // Initializers can use previously declared variables
```

If you don’t specify an initial value for a variable with the `let` statement, the variable is declared, but its value is undefined until your code assigns a value to it.

It may seem surprising, but you can also use const to declare the loop “variables” for `for/in` and `for/of` loops, as long as the body of the loop does not reassign a new value. In this case, the const declaration is just saying that the value is constant for the duration of one loop iteration:

```
for(const datum of data) console.log(datum);
for(const property in object) console.log(property);
```

### Variable and constant scope

The `scope` of a variable is the region of your program source code in which it is defined. Variables and constants declared with `let` and `const` are block scoped. This means that they are only defined within the block of code in which the `let` or `const` statement appears. JavaScript class and function definitions are blocks, and so are the bodies of `if/else` statements, `while` loops, `for` loops, and so on. Roughly speaking, if a variable or constant is declared within a set of curly braces, then those curly braces delimit the region of code in which the variable or constant is defined (though of course it is not legal to reference a variable or constant from lines of code that execute before the let or const statement that declares the variable). **Variables and constants declared as part of a `for`, `for/in`, or `for/of` loop have the loop body as their scope, even though they technically appear outside of the curly braces.**

When a declaration appears at the top level, outside of any code blocks, we say it is a `global` variable or constant and has global scope. In Node and in client-side JavaScript modules, the scope of a global variable is the file that it is defined in.

### Repeated declarations

It is a syntax error to use the same name with more than one let or const declaration in the same scope. It is legal (though a practice best avoided) to declare a new variable with the same name in a nested scope:

```
const x = 1;        // Declare x as a global constant
if (x === 1) {
    let x = 2;      // Inside a block x can refer to a different value
    console.log(x); // Prints 2
}
console.log(x);     // Prints 1: we're back in the global scope now
let x = 3;          // ERROR! Syntax error trying to re-declare x
```

### Variable Declarations with var

In versions of JavaScript before ES6, the only way to declare a variable is with the `var` keyword, and there is no way to declare constants.

Although `var` and `let` have the same syntax, there are important differences in the way they work:


- Variables declared with `var` do not have block scope. Instead, they are scoped to the body of the containing function no matter how deeply nested they are inside that function.

- If you use `var` outside of a function body, it declares a global variable. But global variables declared with `var` differ from globals declared with `let` in an important way. Globals declared with `var` are implemented as properties of the global object. The global object can be referenced as `globalThis`. So if you write var `x = 2;` outside of a function, it is like you wrote `globalThis.x = 2;`. Note however, that the analogy is not perfect: the properties created with global var declarations cannot be deleted with the delete operator. Global variables and constants declared with `let` and `const` are not properties of the global object.

- Unlike variables declared with `let`, it is legal to declare the same variable multiple times with `var`. And because var variables have function scope instead of block scope, it is actually common to do this kind of redeclaration.  

- One of the most unusual features of `var` declarations is known as `hoisting`. When a variable is declared with `var`, the declaration is lifted up (or “hoisted”) to the top of the enclosing function. The initialization of the variable remains where you wrote it, but the definition of the variable moves to the top of the function. So variables declared with `var` can be used, without error, anywhere in the enclosing function. If the initialization code has not run yet, then the value of the variable may be `undefined`, but you won’t get an error if you use the variable before it is initialized. (This can be a source of bugs and is one of the important misfeatures that `let` corrects: if you declare a variable with `let` but attempt to use it before the let statement runs, you will get an actual error instead of just seeing an `undefined` value.)

#### Using Undeclared Variables

In strict mode, if you attempt to use an undeclared variable, you’ll get a reference error when you run your code. Outside of strict mode, however, if you assign a value to a name that has not been declared with `let`, `const`, or `var`, you’ll end up creating a new global variable. It will be a global no matter now deeply nested within functions and blocks your code is, which is almost certainly not what you want, is bug-prone, and is one of the best reasons for using strict mode!

Global variables created in this accidental way are like global variables declared with `var`: they define properties of the global object. But unlike the properties defined by proper `var` declarations, these properties can be deleted with the `delete` operator.

### Destructuring Assignment

ES6 implements a kind of compound declaration and assignment syntax known as `destructuring assignment`. In a destructuring assignment, the value on the righthand side of the equals sign is an array or object (a “structured” value), and the lefthand side specifies one or more variable names using a syntax that mimics array and object literal syntax. When a destructuring assignment occurs, one or more values are extracted (“destructured”) from the value on the
right and stored into the variables named on the left.

The number of variables on the left of a destructuring assignment does not have to match the number of array elements on the right. Extra variables on the left are set to `undefined`, and extra values on the right are ignored. The list of variables on the left can include extra commas to skip certain values on the right:

```
let [x,y] = [1];     // x == 1; y == undefined
[x,y] = [1,2,3];     // x == 1; y == 2
[,x,,y] = [1,2,3,4]; // x == 2; y == 4
```

If you want to collect all unused or remaining values into a single variable when `destructuring an array`, use three dots (`...`) before the last variable name on the left-hand side:

```
let [x, ...y] = [1,2,3,4];  // y == [2,3,4]
```

Destructuring assignment can be used with nested arrays. In this case, the lefthand side of the assignment should look like a nested array literal:

```
let [a, [b, c]] = [1, [2,2.5], 3]; // a == 1; b == 2; c == 2.5
```

A powerful feature of array destructuring is that it does not actually require an array! You can use any iterable object on the righthand side of the assignment; any object that can be used with a `for/of` loop can also be destructured:

```
let [first, ...rest] = "Hello"; // first == "H"; rest == ["e","l","l","o"]
```

Destructuring assignment can also be performed when the righthand side is an object value. In this case, the lefthand side of the assignment looks something like an object literal: a comma-separated list of variable names within curly braces:

```
let transparent = {r: 0.0, g: 0.0, b: 0.0, a: 1.0}; // A RGBA color
let {r, g, b} = transparent;  // r == 0.0; g == 0.0; b == 0.0
```

The next example copies global functions of the `Math` object into variables, which might simplify code that does a lot of trigonometry:

```
// Same as const sin=Math.sin, cos=Math.cos, tan=Math.tan
const {sin, cos, tan} = Math;
```

Notice in the code here that the Math object has many properties other than the three that are destructured into individual variables. Those that are not named are simply ignored. If the lefthand side of this assignment had included a variable whose name was not a property of Math, that variable would simply be assigned `undefined`.

In each of these object destructuring examples, we have chosen variable names that match the property names of the object we’re destructuring. This keeps the syntax simple and easy to understand, but it is not required. Each of the identifiers on the lefthand side of an object destructuring assignment can also be a colon-separated pair of identifiers, where the first is the name of the property whose value is to be assigned and the second is the name of the variable to assign it to:

```
// Same as const cosine = Math.cos, tangent = Math.tan;
const { cos: cosine, tan: tangent } = Math;
```

Destructuring assignment becomes even more complicated when it is used with nested objects, or arrays of objects, or objects of arrays, but it is legal:

```
let points = [{x: 1, y: 2}, {x: 3, y: 4}];     // An array of two point objects
let [{x: x1, y: y1}, {x: x2, y: y2}] = points; // destructured into 4 variables.
(x1 === 1 && y1 === 2 && x2 === 3 && y2 === 4) // => true
```

Or, instead of destructuring an array of objects, we could destructure an object of arrays:

```
let points = { p1: [1,2], p2: [3,4] };         // An object with 2 array props
let { p1: [x1, y1], p2: [x2, y2] } = points;   // destructured into 4 vars
(x1 === 1 && y1 === 2 && x2 === 3 && y2 === 4) // => true
```
