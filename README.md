# Name
`intervals` - Pure Python implementation of data structures for interval operations

# Description

The `intervals` module implements classes for performing arithmetic, `set`-like, and search operations on one or collections of one-dimensionale interval(s). 

### Terminology

- **namespace**: Optional, depending on class. Namespace can represent axes (*e.g.*, `X`), contig names (*e.g.*, `Chr1`), etc. Interval methods operate only between instances in the same namespace. The default namespace is `None`.

- **null**: an interval without both start *and* stop coordinate values. Null coordinates are implemented as `nan` values and null namespace as `None`.

- **empty**: an interval that is null or with distance (length) between beginning and end coordinates less-than or equal-to zero units long.


# Installation

Currently, only installation on Unix-/Linux-like systems from source using `make` is supported:

```bash
$ git clone https://github.com/bredeson/intervals.git
$ cd intervals
$ make install PREFIX=/full/path/to/install/prefix
```

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

# Examples

## `Interval` objects

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

### `BaseInterval` variables and methods

In the following table, `self` and `other` represent an instance of `BaseInterval` or one of its subclasses.

| Attribute                                 | Description                                                  |
| ----------------------------------------- | ------------------------------------------------------------ |
| `self.beg`                                | Return the begin/start coordinate (0-based, inclusive) of `self`. |
| `self.clear()`                            | Alias for `null()`.                                           |
| `self.copy()`                             | Return new copy of `self`.                                    |
| `self.difference(other)`                  | Return an Interval object representing the set difference of `self` and `other`. |
| `self.difference_update(other)`           | Update `self` with the result of `difference()`.              |
| `self.empty()`                            | Set the `self` start and end coordinates both to zero.        |
| `self.end`                                | Return the end/stop coordinate (0-based, exclusive) of `self`. |
| `self.hull()` or `self.hull(other)`       | Return an Interval representing the hull of `self` or, optionally, `self` and `other`. |
| `self.inner_distance(other)`              | Return the numeric inner distance between two `self` and `other`. |
| `self.intersection(other)`                | Return an Interval representing the set intersection between `self` and `other`. |
| `self.intersection_update(other)`         | Update the `self` with the result of `intersection()`.        |
| `self.isabutting(other)`                  | Test if `self` is abutting the start or end of `other`.       |
| `self.isabutting_beg(other)`              | Test if `self` is abutting the start of `other`.              |
| `self.isabutting_end(other)`              | Test if `self` is abutting the end of `other`.                |
| `self.isabutting_start(other)`            | Alias for `isabutting_beg()`.                                 |
| `self.isabutting_stop(other)`             | Alias for `isabutting_stop()`.                                |
| `self.isdisjoint(other)`                  | Test if `self` and `other` are non-intersecting.               |
| `self.isempty()`                          | Test if `self` is a zero-lengthed interval.                   |
| `self.isfinite()`                         | Test if `self` is a finite interval.                          |
| `self.isnull()`                           | Test if `self` has `nan`-valued start or end.                 |
| `self.isintersecting(other)`              | Test if `self` intersects `other`.                              |
| `self.isintersecting_beg(other)`          | Test if `self` intersects the start of `other`.                 |
| `self.isintersecting_end(other)`          | Test if `self` intersects the end of `other`.                   |
| `self.isintersecting_start(other)`        | Alias for `isintersecting_beg()`.                             |
| `self.isintersecting_stop(other)`         | Alias for `isintersecting_end()`.                             |
| `self.issingleton()`                      | Test if `self` is 1 unit long.                                |
| `self.issubinterval(other)`               | Alias for `issubset()`.                                       |
| `self.issubset(other)`                    | Test if `self` is contained within `other`.                   |
| `self.issuperinterval(other)`             | Alias for `issuperset()`.                                     |
| `self.issuperset(other)`                  | Test if `self` contains `other`.                              |
| `self.mid`                                | Return the mid-point coordinate of `self`.                    |
| `self.name`                               | Alias for `namespace`.                                        |
| `self.namespace`                          | The namespace of `self` (optional).                           |
| `self.null()`                             | Delete from `self` the values in the `name`, `start`, and `end` bound variables. |
| `self.outer_distance(other)`              | Return the outer distance between `self` and `other`.         |
| `self.intersection_fraction(other)`            | Return the intersection fraction as relative to length of `self`.  |
| `self.intersection_length(other)`              | Return the length of intersection betwen `self` and `other`.       |
| `self.start`                              | Alias for `beg`.                                              |
| `self.stop`                               | Alias for `end`.                                              |
| `self.symmetric_difference(other)`        | Return 2-tuple representing the symmetric difference (XOR) between `self` and `other`. |
| `self.symmetric_difference_update(other)` | Raises `NotImplementedError`.                                 |
| `self.to_slice()`                         | Return a `slice` object containing the Pythonic range of intersecting items, or `slice(-1, -1)` if none.  |
| `self.to_string()`                        | Return string representatio of `self`. Same as `str(self)`.   |
| `self.union(other)`                       | Return an Interval object representing the union of `self` and `other`. |
| `self.union_update(other)`                | Update `self` with the result of `union()`.                   |
|                                           |                                                               |



## Interval collections: 

### `IntervalList`

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



#### `IntervalList` variables and methods

In the following table, `self` represents an `IntervalList` instance, `interval` an instance of `BaseInterval` or one of its subclasses, and `iterable` is an iterable object containing zero or more interval objects as queries for searching.

| Attribute  | Description |
|---------------------------------------------|------------------------------|
| `self.append(interval)`                     | Add an interval to the right side of `self`. |
| `self.appendleft(interval)`                 | Add an interval to the left side of `self`. |
| `self.beg`                                  | Return the begin/start coordinate (0-based, inclusive) of the first interval in `self`, or `nan` if empty. |
| `self.clear()`                              | Remove all elements from `self`. |
| `self.copy()`                               | Return a shallow copy of `self`. |
| `self.count(interval)`                      | Return number of occurrences of `interval` in `self`. |
| `self.end`                                  | Return the end/stop coordinate (0-based, exclusive) of the last interval in `self`, or `nan` if empty. |
| `self.extend(iterable)`                     | Extend the right side of the `self` with intervals from `iterable`. |
| `self.extendleft(iterable)`                 | Extend the left side of `self` with elements from the iterable. |
| `self.find_index(interval)`                 | Return the first index of `interval` in `self`. Raises ValueError if the value is not present. |
| `self.find_index_beg(interval)`             | Return the start (0-based inclusive) index for `interval`. |
| `self.find_index_end(interval)`             | Return the end (0-based exclusive) index for `interval`. |
| `self.find_index_nearest(interval)`         | Return the nearest (inclusive) index for an `interval`, returns the left-most index when members are equidistant to `interval`. |
| `self.find_index_start(interval)`           | Alias for `find_index_beg()`. |
| `self.find_index_stop(interval)`            | Alias for `find_index_end()`. |
| `self.find_intersection_fraction(iterable)`      | Returns the fraction of intersection an `iterable` of `interval`s has with those of `self`. |
| `self.find_intersection_index_beg(interval)`     | Return the (0-based inclusive) index of the left-most intersecting interval in `self` for a given `interval`, or -1 if none. |
| `self.find_intersection_index_end(interval)`     | Return the (0-based exclusive) index of the right-most intersecting interval in `self` for a given `interval`, or -1 if none. |
| `self.find_intersection_index_nearest(interval)` | Return the (0-based inclusive) index of the nearest intersecting interval in `self` for a given `interval`, or -1 if none. Returns the left-most index when members are equidistant to `interval`. |
| `self.find_intersection_index_range(iterable)`   | Homage to `range()`. Returns generator object yielding the indices for intervals in `self` intersecting those in `iterable`. |
| `self.find_intersection_index_slice(iterable)`   | Perform an intersect search with one or more query interval objects in `iterable` and return a `slice` object containing the Pythonic range of intersecting items, or `slice(-1, -1)` if none. |
| `self.find_intersection_index_start(interval)`   | Alias for `find_intersection_index_beg()`. |
| `self.find_intersection_index_stop(interval)`    | Alias for `find_intersection_index_end()`. |
| `self.find_intersection_length(iterable)`        | Returns the length of intersects an `iterable` of interval objects have with `self`. |
| `self.find_intersection_pairs(iterable)`         | Preform an intersect search of `self` with one or more interval objects in `iterable` and return a generator object producing a 2-tuple for each interval in `iterable` and its intersecting member in `self`. |
| `self.find_intersecting(iterable)`              | Perform an intersect search of `self` with an `iterable` of interval objects and return an generator object producing members of `self` that intersect. |
| `self.index(interval)`                      | Alias of `find_index()`. |
| `self.insert(index, interval)`              | Insert `interval` into `self` before `index`. |
| `self.insort(interval)`                     | Insert an `interval` into its sorted position, with identical intervals inserted to the right of existing ones. |
| `self.insortleft(interval)`                 | Insert an `interval` into its sorted position, with identical intervals inserted to the left of existing ones. |
| `self.isempty()`                            | Test if `self` is contains no intervals. |
| `self.isfinite()`                           | Test if `self` is a finite interval. |
| `self.isnull()`                             | Test if `self` has `nan`-valued start or end. |
| `self.namespace`                            | The namespace of `self` (optional). |
| `self.null()`                                | Alias for `clear()`. |
| `self.pop()`                                | Pop one interval off the right side of `self` and return it. |
| `self.popleft()`                            | Pop one interval off the left side of `self` and return it. |
| `self.remove(interval)`                     | Remove an `interval` from `self`. |
| `self.reverse()`                            | Reverse in place the order of interval members in `self.` |
| `self.rotate(int)`                          | Rotate `self` n steps to the right (default n=1). If n is negative, rotates left. |
| `self.start`                                | Alias for `beg.` |
| `self.stop`                                 | Alias for `end`. |
| `self.update(iterable)`                     | Insort into `self` the intervals contained in `iterable`, with identical intervals inserted to the right of existing ones. |
| `self.updateleft(iterable)`                 | Insort into `self` the intervals contained in `iterable`, with identical intervals inserted to the left of existing ones. |

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


### `IntervalSet`

Inspired by and implemented as a [Nested Containment List](https://doi.org/10.1093/bioinformatics/btl647). 

