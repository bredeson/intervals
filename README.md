# intervals
Pure Python implementation of NCLS data structures for interval operations

## Installation

```bash
git clone https://github.com/bredeson/intervals.git
cd intervals
make install PREFIX=/full/path/to/installbase
```

## Usage

### Manipulating `Interval()`s 

```python
$ from intervals import Interval

$ i1 = Interval("chr1", 100, 1000)
$ i2 = Interval("chr1", 750, 2000)

$ i1 & i2
Interval(chr1:750-1000)

$ i1 | i2
Interval(chr1:100-2000)

$ i1 ^ i2
(Interval(chr1:100-750), Interval(chr1:1000-2000))

$ i1.isoverlapping(i2)
True

$ i1.isoverlapping_start(i2)
True

$ i1.isoverlapping_end(i2)
False

$ i1.overlap_length(i2)
250

$ i1.name
'chr1'

$ i1.start
100

$ i2.end = 1000
$ i1.issuperset(i2)
True

$ i2 in i1
True

$ i1 in i2
False
```

#### Table of `Interval()` attributes

+-------------------------------------+---------------------------------------------------------------------------------------------------+
| `self.beg`                          | Return the begin/start coordinate (0-based, inclusive) of `self`  |
| `self.clear()`                      | Alias for `null()`  |
| `self.copy()`                       | Return new copy of `self`  |
| `self.difference(other)`            | Return an Interval object representing the set difference of self and other  |
| `self.difference_update(other)`     | Update `self` with the result of `difference()`  |
| `self.empty()`                      | Set the `self` start and end coordinates both to zero  |
| `self.end`                          | Return the end/stop coordinate (0-based, exclusive) of `self`  |
| `self.hull()` or `self.hull(other)` | Return an Interval representing the hull of `self` or, optionally, `self` and `other` |
| `self.inner_distance(other)`        | Return the numeric inner distance between two `self` and `other`  |
| `self.intersection(other)`          | Return an Interval representing the set intersection between `self` and `other`  |
| `self.intersection_update(other)`   | Update the calling object with the result of `intersection()`  |
| `self.isabutting(other)`            | Test if `self` is abutting the start or end of `other` |
| `self.isabutting_beg(other)`        | Test if `self` is abutting the start of `other`  |
| `self.isabutting_end(other)`        | Test if `self` is abutting the end of `other`  |
| `self.isabutting_start(other)`      | Alias for `isabutting_beg()`  |
| `self.isabutting_stop(other)`       | Alias for `isabutting_stop()`  |
| `self.isdisjoint(other)`            | Test if `self` and `other` are non-overlapping  |
| `self.isempty()`                    | Test if `self` is a zero-lengthed interval |
| `self.isfinite()`                   | Test if `self` is a finite interval  |
| `self.isnull()`                     | Test if `self` has `nan` in start or end  |
| `self.isoverlapping(other)`         | Test if `self` overlaps `other`  |
| `self.isoverlapping_beg(other)`     | Test if `self` overlaps the start of `other`  |
| `self.isoverlapping_end(other)`     | Test if `self` overlaps the end of `other`
| `self.isoverlapping_start(other)`   | Alias for `isoverlapping_beg()`  |
| `self.isoverlapping_stop(other)`    | Alias for `isoverlapping_end()`  |
| `self.issingleton()`                | Test if `self` is 1 unit long  |
| `self.issubinterval(other)`         | Alias for `issubset()`  |
| `self.issubset(other)`              | Test if `self` is contained within `other`  |
| `self.issuperinterval(other)`       | Alias for `issuperset()`  |
| `self.issuperset(other)`            | Test if `self` contains `other`  |
| `self.mid`                          | Return the mid-point coordinate of `self` |
| `self.name`                         | Alias for `namespace`  |
| `self.namespace`                    | The namespace of `self` (optional)  |
| `self.null()`                       | Delete from `self` the values in the `name`, `start`, and `end` bound variables  |
| `self.outer_distance(other)`        | Return the outer distance between `self` and `other`  |
| `self.overlap_fraction(other)`      | Return the overlap fraction as relative to length of `self` |
| `self.overlap_length(other)`        | Return the length of overlap betwen `self` and `other`  |
| `self.start`                        | Alias for `beg`  |
| `self.stop`                         | Alias for `end`  |
| `self.symmetric_difference(other)`  | Return 2-tuple representing the symmetric difference (XOR) between `self` and `other`  |
| `self.symmetric_difference_update(other)`  | raises `NotImplementedError`  |
| `self.to_slice()`                   | Return a `slice()` object representing the coordinates in `self`  | 
| `self.to_string()`                  | Return string representatio of `self`. Same as `str(self)`  |
| `self.union(other)`                 | Return an Interval object representing the union of `self` and `other`  |
| `self.union_update(other)`          | Update `self` with the result of `update()`  |
+-------------------------------------+---------------------------------------------------------------------------------------------------+

### Searching `IntervalList()` objects

```python
$ from intervals import Interval, IntervalList

$ ilist = IntervalList([Interval("chr1",0,100),Interval("chr1",150,350)])

$ ilist.append(Interval("chr1",500,750))

$ ilist.insort(Interval("chr1",125,145))

$ ilist
IntervalList([Interval(chr1:0-100),
              Interval(chr1:125-145),
              Interval(chr1:150-350),
              Interval(chr1:500-750)])
	      
$ ilist.find_index_beg(Interval("chr1",170,300))
2

$ ilist.find_index_end(Interval("chr1",170,300))
3

$ for interval in ilist.find_overlaps(Interval("chr1",140,300)):
>     print(interval)
chr1:125-145
chr1:150-350
```

#### Table of `IntervalList()` attributes

`self` is an `IntervalList`, `interval` is an `BaseInterval`-inheriting object, and `iterable` is an iterable containing `interval`s.
+---------------------------------------------+------------------------------+
| `self.append(interval)`                     |  |
| `self.appendleft(interval)`                 |  |
| `self.beg`                                  |  |
| `self.clear()`                              |  |
| `self.copy()`                               |  |
| `self.count(interval)`                      |  |
| `self.end`                                  |  |
| `self.extend(iterable)`                     |  |
| `self.extendleft(iterable)`                 |  |
| `self.find_index(interval)`                 |  |
| `self.find_index_beg(interval)`             |  |
| `self.find_index_end(interval)`             |  |
| `self.find_index_nearest(interval)`         |  |
| `self.find_index_start(interval)`           |  |
| `self.find_index_stop(interval)`            |  |
| `self.find_overlap_fraction(iterable)`      |  |
| `self.find_overlap_index_beg(interval)`     |  |
| `self.find_overlap_index_end(interval)`     |  |
| `self.find_overlap_index_nearest(interval)` |  |
| `self.find_overlap_index_range(iterable)`   |  |
| `self.find_overlap_index_slice(iterable)`   |  |
| `self.find_overlap_index_start(interval)`   |  |
| `self.find_overlap_index_stop(interval)`    |  |
| `self.find_overlap_length(iterable)`        |  |
| `self.find_overlap_pairs(iterable)`         |  |
| `self.find_overlaps(iterable)`              |  |
| `self.index(interval)`                      |  |
| `self.insert(index, interval)`              |  |
| `self.insort(interval)`                     |  |
| `self.insortleft(interval)`                 |  |
| `self.isempty()`                            |  |
| `self.isfinite()`                           |  |
| `self.isnull()`                             |  |
| `self.namespace`                            |  |
| `self.pop()`                                |  |
| `self.popleft()`                            |  |
| `self.remove(interval)`                     |  |
| `self.reverse()`                            |  |
| `self.rotate(int)`                          |  |
| `self.start`                                |  |
| `self.stop`                                 |  |
| `self.update(iterable)`                     |  |
| `self.updateleft(iterable)`                 |  |
+---------------------------------------------+------------------------------+

## Documentation
To see the full documentation for the `intervals` API, there are two ways of getting `man`-like help page:

1. On the command line:
    ```bash
    $ cd intervals
    $ pydoc ./src/intervals/intervals.py
    $ pydoc ./src/intervals/collections.py
    ```

2. In the Python REPL:
    ```python
    $ from intervals import Interval, IntervalList

    # for a full `man`-like help page:
    $ help(Interval)
    $ help(IntervalList)

    # for a specific method:
    $ help(Interval.isoverlapping)
    ```
