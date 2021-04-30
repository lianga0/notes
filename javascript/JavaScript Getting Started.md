# JavaScript The Ultimate Guide to Modern JavaScript Development — Third Edition — Russ Ferguson

> ISBN-13 (pbk): 978-1-4842-4394-7

>ISBN-13 (electronic): 978-1-4842-4395-4

> https://doi.org/10.1007/978-1-4842-4395-4

> Copyright © 2019 by Russ Ferguson 

## Introduction to JavaScript

JavaScript is an interpreted scripting language. The host environment will provide access
to all the objects needed to execute the code.

The primary example for JavaScript is the ability to add interactivity to a website.
This works because the interpreter is embedded into a web browser so you do not need
to add any software.

Another use case is to execute JavaScript on the server, using an environment
like Node.js. An example of server-side JavaScript is the ability to do things like make
requests from a database and respond to HTTP requests and create files. 

JavaScript是一门高级的、动态的、弱类型的编程语言，非常适合面向对象和函数式的编程风格。通常每一种编程语言都有各自的开发平台、标准库或API函数，用来提供诸如基本输入输出的功能。JavaScript语言核心针对文本、数组、日期和正则表达式的操作定义了很少的API，但是这些API不包括输入输出功能。输入和输出功能（类似网络、存储和图形相关的复杂特性）是由JavaScript所属的“宿主环境”（host enviroment）提供的。

### JavaScript in a Web Page and Essential Syntax

Applying JavaScript to a web document is very easy; all you need to do is use the
script tag:

```
<script>
 // Your code here
</script>
```

While this is the simplest way of adding JavaScript to the page, it is not
recommended. This is an example of inline JavaScript.

The preferred way to add JavaScript to an HTML page is to refer to an external
.js file:

```
<script src="js/myfile.js"></script>
```

> Note: HTML 5 requires that the script tag have its own closing tag. This will
ensure backwards combability with older browsers. In addition, adding the script
tag right before the ending body tag is considered a best practice.


## JavaScript Variables

JavaScript is a loosely typed or dynamic language. If you create a variable and assign it a value, you can then change that value for something that is completely different.

Once you tell the environment that you need to hold onto some information, the next thing is to assign data to that variable. That data is of a certain type.

Strings are a representation of data that can be used in text form. When creating a string variable in JavaScript you can use either single or double quotes around the characters you want to use.

At the end of each statement is a semicolon. If you do not add one, the environment is good at trying to figure out what you mean and will insert one where it thinks it’s necessary.

In summary, when declaring variables in JavaScript, use a keyword (e.g. `var`), name your variable, and then assign its value.


Using true or false as values makes your variable a Boolean datatype, meaning that it should only have one value or the other. Booleans can only be true or false.

### Variables That Can’t Be Reassigned

If you want a variable that can contain a value that will stay constant no matter what else is going on. JavaScript provides such a variable type and it’s called a constant.

Constants are a type of variable where you cannot change the value after first assigning it. The keyword in this case is `const`. The vaule must be initialized when you declare a const variable.

### Variables That Can Only Be Used in a Single Code Block

#### Code Block

Let’s first define a `code block`. When you work with JavaScript functions, you will often see a set of curly braces ({}). This is your code block. Anything inside these braces is code that will be executed.

When using the keyword `let` to declare your variables, the browser understands that the value that you are assigning to the variable can only be seen inside that block.

```
// A let Statement Only Has a Value While Inside the Code Block
for (let i = 0; i < 10; i++) {
console.log(i); //output = numbers between 0 and 9
}
console.log(i) //error i is undefined
```

All of this is happening inside the curly braces. Once this loop is finished, the variable i goes away. The environment does not think about it anymore. So, when you try to reference that variable in the very next line, it will throw you an error.

This is one of the major differences between `let` and `var`.

```
// When Creating a Variable with the var Keyword, It Will Exist Inside the Current Execution Context. The Code Here Is Outside a Function, Making the Context Global.
for (var i = 0; i < 10; i++) {
console.log(i); //output = numbers between 0 and 9
}
console.log(i) //returns 10
```

**Variables created with the `var` keyword are declared based on its current execution context.** In the first instance, the loop is not inside a function; because of this, the variable becomes global in scope.

Right under that you have the same loop, but this time it’s inside a function block. The variable then is inside a different execution context. If you try to print the value of the variable outside the function, the browser will throw an error.

```
// When Creating a Variable Using the var Keyword Inside a Function, the Execution Context is Local to the Function 
function goLoop(){
    for (var i = 0; i < 10; i++) {
    console.log(i); //output = numbers between 0 and 9
}
}
goLoop();
console.log(i) //returns error
```

### Variable Hoisting (自动把var类型变量的声明提升到作用域开始的地方)

When the browser is going through its compile phase, it will put both functions and variable declarations into memory.

Here is an example of how you declare a variable:

```
userName = "Stephanie";
```

This is different than when you initialize a variable using one of the keywords like `let`. Here you are assigning a value to a variable and not using any keywords. Because no keyword has been assigned to this variable, it is considered a global variable. It’s the same as using the `var` keyword.

Variables that are hoisted move to the top of the current scope. So, if there are no functions, variables are moved to the global scope. If a variable (using the var keyword) is declared inside a function, it would move to the top of that scope.

Variable hoisting takes effect when the variable has been declared, not when it has been assigned a value. If you declare a variable without a value, it is still hoisted even if it does not have a value.

> When using the keyword var, variables can then be hoisted or moved to the top of the execution context. This can cause situations where even though a variable has been declared, it may not yet have a value and so will return undefined as a value.

#### 总结：

- 关键字 let 和 const 在 JavaScript 中添加块级作用域。

- 当我们将一个变量声明为 let 时，我们不能在同一作用域(函数或块级作用域)中重新定义或重新声明另一个具有相同名称的 let 变量，但是我们可以重新赋值。

- 当我们将一个变量声明为 const 时，我们不能在同一作用域(函数或块级作用域)中重新定义或重新声明具有相同名称的另一个 const 变量。但是，如果变量是引用类型(如数组或对象)，我们可以更改存储在该变量中的值。


#### var关键字的缺点：

- 没有块级作用域的概念（仅函数作用域和全局变量）

- 默认情况下，顶级变量是全局变量（全局对象）

- 一个变量可以使用两次var（重声明）

- 可以在声明前使用变量（提升）

- 循环中的变量重复使用同样的引用（闭包）

当闭包中带有var时，该引用会被记住，当循环中的变量发生变化时，会造成麻烦。

```
var functions = [];
for (var i = 0; i < 3; i++) {
    functions[i] = () => { console.log(i); };
}
for (var j = 0; j < 3; j++) {
    functions[j]();
} // 3 3 3
```

如果使用let，每次都会创建新的引用。

```
var functions = [];
for (let i = 0; i < 3; i++) {
    functions[i] = () => { console.log(i); };
}
for (var j = 0; j < 3; j++) {
    functions[j]();
} // 0 1 2
```

说到底，即使不是100％出于这些原因以及它们为何按其工作方式工作，切换到let还将产生更明确的代码，这些代码的行为始终如一，并且更易于故障排除和维护。

尽管let和const应该可以有效替换var关键字，但是一切并不总是那么简单。由于这些关键字是在ECMAScript2015（ES6）中引入的，因此，如果你使用的平台不允许使用该关键字，那就很不幸了。


### Strict Mode

Strict mode tells the browser to run a more restricted version of JavaScript. This is something you can opt into. Running your code in strict mode will keep the browser from making mistakes that make it difficult to optimize the code.

It will also prevent some syntax from being executed when that syntax will likely be added to a future version of JavaScript. It also eliminates silent errors (errors without feedback from the browser).

**You can invoke strict mode on the whole JavaScript file or on individual functions. To add it to the entire script at the top, add `'use strict;'` to your code.**

```
// Using “use strict” Inside a Function Declaration Will Tell the Browser to Run Just That Function in Strict Mode
function myFunction(){
    "use strict";
    // add commands here
}
```

Using strict mode ensures that the browser will execute your code in the most efficient way possible and give you the most amount of feedback when errors occur.

### Destructuring assignment

The **destructuring assignment** syntax is a JavaScript expression that makes it possible to unpack values from arrays, or properties from objects, into distinct variables.

#### Syntax

```
let a, b, rest;
[a, b] = [10, 20];
console.log(a); // 10
console.log(b); // 20

[a, b, ...rest] = [10, 20, 30, 40, 50];
console.log(a); // 10
console.log(b); // 20
console.log(rest); // [30, 40, 50]

({ a, b } = { a: 10, b: 20 });
console.log(a); // 10
console.log(b); // 20


// Stage 4(finished) proposal
({a, b, ...rest} = {a: 10, b: 20, c: 30, d: 40});
console.log(a); // 10
console.log(b); // 20
console.log(rest); // {c: 30, d: 40}
```

Reference: [Destructuring assignment](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Destructuring_assignment)

### JavaScript语言核心

#### JavaScript支持多种数据类型

```
x = 1;               // 数字
x = 0.01;            // 整数和实数共用一种数据类型
x = "hello world";   // 由双引号内的文本构成的字符串
x = 'JavaScript';    // 单引号内的文本同样构成字符串
x = true;            // 布尔值
x = false;           // 另一个布尔值
x = null;            // null是一个特殊的值，意思是“空”
x = undefined;       // undefined和null非常类似
```

#### JavaScript中两个非常重要的数据类型是对象和数组。



## JavaScript Objects and Arrays

Objects are central to the way you use JavaScript.

Objects have

- Properties (analogous to adjectives): The car is red.
- Methods (like verbs in a sentence): The method for starting the car might be to turn ignition key.
- Events: Turning the ignition key results in the car starting event.


Some of the objects you’ll be using are part of the language specification: the `String` object, the `Date` object, and the `Math` object, for example. These objects provide lots of useful functionality that could save you tons of programming time. These objects are usually referred to as **core objects** because they are independent of the implementation.

The browser also makes itself available for programming through objects you can use to obtain information about the browser and to change the look and feel of the application. For example, the browser makes available the Document object, which represents a web page available to JavaScript. You can use this in JavaScript to add new HTML to the web page being viewed by the user of the web browser. If you used JavaScript with a different host, a Node.js server, for example, you’d find that the server hosting JavaScript exposes a very different set of host objects because their functionality is related to things you want to do on a web server.


### Host Object or Native Object

Since JavaScript is a language that can work in multiple environments, the code itself may have to act differently in different environments. To illustrate, there may be things in the browser like history or location that will not be available on the server. There may also be other environments like mobile devices that have unique capabilities. For the most part, I will discuss how JavaScript works in the browser.

You may run into the term “isomorphic JavaScript.” In this case, it’s the ability to have JavaScript applications that can run both on the client side (browser) and the server. Native (sometimes called built-in) objects are objects that are part of the ECMAScript standard. **ECMAScript is not a language itself, but a specification of a scripting language.** JavaScript is the most popular implementation of this specification. Other implementations include ActionScript. With that understanding, the ECMAScript specification will define objects independent of the environment. Some of these objects include

- Object
- Array
- Promise
- JSON

Host objects are part of the environment that your code runs in. For example, host objects in your browser include

- Window
- Document
- History
- Navigator

> Note If you are interested in what native objects are available to you in the browser, look at the MDN web docs at https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects


### An array is a more specialized object.

An array is not just good at holding groups of data; it is also good at keeping that data in order. Javascript array object do not need its elements have a same data type.

```
//create an array using the new operator
let myArray = new Array();
//create an array using square braces
let myOtherArray = [];
```
```
let nameArray = new Array();
nameArray[0] = 'Hunter';
nameArray[2] = 'Grant';
```

While this code is correct, and the browser will not tell you that there is anything wrong with it, if you tried to get an element that has not yet been assigned a value, the browser will return undefined.

#### Using Loops and Filters

The array object has a method called `forEach`. It lets you iterate or go over each element that is in the array. The way that each item is reviewed is by using a function.

```
let myArray = ['one', 'two', 'three', 'four'];
myArray.forEach((value, index, array) => {
    console.log(value); //current value
    console.log(index); //current index
    console.log(array); //entire array
});
```

What if you want to filter out some of the information that is inside that array? You can use the `filter` method to do so. The filter method will return a new array based on the results of the test you create.

```
let numberArray = [1,2,3,4,5,6,7,8,9];
let oddNumbers = numberArray.filter((value, index, array) => {
if(value % 2){
    console.log(value);
    return value;
    }
});
```

Two other methods built into an array are the map and reduce methods.

```
// array.reduce(function(total, currentValue, currentIndex, arr), initialValue)
let reducedValue = [10,1,2,3,4,5,6,7,8,9].reduce( (total, currentValue, index, array)=> {
   return total + currentValue;
});
console.log(reducedValue) //returns 55
```

initialValue是可选参数，未设置的话，取数组第一原始作为初始值，这是reduce函数从数组第二个元素开始调用指定function。设置initialValue参数的话，会对每个数组元素均调用一次指定function。



## JS Functions and Context

Functions are extremely flexible in JavaScript. They can be assigned to variables and passed as a property to other functions as an argument. Functions can also return another function. Let’s take a look at a few examples:

```
var doMath = function(num1, num2) {
    var result = num1 + num2;
    return result;
};
var myResult = doMath(2,3);
```

### Making a Function Declaration

This may go by a few names, such as `function declaration`, `function definition`, or `function statement`. In any case, creating a basic function will require a few things:

- The name of the function
- An optional list of arguments separated by commas
- Code that will perform an operation on the data, surrounded by curly braces

Here is some code:

```
function myFunction(optional, data, here ){
//some code goes here
}
```

Functions will always return a value and most of the time the value will be `undefined`.

Another sample code:

```
const addNumbers = function(num1, num2){ return num1+ num2 };
addNumbers(2,3);
```

Here you create a constant variable and assign your function to it. Then you use the variable in the same way that you would call a function. In this case, the function does not have a name, making it an anonymous function. This is called a `function expression`.

### Using Arrow Functions

An arrow function expression is a shorter way of creating a function expression. It changes the function’s relationship to the rest of the code and provides a good introduction to the keyword this and the concept of scope.

a simple arrow function:

```
const arrowFun = (num1, num2) => { num1 + num2 };
```

Here you create a constant variable just as before. You lose the `function` keyword and use what is sometimes called a `fat arrow: =>`. The curly braces remain.

You may also notice that you dropped the `return` keyword. When using an arrow function, if the body of your function is only one line, JavaScript will use what is called an `implicit return`.

If your function’s code block (the part between the curly brackets) is more than one line and you want to specify a return value, it then needs a `return` statement:

This is just one of the ways in which arrow functions are different than the types of functions you used before. Here are some other examples to keep in mind when working with arrow functions:

```
//If there is only one argument, you do not need to put it in parentheses.
const arrowFun = num1 => num1 * 2;
//if your function needs more than one argument, then it needs to be in parentheses:
const arrowFun = (num1, num2) => 2
```

```
const arrowFun = _ => 2
const arrowFun = () => 2
```

These two statements are the same. If you do not have any arguments to pass over, you can have an empty set of parentheses or use an underscore.

Normally, when using functions the code block goes between curly backets. This causes a problem when trying to return an object literal using an arrow function. The reason for this is that the interpreter does not know that you are trying to return an object. The way to fix this is to use parentheses on the outside and create the object literal on the inside.

```
const arrowFun = () => ({firstName:Paul});
```

If you just want a function to do some work for you, either way will do. What makes this one different is the keyword `this`. 

### How Does the Keyword `this` Work?

The place in your code where you call a function is called the `execution context`. The execution context determines the value of `this`.

Get the Current Context of a Function in the Global Scope

```
function getThis()(
 console.log(this)
}
getThis(); //returns Window {postMessage: ƒ, blur: ƒ, focus: ƒ, close: ƒ,
frames: Window, ...}
```

The place in your code where you call a function is called the execution context. The execution context determines the value of `this`.

> Note If you run this code in `strict mode`, the result will be `undefined`.

The execution context is different when trying to get the value of this from inside an object.

Get the Value from Inside an Object

```
var myObj = {
 getThis : function ()(
 console.log(this)
 }
 }
myObj.getThis() //returns {getThis: ƒ}
```

In this example, the starting point is inside the object myObj. When the method is called, the value of this is the object itself.


#### immediately invoked function expression (IIFE)

IIFE is a function that will execute immediately.

```
//Referencing a Variable from Inside and Outside the Function Scope
(function () {
    var person = "Friend";
    console.log(this); // returns Window {postMessage: ƒ, blur: ƒ, focus: ƒ, close: ƒ, frames: Window, ...}
    console.log("Hello " + this.person); //returns undefined
    console.log("Hello " + person); //returns Hello Friend
})()
console.log("Hello = " + person); //returns reference error variable not defined.
```

You can see from the output that the function is living inside the global scope. All variables declared inside of the IIFE function live inside that function scope.

In the current example, the immediately invoked function has its own function scope. You can see from the output that the function is living inside the global scope. All variables declared inside of the function live inside that function scope.


One of the benefits to this is that variables that would otherwise end up in the global scope will now be in the scope of the IIFE. This is a technique used by many developers to not “pollute” the global scope. Functions and variables will never be part of the global scope. This also prevents overriding other functions or variables that may have the same name.

You can see that referencing properties and methods (variables and functions) using the keyword this can produce unexpected results if you are not careful. JavaScript does provide a few ways to have a more predictable way of controlling the execution context.

When calling a function, the location of where the call happens will determine the execution context of that function. This is one of the reasons why the value of the keyword this varies. Using the `bind`, `apply`, or `call` methods lets you control the context and gives you a more predictable way of using this.

Using the Keyword `bind` to Set the Value of `this`

```
var myObj = {
 person: "Friend"
}
function sayHello() {
 console.log("Hello " + this.person);
}
sayHello() //returns Hello undefined
var tryAgain = sayHello.bind(myObj) //assigning the value of this to the object myObj
tryAgain() // returns Hello Friend
```

The call and apply methods are similar. The main difference is, not only can you define the execution context, but you can also pass information to the method that you want to execute.

```
Using the call Method
sayHello(message){
 console.log(message, this.mainCharacter);
}
const characters = {
 mainCharacter: "Elliot"
}
sayHello.call(characters, "Hello "); //returns Hello Elliot
```

The apply method is very similar. The big difference is that the apply method expects an array.

```
function sayHello(firstName, secondName, thirdName) {
 console.log(this.message, firstName); //returns Hello Elliot
 console.log(this.message, secondName); //returns Hello Tyrell
 console.log(this.message, thirdName); //returns Hello Dominique
}
const show = {
 message: "Hello"
}
sayHello.apply(show, ["Elliot ", " Tyrell ", "Dominique"]);
```

**Functions in JavaScript are objects.** These function objects have their own set of properties and methods associated with them.

It is also important to remember that a function is also an object (native or host object) and these objects have their own properties and methods. The methods you learned were `call`, `apply`, and `bind`. These methods help control the execution context, which controls the value of the keyword `this`.


### Understanding Closures

Functions and variables that are created inside a function live in what is called the `lexical scope`. The inner function has access to the variables and functions not just in its own scope but in both the outer function scope and the global scope. It is also important to note that this does not work in the other direction.

(在词法范围中，程序源码的结构决定了你引用的是哪一个变量。而在动态范围中，程序的运行栈才决定了你引用的是哪一个变量。)

```
// Using a Closure to Create Private Variables

const sayHello = function(){
    let greetingMsg = "Greetings ";
    function msgTo(firstName, lastName){
        greetingMsg = greetingMsg + firstName + " " + lastName;
    }
    return {
        sendGreeting: function(firstName, lastName){
            msgTo(firstName, lastName);
        },
        
        getMsg: function(){
            return greetingMsg;
        }
    }
}

const createMsg = sayHello();
createMsg.sendGreeting("Professor" , "Falken");
console.log(createMsg.getMsg()); //returns "Greetings Professor Falken";
```

It is also important to note that if you assign the result of sayHello to a second variable, it will be independent of the first instance. The way the functions execute will be exactly the same. However, the values may be different.

```
const createMgs2 = sayHello();
createMsg2.sendGreeting("David", "Lightman");
console.log (createMsg2.getMg()); //returns Greetings David Lightman
```

Here you are use the exact same functions and end up with different results.




## JavaScript and Events

Functions are often called because of an event. Events can be things like a page loading or a button click. JavaScript allows you to “listen” for events and then execute a function in response to the event.

The document object is one of many objects that include a method called `addEventListener`. This method takes two arguments, the event that you are listening for and a function that will do something when the event happens.

There is a long list of events for the environment (https://developer.mozilla.org/en-US/docs/Web/Events) that you are working with。

### Using preventDefault

If you want to have someone click a link, and not have the browser go to another page, you can use the `preventDefault` method.

### Event propagation.

A large amount of work in the browser is tied to events. An important concept to understand is that of `event propagation`. Event propagation is when you want to discuss both the bubbling phase and the capture phase of an event. Event propagation deals with how various objects in the browser are able to receive events.

One phase of propagation is `event bubbling`. An example of this is when a button inside a `div` is clicked. The target of the click is the button itself.

However, the event travels up from the button to its parent. This process will continue until the event meets the `window object`.

You can see that once the button has been clicked, the event travels up to the window object without you needing to do anything. This is the default way that browsers handle events. You can stop this from happening by using the `stopPropagation` method. It keeps the other objects from listening to events as they bubble up. This prevents any of the other objects higher up in the chain from receiving the event, even if they have listeners for that event.

Another way that browsers can work with events is though `event capturing`. This is the exact opposite of what you have been doing with bubbling, where the browser starts at the top of the document and works its way down to the target.

```
window.addEventListener("click", onWinowClick, true);
```

To have the browser use this method of dealing with events, you need to tell the `addEventListener` method to use capturing and not bubbling. Adding the last property to the `addEventListener` method tells the browser to enable `event capturing`.

### Creating Custom Events

```
// Creating and Using Custom Events
function onPageLoad(){
    let myButton = document.getElementById("myButton");
    myButton.addEventListener("click", onButtonClick, true);
    myButton.addEventLIstener("WORLD_ENDING_EVENT", onWorldEnd);
}
function onButtonClick(evt){
    let custEvent = new CustomEvent("WORLD_ENDING_EVENT", {
    detail: {
            message: "And I feel fine"
        }
    });
    let myButton = document.getElementById("myButton");
    myButton.dispatchEvent(custEvent);
};
function onWorldEnd(evt){
    console.log(evt); // returns CustomEvent {isTrusted: false, detail:
    //{...}, type: "WORLD_ENDING_EVENT", target: button#myButton,
    //currentTarget: button#myButton, ...}
    console.log(evt.type); //returns WORLD_ENDING_EVENT
    console.log(evt.detail); //returns {message: "And I feel fine"}
}
```

Event handlers can use both anonymous functions and named functions. Event objects are passed to function handlers to describe everything about the function that just happened. Using an event object, you can see what HTML element dispatched the event, and you have the ability to stop the browser from performing some of its native operations.


## Object-Oriented Programming with JavaScript

A class is often thought of as a blueprint. Inside this blueprint is code that deals with all the things you know about a object, without any of the details. You can use the ES6 `class` keyword to create a class. There are other ways to do this but for the sake of clarity you are going to use the most current syntax. 

```
//Creating a Robot Class
class Robot {
    constructor(name, type){
        this.name = name;
        this.type = type;
        this.greeting = function(){
            return "I'm " + this.name + " I'm a " + this.type + ".";
        }
    }
}
```

When creating a class instance, you use the keyword new. This creates an object that contains all the properties and methods defined in that class.

```
//Inheriating from a Parent Class Using the ES6 extends Keyword
class BendingUnit extends Robot {
    constructor(name, type){
            super(name, type);
        }
    }

    primaryFunction(){
        console.log(this.name + " bends things");
    }
}
```

This code uses the extends keyword to tell the environment that it wants to use everything that is available from the parent class Robot in addition to the features in this current class.

Using the `extends` keyword gives you the ability to inherit from another class. **JavaScript only allows you to inherit from one parent class.**


### JavaScript Classes and Prototypical Inheritance

JavaScript is `prototype based`, meaning that if the property or method does
not exist in the current object, it will look at the `prototype` property of the object and move to its parent object to see if the property exists there. This is often called moving up the `prototype chain`.

In the previous examples, you used the **ES6 syntax** to create objects. One of the keywords you used was `constructor`. A function `constructor` is really just a function that creates a function object.

```
// Creating the Robot Object Using Function Contructors
const Robot = function(name, type) {
    this.name = name;
    this.type = type;
}

Robot.prototype.greeting = function(){
    return "I'm " + this.name + " I'm a " + this.type + ".";
}
let bender = new Robot ("Bender", "Bending Robot");
bender.greeting() // "My name is Bender I'm a Bending Robot."
```

Properties and methods are added to the object’s `prototype`. This means if there are any classes that can inherit from this class, JavaScript moves up the `prototype chain` from the child object to its parent objects to access the property.

```
// Creating Inheritance Without Using the ES6 Syntax
const Robot = function(name, type) {
    this.name = name;
    this.type = type;
}
Robot.prototype.greeting = function(){
    return "I'm " + this.name + " I'm a " + this.type + ".";
}
const BendingUnit = function(){
    Robot.apply(this, arguments);
}
BendingUnit.prototype = Object.create(Robot.prototype);
BendingUnit.prototype.constructor = BendingUnit;
let bender = new BendingUnit("Bender", "Bending Unit");
bender.greeting() // "My name is Bender I'm a Bending Unit."
```

One of the key differences here is that the function BendingUnit is calling the original Robot class and using the `apply` method.

The `apply` method tells the browser that the BendingUnit class can be used as a starting point to access the properties of the Robot class.

The next line tells the environment to update the `prototype` object of the BendingUnit class and assign to it the value of the Robot `prototype`.

Now that the `prototype` has been updated, the `constructor` thinks that is a copy of the Robot class and not its own BendingUnit class.

To fix this, assign the `contractor` function to the BendingUnit function, so it will know that even though it inherits functions from the Robot class, it itself is not the Robot.


### Functional Programming with JavaScript

As mentioned, JavaScript is a very flexible language. The two paradigms often used are object-oriented programing and functional programing.

Previously you created objects in JavaScript using both the ES6 syntax that contains the keyword class and the ES5 syntax that relies on your understanding of prototypical inheritance.

Functions in JavaScript can be passed as properties of a function. They can also be values returned from other functions.

The ability to chain functions is something that you will see often. Using the fetch method to retrieve data from a remote source requires chaining the method and then processing the results that return from the server. Here is an example:

```
fetch('https://swapi.co/api/people/1').then(results => results.json()).then(json => console.log(json));
//results
//{name: "Luke Skywalker", height: "172", mass: "77", hair_color: "blond", skin_color: "fair", ...}
```

Here you use the fetch method to retrieve data from the Star Wars API (https://swapi.co). This method returns what is called a `promise`. It will wait until the request is resolved or fails.

When the request is resolved, the then method is chained to it. Here you can process the results. The first then method takes the results and converts them into a JSON object. When using arrow functions, the result is automatically returned when there are no curly braces and only one line of code.

This is sent over to the second then method, where the results of the first method become a parameter called json and are printed in the browser console.


## JavaScript and Client-Side Development

So far, you have a local server running and JavaScript working. However, you have not yet been able to connect your jQuery library to your project.

In order to get that to work, you need to add a module builder. The next section will explain how that works and why it’s important.

### Introduction to Module Bundlers (Webpack)

Up to this point you have not used the jQuery library that you previously installed in your project. If you remember, when installing jQuery it created a folder called `node_modules` that contained your library.

As your projects start to get more complex, you will need a few different modules to make everything work. It would be great to add these modules and not add a long list of `script` tags to your document for every module you want to use.


**Webpack** is a tool that you can use to help use import any library you use in your project and also make sure that the code is compatible with some older browsers.

Your project now has the ability to import external libraries, automatically update when files are changed, and output JavaScript that can work on as many browsers as possible despite being writing using the latest JavaScript development techniques.

You are also using Sass, which means your styles work in as many browsers as possible. You get these features because you are using NodeJS as your base. Webpack uses Node to give you a local server to use. Your scripts tell the server to watch the files so that the page will refresh as changes occur.

This is just the beginning of how you can work with Node on the client side. Node is the building block for a large amount of client-side tooling. For example, using the latest version of Angular, you can use the command line to build out a bare bones application.

React has a similar tool called `create-react-app`. Either tool will do a lot of the work for you because Node has access to the file system and can create files and folders for you.

## JavaScript and Server- Side Development

## JavaScript and Application Frameworks: Angular

## JavaScript and Application Frameworks: React

## JavaScript and Static Deployment

### Deploying a Static Site to Netlify

Netlify (www.netlify.com/) is one of a series of services that try to make deploying your site fairly painless. There is a free tier for someone working on a personal site.
