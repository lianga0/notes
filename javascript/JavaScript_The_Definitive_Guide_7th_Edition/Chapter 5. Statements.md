# Chapter 5. Statements

Chapter 4 described *expressions* as JavaScript phrases. By that analogy, *statements* are JavaScript sentences or commands. Just as English sentences are terminated and separated from one another with periods, JavaScript statements are terminated with semicolons. Expressions are evaluated to produce a value, but statements are executed to make something happen.

One way to “make something happen” is to evaluate an expression that has side effects. Expressions with side effects, such as assignments and function invocations, can stand alone as statements, and when used this way are known as expression statements. A similar category of statements are the *declaration statements* that declare new variables and define new functions.

JavaScript programs are nothing more than a sequence of statements to execute. By default, the JavaScript interpreter executes these statements one after another in the order they are written. Another way to “make something happen” is to alter this default order of execution, and JavaScript has a number of statements or control structures that do just this:

**Conditionals**

Statements like `if` and `switch` that make the JavaScript interpreter execute or skip other statements depending on the value of an expression

**Loops**

Statements like `while` and `for` that execute other statements repetitively

**Jumps**

Statements like `break`, `return`, and `throw` that cause the interpreter to jump to another part of the program

A JavaScript program is simply a sequence of statements, separated from one another with semicolons, so once you are familiar with the statements of JavaScript, you can begin writing JavaScript programs.

## Expression Statements

The simplest kinds of statements in JavaScript are expressions that have side effects.

Function calls are another major category of expression statements.

## Compound and Empty Statements

Just as the comma operator combines multiple expressions into a single expression, a *statement block* combines multiple statements into a single compound statement. A *statement block* is simply a sequence of statements enclosed within curly braces. Thus, the following lines act as a single statement and can be used anywhere that JavaScript expects a single statement:

```
{
    x = Math.PI;
    cx = Math.cos(x);
    console.log("cos(π) = " + cx);
}
```

Just as expressions often contain subexpressions, many JavaScript statements contain substatements. Formally, JavaScript syntax usually allows a single substatement. For example, the `while` loop syntax includes a single statement that serves as the body of the loop. Using a statement block, you can place any number of statements within this single allowed substatement.

A compound statement allows you to use multiple statements where JavaScript syntax expects a single statement. The empty statement is the opposite: it allows you to include no statements where one is expected. The empty statement looks like this:

```
;
```

The JavaScript interpreter takes no action when it executes an empty statement. The empty statement is occasionally useful when you want to create a loop that has an empty body. Consider the following for loop:

```
// Initialize an array a
for(let i = 0; i < a.length; a[i++] = 0) ;
```

In this loop, all the work is done by the expression `a[i++] = 0`, and no loop body is necessary. JavaScript syntax requires a statement as a loop body, however, so an empty statement—just a bare semicolon—is used.

Note that the accidental inclusion of a semicolon after the right parenthesis of a `for` loop, `while` loop, or `if` statement can cause frustrating bugs that are difficult to detect. For example, the following code probably does not do what the author intended:

```
if ((a === 0) || (b === 0));  // Oops! This line does nothing...
    o = null;                 // and this line is always executed.
```

When you intentionally use the empty statement, it is a good idea to comment your code in a way that makes it clear that you are doing it on purpose. For example:

```
for(let i = 0; i < a.length; a[i++] = 0) /* empty */ ;
```

## Conditionals

Conditional statements execute or skip other statements depending on the value of a specified expression. These statements are the decision points of your code, and they are also sometimes known as “branches.”

### `if`

The `if` statement is the fundamental control statement that allows JavaScript to make decisions, or, more precisely, to execute statements conditionally. This statement has two forms. The first is:

```
if (expression)
    statement
```

Note that the parentheses around the expression are a required part of the syntax for the if statement.

JavaScript syntax requires a single statement after the if keyword and parenthesized expression, but you can use a statement block to combine multiple statements into one. 

The second form of the `if` statement introduces an else clause that is executed when *expression* is false. Its syntax is:

```
if (expression)
    statement1
else
    statement2
```

When you have nested `if` statements with `else` clauses, some caution is required to ensure that the else clause goes with the appropriate `if` statement. Consider the following lines:

```
i = j = 1;
k = 2;
if (i === j)
    if (j === k)
        console.log("i equals k");
else
    console.log("i doesn't equal j");    // WRONG!!
```

In this example, the inner `if` statement forms the single statement allowed by the syntax of the outer `if` statement. Unfortunately, it is not clear (except from the hint given by the indentation) which `if` the else goes with. And in this example, the indentation is wrong, because a JavaScript interpreter actually interprets the previous
example as:

```
if (i === j) {
    if (j === k)
        console.log("i equals k");
    else
        console.log("i doesn't equal j");    // OOPS!
}
```

The rule in JavaScript (as in most programming languages) is that by default an `else` clause is part of the nearest `if` statement. 

### else if

```
if (n === 1) {
    // Execute code block #1
} else if (n === 2) {
    // Execute code block #2
} else if (n === 3) {
    // Execute code block #3
} else {
    // If all else fails, execute block #4
}
```

### switch

```
switch(n) {
case 1:                        // Start here if n === 1
    // Execute code block #1.
    break;                     // Stop here
case 2:                        // Start here if n === 2
    // Execute code block #2.
    break;                     // Stop here
case 3:                        // Start here if n === 3
    // Execute code block #3.
    break;                     // Stop here
default:                       // If all else fails...
    // Execute code block #4.
    break;                     // Stop here
}
```

When a switch executes, it computes the value of *expression* and then looks for a case label whose expression evaluates to the same value (where sameness is determined by the `===` operator). If it finds one, it starts executing the block of code at the statement labeled by the case. If it does not find a case with a matching value, it looks for a statement labeled `default:`. If there is no `default:` label, the switch statement skips the block of code altogether.

The `case` clauses in a switch statement specify only the starting point of the desired code; they do not specify any ending point. In the absence of `break` statements, a switch statement begins executing its block of code at the case label that matches the value of its expression and continues executing statements until it reaches the end of the block. 

When using switch inside a function, however, you may use a `return` statement instead of a break statement. Both serve to terminate the switch statement and prevent execution from falling through to the next case.

## Loops

The *looping statements* are those that bend that path back upon itself to repeat portions of your code. JavaScript has five looping statements: `while`, `do/while`, `for`, `for/of` (and its `for/await` variant), and `for/in`.

### while

The `while` statement is JavaScript’s basic loop. It has the following

```
syntax:
while (expression)
    statement
```

To execute a `while` statement, the interpreter first evaluates `expression`. If the value of the `expression` is falsy, then the interpreter skips over the `statement` that serves as the loop body and moves on to the next statement in the program. If, on the other hand, the `expression` is truthy, the interpreter executes the statement and repeats, jumping back to the top of the loop and evaluating expression again. Another way to say this is that the interpreter executes `statement` repeatedly `while` the `expression` is truthy.

### `do/while`

The `do/while` loop is like a `while` loop, except that the loop `expression` is tested at the bottom of the loop rather than at the top. This means that the body of the loop is always executed at least once. The syntax is:

```
do
    statement
while (expression);
```

Note: the `do/while` loop must always be terminated with a semicolon. 

### for

```
for(initialize ; test ; increment)
    statement
```

*initialize*, *test*, and *increment* are three expressions (separated by semicolons) that are responsible for initializing, testing, and incrementing the loop variable. Putting them all in the first line of the loop makes it easy to understand what a `for` loop is doing and prevents mistakes such as forgetting to initialize or increment the loop variable.

The simplest way to explain how a for loop works is to show the equivalent `while` loop:

```
initialize;
while(test) {
    statement
    increment;
}
```
In other words, the *initialize* expression is evaluated once, before the loop begins. JavaScript also allows *initialize* to be a variable declaration statement so that you can declare and initialize a loop counter at the same time. The *test* expression is evaluated before each iteration and controls whether the body of the loop is executed. If *test* evaluates to a truthy value, the statement that is the body of the loop is executed. Finally, the *increment* expression is evaluated.


Any of the three expressions may be omitted from a `for` loop, but the two semicolons are required. If you omit the test expression, the loop repeats forever, and `for(;;)` is another way of writing an infinite loop, like `while(true)`.

### `for/of`

ES6 defines a new loop statement: `for/of`. 

The `for/of` loop works with *iterable* objects.

Arrays are iterated “live”—changes made during the iteration may affect the outcome of the iteration. If we modify the preceding code by adding the line `data.push(sum);` inside the loop body, then we create an infinite loop because the iteration can never reach the last element of the array.

#### `for/of` with objects

Objects are not (by default) iterable. Attempting to use `for/of` on a regular object throws a `TypeError` at runtime:

```
let o = { x: 1, y: 2, z: 3 };
for(let element of o) { // Throws TypeError because o is not iterable
    console.log(element);
}
```

If you want to iterate through the properties of an object, you can use the `for/in` loop, or use `for/of` with the `Object.keys()` method:

```
let o = { x: 1, y: 2, z: 3 };
let keys = "";
for(let k of Object.keys(o)) {
    keys += k;
}
keys  // => "xyz"
```

This works because `Object.keys()` returns an array of property names for an object, and arrays are iterable with `for/of`. 

If you don’t care about the keys of an object, you can also iterate through their corresponding values like this:

```
let sum = 0;
for(let v of Object.values(o)) {
    sum += v;
}
sum // => 6
```

And if you are interested in both the keys and the values of an object’s properties, you can use `for/of` with` Object.entries()` and destructuring assignment:

```
let pairs = "";
for(let [k, v] of Object.entries(o)) {
    pairs += k + v;
}
pairs  // => "x1y2z3"
```

`Object.entries()` returns an array of arrays, where each inner array represents a key/value pair for one property of the object. We use destructuring assignment in this code example to unpack those inner arrays into two individual variables.

#### `for/of` with strings

Strings are iterable character-by-character in ES6:

```
let frequency = {};
for(let letter of "mississippi") {
    if (frequency[letter]) {
        frequency[letter]++;
    } else {
        frequency[letter] = 1;
    }
}
frequency   // => {m: 1, i: 4, s: 4, p: 2}
```

Note that strings are iterated by Unicode codepoint, not by UTF-16 character. The string "I💓" has a `.length` of 3 (because the one emoji character requires two UTF-16 characters to represent). But if you iterate that string with `for/of`, the loop body will run two times, once for each of the three code points “I” and “💓”.

#### `for/of` with `Set` and `Map`

The built-in ES6 `Set` and `Map` classes are iterable.  

When you iterate a `Set` with `for/of`, the loop body runs once for each element of the set.

Maps are an interesting case because the iterator for a Map object does not iterate the Map keys, or the Map values, but *key/value* pairs. Each time through the iteration, the iterator returns an array whose first element is a key and whose second element is the corresponding value.  Given a Map `m`, you could iterate and destructure its *key/value* pairs like this:

```
let m = new Map([[1, "one"]]);
for(let [key, value] of m) {
    key    // => 1
    value  // => "one"
}
```

#### Asynchronous iteration with for/await

ES2018 introduces a new kind of iterator, known as an asynchronous iterator, and a variant on the `for/of` loop, known as the `for/await` loop that works with asynchronous iterators.

```
async function printStream(stream) {
    for await (let chunk of stream) {
        console.log(chunk);
    }
}
```

### `for/in`

A `for/in` loop looks a lot like a `for/of` loop, with the of keyword changed to in. While a `for/of` loop requires an iterable object after the `of`, a `for/in` loop works with any object after the `in`. The `for/of` loop is new in ES6, but `for/in` has been part of JavaScript since the very beginning (which is why it has the more natural sounding syntax).

The `for/in` statement loops through the property names of a specified object. The syntax looks like this:

```
for (variable in object)
    statement
```

And you might use a `for/in` loop like this:

```
for(let p in o) {      // Assign property names of o to variable p
    console.log(o[p]); // Print the value of each property
}
```

To execute a `for/in` statement, the JavaScript interpreter first evaluates the object expression. If it evaluates to `null` or `undefined`, the interpreter skips the loop and moves on to the next statement. The interpreter now executes the body of the loop once for each enumerable property of the object. Before each iteration, however, the interpreter evaluates the variable expression and assigns the name of the property (a string value) to it.

The `for/in` loop does not actually enumerate all properties of an object. It does not enumerate properties whose names are symbols. And of the properties whose names are strings, it only loops over the enumerable properties. The various built-in methods defined by core JavaScript are not enumerable. All objects have a `toString()` method, for example, but the `for/in` loop does not enumerate this `toString` property. In addition to built-in methods, many other properties of the built-in objects are non-enumerable. All properties and methods defined by your code are enumerable, by default.

Enumerable inherited properties are also enumerated by the `for/in` loop. This means that if you use `for/in` loops and also use code that defines properties that are inherited by all objects, then your loop may not behave in the way you expect. For this reason, many programmers prefer to use a `for/of` loop with `Object.keys()` instead of a `for/in` loop.

If the body of a `for/in` loop deletes a property that has not yet been enumerated, that property will not be enumerated. If the body of the loop defines new properties on the object, those properties may or may not be enumerated.

## Jumps

The `break` statement makes the interpreter jump to the end of a loop or other statement. `continue` makes the interpreter skip the rest of the body of a loop and jump back to the top of a loop to begin a new iteration. JavaScript allows statements to be named, or labeled, and `break` and `continue` can identify the target loop or other statement label.

The `return` statement makes the interpreter jump from a function invocation back to the code that invoked it and also supplies the value for the invocation. The `throw` statement is a kind of interim return from a generator function. The throw statement *raises*, or *throws*, an exception and is designed to work with the `try/catch/finally` statement, which establishes a block of exception-handling code. This is a complicated kind of jump statement: when an exception is thrown, the interpreter jumps to the nearest enclosing exception handler, which may be in the same function or up the call stack in an invoking function.

### Labeled Statements

Any statement may be **labeled** by preceding it with an identifier and a colon:

```
identifier: statement
```

By labeling a statement, you give it a name that you can use to refer to it elsewhere in your program. **You can label any statement, although it is only useful to label statements that have bodies, such as loops and conditionals.** By giving a loop a name, you can use `break` and `continue` statements inside the body of the loop to exit the loop or to jump directly to the top of the loop to begin the next iteration. `break` and `continue` are the only JavaScript statements that use statement labels; Here is an example of a labeled while loop and a continue statement that uses the label.

```
mainloop: while(token !== null) {
    // Code omitted...
    continue mainloop;  // Jump to the next iteration of the named loop
    // More code omitted...
}
```

The *identifier* you use to label a statement can be any legal JavaScript identifier that is not a reserved word. The namespace for labels is different than the namespace for variables and functions, so you can use the same identifier as a statement label and as a variable or function name. Statement labels are defined only within the statement to which they apply (and within its substatements, of course). A statement may not have the same label as a statement that contains it, but two statements may have the same label as long as neither one is nested within the other. Labeled statements may themselves be labeled. Effectively, this means that any statement may have multiple labels.


### break

The break statement, used alone, causes the innermost enclosing loop
or switch statement to exit immediately. Its syntax is simple:

```
break;
```

Because it causes a `loop` or `switch` to exit, this form of the `break` statement is legal only if it appears inside one of these statements.

JavaScript also allows the `break` keyword to be followed by a statement label (just the identifier, with no colon):

```
break labelname;
```

When `break` is used with a label, it jumps to the end of, or terminates, the enclosing statement that has the specified label. It is a syntax error to use `break` in this form if there is no enclosing statement with the specified label. With this form of the `break` statement, the named statement need not be a `loop` or `switch`: `break` can “break out of” any enclosing statement. This statement can even be a statement block grouped within curly braces for the sole purpose of naming the block with a label.

You need the labeled form of the `break` statement when you want to break out of a statement that is not the nearest enclosing `loop` or a `switch`. The following code demonstrates:

```
let matrix = getData();  // Get a 2D array of numbers from somewhere
// Now sum all the numbers in the matrix.
let sum = 0, success = false;
// Start with a labeled statement that we can break out of if errors occur
computeSum: if (matrix) {
    for(let x = 0; x < matrix.length; x++) {
        let row = matrix[x];
        if (!row) break computeSum;
        for(let y = 0; y < row.length; y++) {
            let cell = row[y];
            if (isNaN(cell)) break computeSum;
            sum += cell;
        }
    }
    success = true;
}
// The break statements jump here. If we arrive here with success == false
// then there was something wrong with the matrix we were given.
// Otherwise, sum contains the sum of all cells of the matrix.
```

Finally, note that a `break` statement, with or without a label, can not transfer control across function boundaries. You cannot label a function definition statement, for example, and then use that label inside the function.

### continue

The `continue` statement is similar to the `break` statement. Instead of exiting a loop, however, continue restarts a loop at the next iteration. The `continue` statement’s syntax is just as simple as the `break` statement’s:

```
continue;
```

The `continue` statement can also be used with a label: 

```
continue labelname;
```

**The `continue` statement, in both its labeled and unlabeled forms, can be used only within the body of a loop. Using it anywhere else causes a syntax error.**

When the `continue` statement is executed, the current iteration of the enclosing loop is terminated, and the next iteration begins. This means different things for different types of loops:

- In a `while` loop, the specified expression at the beginning of the loop is tested again, and if it’s `true`, the loop body is executed starting from the top.

- In a `do/while` loop, execution skips to the bottom of the loop, where the loop condition is tested again before restarting the loop at the top.


- In a `for` loop, the increment expression is evaluated, and the test expression is tested again to determine if another iteration should be done.

- In a `for/of` or `for/in` loop, the loop starts over with the next iterated value or next property name being assigned to the specified variable.

Like the `break` statement, the `continue` statement can be used in its labeled form within nested `loops` when the loop to be restarted is not the immediately enclosing loop. Also, as with the `break` statement, line breaks are not allowed between the `continue` statement and its labelname.

### return

A `return` statement within a function specifies the value of invocations of that function. Here’s the syntax of the return statement:

```
return expression;
```

A `return` statement may appear only within the body of a function. It is a syntax error for it to appear anywhere else. When the `return` statement is executed, the function that contains it returns the value of expression to its caller. 

With no `return` statement, a function invocation simply executes each of the statements in the function body in turn until it reaches the end of the function and then returns to its caller. In this case, the invocation expression evaluates to `undefined`.  

The return statement can also be used without an expression to make the function return `undefined` to its caller.

Because of JavaScript’s automatic semicolon insertion, you cannot include a line break between the return keyword and the expression that follows it.

### yield

The `yield` statement is much like the `return` statement but is used only in ES6 generator functions to produce the next value in the generated sequence of values without actually returning:

```
// A generator function that yields a range of integers
function* range(from, to) {
    for(let i = from; i <= to; i++) {
        yield i;
    }
}
```

### throw

An `exception` is a signal that indicates that some sort of exceptional condition or error has occurred. To `throw` an exception is to signal such an error or exceptional condition. To `catch` an exception is to handle it—to take whatever actions are necessary or appropriate to recover from the exception. In JavaScript, exceptions are thrown whenever a runtime error occurs and whenever the program explicitly throws one using the `throw` statement. Exceptions are caught with the `try/catch/finally` statement.

The throw statement has the following syntax:

```
throw expression;
```

*expression* may evaluate to a value of any type. The `Error` class and its subclasses are used when the JavaScript interpreter itself throws an error, and you can use them as well. An Error object has a `name` property that specifies the type of error and a `message` property that holds the string passed to the constructor function. 

When an exception is thrown, the JavaScript interpreter immediately stops normal program execution and jumps to the nearest exception handler. Exception handlers are written using the catch clause of the `try/catch/finally` statement. If the block of code in which the exception was thrown does not have an associated `catch` clause, the interpreter checks the next-highest enclosing block of code to see if it has an exception handler associated with it. This continues until a handler is found. If an exception is thrown in a function that does not contain a t`ry/catch/finally` statement to handle it, the exception propagates up to the code that invoked the function. In this way, exceptions propagate up through the lexical structure of JavaScript methods and up the call stack. If no exception handler is ever found, the exception is treated as an error and is reported to the user.

### `try/catch/finally`

The `try/catch/finally` statement is JavaScript’s exception handling mechanism. The `try` clause of this statement simply defines the block of code whose exceptions are to be handled. The `try` block is followed by a `catch` clause, which is a block of statements that are invoked when an exception occurs anywhere within the try block. The `catch` clause is followed by a `finally` block containing cleanup code that is guaranteed to be executed, regardless of what happens in the `try` block. Both the `catch` and `finally` blocks are optional, but a `try` block must be accompanied by at least one of these blocks. The `try`, `catch`, and `finally` blocks all begin and end with curly braces. These braces are a required part of the syntax and cannot be omitted, even if a clause contains only a single statement.

The following code illustrates the syntax and purpose of the `try/catch/finally` statement:

```
try {
    // Normally, this code runs from the top of the block to the bottom
    // without problems. But it can sometimes throw an exception,
    // either directly, with a throw statement, or indirectly, by calling
    // a method that throws an exception.
}
catch(e) {
    // The statements in this block are executed if, and only if, the try
    // block throws an exception. These statements can use the local variable
    // e to refer to the Error object or other value that was thrown.
    // This block may handle the exception somehow, may ignore the
    // exception by doing nothing, or may rethrow the exception with throw.
}
finally {
    // This block contains statements that are always executed, regardless of
    // what happens in the try block. They are executed whether the try
    // block terminates:
    //   1) normally, after reaching the bottom of the block
    //   2) because of a break, continue, or return statement
    //   3) with an exception that is handled by a catch clause above
    //   4) with an uncaught exception that is still propagating
}
```

Note that the `catch` keyword is generally followed by an identifier in parentheses. This identifier is like a function parameter. When an exception is caught, the value associated with the exception (an `Error` object, for example) is assigned to this parameter. The identifier associated with a `catch` clause has block scope—it is only defined within the `catch` block.

The `finally` clause is guaranteed to be executed if any portion of the `try` block is executed, regardless of how the code in the `try` block completes. It is generally used to clean up after the code in the `try` clause.

In the normal case, the JavaScript interpreter reaches the end of the `try` block and then proceeds to the `finally` block, which performs any necessary cleanup. If the interpreter left the `try` block because of a `return`, `continue`, or `break` statement, the `finally` block is executed before the interpreter jumps to its new destination.

If an exception occurs in the `try` block and there is an associated `catch` block to handle the exception, the interpreter first executes the `catch` block and then the `finally` block. If there is no local `catch` block to handle the exception, the interpreter first executes the finally `block` and then jumps to the nearest containing `catch` clause.

**If a `finally` block itself causes a jump with a `return`, `continue`, `break`, or `throw` statement, or by calling a method that throws an exception, the interpreter abandons whatever jump was pending and performs the new jump. For example, if a `finally` clause throws an exception, that exception replaces any exception that was in the process of being thrown. If a `finally` clause issues a `return` statement, the method returns normally, even if an exception has been thrown and has not yet been handled.**

`try` and `finally` can be used together without a `catch` clause. In this case, the finally block is simply cleanup code that is guaranteed to be executed, regardless of what happens in the `try` block. 

In ES2019 and later, you can omit the parentheses and the identifier and use the `catch` keyword bare in this case. Here is an example:

```
// Like JSON.parse(), but return undefined instead of throwing an error
function parseJSON(s) {
    try {
        return JSON.parse(s);
    } catch {
        // Something went wrong but we don't care what it was
        return undefined;
    }
}
```

##  Miscellaneous Statements

### with

The `with` statement runs a block of code as if the properties of a specified object were variables in scope for that code. It has the following syntax:

```
with (object)
    statement
```

This statement creates a temporary scope with the properties of object as variables and then executes statement within that scope.

The `with` statement is forbidden in strict mode and should be considered deprecated in *non-strict* mode: avoid using it whenever possible. JavaScript code that uses with is difficult to optimize and is likely to run significantly more slowly than the equivalent code written without the with statement.

The common use of the with statement is to make it easier to work with deeply nested object hierarchies. 


###  debugger

**The debugger statement normally does nothing.** If, however, a debugger program is available and is running, then an implementation may (but is not required to) perform some kind of debugging action. In practice, this statement acts like a breakpoint: execution of JavaScript code stops, and you can use the debugger to print variables’ values, examine the call stack, and so on. Suppose, for example, that you are getting an exception in your function `f()` because it is being called with an `undefined` argument, and you can’t figure out where this call is coming from. To help you in debugging this problem, you might alter `f()` so that it begins like this:

```
function f(o) {
  if (o === undefined) debugger;  // Temporary line for debugging purposes
  ...                             // The rest of the function goes here.
}
```

Now, when `f()` is called with no argument, execution will stop, and you can use the debugger to inspect the call stack and find out where this incorrect call is coming from.

Note that it is not enough to have a debugger available: the debugger statement won’t start the debugger for you. If you’re using a web browser and have the developer tools console open, however, this statement will cause a breakpoint.


### use strict

"use strict" is a *directive* introduced in ES5. Directives are not statements. There are two important differences between the "use strict" directive and regular statements:

- It does not include any language keywords: the directive is just an expression statement that consists of a special string literal (in single or double quotes).

- It can appear only at the start of a script or at the start of a function body, before any real statements have appeared.

The purpose of a "use strict" directive is to indicate that the code that follows (in the script or function) is strict code. The top-level (nonfunction) code of a script is strict code if the script has a "use strict" directive. A function body is strict code if it is defined within strict code or if it has a "use strict" directive. Code passed to the `eval()` method is strict code if `eval()` is called from strict code or if the string of code includes a "use strict" directive. In addition to code explicitly declared to be strict, any code in a class body or in an ES6 module is automatically strict code. This means that if all of your JavaScript code is written as modules, then it is all automatically strict, and you will never need to use an explicit "use strict" directive.

Strict code is executed in *strict mode*. Strict mode is a restricted subset of the language that fixes important language deficiencies and provides stronger error checking and increased security. Because strict mode is not the default, old JavaScript code that still uses the deficient legacy features of the language will continue to run correctly. The differences between strict mode and non-strict mode are the following (the first three are particularly important):

- The `with` statement is not allowed in strict mode.

- In strict mode, all variables must be declared: a `ReferenceError` is thrown if you assign a value to an identifier that is not a declared variable, function, function parameter, `catch` clause parameter, or property of the global object. (In non-strict mode, this implicitly declares a global variable by adding a new property to the global object.)

- In strict mode, functions invoked as functions (rather than as methods) have a `this` value of `undefined`. (In non-strict mode, functions invoked as functions are always passed the global object as their this value.) Also, in strict mode, when a function is invoked with `call()` or `apply()`, the `this` value is exactly the value passed as the first argument to `call()` or `apply()`. (In non-strict mode, `null` and `undefined` values are replaced with the global object and nonobject values are converted to objects.)

- In strict mode, assignments to nonwritable properties and attempts to create new properties on non-extensible objects throw a `TypeError`. (In non-strict mode, these attempts fail silently.)

- In strict mode, code passed to` eval()` cannot declare variables or define functions in the caller’s scope as it can in non-strict mode. Instead, variable and function definitions live in a new scope created for the `eval()`. This scope is discarded when the `eval()` returns.

- In strict mode, the Arguments object in a function holds a static copy of the values passed to the function. In non-strict mode, the Arguments object has “magical” behavior in which elements of the array and named function parameters both refer to the same value.

- In strict mode, a `SyntaxError` is thrown if the `delete` operator is followed by an unqualified identifier such as a variable, function, or function parameter. (In nonstrict mode, such a delete expression does nothing and evaluates to false.)

- In strict mode, an attempt to `delete` a nonconfigurable property throws a `TypeError`. (In non-strict mode, the attempt fails and the `delete` expression evaluates to false.)

- In strict mode, it is a syntax error for an object literal to define two or more properties by the same name. (In non-strict mode, no error occurs.)

- In strict mode, it is a syntax error for a function declaration to have two or more parameters with the same name. (In non-strict mode, no error occurs.)

- In strict mode, octal integer literals (beginning with a `0` that is not followed by an `x`) are not allowed. (In non-strict mode, some implementations allow octal literals.)

- In strict mode, the identifiers `eval` and `arguments` are treated like keywords, and you are not allowed to change their value. You cannot assign a value to these identifiers, declare them as variables, use them as function names, use them as function parameter names, or use them as the identifier of a `catch` block.

- In strict mode, the ability to examine the call stack is restricted. `arguments.caller` and `arguments.callee` both throw a `TypeError` within a strict mode function.

## Declarations

The keywords `const`, `let`, `var`, `function`, `class`, `import`, and `export` are not technically *statements*, but they look a lot like statements, and this book refers informally to them as statements, so they deserve a mention in this chapter.

These keywords are more accurately described as *declarations* rather than statements. We said at the start of this chapter that statements “make something happen.” Declarations serve to define new values and give them names that we can use to refer to those values. They don’t make much happen themselves, but by providing names for values they, in an important sense, define the meaning of the other statements in your program.

When a program runs, it is the program’s expressions that are being evaluated and the program’s statements that are being executed. The declarations in a program don’t “run” in the same way: instead, they define the structure of the program itself. Loosely, you can think of declarations as the parts of the program that are processed before the code starts running.

JavaScript declarations are used to define constants, variables, functions, and classes and for importing and exporting values between modules. 

### `const`, `let`, and `var`

In ES6 and later, `const` declares constants, and `let` declares variables. Prior to ES6, the `var` keyword was the only way to declare variables and there was no way to declare constants. Variables declared with `var` are scoped to the containing function rather than the containing block. This can be a source of bugs, and in modern JavaScript there is really no reason to use `var` instead of `let`.

### function

The function declaration is used to define functions. A function declaration looks like this:

```
function area(radius) {
    return Math.PI * radius * radius;
}
```

The function declarations in any block of JavaScript code are processed before that code runs, and the function names are bound to the function objects throughout the block. We say that function declarations are “hoisted” because it is as if they had all been moved up to the top of whatever scope they are defined within. The upshot is that code that invokes a function can exist in your program before the code that declares the function.

### class

In ES6 and later, the class declaration creates a new class and gives it a name that we can use to refer to it. 

A simple class declaration might look like this:

```
class Circle {
    constructor(radius) { this.r = radius; }
    area() { return Math.PI * this.r * this.r; }
    circumference() { return 2 * Math.PI * this.r; }
}
```

Unlike functions, class declarations are not hoisted, and you cannot use a class declared this way in code that appears before the declaration.

### import and export

The `import` and `export` declarations are used together to make values defined in one module of JavaScript code available in another module. A module is a file of JavaScript code with its own global namespace, completely independent of all other modules. The only way that a value (such as function or class) defined in one module can be used in another module is if the defining module exports it with `export` and the using module imports it with `import`.

`import` directives are used to import one or more values from another file of JavaScript code and give them names within the current module. `import` directives come in a few different forms. Here are some examples:

```
import Circle from './geometry/circle.js';
import { PI, TAU } from './geometry/constants.js';
import { magnitude as hypotenuse } from './vectors/utils.js';
```

Values within a JavaScript module are private and cannot be imported into other modules unless they have been explicitly exported. The `export` directive does this: it declares that one or more values defined in the current module are exported and therefore available for import by other modules. The `export` directive has more variants than the import directive does. Here is one of them:

```
// geometry/constants.js
const PI = Math.PI;
const TAU = 2 * PI;
export { PI, TAU };
```

The `export` keyword is sometimes used as a modifier on other declarations, resulting in a kind of compound declaration that defines a `constant`, `variable`, `function`, or `class` and exports it at the same time. And when a module exports only a single value, this is typically done with the special form `export default`:

```
export const TAU = 2 * Math.PI;
export function magnitude(x,y) { return Math.sqrt(x*x + y*y); }
export default class Circle { /* class definition omitted here */ }
```
