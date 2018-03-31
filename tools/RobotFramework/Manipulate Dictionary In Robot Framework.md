### Manipulate Dictionary In Robot Framework

> 2018.3.30

In Robot Framework, users can use following keywords to manipulate Dictionaries.  

- Create Dictionary (used for creating a new dictionary)
- Set To Dictionary (used for adding key and value to a dictionary)
- Copy Dictionary (used for copying existing dictionary to a new dictionary)
- Log Dictionary (used for logging dictionary keys and values)
- Get Dictionary Keys (used for retrieving all keys in a dictionary)
- Get From Dictionary (used for returning a value of a key)
- Remove From Dictionary (used for removing given keys from a dictionary)
- Keep In Dictionary (used for keeping the given keys in the dictionary and removes all other) 
- Dictionary Should Contain Key (used for verifying that the dictionary should contain the key) 


See the example below. 

```
*** Settings ***
Library           Collections

*** Test Cases ***
Create Dictionary Test
    [Documentation]    Creates and returns a dictionary based on given items
    Comment    Create a Dictionary Object
    ${MyDictionary}=    Create Dictionary
    Comment    Adds the given key_value_pairs and items to the dictionary
    Set To Dictionary    ${MyDictionary}    Foo1    Value1
    Set To Dictionary    ${MyDictionary}    Foo2    Value2
    Set To Dictionary    ${MyDictionary}    Foo3    Value3
    Set To Dictionary    ${MyDictionary}    Foo4    Value4
    Comment    Logs the size and contents of the dictionary using given level.
    Log Dictionary    ${MyDictionary}
    Comment    Copy Existing Dictionary to a new Dictionary
    ${MyDictionary2}=    Copy Dictionary    ${MyDictionary}
    Log Dictionary    ${MyDictionary2}
    Comment    Returns keys of the given dictionary
    ${Keys}=    Get Dictionary Keys    ${MyDictionary}
    Log    ${Keys}
    Comment    Returns a value from the given dictionary based on the given key
    ${keyValue}=    Get From Dictionary    ${MyDictionary}    Foo2
    Log    ${keyValue}
    Comment    Removes the given keys from the dictionary.
    Remove From Dictionary    ${MyDictionary}    Foo1
    Log Dictionary    ${MyDictionary}
    Comment    Keeps the given keys in the dictionary and removes all other.
    Keep In Dictionary    ${MyDictionary}    Foo4
    Log Dictionary    ${MyDictionary}
    Dictionary Should Contain Key    ${MyDictionary}    Foo4
```

Run the script above and see the result below

```
Starting test: RobotCollectionsExample.Collections Keyword Test Suite.Create Dictionary Test
20150416 23:54:37.718 :  INFO : ${MyDictionary} = {}
20150416 23:54:37.728 :  INFO : 
Dictionary size is 4 and it contains following items:
Foo1: Value1
Foo2: Value2
Foo3: Value3
Foo4: Value4
20150416 23:54:37.728 :  INFO : ${MyDictionary2} = {u'Foo4': u'Value4', u'Foo1': u'Value1', u'Foo2': u'Value2', u'Foo3': u'Value3'}
20150416 23:54:37.728 :  INFO : 
Dictionary size is 4 and it contains following items:
Foo1: Value1
Foo2: Value2
Foo3: Value3
Foo4: Value4
20150416 23:54:37.728 :  INFO : ${Keys} = [u'Foo1', u'Foo2', u'Foo3', u'Foo4']
20150416 23:54:37.728 :  INFO : [u'Foo1', u'Foo2', u'Foo3', u'Foo4']
20150416 23:54:37.728 :  INFO : ${keyValue} = Value2
20150416 23:54:37.728 :  INFO : Value2
20150416 23:54:37.738 :  INFO : Removed item with key 'Foo1' and value 'Value1'.
20150416 23:54:37.738 :  INFO : 
Dictionary size is 3 and it contains following items:
Foo2: Value2
Foo3: Value3
Foo4: Value4
20150416 23:54:37.738 :  INFO : Removed item with key 'Foo2' and value 'Value2'.
20150416 23:54:37.738 :  INFO : Removed item with key 'Foo3' and value 'Value3'.
20150416 23:54:37.738 :  INFO : 
Dictionary has one item:
Foo4: Value4
Ending test:   RobotCollectionsExample.Collections Keyword Test Suite.Create Dictionary Test
```

In this example, we used all the keywords mentioned above. The test passed.

From: [Manipulate Dictionary In Robot Framework](http://seleniummaster.com/sitecontent/index.php/selenium-robot-framework-menu/selenium-robot-framework-python-menu/259-manipulate-dictionary-in-robot-framework)