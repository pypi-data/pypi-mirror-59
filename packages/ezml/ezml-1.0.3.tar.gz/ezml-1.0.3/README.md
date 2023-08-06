# E-Z Markup Language / Python Parser

## What Is E-Z Markup/Parser?
E-Z Markup Language is an extremely simple, xml-flavored, data storage + aquisition method, 
revolving around this parser, written in Python.

At this point, general usage is simply variable storage.

# Basic usage:


 

### Example .ezml file(test.ezml):

```xml
<ezml>
<meta>
Author: Example Author
Info: Class Schedule
Date: January 17th, 2020
</meta>
<var title>Campus #1 Weekly Schedule Example</title>
<var monday>No School</monday>
<var tuesday>
class 1: history
class 2: science
</tuesday>
<var wednesday>Not On Campus</wednesday>
<var thursday>
class 1: history
class 2: science
</thursday>
<var friday>
class 1: history
class 2: ap-history
class 3: science
</ezml>

```


### Parsing Example (From File) :

```python

from EZML import EZML, utils

ezml = EZML(utils.dump_file('test.ezml')) 
print(ezml.meta)
print(ezml.var['title'])

print(ezml.var['monday'])

print(f"Tuesdays Schedule:\n {ezml.var['tuesday']}")

```


### Parsing Example (From String):

```python

from EZML import EZML

ezml = EZML("<ezml><meta>Title: Hello World!</meta><var title>Foo<title><var bar>Hello World!</bar></ezml>") 
print(ezml.meta)
print(ezml.var['title'])
print(ezml.var['bar'])

```

