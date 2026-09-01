# Name
`intervals` - Pure Python implementation of data structures for interval operations

- [Description](#description)
  - [Terminology](#terminology)
- [Installation](#installation)
- [API](#api)
  - [Generic Intervals](#generic-intervals)
    - [The BaseInterval class](the-baseinterval-class)
      - [BaseInterval variables and methods](BaseInterval-variables-and-methods)
    - [The LeftClosedInterval subclass](#the-leftclosedinterval-subclass)
    - [The Interval subclass](#the-interval-subclass)
      - [Interval  examples](#interval-examples)
    - [The LeftClosedPoint subclass](#the-leftclosedpoint-subclass)
    - [The Point subclass](#the-point-subclass)
    - [The ClosedInterval subclass](#the-closedinterval-subclass)
    - [The ClosedPoint subclass](#the-closedpoint-subclass)
  - [Interval collections](#Interval-collections)
    - [The IntervalList class](#the-intervallist-class)
      - [IntervalList variables and methods](#IntervalList-variables-and-methods)
      - [IntervalList examples](#intervallist-examples)
    - [The IntervalSet class](#the-intervalset-class)


# Description

The `intervals` module implements classes for performing arithmetic, `set`-like, and search operations on one or a collection of one-dimensionale interval(s). 

### Terminology

- **namespace**: Optional, depending on class. Namespace can represent axes (*e.g.*, `X`), contig names (*e.g.*, `Chr1`), etc. Interval methods operate only between instances in the same namespace. The default namespace is `None`.
  
- **null**: an interval without both start *and* stop coordinate values. Null coordinates are implemented as `nan` values and null namespace as `None`.
  
- **empty**: an interval that is null or with distance (length) between beginning and end coordinates less-than or equal-to zero units long.


# Installation

Currently, only installation on Unix-/Linux-like (including macOS) systems from source using `make` is supported (installing on macOS futher requires [Xcode Command Line Tools](https://developer.apple.com/download) to be installed):

```bash
$ git clone https://github.com/bredeson/intervals.git
$ cd intervals
$ make install PREFIX=/full/path/to/install/prefix
```
The above will install the `intervals` module into the subdirectory heirarchy `$(PREFIX)/lib/pythonX.X/site-packages` (default `$(PREFIX)` is `/usr/local`). The above works well for installing into Conda/Mamba environments. Assuming the user has an environment named `pyenv` with the python interpreter installed, the following command will install `intervals` into the right location:

```bash
$ mamba activate pyenv
$ make install PREFIX=${CONDA_PREFIX}
```

To install the `intervals` module into a non-standard user-location, use the `$(INSTALL_PATH)` variable with `make`:

```bash
$ make install INSTALL_PATH=/full/path/to/install/prefix
```
This will install the `intervals` module into the `$(PREFIX)`dirctory directly (without the additional subdirectory heirarchy).


# Documentation

After proper installation, there are two ways of getting the complete documentation for the `intervals` API. Read `man`-like help pages by doing either of the following:

1. On the command line:
    ```bash
    $ pydoc intervals.intervals
    $ pydoc intervals.collections
    ```

2. In the Python REPL:
    ```python
    >>> from intervals import Interval, IntervalList
    
    # for a full `man`-like help page:
    >>> help(Interval)
    >>> help(IntervalList)
    
    # for a specific method:
    >>> help(Interval.isintersecting)
    ```


# API

## Generic Intervals

### The BaseInterval class

Base class representing generic one-dimensional intervals. Not meant to be used directly. Instead, users are encouraged to use any of `BaseInterval`'s child classes.

The `self.namespace` attribute provides an abstraction allowing this module access to a stable id or name and enable comparions between objects in potentially different namespaces (X, Y, or Z dimensions, sequence names, etc.).


#### BaseInterval variables and methods

In the following table, `self` and `other` both represent instances of `BaseInterval` or one of its subclasses.

| Attribute                                 | Description                                                  |
| ----------------------------------------- | ------------------------------------------------------------ |
| `self.beg`                                | Bound variable. Return the begin/start coordinate (0-based, inclusive) of `self`. |
| `self.clear()`                            | Callable. Alias for `null()`.                                           |
| `self.copy()`                             | Callable. Return new copy of `self`.                                    |
| `self.difference(other)`                  | Callable. Return an Interval object representing the set difference of `self` and `other`. |
| `self.difference_update(other)`           | Callable. Update `self` with the result of `difference()`.              |
| `self.empty()`                            | Callable. Set the `self` start and end coordinates both to zero.        |
| `self.end`                                | Bound variable. Return the end/stop coordinate (0-based, exclusive) of `self`. |
| `self.hull()` or `self.hull(other)`       | Callable. Return an Interval representing the hull of `self` or, optionally, `self` and `other`. |
| `self.inner_distance(other)`              | Callable. Return the numeric inner distance between two `self` and `other`. |
| `self.intersection(other)`                | Callable. Return an Interval representing the set intersection between `self` and `other`. |
| `self.intersection_update(other)`         | Update the `self` with the result of `intersection()`.        |
| `self.isabutting(other)`                  | Callable. Test if `self` is abutting the start or end of `other`.       |
| `self.isabutting_beg(other)`              | Callable. Test if `self` is abutting the start of `other`.              |
| `self.isabutting_end(other)`              | Callable. Test if `self` is abutting the end of `other`.                |
| `self.isabutting_start(other)`            | Callable. Alias for `isabutting_beg()`.                                 |
| `self.isabutting_stop(other)`             | Callable. Alias for `isabutting_stop()`.                                |
| `self.isdisjoint(other)`                  | Callable. Test if `self` and `other` are non-intersecting.               |
| `self.isempty()`                          | Callable. Test if `self` is a zero-lengthed interval.                   |
| `self.isfinite()`                         | Callable. Test if `self` is a finite interval.                          |
| `self.isnull()`                           | Callable. Test if `self` has `nan`-valued start or end.                 |
| `self.isintersecting(other)`              | Callable. Test if `self` intersects `other`.                              |
| `self.isintersecting_beg(other)`          | Callable. Test if `self` intersects the start of `other`.                 |
| `self.isintersecting_end(other)`          | Callable. Test if `self` intersects the end of `other`.                   |
| `self.isintersecting_start(other)`        | Callable. Alias for `isintersecting_beg()`.                             |
| `self.isintersecting_stop(other)`         | Callable. Alias for `isintersecting_end()`.                             |
| `self.issingleton()`                      | Callable. Test if `self` is 1 unit long.                                |
| `self.issubinterval(other)`               | Callable. Alias for `issubset()`.                                       |
| `self.issubset(other)`                    | Callable. Test if `self` is contained within `other`.                   |
| `self.issuperinterval(other)`             | Callable. Alias for `issuperset()`.                                     |
| `self.issuperset(other)`                  | Callable. Test if `self` contains `other`.                              |
| `self.mid`                                | Bound variable. Read only. Return the mid-point coordinate of `self`.                    |
| `self.name`                               | Bound variable. Alias for `namespace`.                                        |
| `self.namespace`                          | Bound variable. The namespace of `self` (optional).                           |
| `self.null()`                             | Callable. Delete from `self` the values in the `name`, `start`, and `end` bound variables. |
| `self.outer_distance(other)`              | Callable. Return the outer distance between `self` and `other`.         |
| `self.intersection_fraction(other)`       | Callable. Return the intersection fraction as relative to length of `self`.  |
| `self.intersection_length(other)`         | Callable. Return the length of intersection betwen `self` and `other`.       |
| `self.start`                              | Bound variable. Alias for `beg`.                                              |
| `self.stop`                               | Bound variable. Alias for `end`.                                              |
| `self.symmetric_difference(other)`        | Callable. Return 2-tuple representing the symmetric difference (XOR) between `self` and `other`. |
| `self.symmetric_difference_update(other)` | Callable. Raises `NotImplementedError`.                                 |
| `self.to_slice()`                         | Callable. Return a `slice` object containing the Pythonic range of intersecting items, or `slice(-1, -1)` if none.  |
| `self.to_string()`                        | Callable. Return string representatio of `self`. Same as `str(self)`.   |
| `self.union(other)`                       | Callable. Return an Interval object representing the union of `self` and `other`. |
| `self.union_update(other)`                | Callable. Update `self` with the result of `union()`.                   |
|                                           |                                                               |


### The LeftClosedInterval subclass

Class representing a generic left-closed, right-open continuous interval; *i.e.*, start and end coordinates may be floating-point values, with start inclusive in interval intersection and exclusive end. Inherits from the `BaseInterval` class.

The `self.namespace` attribute provides an abstraction allowing this module access to a stable id or name and enable comparions between objects in potentially different namespaces (X, Y, or Z dimensions, sequence names, etc.).


### The Interval subclass

Class representing a generic left-closed, right-open discrete interval; *i.e.*, start and end coordinates only permit integer values, with start (0-based) inclusive in interval intersection and exclusive end (1-based). Inherits from the `LeftClosedInterval` subclass.

The primary simple interval object type for genomic applications is the `Interval`. It inherits from `BaseInterval` and enforces integer `start` and`end` bound variables. It's first argument is the `name` (*i.e.*, the `namespace`) of the sequence for which the interval spans.


#### Interval examples:

```python
>>> from intervals import Interval

>>> i1 = Interval("chr1", 100, 1000)
>>> i2 = Interval("chr1", 750, 2000)

>>> i1 & i2
Interval(chr1:750-1000)

>>> i1 | i2
Interval(chr1:100-2000)

>>> i1 ^ i2
(Interval(chr1:100-750), Interval(chr1:1000-2000))

>>> i1.isintersecting(i2)
True

>>> i1.isintersecting_start(i2)
True

>>> i1.isintersecting_end(i2)
False

>>> i1.intersection_length(i2)
250

>>> i1.name
'chr1'

>>> i1.start
100

>>> i2.end = 1000
>>> i1.issuperset(i2)
True

>>> i2 in i1
True

>>> i1 in i2
False
```

### The LeftClosedPoint subclass

Class representing a generic left-closed, right-open continuous point.  Inherits from the `LeftClosedInterval` subclass.


### The Point subclass

Class representing a generic left-closed, right-open discrete point.  Inherits from the `LeftClosedPoint` subclass.


### The ClosedInterval subclass

Class representing a generic fully-closed continuous interval; *i.e.*, start and end coordinates may be floating-point values, and are inclusive in interval intersection. Inherits from the `BaseInterval` class.

The `self.namespace` attribute provides an abstraction allowing this module access to a stable id or name and enable comparions between objects in potentially different namespaces (X, Y, or Z dimensions, sequence names, etc.).


### The ClosedPoint subclass

Class representing a generic fully-closed continuous point.  Inherits from the `ClosedInterval` class.


## Interval collections: 

### The IntervalList class

 A list of BaseInterval-descendant objects, sorted by start position. IntervalList inherits from `collections.deque()` but requires all `BaseBaseInterval`-descendant object members to be of the same namespace, or a ValueError is raised. 
    
For many functions to work as expected, the user is required to maintain IntervalList members in sorted order (which is not  enforced by the class) or risk incorrect behavior. As such, the  user is recommended to use the `insort()` and `insortleft()`  methods to insert new members into the IntervalList in proper order. The `update()` and `updateleft()` methods are provided to insert multiple members at once. Methods such as `append()`, `appendleft()`, `extend()`, and `extendleft()` are provided for convenience and API consistency with `collections.deque()`, but the user is responsible for ensuring sort order is maintained when using these methods. Unlike the `deque()` class,however,  an in-place `list()`-like `sort()` method is provided.

Use the `find_index()` method to find the index of a member equal to a given interval.

Use `find_index_beg()` and `find_index_end()` methods to find the indices of the first and last members that intersect a given interval, respectively, or the indices between existing members when no intersection is found. 

`find_intersection_index_beg()` and `find_intersection_index_end()`  methods are intended to find the indices of the first and last  members intersecting a given interval, respectively, or return -1 when no intersection is found.

Use `find_insertion_index_beg()` and `find_insertion_index_end()` methods to find the indices where new members should be inserted that will maintain sort order.


#### IntervalList variables and methods

In the following table, `self` represents an `IntervalList` instance, `interval` an instance of `BaseInterval` or one of its subclasses, and `iterable` is an iterable object containing zero or more interval objects as queries for searching.

| Attribute  | Description |
|---------------------------------------------|------------------------------|
| `self.append(interval)`                     | Callable. Add an interval to the right side of `self`. |
| `self.appendleft(interval)`                 | Callable. Add an interval to the left side of `self`. |
| `self.beg`                                  | Bound variable. Read only. Return the begin/start coordinate (0-based, inclusive) of the first interval in `self`, or `nan` if empty. |
| `self.clear()`                              | Callable. Remove all elements from `self`. |
| `self.copy()`                               | Callable. Return a shallow copy of `self`. |
| `self.count(interval)`                      | Callable. Return number of occurrences of `interval` in `self`. |
| `self.end`                                  | Bound variable. Read only. Return the end/stop coordinate (0-based, exclusive) of the last interval in `self`, or `nan` if empty. |
| `self.extend(iterable)`                     | Callable. Extend the right side of the `self` with intervals from `iterable`. |
| `self.extendleft(iterable)`                 | Callable. Extend the left side of `self` with elements from the iterable. |
| `self.find_index(interval)`                 | Callable. Return the first index of `interval` in `self`. Raises ValueError if the value is not present. |
| `self.find_index_beg(interval)`             | Callable. Return the start (0-based inclusive) index for `interval`. |
| `self.find_index_end(interval)`             | Callable. Return the end (0-based exclusive) index for `interval`. |
| `self.find_index_nearest(interval)`         | Callable. Return the nearest (inclusive) index for an `interval`, returns the left-most index when members are equidistant to `interval`. |
| `self.find_index_start(interval)`           | Callable. Alias for `find_index_beg()`. |
| `self.find_index_stop(interval)`            | Callable. Alias for `find_index_end()`. |
| `self.find_insertion_index(interval)`       | Callable. The recommended method for determining an `interval`s insertion position. Return the insertion index to the right of any existing identical intervals, maintaining the observed order.  |
| `self.find_insertion_index_beg(interval)`   | Callable. Return the insertion index for a given `interval`, where the index points to the beginning/left of any existing identical intervals.  |
| `self.find_insertion_index_end(interval)`   | Callable. Return the insertion index for a given `interval`, where the index points to the end/right of any existing identical intervals.  |
| `self.find_insertion_index_start(interval)` | Callable. Alias for `find_insertion_index_beg()`  |
| `self.find_insertion_index_stop(interval)`  | Callable. Alias for `find_insertion_index_end()`  |
| `self.find_intersection_index_beg(interval)`     | Callable. Return the (0-based inclusive) index of the left-most intersecting interval in `self` for a given `interval`, or -1 if none. |
| `self.find_intersection_index_end(interval)`     | Callable. Return the (0-based exclusive) index of the right-most intersecting interval in `self` for a given `interval`, or -1 if none. |
| `self.find_intersection_index_nearest(interval)` | Callable. Return the (0-based inclusive) index of the nearest intersecting interval in `self` for a given `interval`, or -1 if none. Returns the left-most index when members are equidistant to `interval`. |
| `self.find_intersection_index_range(iterable)`   | Callable. Homage to `range()`. Returns generator object yielding the indices for intervals in `self` intersecting those in `iterable`. |
| `self.find_intersection_index_slice(iterable)`   | Callable. Perform an intersect search with one or more query interval objects in `iterable` and return a `slice` object containing the Pythonic range of intersecting items, or `slice(-1, -1)` if none. |
| `self.find_intersection_index_start(interval)`   | Callable. Alias for `find_intersection_index_beg()`. |
| `self.find_intersection_index_stop(interval)`    | Callable. Alias for `find_intersection_index_end()`. |
| `self.find_intersection_pairs(iterable)`         | Callable. Preform an intersect search of `self` with one or more interval objects in `iterable` and return a generator object producing a 2-tuple for each interval in `iterable` and its intersecting member in `self`. |
| `self.find_intersecting(iterable)`              | Callable. Perform an intersect search of `self` with an `iterable` of interval objects and return an generator object producing members of `self` that intersect. |
| `self.index(interval)`                      | Callable. Alias of `find_index()`. |
| `self.insert(index, interval)`              | Callable. Insert `interval` into `self` before `index`. |
| `self.insort(interval)`                     | Callable. Insert an `interval` into its sorted position, with identical intervals inserted to the right of existing ones. |
| `self.insortleft(interval)`                 | Callable. Insert an `interval` into its sorted position, with identical intervals inserted to the left of existing ones. |
| `self.intersection_fraction(iterable)`      | Callable. Returns the fraction of intersection an `iterable` of `interval`s has with those of `self`. |
| `self.intersection_length(iterable)`        | Callable. Returns the length of intersects an `iterable` of interval objects have with `self`. |
| `self.isempty()`                            | Callable. Test if `self` is contains no intervals. |
| `self.isfinite()`                           | Callable. Test if `self` is a finite interval. |
| `self.isnull()`                             | Callable. Test if `self` has `nan`-valued start or end. |
| `self.namespace`                            | Bound variable. Read only. The namespace of `self` (optional). |
| `self.null()`                               | Callable. Alias for `clear()`. |
| `self.pop()`                                | Callable. Pop one interval off the right side of `self` and return it. |
| `self.popleft()`                            | Callable. Pop one interval off the left side of `self` and return it. |
| `self.remove(interval)`                     | Callable. Remove an `interval` from `self`. |
| `self.reverse()`                            | Callable. Reverse in place the order of interval members in `self.` |
| `self.rotate(int)`                          | Callable. Rotate `self` n steps to the right (default n=1). If n is negative, rotates left. |
| `self.sort()`                               | Callable. Sort `self` in-place. |
| `self.start`                                | Bound variable. Read only. Alias for `beg`. |
| `self.stop`                                 | Bound variable. Read only. Alias for `end`. |
| `self.update(iterable)`                     | Callable. Insort into `self` the intervals contained in `iterable`, with identical intervals inserted to the right of existing ones. |
| `self.updateleft(iterable)`                 | Callable. Insort into `self` the intervals contained in `iterable`, with identical intervals inserted to the left of existing ones. |

#### IntervalList Examples:

```python
>>> from intervals import Interval, IntervalList

>>> ilist = IntervalList([Interval("chr1",0,100),Interval("chr1",150,350)])

>>> ilist.append(Interval("chr1",500,750))

>>> ilist.insort(Interval("chr1",125,145))

>>> ilist
IntervalList([Interval(chr1:0-100),
              Interval(chr1:125-145),
              Interval(chr1:150-350),
              Interval(chr1:500-750)])
	      
>>> ilist.find_index_beg(Interval("chr1",170,300))
2

>>> ilist.find_index_end(Interval("chr1",170,300))
3

>>> for interval in ilist.find_intersecting(Interval("chr1",140,300)):
...     print(interval)
...
chr1:125-145
chr1:150-350
```

The `IntervalList` constructor and its methods taking `interval` or `iterable` arguments as input provide a `setter` keyword argument, which accepts a function used to extract/construct from the input object a `BaseInterval`-descendant class instance for setting the `IntervalList`. This is useful when the inputs are not of the same object class/interface as the members of `IntervalList`. The `setter` argument function must accept one (and only one) positional input argument and output a single `BaseInterval`-descendant object.

```python
>>> class IntervalPair(object):
...     def __init__(self, trg, qry):
...         self.trg = trg
...         self.qry = qry
...

>>> pair = IntervalPair(
...     trg=Interval("chr1",1000000, 1500000),
...     qry=Interval("chr2",1100000, 1600000)
... )
...

>>> ilist = IntervalList([pair], setter=lambda p: p.trg)

>>> pair in ilist
True
```

The constructed `IntervalList` instance assumes all method arguments will be of the same class/interface as that given at construction. Using the `setter` keyword argument can be used to temporarily override the constructor's `setter` argument and allow objects of different class/interface:

```python
>>> for ipair in ilist.find_intersecting(Interval("chr1",1001000,1005000), setter=lambda i: i):
...     print(ipair.trg, ipair.qry)
...
chr1:1000000-1500000 chr2:1100000-1600000
```


### The IntervalSet class

***WARNING*: Still under development, not yet recommended for use.**

Inspired by and implemented as a [Nested Containment List](https://doi.org/10.1093/bioinformatics/btl647). 

