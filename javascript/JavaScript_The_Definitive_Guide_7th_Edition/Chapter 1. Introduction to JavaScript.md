# JavaScript: Names, Versions, and Modes

To be useful, every language must have a platform, or standard library, for performing things like basic input and output.  The core JavaScript language defines a minimal API for working with numbers, text, arrays, sets, maps, and so on, but does not include any input or output functionality. Input and output (as well as more sophisticated features, such as networking, storage, and graphics) are the responsibility of the “host environment” within which JavaScript is embedded. 


## expression

An expression is a phrase of JavaScript that can be evaluated to produce a value. 

One of the most common ways to form expressions in JavaScript is to use operators:

```
// Operators act on values (the operands) to produce a new value.
// Arithmetic operators are some of the simplest:
3 + 2                      // => 5: addition

// JavaScript defines some shorthand arithmetic operators
let count = 0;             // Define a variable
count++;                   // Increment the variable
count += 2;                // Add 2: same as count = count + 2;
count                      // => 6: variable names are expressions, too.

// Equality and relational operators test whether two values are equal,
// unequal, less than, greater than, and so on. They evaluate to true or false.
let x = 2, y = 3;          // These = signs are assignment, not equality tests
x === y                    // => false: equality
x !== y                    // => true: inequality
x < y                      // => true: less-than
x <= y                     // => true: less-than or equal
x > y                      // => false: greater-than
x >= y                     // => false: greater-than or equal
"two" === "three"          // => false: the two strings are different
"two" > "three"            // => true: "tw" is alphabetically greater than "th"
false === (x > y)          // => true: false is equal to false

// Logical operators combine or invert boolean values
(x === 2) && (y === 3)     // => true: both comparisons are true. && is AND
(x > 3) || (y < 3)         // => false: neither comparison is true. || is OR
!(x === y)                 // => true: ! inverts a boolean value
```

## statements 

If JavaScript expressions are like phrases, then JavaScript statements are like full sentences. 

Roughly, an expression is something that computes a value but doesn’t do anything: it doesn’t alter the program state in any way. Statements, on the other hand, don’t have a value, but they do alter the state. You’ve seen variable declarations and assignment statements above. The other broad category of statement is control structures, such as conditionals and loops. 

## function 

A function is a named and parameterized block of JavaScript code that you define once, and can then invoke over and over again. Here are some simple examples:

```
// Functions are parameterized blocks of JavaScript code that we can invoke.
function plus1(x) {        // Define a function named "plus1" with parameter "x"
    return x + 1;          // Return a value one larger than the value passed in
}                          // Functions are enclosed in curly braces

plus1(y)                   // => 4: y is 3, so this invocation returns 3+1

let square = function(x) { // Functions are values and can be assigned to vars
    return x * x;          // Compute the function's value
};                         // Semicolon marks the end of the assignment.

square(plus1(y))           // => 16: invoke two functions in one expression
```

## arrow functions

In ES6 and later, there is a shorthand syntax for defining functions. This concise syntax uses => to separate the argument list from the function body, so functions defined this way are known as arrow functions. Arrow functions are most commonly used when you want to pass an unnamed function as an argument to another function. 

When functions are assigned to the properties of an object, we call them "methods".
