# ES6 Import 和 Export 语法

> https://www.v2ex.com/t/738530

在 ES6 之前，我们在一个 HTML 文件中可以使用多个 script 标签来引用不同的 JavaScript 文件，如下所示:

```
<script type="text/javascript" src="home.js"></script>
<script type="text/javascript" src="profile.js"></script>
<script type="text/javascript" src="user.js"></script>
```

但是如果我们在不同的 JavaScript 文件中有一个同名的变量，将会出现命名冲突，你实际得到的可能并不是你期望的值。

ES6 增加了模块的概念来解决这个问题。

在 ES6 中，我们编写的每一个 JavaScript 文件都被称为模块。我们在每个文件中声明的变量和函数不能用于其他文件，除非我们将它们从该文件中导出并、在另一个文件中得到引用。

因此，在文件中定义的函数和变量是每个文件私有的，在导出它们之前，不能在文件外部访问它们。

`export` 有两种类型:

命名导出: 在一个文件中可以有多个命名导出

默认导出: 单个文件中只能有一个默认导出

## JavaScript 中的命名导出

如下所示，将单个变量命名导出:

```
export const temp = "This is some dummy text";
```

如果想导出多个变量，可以使用大括号指定要输出的一组变量。

```
const temp1 = "This is some dummy text1";
const temp2 = "This is some dummy text2";
export { temp1, temp2 };
```


需要注意的是，导出语法不是对象语法。因此，在 ES6 中，不能使用键值对的形式导出。

```
// This is invalid syntax of export in ES6
export { key1: value1, key2: value2 }
```

import 命令接受一对大括号，里面指定要从其他模块导入的变量名。

```
import { temp1, temp2 } from './filename';
```
> **注意，不需要在文件名中添加.js 扩展名，因为默认情况下会考虑该拓展名。**

```
 // import from functions.js file from current directory

import  { temp1, temp2 }  from  './functions';

 // import from functions.js file from parent of current directory

import  { temp1 }  from  '../functions';
```
提示一点，导入的变量名必须与被导入模块对外接口的名称相同。

因此，导出应使用：

```
// constants.js

export  const  PI  =  3.14159;
```

那么在导入的时候，必须使用与导出时相同的名称：

```
import  {  PI  }  from  './constants';

// This will throw an error

import  { PiValue }  from  './constants';
```

如果想为输入的变量重新命名，可以使用 `as` 关键字，语法如下:

```
import  {  PI  as PIValue }  from  './constants';
```

我们以为 PI 重命名为 PIValue，因此不能再使用 PI 变量名。

导出时也可使用下面的重命名语法：

```
// constants.js

const  PI  =  3.14159;

export  {  PI  as PIValue };
```

然后在导入是，必须使用 PIValue 。

```
import  { PIValue }  from  './constants';
```

命名导出某些内容之前必须先声明它。

```
export  'hello';  // this will result in error

export  const greeting =  'hello';  // this will work

export  { name:  'David'  };  // This will result in error

export  const object =  { name:  'David'  };  // This will work
```

我们来看下面的 validations.js 文件:

```
// utils/validations.js

const  isValidEmail  =  function(email)  {

  if  (/^[^@ ]+@[^@ ]+\.[^@ \.]{2,}$/.test(email))  {

  return  "email is valid";

  }  else  {

  return  "email is invalid";

  }

};

const  isValidPhone  =  function(phone)  {

  if  (/^[\\(]\d{3}[\\)]\s\d{3}-\d{4}$/.test(phone))  {

  return  "phone number is valid";

  }  else  {

  return  "phone number is invalid";

  }

};

function  isEmpty(value)  {

  if  (/^\s*$/.test(value))  {

  return  "string is empty or contains only spaces";

  }  else  {

  return  "string is not empty and does not contain spaces";

  }

}

export  { isValidEmail, isValidPhone, isEmpty };
```

在 index.js 中，我们可以使用如下函数:

```
// index.js

import  { isEmpty, isValidEmail }  from  "./utils/validations";

console.log("isEmpty:",  isEmpty("abcd"));  // isEmpty: string is not empty and does not contain spaces

console.log("isValidEmail:",  isValidEmail("abc@11gmail.com"));  // isValidEmail: email is valid

console.log("isValidEmail:",  isValidEmail("ab@c@11gmail.com"));  // isValidEmail: email is invalid
```

## JavaScript 的默认导出

单个文件中最多只能有一个默认导出。但是，你可以在一个文件中使用多个命名导出和一个默认导出。

要声明一个默认导出，我们需要使用以下语法：

```
//constants.js

const name =  'David';

export  default name;
```

在导入时就不需要再使用花括号了。

```
import name from  './constants';
```

如下，我们有多个命名导出和一个默认导出:

```
// constants.js

export  const  PI  =  3.14159;

export  const  AGE  =  30;

const  NAME  =  "David";

export  default  NAME;
```

此时我们使用 `import` 导入时，只需要在大括号之前指定默认导出的变量名。

```
// NAME is default export and PI and AGE are named exports here

import  NAME,  {  PI,  AGE  }  from  './constants';
```

使用 export default 导出的内容，在导入的时候，import 后面的名称可以是任意的。

```
// constants.js

const  AGE  =  30;

export  default  AGE;

import myAge from ‘./constants’;

console.log(myAge);  // 30
```

另外，export default 的变量名称从 Age 到 myAge 之所以可行，是因为只能存在一个 export default 。因此你可以随意命名。还需注意的是，关键字不能在声明变量之前。

```
// constants.js

export  default  const  AGE  =  30;  // This is an error and will not work
```

因此，我们需要在单独的一行使用关键字。

```
// constants.js

const  AGE  =  30;

export  default  AGE;
```

不过以下形式是允许的:

```
//constants.js

export  default  {

 name:  "Billy",

 age:  40

};
```

并且需要在另一个文件中使用它

```
import user from  './constants';

console.log(user.name);  // Billy

console.log(user.age);  // 40
```

还有，可以使用以下语法来导入 constants.js 文件中导出的所有变量:

```
// test.js

import  *  as constants from  './constants';
```

下面，我们将导入所有我们 constants.js 存储在 constants 变量中的命名和 export default 。因此，constants 现在将成为对象。

```
// constants.js

export  const  USERNAME  =  "David";

export  default  {

 name:  "Billy",

 age:  40

};
```

在另一个文件中，我们按一下方式使用。

```
// test.js

import  *  as constants from  './constants';

console.log(constants.USERNAME);  // David

console.log(constants.default);  // { name: "Billy", age: 40 }

console.log(constants.default.age);  // 40
```

也可以使用以下方式组合使用命名导出和默认导出:

```
// constants.js

const  PI  =  3.14159;  const  AGE  =  30;

const  USERNAME  =  "David";

const  USER  =  {

 name:  "Billy",

 age:  40

};

export  {  PI,  AGE,  USERNAME,  USER  as  default  };

import  USER,  {  PI,  AGE,  USERNAME  }  from  "./constants";
```

总而言之:

ES6 中，一个模块就是一个独立的文件，该文件内部的所有变量，外部都无法获取。如果想从外部读取模块内的某个变量，必须使用 export 关键字导出该变量，使用 import 关键字导入该变量。

# [Node.js 如何处理 ES6 模块](http://www.ruanyifeng.com/blog/2020/08/how-nodejs-use-es6-module.html)

ES6 模块和 Node.js 默认用的CommonJS 模块有很大的差异。

语法上面，CommonJS 模块使用`require()`加载和`module.exports`输出，ES6 模块使用`import`和`export`。

用法上面，`require()`是同步加载，后面的代码必须等待这个命令执行完，才会执行。`import`命令则是异步加载，或者更准确地说，ES6 模块有一个独立的静态解析阶段，依赖关系的分析是在那个阶段完成的，最底层的模块第一个执行。

《完》
