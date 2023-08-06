# Dyndis
[`pip install dyndis`](https://pypi.org/project/dyndis/)
## About
Dyndis is a library to easily and fluently make multiple-dispatch functions and methods. It was originally made for operators in non-strict hierarchical systems but can also serve any other multiple-dispatch purpose.
## Simple Example
```python
from typing import Union

from dyndis import MultiDispatch

foo = MultiDispatch()
@foo.add_func()
def foo(a: int, b: Union[int, str]):
    return "overload 1 <int, (int, str)>"
@foo.add_func()
def foo(a: object, b: float):
    return "overload 2 <any, float>"

foo(1, "hello")  # overload 1
foo(("any", "object", "here"), 2.5)  # overload 2
foo(2, 3)  # overload 1
foo(2, 3.0)  # overload 2
```
## Features
* dynamic upcasting
* customizable priorities for candidates
* seamless usage of type-hints and type variables
* advanced data structures to minimize candidate lookup time
* powerful caching of candidates by layer to minimize lookup time for repeat parameters without iterating through all candidates unnecessarily.
* implementor interface makes it easy to create method-like overloads
## How Does it Work?
The central class (and only one users need to import) is `MultiDispatch`. `MultiDispatch` contains candidate implementations sorted by both priority and types of the parameters they accept. When the `MultiDispatch` is called, it calls its relevant candidates (ordered by both priority, inheritance, and compatibility, expanded upon below) until one returns a non-`NotImplemented` return value.
## The Lookup Order
All candidates for parameters of types <T0, T1, T2..., TN> are ordered as follows:
 * Any candidate with a types that is incompatible with any type in the key is excluded. That is, if for any 0 <= `i` <= N, a candidate's type constraint for parameter `i` is not a superclass of Ti, the candidate is excluded.
 * Candidates are ordered by inheritance. A candidate is considered to inherit another candidate if all its parameter types are subclasses of (or are likewise covered by) the other's respective parameter type. A candidate will be considered before any other candidate it inherits. So for example, <int,object> will be considered before <Number, object>.
 * All candidates that do not inherit each other are sorted (descending) by their priority. All decorators have a parameter to set a priority for candidates, by default the priority is 0. Some automatic processes can change a candidate's priority over other candidates of equal priority (such as with symmetric candidates, below).
 
If two candidates have equal priority, and neither inherits of the other, an exception (of type `dyndis.AmbiguityError`) is raised (unless a candidate with greater precedence than both succeeds first).

If a candidate returns `NotImplemented`, the next candidate in the order is tried.
## Topology, Tries and Caches
`dyndis` uses a topological set composing non-compressing tries to order all its candidates by the parameter types, so that most of the candidates can be disregarded without any overhead.

Considering all these candidates for every lookup gets quite slow and encumbering very quickly. For this reason, every `MultiDispatch` automatically caches any work done by previous calls when it comes to sorting and processing candidates. The cache maintains the laziness of the lookup, and minimizes the work done at any given time.
## Default, Variadic, and Keyword parameters
* If a candidate has positional parameters with a default value and a type annotation, it will be included as an optional value. If the default value is `None`, it will be added to the type hint.
* If a candidate has positional parameters with a default value and no type annotation, or they are preceded by a default parameter without a type annotation, these parameters are ignored for the purpose of the candidate's parameter types. When called from a `MultiDispatch`, the parameter's values will always be the default.
* If a candidate has a variadic positional parameter, it is ignored. When called from a `MultiDispatch`, its value will always be `()`.
* If a candidate has keyword-only parameters, the parameter will not be considered for candidate types, it must either have a default value or be set when the `MultiDispatch` is called.
* If a candidate has a variadic keyword parameter, it is ignored. When called from a `MultiDispatch`, its value will be according to the (type-ignored) keyword arguments.

In general, when a `MultiDispatch` is called with keyword arguments, those arguments are not considered for candidate resolution and are sent to each attempted candidate as-is.
## Implementors
an `Implementor` is a descriptor that makes it easy to create method-like candidates inside classes.
```python
from dyndis import MultiDispatch

add = MultiDispatch()
class Base:
    __add__ = add.op  # MultiDispatch.op returns a delegate descriptor that acts as an operator

class A(Base):
    @add.implementor()
    def add(self, other):
        # in implementor methods, any parameter without a type hint is assumed to be of the owner class
        return "A+A"
    @add.implementor()
    def add(self, other: Base):
        return "A+Base"

class B(Base):
    @add.implementor()
    def add(self, other: A):
        return 'B+A'
    @add.implementor()
    def add(other: A, self):
        # this isn't pretty, we'll see how to circumvent this later
        return 'A+B'

a = A()
b = B()
base = Base()
a + b  # A+B
a + base  # A+Base
a + a  # A+A
b + a  # B+A
```

In addition, implementor methods can also use the `Self` object to represent the containing class in more powerful manners.

```python
from typing import Union
from dyndis import Self, MultiDispatch

foo = MultiDispatch('foo')

class A:
    @foo.implementor()
    def foo(self, other: bool):
        return "bool"
    @foo.implementor()
    def foo(self, other: Union[Self, str]):
        return "A or str"

a = A()
a.foo(False)  # "bool"
a.foo(a)  # "A or str"
```

## Symmetric Candidates
In some cases, we will have multiple candidates that only differ by the order of the parameters (for example, addition is usually symmetrical). For this, we can make use of the `symmetric` parameter available both in `add_func` and `implementor` methods. Setting this parameter to `True` will also add virtual candidates of all the permutations of the argument types.
```python
from dyndis import MultiDispatch

add = MultiDispatch()
class Base:
    __add__ = add.op  # MultiDispatch.op returns a delegate descriptor that acts as an operator

class A(Base):
    ...

class B(Base):
    @add.implementor(symmetric = True)
    def add(self, other: A):
        return 'A+B/B+A'

a = A()
b = B()
a + b  # A+B/B+A
b + a  # A+B/B+A
```
All permutations of a candidate are considered to have a priority lower than the original candidate.

One should take care when making symmetric candidates, as it can create an inordinate number of candidates (super-exponential to the number of parameters).
## Special Type Annotations
type annotations can be of any type, or among any of these special values
* `dyndis.Self`: used in implementors (see above), and is an error to use outside of them
* `typing.Union`: accepts parameters of any of the enclosed type
* `typing.Optional`: accepts the enclosed type or `None`
* `typing.Any`: is considered a supertype for any type, including `object`
* Any of typing's aliases and abstract classes such as `typing.List` or `typing.Sized`: equivalent to their origin type (note that specialized aliases such as `typing.List[str]` are invalid)
* `typing.TypeVar`: see below
* `None`, `...`, `NotImplemented`: equivalent to their types
* python 3.8 only: `typing.Literal` for singletons (`None`, `...`, `NotImplemented`): equivalent to their enclosed value

In addition, the following types are automatically converted (in compliance with various PEPs):
* `float` -> `Union[int, float]`
* `complex` -> `Union[int, float, complex]`
* `bytes` -> `typing.ByteString`
## `TypeVar` annotations
Parameters can also be annotated with `typing.TypeVar`s. These variables bind greedily as they are encountered, and count as matched upon first binding. After first binding, they are treated as the bound type (or the lowest constraint of the `TypeVar`) for all respects.

```python
from typing import TypeVar, Any

from dyndis import MultiDispatch

T = TypeVar('T')
foo = MultiDispatch()

@foo.add_func()
def foo(a: T, b: T):
    return "type(b) <= type(a)"
@foo.add_func()
def foo(a: Any, b: Any):
    return "type(b) </= type(a"

foo(1, 1)  # <=
foo(1, True)  # <=
foo(2, 'a')  # </=
foo(object(), object())  # <=
# type variables bind greedily, meaning their exact value will be equal to the first type they encounter
foo(False, 2)  # </=
```

`Typevars` are considered supertypes of their bound (or `object` if they are without bounds), or their constraints.

## `UnboundDelegate`
Advanced usage can also make use of the various `UnboundDelegate` subclasses to get attributes of types assigned to type variables, to allow for Rust-style type requirements

```python
from typing import TypeVar

from dyndis import MultiDispatch, UnboundAttr

class StrDict(dict):
    I = str

class MyList(list):
    I = int

T = TypeVar('T', StrDict, MyList)
T_I = UnboundAttr(T, 'I')
foo = MultiDispatch()

@foo.add_func()
def foo(a: T, i: T_I):
    return a[i]

d = StrDict(a=3, b=4)
m = MyList([3,4])

foo(d, 'a')  # 3
foo(m, 1)  # 4
``` 
## RawReturnValue
By default, if a candidate returns `NotImplemented`, it indicates to the `MultiDispatch` that the next candidate should be tried. However, on the rare occasion when `NotImplemented` is the actual return value desired, a candidate should return `dyndis.RawNotImplemented`.