# JSchema2py #
JSchema2py is able to generate python classes starting from JSONSchema and provides the automatic support for types
and constraints checking.

## Installation
The package can be installed through pip:

    $ pip install jschema2py

or downloaded from [GitHub](https://github.com/jacopodl/jschema2py).

## Examples
For example, given the following schema:
```json
{
  "title": "UserInfo",
  "type": "object",
  "properties": {
    "name": {
      "type": "string",
      "pattern": "^[^a-z0-9]"
    },
    "userName": {
      "type": "string"
    },
    "age": {
      "type": "integer",
      "minimum": 0,
      "maximum": 100
    }
  }
}
```
jschema2py can easily convert it into python class in this way (Assume here that the schema is stored into variable 
called schema):
```python
from jschema2py import build_class
UserInfo = build_class(schema)
user = UserInfo()
user.name = "Jacopo"
user.userName = "JDL"
user.age = 24
print(user)
```
validation will be performed on the object manipulation:
```python
user.name = "jacopo" # raise ConstraintError (pattern: ^[^a-z0-9])
user.age = "24" # raise TypeError
```
The object can be serialized into a JSON document:
```python
jsdoc = str(user)
```
### Accessing generated classes
If one of the property of the schema refers to another object, you can access the class that represents the referred 
object by using method get_class:
```json
{
  "title": "Nested",
  "type": "object",
  "properties": {
    "inner": {
      "title": "Inner",
      "type": "object",
      "properties": {
        "string": {
          "type": "string",
          "default": "I'm inner!"
        }
      }
    }
  }
}
```
```python
from jschema2py import build_class
Nested = build_class(schema)
nested = Nested()
nested.inner = nested.get_class("inner")() # Gets the class associated with the property "inner" 
print(nested.inner.string)
```
