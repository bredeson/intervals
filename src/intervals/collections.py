"""
Performance Notes:
 1. A collections.deque() is implemented in C and supports O(1) 
    insert()s and pop()s on either end, and is therefore faster 
    than a builtin.list() (which is O(n) performance b/c of re-allocs). 
    See:
    https://stackoverflow.com/questions/23487307/python-deque-vs-list-performance-comparison

"""

import sys

from collections import deque as _deque
from .constants import NULL_NAMESPACE as _NULL_NS
from .constants import NULL_BEG as _NULL_BEG
from .constants import NULL_END as _NULL_END
from .constants import inf as _INF
from .intervals import Interval
from math import isnan as _isnull
from math import isinf as _isinf


def _pass(x):
    return x


def _interval_pos(interval):
    return (interval.isempty(), interval.beg, interval.end)


def _node_pos(node):
    return (node.interval.isempty(), node.interval.beg, node.interval.end)


def _interval_pos_longest(interval):
    return (interval.isempty(), interval.beg, -interval.end)


def _node_pos_longest(node):
    return (node.interval.isempty(), node.interval.beg, -node.interval.end)


def isiterable(item):
    return \
        hasattr(item, '__iter__') or \
        hasattr(item, '__next__')


def _listify(item, sort=False):
    if not isiterable(item):
        item = [item]
    if sort:
        item = sorted(item, key=sort)
    return item


def _reprify(item, sep=', ', indent=False):
    if isiterable(item):
        if indent:
            sep += " "
        return '[%s]' % sep.join((
            _reprify(i, sep, indent) for i in item
        ))
    else:
        return repr(item)  # .instance)


def _filter_proper(nodes, sort=False):
    if sort:
       nodes = sorted(nodes, key=sort)
    prev_node = None
    for curr_node in nodes:
        if prev_node and \
           prev_node.interval.issuperinterval(curr_node.interval):
            continue
        prev_node = curr_node
        yield curr_node



class DuplicateKeyError(LookupError):
    pass



class _Node(object):
    __slots__ = ('instance','interval','sublist')

    def __init__(self, interval, instance=None, sublist=-1):
        """
        Create a _Node for an object instance. The instance 
        must return an Interval object when 
        """
        self.instance = interval if instance is None else instance
        self.interval = interval
        self.sublist = sublist


    def __eq__(self, other):
        return self.interval == other.interval


    def __ne__(self, other):
        return self.interval != other.interval


    def __lt__(self, other):
        return self.interval < other.interval
    

    def __hash__(self):
        # would be preferable to hash(self.instance), but
        # instance hashabilty is not guarenteed.
        return hash(self.interval)
        

    def __repr__(self):
        return "%s(%s)" % (
            self.__class__.__name__, str(self.interval)
        )

    def copy(self):
        return self.__class__(self.interval, self.instance)



class BaseIntervalCollection(object):
    # Copied and extended this pattern from collections.abc.Collection
    def __init__(self, setter=_pass):
        self._setter = setter


    def __contains__(self, value):
        raise NotImplementedError('%s.__contains__()' % self.__class__.__name__)


    def __iter__(self):
        raise NotImplementedError('%s.__iter__()' % self.__class__.__name__)


    def __len__(self):
        raise NotImplementedError('%s.__len__()' % self.__class__.__name__)
    

    def _set(self, interval, setter=None):
        setter = setter or self._setter
        return _Node(setter(interval), interval)


    def _set_node(self, index, item):
        raise NotImplementedError('%s._set_node()' % self.__class__.__name__)
    

    def _get(self, node):
        return node.instance


    def _get_node(self, index):
        raise NotImplementedError('%s._get_node()' % self.__class__.__name__)


    def _iter_nodes(self, lower=0, upper=-1):
        raise NotImplementedError('%s._iter_nodes()' % self.__class__.__name__)
    

    def _copy_nodes(self):
        return map(_Node.copy, self._iter_nodes())


    @property
    def namespace(self):
        raise NotImplementedError('%s.namespace' % self.__class__.__name__)


    @property
    def beg(self):
        raise NotImplementedError('%s.beg' % self.__class__.__name__)


    @property
    def end(self):
        raise NotImplementedError('%s.end' % self.__class__.__name__)


    def isnull(self):
        return _isnull(self.beg) or _isnull(self.end)


    def isempty(self):
        raise NotImplementedError('%s.isempty()' % self.__class__.__name__)


    def isfinite(self):
        return not (_isinf(self.beg) or _isinf(self.end))

    
    
class IntervalList(BaseIntervalCollection, _deque):
    def __init__(self, intervals=[], setter=_pass):
        """
        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for setting the IntervalList. This is useful
        for when the inputs are not of the same object class as the 
        members of IntervalList. The function must accept one (and only
        one) argument and outputs a single Interval-descendant object.
        """
        BaseIntervalCollection.__init__(self, setter)
        _deque.__init__(self)
        if len(intervals) > 0:
            self.extend(sorted(
                intervals, key=lambda i: _interval_pos(setter(i))
            ))

        
    def _set_node(self, index, node):
        return _deque.__setitem__(self, index, node)    


    def _get_node(self, index):
        return _deque.__getitem__(self, index)
    
    
    def __getitem__(self, index):
        return self._get(_deque.__getitem__(self, index))


    def __setitem__(self, index, interval):
        _deque.__setitem__(self, index, self._set(interval))


    def __contains__(self, interval):
        return _deque.__contains__(self, self._set(interval))
        # return self.find_index(interval) >= 0

        
    def __iter__(self):
        return (self._get(n) for n in self._iter_nodes())


    def _iter_nodes(self):
        return _deque.__iter__(self)


    def __len__(self):
        return _deque.__len__(self)

    
    @property
    def namespace(self):
        return _NULL_NS \
            if   self.isnull() \
            else self._get_node(0).interval.namespace


    @property
    def beg(self):
        return _NULL_BEG \
            if   self.isnull() \
            else self._get_node(0).interval.beg


    @property
    def start(self):
        return self.beg


    @property
    def end(self):
        return _NULL_END \
            if   self.isnull() \
            else self._get_node(-1).interval.end


    @property
    def stop(self):
        return self.end


    def isnull(self):
        return len(self) < 1

    
    def append(self, interval, setter=None):
        """
        Append interval to the right side of IntervalList.

        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for setting the IntervalList. This is useful
        for when the input is not of the same object class as the 
        members of IntervalList. The function must accept one (and only
        one) argument and outputs a single Interval-descendant object.
        """
        _deque.append(self, self._set(interval, setter))


    def appendleft(self, interval, setter=None):
        """
        Append interval to the left side of IntervalList.

        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for setting the IntervalList. This is useful
        for when the input is not of the same object class as the 
        members of IntervalList. The function must accept one (and only
        one) argument and outputs a single Interval-descendant object.
        """
        _deque.appendleft(self, self._set(interval, setter))


    def copy(self):
        """Create a copy of the IntervalList."""
        return self.__class__(self, setter=self._setter)
        

    def count(self, interval, setter=None):
        """
        Count the number of elements equal to interval.
        
        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for querying the IntervalList. This is useful
        for when the query is not of the same object class as the 
        members of IntervalList. The function must accept one (and only
        one) argument and outputs a single Interval-descendant object.
        """
        return _deque.count(self, self._set(interval, setter))
        

    def extend(self, intervals, setter=None):
        """
        Extend the right side of the IntervalList with elements from
        the iterable.

        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for setting the IntervalList. This is useful
        for when the intputs are not of the same object class as the 
        members of IntervalList. The function must accept one (and only
        one) argument and outputs a single Interval-descendant object.
        """
        _deque.extend(self, map(
            lambda i: self._set(i, setter),
            intervals
        ))


    def extendleft(self, intervals, setter=None):
        """
        Extend the left side of the IntervalList with elements from the
        iterable.

        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for setting the IntervalList. This is useful
        for when the inputs are not of the same object class as the 
        members of IntervalList. The function must accept one (and only
        one) argument and outputs a single Interval-descendant object.
        """
        _deque.extendleft(self, map(
            lambda i: self._set(i, setter),
            intervals
        ))


    def index(self, interval, start=0, stop=-1, setter=None):
        """
        Return the first index of interval.
        
        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for querying the IntervalList. This is useful
        for when the query is not of the same object class as the 
        members of IntervalList. The function must accept one (and only
        one) argument and outputs a single Interval-descendant object.
        """
        index = self.find_index(
            interval, lower=start, upper=stop, setter=setter
        )
        if 0 <= index < self._length:
            return index
        else:
            raise ValueError("'%s' is not in list" % str(interval))

        
    def insert(self, index, interval, setter=None):
        """
        Insert interval before index

        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for setting the IntervalList. This is useful
        for when the input is not of the same object class as the 
        members of IntervalList. The function must accept one (and only
        one) argument and outputs a single Interval-descendant object.
        """
        _deque.insert(self, index, self._set(interval, setter))

        
    def insort(self, interval, lower=0, upper=-1, setter=None):
        """
        Insert an interval into its sorted position, with identical
        intervals inserted to the right of existing ones.

        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for setting the IntervalList. This is useful
        for when the input is not of the same object class as the 
        members of IntervalList. The function must accept one (and only
        one) argument and outputs a single Interval-descendant object.
        """
        node = self._set(interval, setter)
        length = len(self)
        if not (0 <= lower < length):
            lower = 0
        if not (0 <= upper < length):
            upper = length
        while lower < upper:
            middle = (lower + upper) // 2
            if node.interval < self._get_node(middle).interval:
                upper = middle
            else:
                lower = middle + 1
        self.insert(lower, interval, setter)

        
    def insortleft(self, interval, lower=0, upper=-1, setter=None):
        """
        Insert an interval into its sorted position, with identical
        intervals inserted to the left of existing ones.

        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for setting the IntervalList. This is useful
        for when the input is not of the same object class as the 
        members of IntervalList. The function must accept one (and only
        one) argument and outputs a single Interval-descendant object.
        """
        node = self._set(interval, setter)
        length = len(self)
        if not (0 <= lower < length):
            lower = 0
        if not (0 <= upper < length):
            upper = length
        while lower < upper:
            middle = (lower + upper) // 2
            if self._get_node(middle).interval < node.interval:
                lower = middle + 1
            else:
                upper = middle
        self.insert(lower, interval, setter)
        

    def update(self, intervals, setter=None):
        """
        `insort()` a collection of intervals
        
        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for setting the IntervalList. This is useful
        for when the inputs are not of the same object class as the 
        members of IntervalList. The function must accept one (and only
        one) argument and outputs a single Interval-descendant object.
        """
        setter = setter or self._setter
        for interval in sorted(intervals,
                               key=lambda i: _interval_pos(setter(i))):
            self.insort(interval, setter=setter)


    def updateleft(self, intervals, setter=None):
        """
        `insortleft()` a collection of intervals

        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for setting the IntervalList. This is useful
        for when the inputs are not of the same object class as the 
        members of IntervalList. The function must accept one (and only
        one) argument and outputs a single Interval-descendant object.
        """
        setter = setter or self._setter
        for interval in sorted(intervals,
                               key=lambda i: _interval_pos(setter(i))):
            self.insortleft(interval, setter=setter)
        

    def pop(self):
        """Pop one item off the right side of IntervalList and return it."""
        return self._get(_deque.pop(self))


    def popleft(self):
        """Pop one item off the left side of IntervalList and return it."""
        return self._get(_deque.popleft(self))
    

    def remove(self, interval, setter=None):
        """
        Remove an interval from the IntervalList.

        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for querying the IntervalList. This is useful
        for when the query is not of the same object class as the 
        members of IntervalList. The function must accept one (and only
        one) argument and outputs a single Interval-descendant object.
        """
        index = self.find_index(interval, setter=setter)
        if 0 <= index < self._length:
            del(self[index])
        else:
            raise ValueError("interval not in deque" % self.__class__.__name__)


    def find_index_beg(self, interval, lower=0, upper=-1, setter=None):
        """
        Return the start (inclusive) index for a query interval. 
        IntervalList members may not necessarily overlap the input 
        interval object.

        The `lower` and `upper` keywords can be used to restrict 
        the search space when the lower and upper bounds are known.

        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for querying the IntervalList. This is useful
        for when the query is not of the same object class as the 
        members of IntervalList. The function must accept one (and only
        one) argument and outputs a single Interval-descendant object.
        """
        node = self._set(interval, setter)
        length = len(self)
        if not (0 <= lower < length):
            lower = 0
        if not (0 <= upper < length):
            upper = length
        while lower < upper:
            middle = (lower + upper) // 2
            if self._get_node(middle).interval.end <= node.interval.beg:
                lower = middle + 1
            else:
                upper = middle
        return lower

    
    def find_index_end(self, interval, lower=0, upper=-1, setter=None):
        """
        Return the end (exclusive) index for a query interval;
        i.e., the index of the first non-overlapping interval.

        The `lower` and `upper` keywords can be used to restrict 
        the search space when the lower and upper bounds are known.

        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for querying the IntervalList. This is useful
        for when the query is not of the same object class as the 
        members of IntervalList. The function must accept one (and only
        one) argument and outputs a single Interval-descendant object.
        """
        node = self._set(interval, setter)
        length = len(self)
        if not (0 <= lower < length):
            lower = 0
        if not (0 <= upper < length):
            upper = length
        if self._get_node(length-1).interval.beg < node.interval.end:
            return length  # - 1  # <=[makes inclusive]
        while lower < upper:
            middle = (lower + upper) // 2
            if node.interval.end <= self._get_node(middle).interval.beg:
                upper = middle
            else:
                lower = middle + 1
        return lower  # - 1  # <=[makes inclusive]


    def find_index(self, interval, lower=0, upper=-1, setter=None):
        """
        Return the index for a query interval, or -1 if it doesn't
        exist.

        The `lower` and `upper` keywords can be used to restrict 
        the search space when the lower and upper bounds are known.

        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for querying the IntervalList. This is useful
        for when the query is not of the same object class as the 
        members of IntervalList. The function must accept one (and only
        one) argument and outputs a single Interval-descendant object.
        """
        node = self._set(interval, setter)
        length = len(self)
        if not (0 <= lower < length):
            lower = 0
        if not (0 <= upper < length):
            upper = length
        while lower < upper:
            middle = (lower + upper) // 2
            if self._get_node(middle).instance == node.instance:
                return middle
            elif self._get_node(middle).interval < node.interval:
                lower = middle + 1
            else:
                upper = middle - 1
        return -1
    
    
    def find_index_nearest(self, interval, lower=0, upper=-1, setter=None):
        """
        Return the nearest (inclusive) index for a query interval. 
        IntervalList members may not necessarily overlap the input 
        Interval object. Returns the left-most index when members 
        are equidistant to the query interval.

        The `lower` and `upper` keywords can be used to restrict 
        the search space when the lower and upper bounds are known.

        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for querying the IntervalList. This is useful
        for when the query is not of the same object class as the 
        members of IntervalList. The function must accept one (and only
        one) argument and outputs a single Interval-descendant object.
        """
        node = self._set(interval, setter)
        length = len(self)
        distance = _INF
        if not (0 <= lower < length):
            lower = 0
        if not (0 <= upper < length):
            upper = length - 1
        while lower < upper:
            middle = (lower + upper) // 2
            if self._get_node(middle).interval < node.interval:
                lower = middle + 1
            else:
                upper = middle
                
        if 0 < lower < length:
            Il = self._get_node(lower-1).interval
            Iu = self._get_node(lower).interval
            l = node.interval.beg - Il.end
            u = Iu.beg - node.interval.end
            if l <= 0 and u <= 0:
                # both overlap
                l = -Il.overlap_length(node.interval)
                u = -Iu.overlap_length(node.interval)
                if l == u:
                    return lower \
                        if abs(node.interval.mid - Iu.mid) < \
                           abs(node.interval.mid - Il.mid) \
                        else lower-1
                elif u < l:
                    return lower
                else:
                    return lower-1
            lower = lower if u < l else lower-1
        return lower


    def find_overlap_index_beg(self, interval, lower=0, upper=-1, setter=None):
        """
        Return the (inclusive) index of the left-most overlapping
        IntervalList member, or -1 if none.

        The `lower` and `upper` keywords can be used to restrict 
        the search space when the lower and upper bounds are known.

        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for querying the IntervalList. This is useful
        for when the query is not of the same object class as the 
        members of IntervalList. The function must accept one (and only
        one) argument and outputs a single Interval-descendant object.
        """
        node = self._set(interval, setter)
        index = self.find_index_beg(node.interval, lower, upper, _pass)
        return index \
            if 0 <= index < len(self) and \
               self._get_node(index).interval.isoverlapping(node.interval) \
            else -1


    def find_overlap_index_end(self, interval, lower=0, upper=-1, setter=None):
        """
        Return the (exclusive) index of the right-most overlapping
        IntervalList member, or -1 if none.

        The `lower` and `upper` keywords can be used to restrict 
        the search space when the lower and upper bounds are known.

        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for querying the IntervalList. This is useful
        for when the query is not of the same object class as the 
        members of IntervalList. The function must accept one (and only
        one) argument and outputs a single Interval-descendant object.
        """
        node = self._set(interval, setter)
        index = self.find_index_end(node.interval, lower, upper, _pass)
        return index \
            if 0 < index <= len(self) and \
               self._get_node(index-1).interval.isoverlapping(node.interval) \
            else -1
    

    def find_overlap_index_nearest(self, interval, lower=0, upper=-1, setter=None):
        """
        Return the (inclusive) index of the nearest overlapping 
        IntervalList member, or -1 if none. Returns the left-most 
        index when members are equidistant to the query interval.

        The `lower` and `upper` keywords can be used to restrict 
        the search space when the lower and upper bounds are known.

        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for querying the IntervalList. This is useful
        for when the query is not of the same object class as the 
        members of IntervalList. The function must accept one (and only
        one) argument and outputs a single Interval-descendant object.
        """
        node = self._set(interval, setter)
        index = self.find_index_nearest(node.interval, lower, upper, _pass)
        return index \
            if 0 <= index < len(self) and \
               self._get_node(index).interval.isoverlapping(node.interval) \
            else -1


    def find_overlap_index_range(self, intervals, setter=None):
        """
        An homage to the `range()` function. Perform an IntervalList 
        overlap search with one or more query interval objects and 
        return a generator object that produces a sequence of integer
        indices between the start (inclusive) and end (exclusive) of
        the overlap range. When an iterable of intervals is inputted,
        indices may not be contiguous. 

        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for querying the IntervalList. This is useful
        for when the query is not of the same object class as the 
        members of IntervalList. The function must accept one (and only
        one) argument and outputs a single Interval-descendant object.
        """
        nodes = map(lambda i: self._set(i, setter), _listify(intervals))
        length = len(self)
        upper = 0
        for node in _filter_proper(nodes, sort=_node_pos_longest):
            index = self.find_index_beg(node.interval, lower=upper, setter=_pass)
            while index < length and \
                  self._get_node(index).interval.isoverlapping(node.interval):
                yield index
                index += 1
            upper = index

            
    def find_overlap_index_bounds(self, intervals, setter=None):
        """
        Perform an IntervalList overlap search with one or more query
        interval objects and return a 2-tuple containing the Pythonic
        range of overlapping items, or `(-1, -1)` if none.

        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for querying the IntervalList. This is useful
        for when the query is not of the same object class as the 
        members of IntervalList. The function must accept one (and only
        one) argument and outputs a single Interval-descendant object.
        """
        nodes = map(lambda i: self._set(i, setter), _listify(intervals))
        length = len(self)
        lower = -1
        upper = -1
        for node in _filter_proper(nodes, sort=_node_pos_longest):
            index = self.find_index_beg(node.interval, lower=upper, setter=_pass)
            while index < length and \
                  self._get_node(index).interval.isoverlapping(node.interval):
                if lower < 0:
                    lower = index
                index += 1
                upper = index
        return lower, upper

    
    def find_overlap_length(self, intervals, setter=None):
        """
        Returns the length of intersects a query interval or 
        IntervalList object has with this IntervalList object.

        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for querying the IntervalList. This is useful
        for when the query is not of the same object class as the 
        members of IntervalList. The function must accept one (and only
        one) argument and outputs a single Interval-descendant object.
        """
        nodes = map(lambda i: self._set(i, setter), _listify(intervals))
        length = len(self)
        overlap_length = 0
        for node in sorted(nodes, key=_node_pos):
            index = self.find_overlap_index_beg(node.interval, setter=_pass)
            if index < 0:
                continue
            while index < length and \
                  self._get_node(index).interval.isoverlapping(node.interval):
                overlap_length += self._get_node(index).interval.overlap_length(node.interval)
                index += 1
        return overlap_length
    

    def find_overlap_fraction(self, intervals, query=False, setter=None):
        """
        Returns the fraction of overlap a query interval or IntervalList 
        object has with this IntervalList object. Setting `query=True`
        calculates the overlap fraction with respect to the query length.        

        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for querying the IntervalList. This is useful
        for when the query is not of the same object class as the 
        members of IntervalList. The function must accept one (and only
        one) argument and outputs a single Interval-descendant object.
        """
        setter = setter or self._setter
        numerator = self.find_overlap_length(intervals, setter=setter)
        if query:
            denominator = sum(map(lambda i: len(setter(i)), _listify(intervals)))
        else:
            denominator = sum(map(lambda i: len(setter(i)), self))
        return numerator / float(max(1, denominator))


    def find_overlap_pairs(self, intervals, setter=None):
        """
        Preform an overlap search of IntrevalList with one or more query
        interval objects and return a generator object producing 
        2-tuples of each query interval and its overlapping IntervalList 
        member.

        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for querying the IntervalList. This is useful for
        when the query is not of the same object class as the members 
        of IntervalList. The function must accept one (and only one) 
        argument and outputs a single Interval-descendant object.
        """
        nodes = map(lambda n: self._set(n, setter), _listify(intervals))

        # if pairwise:
        nodes = sorted(nodes, key=_node_pos)
        # else:
        #     nodes = _filter_proper(nodes, sort=_node_pos_longest)

        #nr = not pairwise
        #visited = set()
        length = len(self)
        for node in nodes:
            index = self.find_overlap_index_beg(node.interval, setter=_pass)
            while ((0 <= index < length) and
                   (self._get_node(index).interval.isoverlapping(node.interval))):
                # if nr and hash(self._get_node(index).instance) in visited:
                #     index += 1
                #     continue
                # visited.add(hash(self._get_node(index).instance))
                yield (node.instance, self._get_node(index).instance)
                index += 1
        
    
    def find_overlaps(self, intervals, setter=None):
        """
        Perform an overlap search of IntervalList with one or more
        query interval objects and return an generator object producing
        IntervalList members overlapping the input interval record(s).

        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for querying the IntervalList. This is useful
        for when the query is not of the same object class as the 
        members of IntervalList. The function must accept one (and only
        one) argument and outputs a single Interval-descendant object.
        """
        return (self[index] for index in self.find_overlap_index_range(intervals, setter=setter))


    find_overlap_index_start = find_overlap_index_beg

    find_overlap_index_stop = find_overlap_index_end

    find_index_start = find_index_beg

    find_index_stop = find_index_end

    isempty = isnull

    

class _Sublist(BaseIntervalCollection, _deque):
    def __init__(self, nodes=None, index=-1, setter=_pass):
        BaseIntervalCollection.__init__(self, setter)
        if nodes is None:
            _deque.__init__(self)
        else:
            _deque.__init__(self, nodes)
        self.length = len(self)
        self.index = index


    def __delitem__(self, index):
        _deque.__delitem__(self, index)
        self.length -= 1


    def __repr__(self):
        padding_len = len(self.__class__.__name__)
        padding_sep = ',\n' + ' ' * (padding_len + 1)
        return "%s(%s)" % (
            self.__class__.__name__,
            _reprify(self, sep=padding_sep, indent=True)
        )


    def __iter__(self):
        return _deque.__iter__(self)

    
    def __len__(self):
        return _deque.__len__(self)

    
    def __str__(self):
        return _reprify(self)


    def _set(self, node, setter=None):
        return node


    def _set_node(self, index, node):
        return _deque.__setitem__(self, index, node)


    def _get(self, node):
        return node


    def _get_node(self, index):
        return _deque.__getitem__(self, index)

    
    def append(self, node):
        _deque.append(self, node)
        self.length += 1


    def appendleft(self, node):
        _deque.appendleft(self, node)
        self.length += 1


    def clear(self):
        _deque.clear(self)
        self.length = 0


    def extend(self, nodes):
        _deque.extend(self, nodes)
        self.length += len(nodes)


    def extendleft(self, nodes):
        _deque.extendleft(self, nodes)
        self.length += len(nodes)


    def insert(self, index, node):
        _deque.insert(self, index, node)
        self.length += 1


    def pop(self):
        self.length -= 1
        return _deque.pop(self)


    def popleft(self):
        self.length -= 1
        return _deque.popleft(self)


    def remove(self, node):
        _deque.remove(self, node)
        self.length -= 1


    def find_index_beg(self, node, lower=0, upper=-1):
        """
        Return the left-most start (inclusive) index for a query interval. 
        IntervalSet members may not necessarily overlap the query 
        interval. Guarenteed to return an index 0:L, where L is the
        length. Returns `-1` if the query is in the wrong namespace.

        The `lower` and `upper` keywords can be used to restrict 
        the search space when the lower and upper bounds are known.

        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for querying the IntervalSet. This is useful for
        when the query is not of the same object class as the members 
        of IntervalSet. The function must accept one (and only one) argument
        and outputs a single Interval-descendant object.
        """
        if self.length < 1 or \
           self[0].interval.namespace != node.interval.namespace:
            return -1            
        if not (0 <= lower < self.length):
            lower = 0
        if not (0 <= upper < self.length):
            upper = self.length
        while lower < upper:
            middle = (lower + upper) // 2
            if self[middle].interval.end <= node.interval.beg:
                lower = middle + 1
            else:
                upper = middle
        return lower

    
    def find_index_end(self, node, lower=0, upper=-1):
        """
        Return the right-most end (exclusive) index for a query interval;
        i.e., the index of the first non-overlapping IntervalSet member.
        Returns `-1` if the query is in the wrong namespace.

        The `lower` and `upper` keywords can be used to restrict 
        the search space when the lower and upper bounds are known.

        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for querying the IntervalSet. This is useful for
        when the query is not of the same object class as the members 
        of IntervalSet. The function must accept one (and only one) argument
        and outputs a single Interval-descendant object.
        """
        if self.length < 1 or \
           self[0].interval.namespace != node.interval.namespace:
            return -1            
        if not (0 <= lower < self.length):
            lower = 0
        if not (0 <= upper < self.length):
            upper = self.length
        if self[self.length-1].interval.beg < node.interval.end:
            return self.length  # - 1  # <=[makes inclusive]
        while lower < upper:
            middle = (lower + upper) // 2
            if node.interval.end <= self[middle].interval.beg:
                upper = middle
            else:
                lower = middle + 1
        return lower  # - 1  # <=[makes inclusive]


    def find_index(self, node, lower=0, upper=-1):
        """
        Return the index for a query interval, or -1 if it doesn't 
        exist. Returns `-1` if the query is in the wrong namespace.

        The `lower` and `upper` keywords can be used to restrict 
        the search space when the lower and upper bounds are known.

        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for querying the IntervalSet. This is useful for
        when the query is not of the same object class as the members 
        of IntervalSet. The function must accept one (and only one) argument
        and outputs a single Interval-descendant object.
        """
        if self.length < 1 or \
           self[0].interval.namespace != node.interval.namespace:
            return -1
        if not (0 <= lower < self.length):
            lower = 0
        if not (0 <= upper < self.length):
            upper = self.length
        while lower < upper:
            middle = (lower + upper) // 2
            if self[middle].instance == node.instance:
                return middle
            elif self[middle].interval < node.interval:
                lower = middle + 1
            else:
                upper = middle - 1
        return -1
    

    def find_index_nearest(self, node, lower=0, upper=-1):
        """
        Return the nearest (inclusive) index for a query interval. 
        IntervalSet members may not necessarily overlap the query 
        interval. Returns `-1` if the query is in the wrong namespace.

        The `lower` and `upper` keywords can be used to restrict 
        the search space when the lower and upper bounds are known.

        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for querying the IntervalSet. This is useful for
        when the query is not of the same object class as the members 
        of IntervalSet. The function must accept one (and only one) argument
        and outputs a single Interval-descendant object.
        """
        if self.length < 1 or \
           self[0].interval.namespace != node.interval.namespace:
            return -1            
        if not (0 <= lower < self.length):
            lower = 0
        if not (0 <= upper < self.length):
            upper = self.length
        while lower < upper:
            middle = (lower + upper) // 2
            if self[middle].interval < node.interval:
                lower = middle + 1
            else:
                upper = middle
        if 0 < lower and upper < self.length:
            l = ((abs(self[lower-1].interval.inner_distance(node.interval))) or
                 (-self[lower-1].interval.overlap_length(node.interval)))
            u = ((abs(self[lower].interval.inner_distance(node.interval))) or
                 (-self[lower].interval.overlap_length(node.interval)))
            lower = lower if u < l else lower-1
        return lower
    

    def find_overlap_index_beg(self, node, lower=0, upper=-1):
        """
        Return the start (inclusive) index of the left-most overlapping 
        IntervalSet member, or -1 if none or if the query is in the wrong
        namespace.

        The `lower` and `upper` keywords can be used to restrict 
        the search space when the lower and upper bounds are known.

        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for querying the IntervalSet. This is useful for
        when the query is not of the same object class as the members 
        of IntervalSet. The function must accept one (and only one) argument
        and outputs a single Interval-descendant object.
        """
        index = self.find_index_beg(node, lower, upper)
        return index \
            if 0 <= index < self.length and \
               self[index].interval.isoverlapping(node.interval) \
            else -1


    def find_overlap_index_end(self, node, lower=0, upper=-1):
        """
        Return the end (exclusive) index of the right-most overlapping
        IntervalSet member, or -1 if none or if the query is in the wronge
        namespace.

        The `lower` and `upper` keywords can be used to restrict 
        the search space when the lower and upper bounds are known.

        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for querying the IntervalSet. This is useful for
        when the query is not of the same object class as the members 
        of IntervalSet. The function must accept one (and only one) argument
        and outputs a single Interval-descendant object.
        """
        index = self.find_index_end(node, lower, upper)
        return index \
            if 0 < index <= self._toplist.length and \
               self[index-1].interval.isoverlapping(node.interval) \
            else -1
    

    def find_overlap_index_nearest(self, node, lower=0, upper=-1):
        """
        Return the (inclusive) index of the nearest overlapping IntervalSet
        member, or -1 if none or if the query is in the wrong namespace.

        The `lower` and `upper` keywords can be used to restrict 
        the search space when the lower and upper bounds are known.

        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for querying the IntervalSet. This is useful for
        when the query is not of the same object class as the members 
        of IntervalSet. The function must accept one (and only one) argument
        and outputs a single Interval-descendant object.
        """
        index = self.find_index_nearest(node, lower, upper)
        return index \
            if 0 <= index < self._toplist.length and \
               self[index].interval.isoverlapping(node.interval) \
            else -1
 

    def find_overlap_index_range(self, nodes):
        """
        An homage to the `range()` function. Perform an IntervalSet header
        overlap search with one or more query interval objects and 
        return a generator object that produces a sequence of integer
        indices between the start (inclusive) and end (exclusive) of 
        the overlap range. When an iterable of intervals is inputted,
        indices may not be contiguous. 

        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for querying the IntervalSet. This is useful for
        when the query is not of the same object class as the members 
        of IntervalSet. The function must accept one (and only one) argument
        and outputs a single Interval-descendant object.
        """
        upper = 0
        for node in _filter_proper(_listify(nodes), sort=_node_pos_longest):
            index = self.find_index_beg(node, lower=upper)
            while 0 <= index < self.length and \
                  node.interval.isoverlapping(self[index].interval):
                yield index
                index += 1
            upper = index


    def find_overlap_index_bounds(self, nodes):
        """
        Perform an IntervalSet header overlap search with one or more query
        interval objects and return a 2-tuple containing the Pythonic
        range of overlapping items, or `(-1, -1)` if none.

        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for querying the IntervalSet. This is useful for
        when the query is not of the same object class as the members 
        of IntervalSet. The function must accept one (and only one) argument
        and outputs a single Interval-descendant object.
        """
        lower = -1
        upper = -1
        for node in _filter_proper(_listify(nodes), sort=_node_pos_longest):
            index = self.find_index_beg(node, lower=upper)
            while 0 <= index < self.length and \
                  node.interval.isoverlapping(self[index].interval):
                if lower < 0:
                    lower = index
                index += 1
                upper = index
        return lower, upper


    def find_subinterval_index_beg(self, node, lower=0, upper=-1):
        """
        Return the right-most start (inclusive) index for a query interval;
        i.e., the index of the first non-overlapping IntervalSet member.
        Returns `-1` if the query is in the wrong namespace.

        The `lower` and `upper` keywords can be used to restrict 
        the search space when the lower and upper bounds are known.

        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for querying the IntervalSet. This is useful for
        when the query is not of the same object class as the members 
        of IntervalSet. The function must accept one (and only one) argument
        and outputs a single Interval-descendant object.
        """
        if self.length < 1 or \
           self[0].interval.namespace != node.interval.namespace:
            return -1            
        if not (0 <= lower < self.length):
            lower = 0
        if not (0 <= upper < self.length):
            upper = self.length
        if self[self.length-1].interval.beg < node.interval.end:
            return self.length  # - 1  # <=[makes inclusive]
        while lower < upper:
            middle = (lower + upper) // 2
            if node.interval.beg <= self[middle].interval.beg:
                upper = middle
            else:
                lower = middle + 1
        return lower  # - 1  # <=[makes inclusive]

    
    def find_subinterval_index_end(self, node, lower=0, upper=-1):
        """
        Return the left-most end (exclusive) index for a query interval. 
        IntervalSet members may not necessarily overlap the query 
        interval. Guarenteed to return an index 0:L, where L is the
        length. Returns `-1` if the query is in the wrong namespace.

        The `lower` and `upper` keywords can be used to restrict 
        the search space when the lower and upper bounds are known.

        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for querying the IntervalSet. This is useful for
        when the query is not of the same object class as the members 
        of IntervalSet. The function must accept one (and only one) argument
        and outputs a single Interval-descendant object.
        """
        if self.length < 1 or \
           self[0].interval.namespace != node.interval.namespace:
            return -1
        if not (0 <= lower < self.length):
            lower = 0
        if not (0 <= upper < self.length):
            upper = self.length
        while lower < upper:
            middle = (lower + upper) // 2
            if self[middle].interval.end <= node.interval.end:
                lower = middle + 1
            else:
                upper = middle
        return lower

    
    
class IntervalSet(BaseIntervalCollection):
    """
    Implements and extends the Nested Containment List algorithm
    described in:
    
      Alekseyenko AV, Lee CJ. Nested Containment List (IntervalSet): a new
      algorithm for accelerating interval query of genome alignment
      and interval databases. Bioinformatics. 2007 23(11):1386-1393. 
      doi: 10.1093/bioinformatics/btl647. PMID: 17234640.

    The constructor code is ported from:
      https://github.com/biocore-ntnu/ncls/blob/master/ncls/src/intervaldb.c

    This class extends the original IntervalSet algorithm to include 
    `insert()` and `remove()` methods, as well as some useful binary
    searches.

    Build a Nested Containment List:

    >>> intervals = [
    ...    Interval("Chr1", 10, 100),
    ...    Interval("Chr1", 200,500),
    ...    Interval("Chr1",  0, 150)
    ... ]
    >>> ncl = IntervalSet(intervals)

    Find intervals overlapping a query interval:

    >>> overlaps = list(ncl.find_overlaps(Interval("Chr1", 75, 120)))
    [Interval(Chr1:0-150), Interval(Chr1:10-100)]

    """

    # Constructors
    # ============
    def __init__(self, intervals=[], setter=_pass):
        """
        Multiple references to the same object(s) are silently ignored.

        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for querying the IntervalSet. This is useful for
        when the query is not of the same object class as the members 
        of IntervalSet. The function must accept one (and only one) argument
        and outputs a single Interval-descendant object.
        """
        BaseIntervalCollection.__init__(self, setter)
        self._set_ncls(map(self._set, intervals))  # calls clear()


    def _set_ncls(self, nodes):
        self.clear()

        # TODO: avoid sorting every time
        nodes = sorted(nodes, key=_node_pos_longest)  
        length = len(nodes)
        # null intervals are sorted to the end, so any list with a
        # null interval at index 0 is therefore empty.
        if ((length < 1) or nodes[0].interval.isempty()):
            return

        d = 0  # duplicate count
        p = 0  # parent index
        i = 1  # "child" index
        visited = set()
        parents = _Sublist()  # stack of superinterval indices
        toplist = self._toplist
        sublist = self._sublist
        toplist.append(nodes[p])
        while i < length:
            if nodes[i].interval.isempty():
                break
            if nodes[i].interval.namespace != nodes[p].interval.namespace:
                raise ValueError("mixed-namespace IntervalSet")
            if nodes[i].interval.issubinterval(nodes[p].interval, proper=True):
                if hash(nodes[i]) in visited:
                    i += 1
                    d += 1
                    continue
                
                if nodes[i].interval.issubinterval(nodes[i-1].interval, proper=True):
                    # if the parent is not already in the stack, add it:
                    if ((parents.length < 1) or (parents[0] != i-1)):
                        parents.appendleft(i-1)
                    p = parents[0]
                self._insert_sublist(nodes[p])
                sublist[nodes[p].sublist].append(nodes[i])
                visited.add(hash(nodes[i]))
                i += 1
                
            elif parents.length:
                p = parents.popleft()
            else:
                toplist.append(nodes[i])
                visited = set()
                p  = i
                i += 1
                
        self._length = i - d

        
    # Superclass polymorphisms:
    # =========================
    def _get_node(self, node):
        return node

    # TODO: merge _iter_nodes() and _find_nodes() methods
    def _iter_nodes(self, lower=0, upper=-1):
        if self._length < 1:
            return
        if not (0 <= lower < self._toplist.length):
            lower = 0
        if not (0 <= upper < self._toplist.length):
            upper = self._toplist.length
            
        toplists = self._toplist
        sublists = self._sublist
        toplists.index = lower

        listdeque = _deque()
        listdeque.append(toplists)
        rangedeque = _deque()
        rangedeque.append((lower, upper))
        while listdeque:
            toplist = listdeque[0]
            lower, upper = rangedeque[0]
            if lower <= toplist.index < upper:
                yield toplist[toplist.index]

                if 0 <= toplist[toplist.index].sublist < sublists.length:
                    sublist = sublists[toplist[toplist.index].sublist]
                    sublist.index = 0
                    rangedeque.appendleft((0, sublist.length))
                    listdeque.appendleft(sublist)
                toplist.index += 1
            else:
                rangedeque.popleft()
                listdeque.popleft()

        
    def _find_nodes(self, nodes, pairwise=False, get=lambda i,o:o):
        if self._length < 1:
            return
        # Use the depth-first recursive algorithm, leveraging (sub)list
        # stacks, to efficiently search the Nested Containment List for
        # overlaps from the root (toplist) down (through sublists). This
        # method returns a generator object (via `yield`) that collects 
        # overlapping _Node objects, deferring to wrapper methods
        # that will decide what data to extract.
        toplists = self._toplist
        sublists = self._sublist

        nr = not pairwise
        visited  = set()
        for node in _listify(nodes):
            # Search toplist for top-level overlap; if no overlaps,
            # then we are certain there are no sub-intervals with
            # overlaps

            toplist = toplists
            toplist.index = toplist.find_overlap_index_beg(node)

            listdeque = _deque()
            listdeque.append(toplist)
            while listdeque:
                toplist = listdeque[0]
                if ((0 <= toplist.index < toplist.length) and
                    (node.interval.isoverlapping(toplist[toplist.index].interval))):
                    # The interval intersects another, return result if 
                    # non-redundant (if we haven't seen its hash value)
                    if nr and hash(toplist[toplist.index].instance) in visited:
                        toplist.index += 1
                        continue
                    visited.add(hash(toplist[toplist.index].instance))
                    
                    yield get(node, toplist[toplist.index])

                    if 0 <= toplist[toplist.index].sublist < sublists.length:
                        sublist = sublists[toplist[toplist.index].sublist]
                        sublist.index = sublist.find_overlap_index_beg(node)
                        if 0 <= sublist.index < sublist.length:
                            listdeque.appendleft(sublist)
                    toplist.index += 1
                else:
                    # End of overlap with (sub)list
                    listdeque.popleft()

                            
    # Identity and introspection
    # ==========================
    def __bool__(self):
        return not self.isnull()


    def __len__(self):
        return self._length

    
    def __hash__(self):
        return id(self)

    
    def __repr__(self):
        """Return repr(self)."""
        padding_len = len(self.__class__.__name__)
        padding_sep = ' ' * (padding_len + 1)
        padding_hdr = ',\n' + ' ' * (padding_len + 8)
        padding_sub = ',\n' + ' ' * (padding_len + 11)
        return "%s(header=%s,\n%ssubheader=%s)" % (
            self.__class__.__name__,
            _reprify(self._toplist, sep=padding_hdr, indent=True),
            padding_sep,
            _reprify(self._sublist, sep=padding_sub, indent=True)
        )        


    def __str__(self):
        return _reprify(self)


    @property
    def namespace(self):
        return _NULL_NS \
            if   self.isempty() \
            else self._toplist[0].interval.namespace
        
    
    @property
    def beg(self):
        return _NULL_BEG \
            if   self.isempty() \
            else self._toplist[0].interval.beg

    @property
    def start(self):
        return self.beg
    

    @property
    def end(self):
        return _NULL_END \
            if   self.isempty() \
            else self._toplist[-1].interval.end

    
    @property
    def stop(self):
        return self.end
    
    
    @property
    def header(self):
        """Return the IntervalSet header list. Not settable."""
        return self._toplist

    
    @property
    def subheader(self):
        """Return the IntervalSet subheader lists. Not settable."""
        return self._sublist


    # Comparison methods
    def __eq__(self, other):
        return isinstance(other, self.__class__) and \
            self._length  == other._length and \
            self._toplist == other._toplist and \
            self._sublist == other._sublist


    def __ge__(self, other):
        return self == other or self > other

    
    def __gt__(self, other):
        pass


    def __ne__(self, other):
        return not (self == other)
    

    def __le__(self, other):
        return self == other or self < other
    
    
    def __lt__(self, other):
        pass
    
    
    # Update methods
    def _insert(self, index, node, _list=None):
        toplists = self._toplist
        sublists = self._sublist
        subslots = self._subslot

        if toplists.length and \
           toplists[0].interval.namespace != node.interval.namespace:
            raise ValueError("Cannot construct mixed namespace IntervalSet")
        
        toplist = toplists if _list is None else _list
        toplist.index = index

        nodedeque = _deque()  # as a queue
        listdeque = _deque()  # as a queue
        nodedeque.append(node)
        listdeque.append(toplist)
        while nodedeque:
            node = nodedeque[0]  # query node
            toplist = listdeque[0]
            if toplist.index < 0 or \
               toplist.length < 1 or \
               toplist.length <= toplist.index:
                toplist.append(node)
                nodedeque.popleft()
                listdeque.popleft()

            elif ((toplist.index+1 < toplist.length) and
                  ((toplist[toplist.index].interval.beg == toplist[toplist.index+1].interval.beg) and 
                   (toplist[toplist.index].interval.end == toplist[toplist.index+1].interval.end))):
                # list contains equivalents; shift right to maintain
                # sorted order:
                toplist.index += 1
                
            elif toplist[toplist.index].interval.beg == node.interval.beg and \
                 toplist[toplist.index].interval.end == node.interval.end:
                # Target node i and query node are equivalent; insert
                # query node after node i, and transfer its sublist:
                node.sublist = toplist[toplist.index].sublist
                toplist[toplist.index].sublist = -1
                toplist.insert(toplist.index+1, node)
                nodedeque.popleft()
                listdeque.popleft()
                
            elif toplist[toplist.index].interval.issuperinterval(node.interval):
                # Target node i contains query node. Insert into sublist,
                # then update queue
                if toplist[toplist.index].instance is node.instance:
                    raise DuplicateKeyError("'%s'" % repr(node.instance))
                sublist = self._insert_sublist(toplist[toplist.index])
                sublist.index = sublist.find_index_beg(node)
                listdeque[0] = sublist

            elif toplist[toplist.index].interval.issubinterval(node.interval):
                # Target node i contained within query node. Query may
                # contain others, so add the target to node queue, delete
                # target from the toplist, and pull another.
                sublist = self._insert_sublist(node)
                subnode = toplist[toplist.index]
                # sublist = sublists[node.sublist]
                sublist.index = sublist.find_index_beg(subnode)
                nodedeque.append(subnode)
                listdeque.append(sublist)
                del(toplist[toplist.index])
                # Next target node shifts into place, don't increment
                
            elif toplist[toplist.index].interval.end >= node.interval.end:
                # Query node does not contain--and is not contained by--the
                # target node, i. Insert, as target.end >= query.end and
                # the query node cannot contain other nodes.
                toplist.insert(toplist.index, node)
                nodedeque.popleft()  # <= check next target interval too?
                listdeque.popleft()
                
            elif toplist[toplist.index].interval.beg <= node.interval.beg:
                # Query node does not contain--and is not contained by--the 
                # target node, i. Both the start *and* stop of the query
                # node are also downstream of the target node. New node may
                # contain others downstream, so examine target node i+1.

                # Is is possible that sublisted target nodes are present
                # under target node i that should be included under the
                # query before checking node i+1 ?
                toplist.index += 1
                
            else:
                raise NotImplementedError(
                    "BUG: Record %s" % str(node.interval)
                )
        
            
    def _insert_sublist(self, node):
        if node.sublist < 0:
            if self._subslot.length > 0:
                node.sublist = self._subslot.popleft()
            else:
                node.sublist = self._sublist.length
                self._sublist.append(_Sublist())
        return self._sublist[node.sublist]
            

    def _copy_state(self, other):
        self._toplist = other._toplist
        self._sublist = other._sublist
        self._subslot = other._subslot
        self._length  = other._length

                    
    def empty(self):
        """Remove all elements from the IntervalSet."""
        self._toplist = _Sublist()
        self._sublist = _Sublist()
        self._subslot = _Sublist()
        self._length  = 0


    def copy(self):
        """Create and copy of self."""
        copy = self.__class__(setter=self._setter)
        copy._set_ncls(self._copy_nodes())
        return copy
    
        
    def discard(self, interval, setter=None):
        """
        Remove the first object equivalent to the input interval
        object. If the interval is not a IntervalSet member, do nothing.

        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for querying the IntervalSet. This is useful for
        when the query is not of the same object class as the members 
        of IntervalSet. The function must accept one (and only one) argument
        and output a single Interval-descendant object.
        """
        try:
            self.remove(interval, setter)
        except KeyError:
            pass
        
        
    def insort(self, interval, setter=None):
        """
        Add member object to IntervalSet in sorted position.

        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for querying the IntervalSet. This is useful for
        when the query is not of the same object class as the members 
        of IntervalSet. The function must accept one (and only one) argument
        and output a single Interval-descendant object.
        """
        node = self._set(interval, setter)
        index = self._toplist.find_index_beg(node)
        try:
            self._insert(index, node)
            self._length += 1
        except DuplicateKeyError:
            pass


    def pop(self):
        if self._length < 1:
            raise KeyError('pop from an empty set')
        interval = self._toplist[0].instance
        self._remove(self._toplist[0])
        return interval
        
        
    def remove(self, interval, setter=None):
        """
        Remove the first object equivalent to the input interval
        object. If the interval is not a member, raise a KeyError.

        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for querying the IntervalSet. This is useful for
        when the query is not of the same object class as the members 
        of IntervalSet. The function must accept one (and only one) argument
        and output a single Interval-descendant object.
        """
        self._remove(self._set(interval, setter))

                
    def _remove(self, node):
        toplists = self._toplist
        sublists = self._sublist
        subslots = self._subslot
        toplist  = toplists
        toplist.index = toplist.find_overlap_index_beg(node)
        # .find_overlap_index_beg(node) not ideal, it would be
        # more efficient to do a search requiring the query to
        # be contained.

        if toplist.index < 0 or \
           toplist.length < 1:
            raise KeyError("'%s'" % repr(node.instance))
        
        listdeque = _deque()
        listdeque.append(toplists)
        while listdeque:
            toplist = listdeque[0]
            if 0 <= toplist.index < toplist.length:
                if toplist[toplist.index].instance is node.instance:
                    # If node has a sublist, re-insort sublist
                    if 0 <= toplist[toplist.index].sublist < sublists.length:
                        # Save the sublist data before deleting the
                        # node and making its sublist slot available
                        # or the indexing will be incorrect.
                        subnodes = sublists[toplist[toplist.index].sublist]
                        sublists[toplist[toplist.index].sublist] = _Sublist()
                        subslots.append(toplist[toplist.index].sublist)
                        del(toplist[toplist.index])
                        self._length -= 1
                        
                        # befor = toplist.index - 1
                        # after = toplist.index
                        for subnode in subnodes:
                            self._insert(toplist.index-1, subnode, _list=toplist)
                            # if-else condition order matters.
                            # Prioritize sort order:
                            # if ((after < toplist.length) and
                            #     (toplist[after].interval.beg <= subnode.interval.beg) and
                            #     (toplist[after].interval.end >= subnode.interval.end)):
                            #     # Insert after current index
                            #     self._insert(after, subnode, _list=toplist)
                            # elif befor < 0:
                            #     self._insert(after, subnode, _list=toplist)
                            # else:
                            #     # Insert before or at position
                            #     self._insert(befor, subnode, _list=toplist)
                    else:
                        del(toplist[toplist.index])
                        self._length -= 1
                    listdeque.popleft()
                    return

                elif 0 <= toplist[toplist.index].sublist < sublists.length:
                    # No match in toplist, add its sublist to the deque
                    # for dfs search. Increment toplist.index because
                    # our query interval may not be contained in node i,
                    # but may be in/under node i+1.
                    sublist = sublists[toplist[toplist.index].sublist]
                    sublist.index = sublist.find_overlap_index_beg(node)
                    listdeque.appendleft(sublist)
                    toplist.index += 1  
                else:
                    # No sublists to search
                    toplist.index += 1
            else:
                # When searching toplist[i] but our match is in i+1,
                # searching the sublist of i will get us here.
                listdeque.popleft()
                # next element pops into place, don't increment

        raise KeyError("'%s'" % repr(node.instance))
        
                
    # Iteration and search methods
    def __iter__(self):
        return (self._get(n) for n in self._iter_nodes())

                    
    def overlap_length(self, intervals, setter=None):
        """
        Returns the length of overlaps a query interval or 
        IntervalList object has with this IntervalSet object.

        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for querying the IntervalSet. This is useful
        for when the query is not of the same object class as the 
        members of IntervalSet. The function must accept one (and only
        one) argument and outputs a single Interval-descendant object.
        """
        raise NotImplementedError('%s.overlap_length()' % self.__class__.__name__)

    
    def overlap_fraction(self, intervals, setter=None):
        """
        Returns the fraction of overlap a query interval or IntervalList 
        object shares with this IntervalSet object. Setting `query=True`
        calculates the overlap fraction with respect to the query length.        

        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for querying the IntervalSet. This is useful for
        when the query is not of the same object class as the members 
        of IntervalSet. The function must accept one (and only one) argument
        and outputs a single Interval-descendant object.
        """
        raise NotImplementedError('%s.overlap_fraction()' % self.__class__.__name__)

    
    def overlap_pairs(self, intervals, setter=None):
        """
        Preform an inclusive overlap search of IntervalSet with one or more query
        interval objects and return a generator object producing 
        2-tuples of each query interval and its overlapping IntervalSet 
        member.

        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for querying the IntervalSet. This is useful for
        when the query is not of the same object class as the members 
        of IntervalSet. The function must accept one (and only one) argument
        and outputs a single Interval-descendant object.
        """
        nodes = sorted(
            map(lambda i: self._set(i, setter), _listify(intervals)),
            key=_node_pos
        )
        for i,o in self._find_nodes(nodes, True, _pass):
            yield (i.instance, o.instance)
            
                    
    def overlaps(self, intervals, setter=None):
        """
        Perform an inclusive overlap search of IntervalSet with one or more query
        interval objects and return a generator object producing 
        IntervalSet members overlapping the input interval object(s).

        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for querying the IntervalSet. This is useful for
        when the query is not of the same object class as the members 
        of IntervalSet. The function must accept one (and only one) argument
        and outputs a single Interval-descendant object.
        """
        nodes = _filter_proper(
            map(lambda n: self._set(n, setter), _listify(intervals)),
            sort=_node_pos_longest
        )
        return (n.instance for n in self._find_nodes(nodes, False))
    
    
    def subintervals(self, intervals, setter=None):
        raise NotImplementedError('%s.subintervals()' % self.__class__.__name__)
        

    # Overlap set methods:
    def __and__(self, other):
        return self.intersection(self, other)


    def __contains__(self, other):
        return self.issuperinterval(other)


    def __iand__(self, other):
        self.intersection_update(other)


    def __ior__(self, other):
        self.union_update(other)


    def __isub__(self, other):
        self.difference_update(other)


    def __ixor__(self, other):
        self.symmetric_difference_update(other)


    def __or__(self, other):
        return self.union(other)


    def __rand__(self, other):
        return self.intersection(other)


    def __ror__(self, other):
        return self.union(other)


    def __rsub__(self, other):
        raise NotImplementedError('%s.__rsub__()' % self.__class__.__name__)
    
    
    def __rxor__(self, other):
        return self.symmetric_difference(other)


    def __sub__(self, other):
        return self.difference(other)
    
    
    def __xor__(self, other):
        return self.symmetric_difference(other)


    def _coerce_class(self, other, setter=None):
        if isinstance(other, BaseIntervalCollection):
            return other
        else:
            return self.__class__(_listify(other), setter or _pass)

    
    def _isoverlapping(self, other, setter=_pass):
        if not isinstance(other, BaseIntervalCollection):
            return self._isoverlapping(
                self.__class__(_listify(other), setter=setter)
            )
        elif self.namespace == other.namespace:
            lower, upper = (self, other) if self < other else (other, self)
            if isinstance(lower, IntervalList):
                getter = lambda l: l
                setter = lambda n: n.interval
            else:
                getter = lambda l: l._toplist
                setter = lambda n: n
            for node in upper._iter_nodes():
                if 0 <= getter(lower).find_overlap_index_beg(setter(node)):
                    return True
        return False
    
    
    def isabutting(self, other):
        return Interval.isabutting(self, other)

    
    def isabutting_beg(self, other):
        return Interval.isabutting_beg(self, other)

    
    def isabutting_end(self, other):
        return Interval.isabutting_end(self, other)


    def isdisjoint(self, other):
        return not self.isoverlapping(other)

    
    def isempty(self):
        return self._length < 1    

    
    def issuperinterval(self, other, proper=False, strict=False):
        return (Interval.issuperinterval(self, other, proper) and
                ((not strict) or self._isoverlapping(other)))

    
    def issubinterval(self, other, proper=False, strict=False):
        return (Interval.issubinterval(self, other, proper) and
                ((not strict) or self._isoverlapping(other)))

    
    def isoverlapping(self, other, strict=False):
        return (Interval.isoverlapping(self, other) and
                ((not strict) or self._isoverlapping(other)))

    
    def isoverlapping_beg(self, other, strict=False):
        return (Interval.isoverlapping_beg(self, other) and
                ((not strict) or self._isoverlapping(other)))

    
    def isoverlapping_end(self, other, strict=False):
        return (Interval.isoverlapping_end(self, other) and
                ((not strict) or self._isoverlapping(other)))

    
    def merge(self, abutting=False):
        """
        self.merge() -> IntervalSet

        Merge overlapping intervals and output a new IntervalSet of
        non-overlapping interval objects. Abutting intervals are not
        merged by default, but can be when `abutting=True`. Requires
        O(n) time in the average case.
        
        >>> I = IntervalSet([Interval("Chr",1,50), Interval("Chr",45,80)])
        >>> I.merge()
        IntervalSet(header=[Chr:1-80], subheader=[])
        """
        # I independently re-invented the interval merge algorithm:
        # https://www.geeksforgeeks.org/merging-intervals
        ncls = self.__class__(setter=self._setter)
        if self._length < 1:
            return ncls
        N = self._toplist.length
        i = 1
        p = 0
        dist = 0  # = -dist
        nodes = self._toplist
        toplist = ncls._toplist
        toplist.append(_Node(Interval(
            nodes[0].interval.namespace,
            nodes[0].interval.beg,
            nodes[0].interval.end
        )))
        overlap = dist.__ge__ if abutting else dist.__gt__
        while i < N:
            if overlap(nodes[i].interval.beg - toplist[p].interval.end):
                # overlap between the two intervals, extend node p:
                toplist[p].interval.end = nodes[i].interval.end
            else:
                # no overlap, add new node p:
                toplist.append(_Node(Interval(
                    nodes[i].interval.namespace,
                    nodes[i].interval.beg,
                    nodes[i].interval.end
                )))
                p += 1
            i += 1
        ncls._length = p + 1
        return ncls


    def merge_update(self, abutting=False):
        """
        self.merge_update() -> None

        Merge overlapping intervals and update self in-place with the 
        resulting non-overlapping interval objects. Abutting intervals
        are not merged by default, but can be when `abutting=True`. 
        Requires O(n) time in the average case.
        
        >>> I = IntervalSet([Interval("Chr",1,50), Interval("Chr",45,80)])
        >>> I.merge_update()
        >>> repr(I)
        IntervalSet(header=[Chr:1-80], subheader=[])
        """
        self._copy_state(self.merge(abutting))
        

    def complement(self, lower=None, upper=None):
        """
        self.complement() -> IntervalSet

        Computes the complement of the intervals contained in self
        and return a new IntervalSet object. Requires O(n) time in 
        the average case.
        
        Setting `lower` and `upper` defines the lower- and upper-bound
        values of the namespace.
        
        >>> I = IntervalSet([Interval("Chr",100, 1000)])
        >>> I.complement(lower=0, upper=1048)
        IntervalSet(header=[Chr:0-100, Chr:1000-1048], subheader=[])
        """
        if lower is None:
            lower = self.beg
        if lower > self.beg:
            raise ValueError("Lower bound greater than IntervalSet.beg")
        if upper is None:
            upper = self.end
        if upper < self.end:
            raise ValueError("Upper bound less than IntervalSet.end")
        ncls = self.__class__()
        dist = 0  # = -dist
        gapped = dist.__lt__
        nodes = self._toplist
        toplist = ncls._toplist
        if self.beg > lower:
            toplist.append(_Node(Interval(
                self.namespace,
                lower,
                self.beg
            )))
            ncls._length += 1
        for i in range(1, self._toplist.length):
            if gapped(nodes[i].interval.beg - nodes[i-1].interval.end):
                # gap between the two intervals, new record:
                toplist.append(_Node(Interval(
                    nodes[i].interval.namespace,
                    nodes[i-1].interval.end,
                    nodes[i].interval.beg
                )))
                ncls._length += 1
        if self.end < upper:
            toplist.append(_Node(Interval(
                self.namespace,
                self.end,
                upper
            )))
            ncls._length += 1
        return ncls


    def complement_update(self, lower=None, upper=None):
        """
        self.complement_update() -> None

        Computes the complement of the intervals contained in self
        and update self in-place. Requires O(n) time in the average 
        case.
        
        Setting `lower` and `upper` defines the lower- and upper-bound
        values of the namespace.

        >>> I = IntervalSet([Interval("Chr",100, 1000)])
        >>> I.complement_update(lower=0, upper=1048)
        >>> repr(I)
        IntervalSet(header=[Chr:0-100, Chr:1000-1048], subheader=[])
        """
        self._copy_state(self.complement(lower, upper))
        
    
    def difference(self, other, pairwise=True, setter=None):
        """
        When `pairwise=False`, only maximal intersection ranges 
        with other are returned.

        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for querying the IntervalSet. This is useful for
        when the query is not of the same object class as the members 
        of IntervalSet. The function must accept one (and only one) argument
        and output a single Interval-descendant object.
        """
        raise NotImplementedError('%s.difference()' % self.__class__.__name__)

    
    def difference_update(self, other, pairwise=True, setter=None):
        """
        When `pairwise=False`, only maximal intersection ranges 
        with other are returned.

        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for querying the IntervalSet. This is useful for
        when the query is not of the same object class as the members 
        of IntervalSet. The function must accept one (and only one) argument
        and output a single Interval-descendant object.
        """
        self._copy_state(self.difference(other, pairwise, setter))

        
    def hull(self, other=None):
        """
        self.hull() -> Interval
        self.hull(other) -> Interval

        Returns the smallest interval closure of self (and, optionally,
        other).
        """
        this = Interval(self.namespace, self.beg, self.end)
        if this.isempty():
            this.clear()
        if other:
            if other.isempty():
                other = Interval()
            if this.namespace == other.namespace:
                this.beg = min(this.beg, other.beg)
                this.end = max(this.end, other.end)
        return this

    
    def intersection(self, other, pairwise=True, setter=None):
        """
        self.intersection(other) -> IntervalSet

        Computes all pairwise interval intersections between self and
        other. Requires O(m*log(n)) time in the worst case.

        When `pairwise=False`, only maximal intersection ranges 
        with other are returned.

        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for querying the IntervalSet. This is useful for
        when the query is not of the same object class as the members 
        of IntervalSet. The function must accept one (and only one) argument
        and output a single Interval-descendant object.
        """
        other = self._coerce_class(other, setter)
        ncls = self.__class__(setter=setter)
        if self._length < 1 or other._length < 1:
            return ncls
        if not pairwise:
            other = other.merge()
                
        nodes = _deque()
        sublists = self._sublist
        toplists = self._toplist
        for node in other._iter_nodes():
            toplist = toplists
            toplist.index = toplist.find_overlap_index_beg(node)

            listdeque = _deque()
            listdeque.append(toplist)
            while listdeque:
                toplist = listdeque[0]
                if ((0 <= toplist.index < toplist.length) and
                    (toplist[toplist.index].interval.beg < node.interval.end)):
                    # member node must overlap query node by search criterion
                    copy = Interval()
                    copy.namespace = toplist[toplist.index].interval.namespace
                    if toplist[toplist.index].interval.issuperinterval(node.interval):
                        copy.beg = node.interval.beg
                        copy.end = node.interval.end
                    elif toplist[toplist.index].interval.issubinterval(node.interval):
                        copy.beg = toplist[toplist.index].interval.beg
                        copy.end = toplist[toplist.index].interval.end
                    elif toplist[toplist.index].interval.end < node.interval.end:
                        copy.beg = node.interval.beg
                        copy.end = toplist[toplist.index].interval.end
                    else:  # isoverlapping_end of query
                        copy.beg = toplist[toplist.index].interval.beg
                        copy.end = node.interval.end
                    nodes.append(_Node(copy, (toplist[toplist.index].instance, node.instance)))
                    if 0 <= toplist[toplist.index].sublist < sublists.length:
                        sublist = sublists[toplist[toplist.index].sublist]
                        sublist.index = sublist.find_overlap_index_beg(node)
                        listdeque.appendleft(sublist)
                    toplist.index += 1
                else:
                    # no overlap
                    listdeque.popleft()
        ncls._set_ncls(nodes)
        return ncls
        
            
    def intersection_update(self, other, pairwise=True, setter=None):
        """
        self.intersection_update(other) -> None

        Computes all pairwise interval intersections between self and
        other, then updates self. Requires O(m*log(n)) time in the 
        worst case.

        When `pairwise=False`, only maximal intersection ranges 
        with other are returned.

        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for querying the IntervalSet. This is useful for
        when the query is not of the same object class as the members 
        of IntervalSet. The function must accept one (and only one) argument
        and output a single Interval-descendant object.
        """        
        self._copy_state(self.intersection(other, pairwise, setter))

        
    def symmetric_difference(self, other, pairwise=True, setter=None):
        """
        When `pairwise=False`, only maximal union ranges with other are 
        returned.

        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for querying the IntervalSet. This is useful for
        when the query is not of the same object class as the members 
        of IntervalSet. The function must accept one (and only one) argument
        and output a single Interval-descendant object.
        """
        raise NotImplementedError('%s.symmetric_difference()' % self.__class__.__name__)

    
    def symmetric_difference_update(self, other, pairwise=True, setter=None):
        """
        When `pairwise=False`, only maximal union ranges with other are 
        returned.

        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for querying the IntervalSet. This is useful for
        when the query is not of the same object class as the members 
        of IntervalSet. The function must accept one (and only one) argument
        and output a single Interval-descendant object.
        """
        self._copy_state(self.symmetric_difference(other, pairwise, setter))


    def _scan(self, q, Wq, t, Wt, rev=False):
        i = 0
        L = len(Wt)
        Wo = _deque()
        overlaps = []
        while i < L:
            if Wt[i].interval.end <= q.interval.beg:
                # A deque del() was implemented internally by rotate()'ing
                # the deque, pop()'ing, then rotate()'ing back, this is 2n
                # iterations of the deque length. Is this faster than
                # building a new empty deque and freeing the old one (which
                # requires iterating over all elements and freeing mem blocks
                # anyways)?
                del(Wt[i])
                L -= 1
            elif Wt[i].interval.isoverlapping(q.interval):
                if rev:
                    yield (Wt[i], q)
                else:
                    yield (q, Wt[i])
                i += 1
        if q.interval.end > t.interval.beg:
            Wq.append(q)

            
    # def union2(self, other, abutting=False, pairwise=True, setter=None):
    #     ix = 0;
    #     iy = 0;
    #     X  = list(self._iter_nodes())
    #     Y  = list(other._iter_nodes())
    #     Wx = _deque()
    #     Wy = _deque()
    #     Lx = len(X)
    #     Ly = len(Y)
    #     sentinel = _Node(Interval(self.namespace, _INF, _INF))
    #     while ((ix < Lx) or (iy < Ly)):
    #         x = X[ix] if ix < Lx else sentinel
    #         y = Y[iy] if iy < Ly else sentinel
    #         if x.interval.beg <= y.interval.beg:
    #             for pair in self._scan(x, Wx, y, Wy, rev=False):
    #                 print(('x', pair))
    #             ix += 1
    #         else:
    #             for pair in self._scan(y, Wy, x, Wx, rev=True):
    #                 print(('y', pair))
    #             iy += 1

                
    def union(self, other, abutting=False, pairwise=True, setter=None):
        """
        self.union(other) -> IntervalSet

        Find the interval overlap union between self and other. Best
        case, O(m+n); worst case, O(m*n).

        Setting `abutting=True` allows union of abutting intervals. When
        `pairwise=False`, only maximal union ranges with other are 
        returned.

        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for querying the IntervalSet. This is useful for
        when the query is not of the same object class as the members 
        of IntervalSet. The function must accept one (and only one) argument
        and output a single Interval-descendant object.
        """
        other = self._coerce_class(other, setter)
        # I independently re-invented an algorithm similar to fjoin:
        # https://doi.org/10.1089/cmb.2006.13.1457
        if not pairwise:
            other = other.merge(abutting)
        nodes  = _deque()
        nodes1 = sorted(self._copy_nodes(), key=_node_pos)
        nodes2 = sorted(other._copy_nodes(), key=_node_pos)
        len1 = len(self)
        len2 = len(other)
        i = 0  # nodes1 ref index
        j = 0  # nodes2 current overlap index
        k = 0  # nodes2 first overlap index
        dist = 0  # = -dist
        upstream = dist.__gt__ if abutting else dist.__ge__
        while ((i < len1) or (k < len2)):
            print(
                (i, j, k,
                 (nodes1[i].interval if i < len1 else None),
                 (nodes2[k].interval if k < len2 else None),
                 (nodes2[j].interval if j < len2 else None))
            )
            if ((i < len1) and (j < len2)):
                if upstream(nodes1[i].interval.end - nodes2[j].interval.beg):
                    # node1 < node2, next node1
                    if nodes1[i].sublist == -1:
                        nodes.append(nodes1[i])
                        k = j
                    j  = k
                    i += 1
                elif upstream(nodes2[j].interval.end - nodes1[i].interval.beg):
                    # node2 < node1, next node2
                    if nodes2[j].sublist == -1:
                        nodes.append(nodes2[j])
                    k  = j
                    j += 1
                else:
                    # overlap
                    if ((i+1 < len1) and
                        upstream(nodes2[j].interval.end - nodes1[i+1].interval.beg)):
                        # peek at the next node1 to set k
                        k = j + 1
                    nodes.append(_Node(
                        Interval(
                            nodes1[i].interval.namespace,
                            min(nodes1[i].interval.beg, nodes2[j].interval.beg),
                            max(nodes1[i].interval.end, nodes2[j].interval.end),
                        ),
                        (
                            nodes1[i].instance,
                            nodes2[j].instance
                        )
                    ))
                    nodes1[i].sublist = -2
                    nodes2[j].sublist = -2
                    j += 1
            elif i < len1:
                # ergo: j >= len2, nodes1 _may_ be exhausted, reset j
                if nodes1[i].sublist == -1:
                    nodes.append(nodes1[i])
                    k = j
                j  = k
                i += 1
            else:
                # ergo: i >= len1, nodes1 is exhausted
                if nodes2[k].sublist == -1:
                    nodes.append(nodes2[k])
                k += 1
                
        ncls = self.__class__(setter=self._setter)
        ncls._set_ncls(nodes)
        return ncls
        

    def union_update(self, other, abutting=False, pairwise=True, setter=None):
        """
        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for querying the IntervalSet. This is useful for
        when the query is not of the same object class as the members 
        of IntervalSet. The function must accept one (and only one) argument
        and outputs a single Interval-descendant object.
        """
        self._copy_state(self.union(other, abutting, pairwise, setter))


    # Item set methods:
    def isdisjoint_set(self, other):
        return self.intersection_set(other).isnull()

    
    def issubset(self, other):
        return set(self._iter_nodes()).issubset(set(other._iter_nodes()))


    def issuperset(self, other):
        return set(self._iter_nodes()).issuperset(set(other._iter_nodes()))

        
    def difference_set(self, other, setter=None):
        """
        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for querying the IntervalSet. This is useful for
        when the query is not of the same object class as the members 
        of IntervalSet. The function must accept one (and only one) argument
        and outputs a single Interval-descendant object.
        """
        other = self._coerce_class(other, setter)
        ncls = self.__class__(setter=self._setter)
        ncls._set_ncls(
            set(self._copy_nodes()) - set(other._copy_nodes())
        )
        return ncls


    def difference_update_set(self, other):
        """
        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for querying the IntervalSet. This is useful for
        when the query is not of the same object class as the members 
        of IntervalSet. The function must accept one (and only one) argument
        and outputs a single Interval-descendant object.
        """
        self._copy_state(self.difference_set(other))
            

    def intersection_set(self, other, setter=None):
        """
        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for querying the IntervalSet. This is useful for
        when the query is not of the same object class as the members 
        of IntervalSet. The function must accept one (and only one) argument
        and outputs a single Interval-descendant object.
        """
        other = self._coerce_class(other, setter)
        ncls = self.__class__(setter=self._setter)
        ncls._set_ncls(
            set(self._copy_nodes()) & set(other._copy_nodes())
        )
        return ncls

    
    def intersection_update_set(self, other):
        """
        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for querying the IntervalSet. This is useful for
        when the query is not of the same object class as the members 
        of IntervalSet. The function must accept one (and only one) argument
        and outputs a single Interval-descendant object.
        """
        self._copy_state(self.intersection_set(other))

    
    def symmetric_difference_set(self, other, setter=None):
        """
        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for querying the IntervalSet. This is useful for
        when the query is not of the same object class as the members 
        of IntervalSet. The function must accept one (and only one) argument
        and outputs a single Interval-descendant object.
        """
        other = self._coerce_class(other, setter)
        ncls = self.__class__(setter=self._setter)
        ncls._set_ncls(
            set(self._copy_nodes()) ^ set(other._copy_nodes())
        )
        return ncls

    
    def symmetric_difference_update_set(self, other):
        """
        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for querying the IntervalSet. This is useful for
        when the query is not of the same object class as the members 
        of IntervalSet. The function must accept one (and only one) argument
        and outputs a single Interval-descendant object.
        """
        self._copy_state(self.symmetric_difference_set(other))


    def union_set(self, other, setter=None):
        """
        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for querying the IntervalSet. This is useful for
        when the query is not of the same object class as the members 
        of IntervalSet. The function must accept one (and only one) argument
        and outputs a single Interval-descendant object.
        """
        other = self._coerce_class(other, setter)
        ncls = self.__class__(setter=self._setter)
        ncls._set_ncls(
            set(self._copy_nodes()) | set(other._copy_nodes())
        )
        return ncls


    def union_update_set(self, other):
        """
        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for querying the IntervalSet. This is useful for
        when the query is not of the same object class as the members 
        of IntervalSet. The function must accept one (and only one) argument
        and outputs a single Interval-descendant object.
        """
        self._copy_state(self.union_set(other))


    def update(self, intervals, setter=None):
        """
        The `setter` keyword argument accepts a function used to 
        extract/construct from the input object an Interval-descendant
        object instance for querying the IntervalSet. This is useful for
        when the query is not of the same object class as the members 
        of IntervalSet. The function must accept one (and only one) argument
        and outputs a single Interval-descendant object.
        """
        self.union_update_set(intervals, setter)

            
    # Aliases
    add = insort

    clear = empty
    
    to_string = __str__
    

#       10        20        30        40        50        60        70        80
#---+----|----+----|----+----|----+----|----+----|----+----|----+----|----+----|



# NOTES:
# - builtin numeric types all have a .real, .imag, and conjugate attributes

# Resources:
# 1. https://github.com/python/cpython/tree/main/Modules
#
# 2. https://github.com/arq5x/chrom_sweep/blob/master/chrom_sweep.py
#
# 3. https://github.com/BioJulia/Bio.jl/issues/340
