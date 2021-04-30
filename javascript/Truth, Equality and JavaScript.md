## Truth, Equality and JavaScript

> From: https://javascriptweblog.wordpress.com/2011/02/07/truth-equality-and-javascript/

You don’t have to be a JavaScript novice to get confused by this…

```
if ([0]) {
    console.log([0] == true); //false
    console.log(!![0]); //true
}
```
 
or this…

```
if ("potato") {
    console.log("potato" == false); //false
    console.log("potato" == true); //false
}
```
 
The good news is that there is a standard and all browsers follow it. Some authors will tell you to fear coercion and and code against it. I hope to persuade you that coercion is a feature to be leveraged (or at the very least understood), not avoided…

Is x true? Does x equal y? Questions of truth and equality at the kernel of three major areas of JavaScript: conditional, statements and operators (if, ternaries, &&, || etc.), the equals operator (==), and the strict equals operator (===). Lets see what happens in each case…

### Conditionals

In JavaScript, all conditional statements and operators follow the same coercion paradigm. We’ll use the if statement by way of example.

The construct `if ( Expression )` Statement will coerce the result of evaluating the Expression to a boolean using the abstract method [ToBoolean](http://www.ecma-international.org/ecma-262/5.1/#sec-9.2) for which the [ES5 spec](http://www.ecma-international.org/ecma-262/5.1/#sec-12.5) defines the following algorithm:

<table>
        <tbody><tr>
          <th style="border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-top: 2px solid #000000">Argument Type</th>
          <th style="border-bottom: 1px solid #000000; border-right: 1px solid #000000; border-top: 2px solid #000000">Result</th>
        </tr>
        <tr>
          <td>Undefined</td>
          <td><b>false</b></td>
        </tr>
        <tr>
          <td>Null</td>
          <td><b>false</b></td>
        </tr>
        <tr>
          <td>Boolean</td>
          <td>The result equals the input argument (no conversion).</td>
        </tr>
        <tr>
          <td>Number</td>
          <td>The result is <b>false</b> if the argument is <b>+0</b>, <b>−0</b>, or <b>NaN</b>; otherwise the result is <b>true</b>.</td>
        </tr>
        <tr>
          <td>String</td>
          <td>The result is <b>false</b> if the argument is the empty String (its length is zero); otherwise the result is <b>true</b>.</td>
        </tr>
        <tr>
          <td>Object</td>
          <td><b>true</b></td>
        </tr>
      </tbody>
</table>

This is the formula JavaScript uses to classify values as truthy (true, "potato", 36, [1,2,4] and {a:16}) or falsey (false, 0, "", null and undefined).

Now we can see why, in the introductory example, if ([0]) allows entry to the subsequent block: an array is an object and all objects coerce to true.

Here’s a few more examples. Some results may be surprising but they always adhere to the simple rules specified above:

```
var trutheyTester = function(expr) {
    return expr ? "truthey" : "falsey"; 
}
 
trutheyTester({}); //truthey (an object is always true)
 
trutheyTester(false); //falsey
trutheyTester(new Boolean(false)); //truthey (an object!)
 
trutheyTester(""); //falsey
trutheyTester(new String("")); //truthey (an object!)
 
trutheyTester(NaN); //falsey
trutheyTester(new Number(NaN)); //truthey (an object!)
```

### The Equals Operator (==)

The == version of equality is quite liberal. Values may be considered equal even if they are different types, since the operator will force coercion of one or both operators into a single type (usually a number) before performing a comparison. Many developers find this a little scary, no doubt egged on by at least one well-known JavaScript guru who recommends avoiding the == operator altogether.


The avoidance strategy bothers me because you can’t master a language until you know it inside out – and fear and evasion are the enemies of knowledge. Moreover pretending == does not exist will not let you off the hook when it comes to understanding coercion because in JavaScript coercion is everywhere! Its in conditional expressions (as we’ve just seen), its in array indexing, its in concatenation and more. What’s more coercion, when used safely, can be an instrument of concise, elegant and readable code.

Anyway, rant over, lets take a look at the way ECMA defines how == works. Its really not so intimidating. Just remember that `undefined` and `null` equal each other (and nothing else) and most other types get coerced to a number to facilitate comparison:

<table cellspacing="0" cellpadding="0">
<tbody>
<tr>
<td style="width:110px;background-color:#AAAAAA;border-bottom:1px solid black;border-top:0 none;font-size:13px;font-style:italic;font-weight:bold;height:24px;text-align:left;vertical-align:middle;">Type(x)</td>
<td style="width:110px;background-color:#AAAAAA;border-bottom:1px solid black;border-top:0 none;font-size:13px;font-style:italic;font-weight:bold;height:24px;text-align:left;vertical-align:middle;">Type(y)</td>
<td style="background-color:#AAAAAA;border-bottom:1px solid black;border-top:0 none;font-size:13px;font-style:italic;font-weight:bold;height:24px;text-align:left;vertical-align:middle;">Result</td>
</tr>
<tr>
<td colspan="2">x and y are the same type</td>
<td><b>See Strict Equality (===) Algorithm</b></td>
</tr>
<tr>
<td>null</td>
<td>Undefined</td>
<td><b>true</b></td>
</tr>
<tr>
<td>Undefined</td>
<td>null</td>
<td><b>true</b></td>
</tr>
<tr>
<td>Number</td>
<td>String</td>
<td>x == <span style="color:#CC0099;">toNumber</span>(y)</td>
</tr>
<tr>
<td>String</td>
<td>Number</td>
<td><span style="color:#CC0099;">toNumber</span>(x) == y</td>
</tr>
<tr>
<td>Boolean</td>
<td>(any)</td>
<td><span style="color:#CC0099;">toNumber</span>(x) == y</td>
</tr>
<tr>
<td>(any)</td>
<td>Boolean</td>
<td>x == <span style="color:#CC0099;">toNumber</span>(y)</td>
</tr>
<tr>
<td>String or Number</td>
<td>Object</td>
<td>x == <span style="color:#009900;">toPrimitive</span>(y)</td>
</tr>
<tr>
<td>Object</td>
<td>String or Number</td>
<td><span style="color:#009900;">toPrimitive</span>(x) == y</td>
</tr>
<tr>
<td colspan="2">otherwise…</td>
<td><b>false</b></td>
</tr>
</tbody>
</table>

Where the result is an expression the algorithm is reapplied until the result is a boolean. `toNumber` and `toPrimitive` are internal methods which convert their arguments according to the following rules:

<table cellspacing="0" cellpadding="0">
<caption><strong>ToNumber</strong></caption>
<tbody>
<tr>
<td style="width:110px;background-color:#AAAAAA;border-bottom:1px solid black;border-top:0 none;font-size:13px;font-style:italic;font-weight:bold;height:24px;text-align:left;vertical-align:middle;">Argument Type</td>
<td style="background-color:#AAAAAA;border-bottom:1px solid black;border-top:0 none;font-size:13px;font-style:italic;font-weight:bold;height:24px;text-align:left;vertical-align:middle;">Result</td>
</tr><tr>
<td>Undefined</td>
<td><b>NaN</b></td>
</tr>
<tr>
<td>Null</td>
<td><b>+0</b></td>
</tr>
<tr>
<td>Boolean</td>
<td>The result is <b>1</b> if the argument is <b>true</b>.<br>The result is <b>+0</b> if the argument is false.</td>
</tr>
<tr>
<td>Number</td>
<td>The result equals the input argument (no conversion).</td>
</tr>
<tr>
<td>String</td>
<td>In effect evaluates Number(<i>string</i>)<br>“abc” -&gt; NaN<br>“123” -&gt; 123</td>
</tr>
<tr>
<td>Object</td>
<td>Apply the following steps:<p></p>
<p class="color" style="margin-top:4px;margin-bottom:3px;">1. Let <i>primValue</i> be ToPrimitive(<i>input argument</i>, hint Number).<br>
2. Return ToNumber(<i>primValue</i>).</p>
</td>
</tr>
</tbody>
</table>


<table cellspacing="0" cellpadding="0">
<caption><strong>ToPrimitive</strong></caption>
<tbody>
<tr>
<td style="width:110px;background-color:#AAAAAA;border-bottom:1px solid black;border-top:0 none;font-size:13px;font-style:italic;font-weight:bold;height:24px;text-align:left;vertical-align:middle;">Argument Type</td>
<td style="background-color:#AAAAAA;border-bottom:1px solid black;border-top:0 none;font-size:13px;font-style:italic;font-weight:bold;height:24px;text-align:left;vertical-align:middle;">Result</td>
</tr><tr>
<td>Object</td>
<td>(in the case of equality operator coercion) if <code>valueOf</code> returns a primitive, return it. Otherwise if <code>toString</code> returns a primitive return it. Otherwise throw an error</td>
</tr>
<tr>
<td>otherwise…</td>
<td>The result equals the input argument (no conversion).</td>
</tr>
</tbody>
</table>


> In JavaScript, a primitive (primitive value, primitive data type) is data that is not an `object` and has no `methods`. There are 6 primitive data types: `string`, `number`, `bigint`, `boolean`, `undefined`, and `symbol`. There also is `null`, which is seemingly primitive, but indeed is a special case for every `Object`: and any structured type is derived from `null` by the Prototype Chain.

> from: https://developer.mozilla.org/en-US/docs/Glossary/Primitive

Here are some examples – I’ll use pseudo code to demonstrate step-by-step how the coercion algorithm is applied:

[0] == true;

```
//EQUALITY CHECK...
[0] == true; 
 
//HOW IT WORKS...
//convert boolean using toNumber
[0] == 1;
//convert object using toPrimitive
//[0].valueOf() is not a primitive so use...
//[0].toString() -> "0"
"0" == 1; 
//convert string using toNumber
0 == 1; //false!
```


“potato” == true;

```
//EQUALITY CHECK...
"potato" == true; 
 
//HOW IT WORKS...
//convert boolean using toNumber
"potato" == 1;
//convert string using toNumber
NaN == 1; //false!
```


“potato” == false;

```
//EQUALITY CHECK...
"potato" == false; 
 
//HOW IT WORKS...
//convert boolean using toNumber
"potato" == 0;
//convert string using toNumber
NaN == 0; //false!
```

object with valueOf

```
//EQUALITY CHECK...
crazyNumeric = new Number(1); 
crazyNumeric.toString = function() {return "2"}; 
crazyNumeric == 1;
 
//HOW IT WORKS...
//convert object using toPrimitive
//valueOf returns a primitive so use it
1 == 1; //true!
```


object with toString

```
//EQUALITY CHECK...
var crazyObj  = {
    toString: function() {return "2"}
}
crazyObj == 1; 
 
//HOW IT WORKS...
//convert object using toPrimitive
//valueOf returns an object so use toString
"2" == 1;
//convert string using toNumber
2 == 1; //false!
```


### The Strict Equals Operator (===)

This one’s easy. If the operands are of different types the answer is always false. If they are of the same type an intuitive equality test is applied: object identifiers must reference the same object, strings must contain identical character sets, other primitives must share the same value. `NaN`, `null` and `undefined` will never === another type. `NaN` does not even === itself.

Common Examples of Equality Overkill

```
//unnecessary
if (typeof myVar === "function");
 
//better
if (typeof myVar == "function");
```

..since typeOf returns a string, this operation will always compare two strings. Therefore == is 100% coercion-proof.

```
//unnecessary
var missing =  (myVar === undefined ||  myVar === null);
 
//better
var missing = (myVar == null);
```

…null and undefined are == to themselves and each other.

> Note: because of the (very minor) risk that the `undefined` variable might get redefined, equating to null is slightly safer.

```
//unnecessary
if (myArray.length === 3) {//..}
 
//better
if (myArray.length == 3) {//..}
```

…enough said 😉


Reference: 

[12.5The if Statement](http://www.ecma-international.org/ecma-262/5.1/#sec-12.5)

[ToBoolean](http://www.ecma-international.org/ecma-262/5.1/#sec-9.2)

[JavaScript Coercion Demystified](http://webreflection.blogspot.com/2010/10/javascript-coercion-demystified.html)
