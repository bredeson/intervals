"""
This module provides support for collections of Interval objects in sorted
order. The IntervalList class is a subclass of collections.deque() and provides
efficient insertion, deletion, and iteration while maintaining sorted order.

"""

import sys

from collections import deque as _deque
from .constants import NULL_NAMESPACE as _NULL_NAME
from .constants import NULL_POSITION as _NULL_POS
from .constants import POS_INF as _POS_INF
from .constants import NEG_INF as _NEG_INF
from .intervals import BaseInterval, LeftClosedInterval
from .intervals import _IntervalSetInterface, _IntervalIdentityInterface
from .errors import _BAD_METHOD_NAMESPACE, _BAD_OPERAND_NAMESPACE, _BAD_SETTER_TYPE, _NO_METHOD, _NOT_IN


__all__ = (
    'DuplicateKeyError',
    'BaseIntervalCollection',
    'IntervalList',
    'IntervalSet'
)


def _caller(level):
    """PRIVATE
    Return the name of the calling function at the given stack level. Does
    not return the function of the calling function if it is a property.
    """
    return sys._getframe(level).f_code.co_name


def _interval_pos(interval):
    return (interval.isempty(), interval.beg, interval.end)


def _node_pos(node):
    return (node.interval.isempty(), node.interval.beg, node.interval.end)


def _interval_pos_nested(interval):
    return (interval.isempty(), interval.beg, -interval.end)


def _node_pos_nested(node):
    return (node.interval.isempty(), node.interval.beg, -node.interval.end)


def remit(item):
    return item


def isiterable(item):
    return hasattr(item, '__iter__') or hasattr(item, '__next__')


def _iter(item, sort=False):
    if not isiterable(item):
        item = [item]
    if sort:
        item = sorted(item, key=sort)
    return item


def _repr(item, sep=', ', indent=False):
    if isiterable(item):
        if indent:
            sep += " "
        return '[%s]' % sep.join((
            _repr(i, sep, indent) for i in item
        ))
    else:
        return repr(item)


def _filter_nested(nodes, sort=False):
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
    __slots__ = ('instance','interval','max','sublist')

    def __init__(self, interval, instance=None, max=0, sublist=-1):
        """
        Create a _Node for an object instance.
        """
        assert isinstance(interval, BaseInterval), \
            "interval must be a BaseBaseInterval-descendant object"
        self.instance = instance or interval
        self.interval = interval
        self.sublist = sublist
        self.max = max or interval.end


    def __eq__(self, other):
        return \
            self.interval == other.interval and \
            self.instance == other.instance


    def __ne__(self, other):
        return \
            self.interval != other.interval or \
            self.instance != other.instance


    def __lt__(self, other):
        return self.interval < other.interval
    

    def __hash__(self):
        # would be preferable to hash(self.instance), but
        # instance hashabilty is not guarenteed.
        return id(self.instance)
        

    def __repr__(self):
        return "%s(%s)" % (
            self.__class__.__name__, str(self.interval)
        )

    def copy(self):
        return self.__class__(self.interval, self.instance, self.max)



class BaseIntervalCollection(
        _IntervalSetInterface,
        _IntervalIdentityInterface):

    # Copied and extended this pattern from collections.abc.Collection
    def __init__(self, setter=remit):
        super().__init__()
        self._setter = setter


    @property
    def namespace(self):
        """Raises NotImplementedError."""
        raise NotImplementedError(_NO_METHOD(self,'namespace'))

    
    @namespace.setter
    def namespace(self, namespace):
        """Raises NotImplementedError."""
        raise NotImplementedError(_NO_METHOD(self,'namespace'))    

    
    @property
    def beg(self):
        """Raises NotImplementedError."""
        raise NotImplementedError(_NO_METHOD(self,'beg'))

    
    @property
    def start(self):
        """Raises NotImplementedError."""
        return self.beg


    @property
    def mid(self):
        """Raises NotImplementedError."""
        raise NotImplementedError(_NO_METHOD(self,'mid'))


    @property
    def end(self):
        """Raises NotImplementedError."""
        raise NotImplementedError(_NO_METHOD(self,'end'))

    
    @property
    def stop(self):
        """Raises NotImplementedError."""
        return self.end

    
    def clear(self):
        """Raises NotImplementedError."""
        raise NotImplementedError(_NO_METHOD(self,'clear'))

    
    def copy(self):
        """
        self.copy() -> IntervalList

        Create a copy of self.
        """
        return self.__class__(self, setter=self._setter)

    
    def empty(self):
        """Raises NotImplementedError."""
        raise NotImplementedError(_NO_METHOD(self,'empty'))

    
    def null(self):
        """Raises NotImplementedError."""
        raise NotImplementedError(_NO_METHOD(self,'null'))

    
    def pop(self):
        """Raises NotImplementedError."""
        raise NotImplementedError(_NO_METHOD(self,'pop'))

    
    def remove(self, interval):
        """Raises NotImplementedError."""
        raise NotImplementedError(_NO_METHOD(self,'remove'))

    
    def to_slice(self):
        """
        self.to_slice() -> slice

        Return the interval as a slice object for use with lists, 
        strings, or other list-like objects. Returns `slice(-1, -1)`
        if null.
        
        >>> string = 'abcdefghijklmnopqrstuvwxyz'
        >>> interval = Interval("Chr", 2, 10)
        >>> print(string[interval.to_slice()])
        cdefghij
        """
        return slice(self.beg, self.end) if self else slice(-1, -1)


    def to_string(self):
        """
        self.to_string() -> str

        Return a string representation of the interval.

        >>> interval = Interval("Chr", 350, 475)
        >>> print(interval.to_string())
        [Chr, 350, 475]
        """

        return str(self)
    

    def __bool__(self):
        """
        bool(self) -> bool

        Test if an Interval is non-empty.
        
        >>> bool(Interval("Chr", 350, 475))
        True
        >>> bool(Interval())
        False
        """
        return not (self.isempty() or self.isnull())
    

    def __contains__(self, interval):
        """Raises NotImplementedError."""
        raise NotImplementedError(_NO_METHOD(self,'__contains__'))


    def __eq__(self):
        """Raises NotImplementedError."""
        raise NotImplementedError(_NO_METHOD(self,'__eq__'))
    
    
    def __hash__(self):
        """
        hash(self) -> int

        Return a runtime-unique id for the Interval object.
        
        >>> hash(Interval("Chr", 350, 475))
        4465105936
        """
        return id(self)

    
    def __iter__(self):
        """Raises NotImplementedError."""
        raise NotImplementedError(_NO_METHOD(self,'__iter__'))

    
    def __len__(self):
        """Raises NotImplementedError."""
        raise NotImplementedError(_NO_METHOD(self,'__len__'))    

    
    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, str(self))
    

    def __str__(self):
        return '[%s]' % ', '.join(map(str, self))


    def _copy_nodes(self):
        """PRIVATE

        Return a generator object returning copies of the underlying
        _Node objects.
        """
        return map(_Node.copy, self._iter_nodes())

    
    def _get(self, node):
        """PRIVATE

        Return the user object instance from _Node
        """
        return node.instance


    def _get_node(self, index):
        """PRIVATE

        Return the underlying _Node object at the given index
        """
        raise NotImplementedError(_NO_METHOD(self,'_get_node'))


    def _iter_nodes(self, lower=0, upper=-1):
        """PRIVATE
        
        Iterate over the underlying _Node objects
        """
        raise NotImplementedError(_NO_METHOD(self,'_iter_nodes'))
    

    def _set(self, interval, setter=None, strict=True):
        """PRIVATE
        
        Init a _Node object from an input user object. If interval is
        a _Node, pass it through.
        """
        if isinstance(interval, _Node):
            node = interval
        else:
            setter = setter or self._setter or remit
            try:
                # catches when setter:
                #  1. is not a callable
                #  2. does not accept an input argument
                #  3. does not return a BaseBaseInterval-descendant object
                node = _Node(setter(interval), interval)
            except:
                raise TypeError(
                    _BAD_SETTER_TYPE(self, _caller(2), interval)
                ) from None
        if strict and \
           self.namespace is not _NULL_NAME and \
           self.namespace != node.interval.namespace:
            raise ValueError(
                _BAD_METHOD_NAMESPACE(_caller(2), self, node.interval)
            )
        return node


    def _set_node(self, index, node):
        """PRIVATE

        Set a _Node object containing user data at the given index
        """
        raise NotImplementedError(_NO_METHOD(self,'_set_node'))


    def hull(self, other=None):
        """
        self.hull() -> Interval
        self.hull(other) -> Interval

        Returns the smallest interval closure of self (and, optionally,
        other).
        """
        this = LeftClosedInterval(
            namespace=self.namespace,
            beg=self.beg,
            end=self.end
        )
        if this.isempty():
            this.clear()
        if other:
            if other.isempty():
                other = LeftClosedInterval()
            if this.namespace == other.namespace:
                this.beg = min(this.beg, other.beg)
                this.end = max(this.end, other.end)
        return this



class IntervalList(BaseIntervalCollection, _deque):
    """
    A list of BaseInterval-descendant objects, sorted by start position.

    IntervalList inherits from `collections.deque()` but requires all
    BaseBaseInterval-descendant object members to be of the same namespace,
    or a ValueError is raised. 
    
    For many functions to work as expected, the user is required to
    maintain IntervalList members in sorted order (which is not 
    enforced by the class) or risk incorrect behavior. As such, the 
    user is recommended to use the `insort()` and `insortleft()` 
    methods to insert new members into the IntervalList in proper
    order. The `update()` and `updateleft()` methods are provided to
    insert multiple members at once. Methods such as `append()`,
    `appendleft()`, `extend()`, and `extendleft()` are provided for
    convenience and API consistency with `collections.deque()`, but
    the user is responsible for ensuring sort order is maintained
    when using these methods. Unlike the `deque()` class,however, 
    an in-place `list()`-like `sort()` method is provided.

    Use the `find_index()` method to find the index of a member equal
    to a given interval.

    Use `find_index_beg()` and `find_index_end()` methods to find
    the indices of the first and last members that intersect a given
    interval, respectively, or the indices between existing members
    when no intersection is found. 

    `find_intersection_index_beg()` and `find_intersection_index_end()` 
    methods are intended to find the indices of the first and last 
    members intersecting a given interval, respectively, or return 
    -1 when no intersection is found.
    
    Use `find_insertion_index_beg()` and `find_insertion_index_end()`
    methods to find the indices where new members should be inserted
    that will maintain sort order.

    All `find_*()` methods return -1 when the given interval is not
    of the same namespace as existing members of the IntervalList.

    The `lower` and `upper` keyword parameters can be used to restrict
    the search space when the lower and upper bounds are known.

    The `setter` keyword parameter accepts a callable used to extract
    or construct from a method's input object a BaseInterval-descendant
    class instance for querying or storing the IntervalList. This is
    useful when the input is not of the same object class as the
    members of IntervalList. The callable must accept one (and only 
    one) argument and outputs a single BaseInterval-descendant object.
    """
    def __init__(self, intervals=[], setter=None):
        BaseIntervalCollection.__init__(self, setter or remit)
        _deque.__init__(self)
        if intervals:
            self.extend(sorted(map(self._set, intervals), key=_node_pos))


    def _get_node(self, index):
        return _deque.__getitem__(self, index)


    def _iter_nodes(self):
        return _deque.__iter__(self)


    def _set_node(self, index, node):
        return _deque.__setitem__(self, index, node)


    def _reset_node_max(self, node):
        node.max = node.interval.end
        return node
    

    def _update_node_max(self, index, stop):
        prev = None
        if index != 0 and index > -len(self):
            prev = self._get_node(index - 1)
            stop = max(stop, prev.max)
        while index < len(self) and \
              self._get_node(index).interval.end <= stop:
            curr = self._get_node(index)
            if prev and curr.interval.end < prev.max:
                curr.max = prev.max
            else:
                curr.max = curr.interval.end
            prev = curr
            index += 1

    
    def __add__(self, intervals, setter=None):
        """
        self + intervals -> IntervalList

        Return a new IntervalList containing the elements of self and
        the elements of intervals.
        """
        copy = self.__copy__()
        copy.__iadd__(intervals, setter=setter)
        return copy

    
    def __bool__(self):
        """
        bool(self) -> bool

        Test if an IntervalList is non-empty.
        """
        return bool(len(self))

    
    def __contains__(self, interval, setter=None):
        """
        interval in self -> bool
        self.__contains__(interval) -> bool

        Check if an interval is in the IntervalList.
        """
        return not (self.find_index(interval, setter=setter) < 0)

    
    def __copy__(self):
        """
        self.copy() -> IntervalList
        self.__copy__() -> IntervalList

        Create a shallow copy of the IntervalList.
        """
        copy = self.__class__(setter=self._setter)
        copy.__iadd__(self._copy_nodes(), setter=remit)
        return copy

    
    def __delitem__(self, index):
        """
        del(self[index]) -> None
        self.__delitem__(index) -> None

        Delete the interval at the given index.
        """
        node = self._get_node(index)
        _deque.__delitem__(self, index)
        self._update_node_max(index, node.max)


    def __getitem__(self, index):
        """
        self[index] -> interval
        self.__getitem__(index) -> interval

        Return the interval at the given index.
        """
        return self._get(_deque.__getitem__(self, index))


    def __iadd__(self, intervals, setter=None):
        """
        self += intervals
        self.__iadd__(intervals)

        Extend the IntervalList in-place with the elements of intervals.
        """
        prev = self._get_node(-1) if self else None
        for interval in _iter(intervals):
            node = self._set(interval, setter)
            if prev and node.interval.end < prev.max:
                node.max = prev.max
            _deque.append(self, node)
            prev = node
        return self

    
    def __imul__(self, value):
        """
        self *= value
        self.__imul__(value)

        Extend the IntervalList in-place with the elements of self
        repeated value times.
        """
        setter = self._setter
        self.__init__(list(self.iter_nodes()) * value, setter=remit)
        self._setter = setter
        return self

    
    def __iter__(self):
        """
        iter(self) -> generator
        self.__iter__() -> generator

        Return a generator object for iterating over the intervals in
        the IntervalList.
        """
        return map(self._get, self._iter_nodes())

    
    def __len__(self):
        """
        len(self) -> int
        self.__len__() -> int

        Return the number of intervals in the IntervalList.
        """
        return _deque.__len__(self)


    def __mul__(self, value):
        """
        self * value -> IntervalList
        self.__mul__(value) -> IntervalList

        Return a new IntervalList containing the elements of self
        repeated value times.
        """
        copy = self.__class__(list(self.iter_nodes()) * value, setter=remit)
        copy._setter = self._setter
        return copy

    
    def __reversed__(self):
        """
        reversed(self) -> generator
        self.__reversed__() -> generator

        Return a generator object for iterating over the intervals in
        the IntervalList in reverse order.
        """
        return (self[~i] for i in range(len(self)))


    def __rmul__(self, value):
        """
        value * self -> IntervalList
        self.__rmul__(value) -> IntervalList

        Return a new IntervalList containing the elements of self
        repeated value times.
        """
        return self.__mul__(value)
    
    
    def __setitem__(self, index, interval, setter=None):
        """
        self[index] = interval
        self.__setitem__(index, interval)

        Set the interval at the given index.
        """
        node = self._set(interval, setter)
        stop = max(self._get_node(index).max, node.max)
        _deque.__setitem__(self, index, node)
        self._update_node_max(index, stop)


    @property
    def namespace(self):
        """
        self.namespace -> value

        Read only. Return the namespace of the IntervalList. Returns 
        None if null.
        """
        return _NULL_NAME \
            if   self.isnull() \
            else self._get_node(0).interval.namespace


    @property
    def beg(self):
        """
        self.beg -> value

        Read only. Return self's start numeric value (0-based).

        >>> ilist = IntervalList([Interval("Chr", 350, 475)])
        >>> print(ilist.beg)
        350
        """
        return _NULL_POS \
            if   self.isnull() \
            else self._get_node(0).interval.beg


    @property
    def start(self):
        """
        self.start -> value

        Read only. Alias for the `beg` attribute.
        
        >>> ilist = IntervalList([Interval("Chr", 350, 475)])
        >>> print(ilist.start)
        350
        """
        return self.beg


    @property
    def mid(self):
        """
        self.mid -> value

        Read only. Return self's midpoint value.

        >>> ilist = IntervalList([Interval("Chr", 350, 475)])
        >>> print(ilist.mid)
        412.5
        """
        return self.beg + (self.end - self.beg) / 2.0
    

    @property
    def end(self):
        """
        self.end -> value

        Read only. Return self's end value (1-based).

        >>> ilist = IntervalList([Interval("Chr", 350, 475)])
        >>> print(ilist.end)
        475
        """
        return _NULL_POS \
            if   self.isnull() \
            else self._get_node(-1).interval.end


    @property
    def stop(self):
        """
        self.stop -> value

        Read only. Alias for the `end` attribute.

        >>> ilist = IntervalList([Interval("Chr", 350, 475)])
        >>> print(ilist.stop)
        475
        """
        return self.end


    def isnull(self):
        """
        self.isnull() -> bool

        Check if the IntervalList is null.

        >>> ilist = IntervalList()
        >>> ilist.isnull()
        True
        """
        # intervals containing nan values are sorted to the end of the list, 
        # so check the last interval for nullity:
        return len(self) < 1 or self._get_node(-1).interval.isnull()

    
    def append(self, interval, setter=None):
        """
        self.append(interval) -> None
        self.append(interval, setter=callable) -> None
        
        Append interval to the right side of IntervalList.

        The `setter` keyword argument accepts a callable used to
        extract/construct from the input object a BaseInterval-descendant
        class instance for setting the IntervalList. This is useful
        when the input is not of the same object class as the members
        of IntervalList. The callable must accept one (and only one)
        argument and outputs a single BaseInterval-descendant object.

        >>> ilist = IntervalList([Interval("Chr", 50, 300)])
        >>> ilist.append(Interval("Chr", 350, 475))
        >>> print(ilist)
        [Chr:50-300, Chr:350-475]
        """
        node = self._set(interval, setter)
        index = len(self)
        _deque.append(self, node)
        self._update_node_max(index, node.max)


    def appendleft(self, interval, setter=None):
        """
        self.appendleft(interval) -> None
        self.appendleft(interval, setter=callable) -> None

        Append interval to the left side of IntervalList.

        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for setting the IntervalList. This is useful
        when the input is not of the same object class as the members
        of IntervalList. The callable must accept one (and only one)
        argument and outputs a single BaseInterval-descendant object.

        >>> ilist = IntervalList([Interval("Chr", 350, 475)])
        >>> ilist.appendleft(Interval("Chr", 50, 300))
        >>> print(ilist)
        [Chr:50-300, Chr:350-475]
        """
        node = self._set(interval, setter)
        _deque.appendleft(self, node)
        self._update_node_max(0, node.max)


    def clear(self):
        """
        self.clear() -> None

        Clear all elements from the IntervalList.
        """
        _deque.clear(self)

        
    def copy(self):
        """
        self.copy() -> IntervalList
        self.__copy__() -> IntervalList

        Create a shallow copy of the IntervalList.
        """
        return self.__copy__()
        

    def count(self, interval, setter=None):
        """
        self.count(interval) -> int
        self.count(interval, setter=callable) -> int

        Count the number of elements equal to interval.

        Requires the objects in the IntervalList to have an __eq__()
        method defined or the objects cannot be compared.
        
        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for querying the IntervalList. This is useful
        when the input is not of the same object class as the members
        of IntervalList. The callable must accept one (and only one)
        argument and outputs a single BaseInterval-descendant object.

        >>> ilist = IntervalList([
        ...     Interval("Chr", 50, 300),
        ...     Interval("Chr", 50, 300),
        ...     Interval("Chr", 50, 300),
        ...     Interval("Chr", 50, 300),
        ...     Interval("Chr", 350, 475)
        ... ])
        >>> ilist.count(Interval("Chr", 50, 300))
        4
        """
        return _deque.count(self, self._set(interval, setter))
        

    def extend(self, intervals, setter=None):
        """
        self.extend(intervals) -> None
        self.extend(intervals, setter=callable) -> None
        
        Extend the right side of the IntervalList with elements from
        the iterable.

        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for setting the IntervalList. This is useful
        when the inputs are not of the same object class as the members
        of IntervalList. The callable must accept one (and only one)
        argument and outputs a single BaseInterval-descendant object.

        >>> ilist = IntervalList()
        >>> ilist.extend([Interval("Chr", 50, 300), Interval("Chr", 350, 475)])
        >>> print(ilist)
        [Chr:50-300, Chr:350-475]
        """
        self.__iadd__(intervals, setter=setter)
            

    def extendleft(self, intervals, setter=None):
        """
        self.extendleft(intervals) -> None
        self.extendleft(intervals, setter=callable) -> None

        Extend the left side of the IntervalList with elements from 
        the iterable.

        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for setting the IntervalList. This is useful
        when the inputs are not of the same object class as the members
        of IntervalList. The callable must accept one (and only one)
        argument and outputs a single BaseInterval-descendant object.

        >>> ilist = IntervalList()
        >>> ilist.extendleft([Interval("Chr", 350, 475), Interval("Chr", 50, 300)])
        >>> print(ilist)
        [Chr:50-300, Chr:350-475]
        """
        intervals = _iter(intervals)
        _deque.extendleft(self, map(lambda i: self._set(i, setter), intervals))

        index = 0
        length = len(intervals)
        while index <= length and index < len(self):
            node = self._get_node(index)
            if index and node.interval.end < self._get_node(index - 1).max:
                node.max = self._get_node(index - 1).max
                if index == length:
                    length += 1
            index += 1
    
            
    def index(self, interval, setter=None, lower=0, upper=-1, start=None, stop=None):
        """
        self.index(interval) -> int
        self.index(interval, setter=callable) -> int
        self.index(interval, start=int, stop=int) -> int
        self.index(interval, lower=int, upper=int) -> int

        Return the first index of interval. 
        
        Raises ValueError if the interval is not present.
        
        The `lower` and `upper` keywords can be used to restrict the
        search space when the lower and upper bounds are known. The
        equivalent `start` and `stop` keywords are provided for backward
        compatibility.

        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for querying the IntervalList. This is useful
        when the input is not of the same object class as the members
        of IntervalList. The callable must accept one (and only one)
        argument and outputs a single BaseInterval-descendant object.

        >>> ilist = IntervalList([Interval("Chr", 50, 300), Interval("Chr", 350, 475)])
        >>> ilist.index(Interval("Chr", 350, 475))
        1
        """
        lower = lower if start is None else start
        upper = upper if stop is None else stop
        index = \
            self.find_index(
                interval,
                setter=setter,
                lower=lower, 
                upper=upper
            )
        if 0 <= index < len(self):
            return index
        else:
            raise ValueError(_NOT_IN(self, repr(interval)))

        
    def insert(self, index, interval, setter=None):
        """
        self.insert(index, interval) -> None
        self.insert(index, interval, setter=callable) -> None

        Insert interval before index

        The `lower` and `upper` keywords can be used to restrict the
        search space when the lower and upper bounds are known.

        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for setting the IntervalList. This is useful
        when the input is not of the same object class as the members
        of IntervalList. The callable must accept one (and only one)
        argument and outputs a single BaseInterval-descendant object.

        >>> ilist = IntervalList([Interval("Chr", 50, 300), Interval("Chr", 350, 475)])
        >>> ilist.insert(1, Interval("Chr", 300, 350))
        >>> print(ilist)
        [Chr:50-300, Chr:300-350, Chr:350-475]
        """
        node = self._set(interval, setter)
        _deque.insert(self, index, node)
        self._update_node_max(index, node.max)

        
    def insort(self, interval, setter=None, lower=0, upper=-1):
        """
        self.insort(interval) -> int
        self.insort(interval, setter=callable) -> int
        self.insort(interval, lower=int, upper=int) -> int

        Insert an interval into its sorted position, with identical
        intervals inserted to the right of existing ones.

        The `lower` and `upper` keywords can be used to restrict the
        search space when the lower and upper bounds are known.

        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for setting the IntervalList. This is useful
        when the input is not of the same object class as the members
        of IntervalList. The callable must accept one (and only one)
        argument and outputs a single BaseInterval-descendant object.

        >>> ilist = IntervalList([Interval("Chr", 50, 300), Interval("Chr", 350, 475)])
        >>> ilist.insort(Interval("Chr", 300, 350))
        >>> print(ilist)
        [Chr:50-300, Chr:300-350, Chr:350-475]
        """
        index = \
            self.find_insertion_index_end(
                interval,
                setter=setter,
                lower=lower,
                upper=upper
            )
        self.insert(index, interval, setter)
        return index
        

    def insortleft(self, interval, setter=None, lower=0, upper=-1):
        """
        self.insortleft(interval) -> int
        self.insortleft(interval, setter=callable) -> int
        self.insortleft(interval, lower=int, upper=int) -> int

        Insert an interval into its sorted position, with identical
        intervals inserted to the left of existing ones.

        The `lower` and `upper` keywords can be used to restrict the
        search space when the lower and upper bounds are known.

        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for setting the IntervalList. This is useful
        when the input is not of the same object class as the members
        of IntervalList. The callable must accept one (and only one)
        argument and outputs a single BaseInterval-descendant object.

        >>> ilist = IntervalList([Interval("Chr", 50, 300), Interval("Chr", 350, 475)])
        >>> ilist.insortleft(Interval("Chr", 300, 350))
        >>> print(ilist)
        [Chr:50-300, Chr:300-350, Chr:350-475]
        """
        index = \
            self.find_insertion_index_beg(
                interval,
                setter=setter,
                lower=lower,
                upper=upper
            )
        self.insert(index, interval, setter)
        return index
    

    def update(self, intervals, setter=None):
        """
        self.update(intervals) -> None
        self.update(intervals, setter=callable) -> None
        
        `insort()` a collection of intervals
        
        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for setting the IntervalList. This is useful
        when the inputs are not of the same object class as the members
        of IntervalList. The callable must accept one (and only one)
        argument and outputs a single BaseInterval-descendant object.

        >>> ilist = IntervalList([Interval("Chr", 50, 300)])
        >>> ilist.update([Interval("Chr", 350, 475), Interval("Chr", 300, 350)])
        >>> print(ilist)
        [Chr:50-300, Chr:300-350, Chr:350-475]
        """
        nodes = map(lambda i: self._set(i, setter), intervals)
        for node in sorted(nodes, key=_node_pos):
            self.insort(node, setter=setter)


    def updateleft(self, intervals, setter=None):
        """
        self.updateleft(intervals) -> None
        self.updateleft(intervals, setter=callable) -> None

        `insortleft()` a collection of intervals

        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for setting the IntervalList. This is useful
        when the inputs are not of the same object class as the members
        of IntervalList. The callable must accept one (and only one)
        argument and outputs a single BaseInterval-descendant object.

        >>> ilist = IntervalList([Interval("Chr", 50, 300)])
        >>> ilist.updateleft([Interval("Chr", 350, 475), Interval("Chr", 300, 350)])
        >>> print(ilist)
        [Chr:50-300, Chr:300-350, Chr:350-475]
        """
        nodes = map(lambda i: self._set(i, setter), intervals)
        for node in sorted(nodes, key=_node_pos):
            self.insortleft(node, setter=setter)
        

    def pop(self):
        """
        self.pop() -> interval

        Pop one item off the right side of IntervalList and return it.

        >>> ilist = IntervalList([Interval("Chr", 50, 300), Interval("Chr", 350, 475)])
        >>> interval = ilist.pop()
        >>> print(interval)
        Chr:350-475
        >>> print(ilist)
        [Chr:50-300]
        """
        return self._get(_deque.pop(self))


    def popleft(self):
        """
        self.popleft() -> interval

        Pop one item off the left side of IntervalList and return it.

        >>> ilist = IntervalList([Interval("Chr", 50, 300), Interval("Chr", 350, 475)])
        >>> interval = ilist.popleft()
        >>> print(interval)
        Chr:50-300
        >>> print(ilist)
        [Chr:350-475]
        """
        node = _deque.popleft(self)
        self._update_node_max(0, node.max)
        return self._get(node)
    

    def remove(self, interval, setter=None):
        """
        self.remove(interval) -> int
        self.remove(interval, setter=callable) -> int

        Remove an interval from the IntervalList. Returns the index of
        the removed interval.

        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for querying the IntervalList. This is useful
        when the input is not of the same object class as the members
        of IntervalList. The callable must accept one (and only one)
        argument and outputs a single BaseInterval-descendant object.

        >>> ilist = IntervalList([Interval("Chr", 50, 300), Interval("Chr",280,400), Interval("Chr", 350, 475)])
        >>> index = ilist.remove(Interval("Chr",280,400))
        >>> print(index)
        1
        >>> print(ilist)
        [Chr:50-300, Chr:350-475]
        """
        index = self.find_index(interval, setter=setter)
        if 0 <= index < len(self):
            self.__delitem__(index)
        else:
            raise ValueError(_NOT_IN(self, repr(interval)))
        return index


    def sort(self, key=None, reverse=False):
        """
        self.sort() -> None

        Sort the IntervalList in place. The `key` and `reverse` 
        arguments are provided for compatibility with the built-in
        `list.sort()` method, but are ignored; the IntervalList is
        always sorted by start position.

        >>> ilist = IntervalList()
        >>> ilist.extend([Interval("Chr", 350, 475), Interval("Chr", 50, 300)])
        >>> print(ilist)
        [Chr:350-475, Chr:50-300]
        >>> ilist.sort()
        >>> print(ilist)
        [Chr:50-300, Chr:350-475]
        """
        nodes = sorted(self._iter_nodes())
        self.clear()
        self.extend(map(self._reset_node_max, nodes), setter=remit)

        
    def find_index_beg(self, interval, setter=None, lower=0, upper=-1):
        """
        self.find_index_beg(interval) -> int
        self.find_index_beg(interval, setter=callable) -> int
        self.find_index_beg(interval, lower=int, upper=int) -> int
        
        Return the start/left-most (inclusive) index for the input
        interval. IntervalList members may not necessarily intersect 
        the input interval object. When the input interval overlaps
        an existing member, the index of the left-most intersecting 
        member is returned. If no members intersect the input interval,
        the equivalent of the insertion index is returned.

        The `lower` and `upper` keywords can be used to restrict the
        search space when the lower and upper bounds are known.

        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for querying the IntervalList. This is useful
        when the input is not of the same object class as the members
        of IntervalList. The callable must accept one (and only one)
        argument and outputs a single BaseInterval-descendant object.

        >>> ilist = IntervalList([Interval("Chr", 50, 300), Interval("Chr", 350, 475)])
        >>> index = ilist.find_index_beg(Interval("Chr", 280,400))
        >>> print(index)
        0
        """
        if not (0 <= lower < len(self)):
            lower = 0
        if not (0 <= upper < len(self)):
            upper = len(self)

        node = self._set(interval, setter, False)
        if self.namespace is not _NULL_NAME and \
           self.namespace != node.interval.namespace:
            return -1
        while lower < upper:
            middle = lower + (upper - lower) // 2
            if self._get_node(middle).max <= node.interval.beg:
                lower = middle + 1
            else:
                upper = middle
        return lower

    
    def find_index_end(self, interval, setter=None, lower=0, upper=-1):
        """
        self.find_index_end(interval) -> int
        self.find_index_end(interval, setter=callable) -> int
        self.find_index_end(interval, lower=int, upper=int) -> int

        Return the end/right-most (exclusive) index for the input 
        interval (i.e., the index of the first non-intersecting 
        member to the right of the input interval). IntervalList 
        members may not necessarily intersect the input interval 
        object. When the input interval intersects an existing member,
        the index after the right-most intersecting member is returned.
        If no members intersect the input interval, the equivalent of
        the insertion index is returned. 

        The `lower` and `upper` keywords can be used to restrict the
        search space when the lower and upper bounds are known.

        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for querying the IntervalList. This is useful
        when the input is not of the same object class as the members
        of IntervalList. The callable must accept one (and only one)
        argument and outputs a single BaseInterval-descendant object.

        >>> ilist = IntervalList([Interval("Chr", 50, 300), Interval("Chr", 350, 475)])
        >>> index = ilist.find_index_end(Interval("Chr", 280,400))
        >>> print(index)
        2
        """
        if not (0 <= lower < len(self)):
            lower = 0
        if not (0 <= upper < len(self)):
            upper = len(self)

        node = self._set(interval, setter, False)
        if self.namespace is not _NULL_NAME and \
           self.namespace != node.interval.namespace:
            return -1
        if self._get_node(len(self) - 1).interval.beg < node.interval.end:
            return len(self)  # - 1  # <=[makes inclusive]
        while lower < upper:
            middle = lower + (upper - lower) // 2
            if node.interval.end <= self._get_node(middle).interval.beg:
                upper = middle
            else:
                lower = middle + 1
        return lower  # - 1  # <=[makes inclusive]


    def find_index(self, interval, setter=None, lower=0, upper=-1):
        """
        self.find_index(interval) -> int
        self.find_index(interval, setter=callable) -> int
        self.find_index(interval, lower=int, upper=int) -> int

        Return the left-most index for equivalent intervals to the
        input interval, or -1 if none. Requires the objects in the 
        IntervalList to have an __eq__() method defined or the 
        objects cannot be compared.

        The `lower` and `upper` keywords can be used to restrict the
        search space when the lower and upper bounds are known.

        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for querying the IntervalList. This is useful
        when the input is not of the same object class as the members
        of IntervalList. The callable must accept one (and only one)
        argument and outputs a single BaseInterval-descendant object.

        >>> ilist = IntervalList([Interval("Chr", 50, 300), Interval("Chr", 350, 475)])
        >>> index = ilist.find_index(Interval("Chr", 350, 475))
        >>> print(index)
        1
        """
        if not (0 <= lower < len(self)):
            lower = 0
        if not (0 <= upper < len(self)):
            upper = len(self)

        node = self._set(interval, setter, False)
        index = \
            self.find_insertion_index_beg(
                node,
                setter=remit,
                lower=lower,
                upper=upper
            )
        while lower <= index < upper and \
            self._get_node(index).interval == node.interval:
            if self._get_node(index).instance == node.instance:
                return index
            index += 1
        return -1

    
    def find_index_nearest(self, interval, setter=None, lower=0, upper=-1):
        """
        self.find_index_nearest(interval) -> int
        self.find_index_nearest(interval, setter=callable) -> int
        self.find_index_nearest(interval, lower=int, upper=int) -> int

        Return the nearest (inclusive) index for the input interval. 
        IntervalList members may not necessarily intersect the input 
        Interval object. Returns the left-most index when members 
        are equidistant to the query interval.

        The `lower` and `upper` keywords can be used to restrict the
        search space when the lower and upper bounds are known.

        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for querying the IntervalList. This is useful
        when the input is not of the same object class as the members
        of IntervalList. The callable must accept one (and only one)
        argument and outputs a single BaseInterval-descendant object.

        >>> ilist = IntervalList([Interval("Chr", 50, 300), Interval("Chr", 350, 475)])
        >>> index = ilist.find_index_nearest(Interval("Chr", 301,302))
        >>> print(index)
        0 
        """
        if not (0 <= lower < len(self)):
            lower = 0
        if not (0 <= upper < len(self)):
            upper = len(self) - 1

        node = self._set(interval, setter, False)
        if self.namespace is not _NULL_NAME and \
           self.namespace != node.interval.namespace:
            return -1
        while lower < upper:
            middle = lower + (upper - lower) // 2
            if self._get_node(middle).interval < node.interval:
                lower = middle + 1
            else:
                upper = middle
                
        if 0 < lower < len(self):
            Il = self._get_node(lower-1).interval
            Iu = self._get_node(lower).interval
            l = node.interval.beg - Il.end
            u = Iu.beg - node.interval.end
            if l <= 0 and u <= 0:
                # both intersect
                l = -Il.intersection_length(node.interval)
                u = -Iu.intersection_length(node.interval)
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

    
    def find_insertion_index_beg(self, interval, setter=None, lower=0, upper=-1):
        """
        self.find_insertion_index_beg(interval) -> int
        self.find_insertion_index_beg(interval, setter=callable) -> int
        self.find_insertion_index_beg(interval, lower=int, upper=int) -> int

        Return the index at which to insert the input interval into 
        its sorted position, with identical intervals inserted to the 
        beginning/left of existing ones.

        The `lower` and `upper` keywords can be used to restrict the
        search space when the lower and upper bounds are known.

        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for setting the IntervalList. This is useful
        when the input is not of the same object class as the members
        of IntervalList. The callable must accept one (and only one)
        argument and outputs a single BaseInterval-descendant object.

        >>> ilist = IntervalList([Interval("Chr", 50, 300), Interval("Chr", 350, 475)])
        >>> index = ilist.find_insertion_index_beg(Interval("Chr", 280, 350))
        >>> print(index)
        1
        """
        if not (0 <= lower < len(self)):
            lower = 0
        if not (0 <= upper < len(self)):
            upper = len(self)

        node = self._set(interval, setter)
        if self.namespace is not _NULL_NAME and \
           self.namespace != node.interval.namespace:
            return -1
        while lower < upper:
            middle = lower + (upper - lower) // 2
            if self._get_node(middle).interval < node.interval:
                lower = middle + 1
            else:
                upper = middle
        return lower


    def find_insertion_index_end(self, interval, setter=None, lower=0, upper=-1):
        """
        self.find_insertion_index_end(interval) -> int
        self.find_insertion_index_end(interval, setter=callable) -> int
        self.find_insertion_index_end(interval, lower=int, upper=int) -> int

        Return the index at which to insert the input interval into 
        its sorted position, with identical intervals inserted to the 
        end/right of existing ones.

        The `lower` and `upper` keywords can be used to restrict the
        search space when the lower and upper bounds are known.

        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for setting the IntervalList. This is useful
        when the input is not of the same object class as the members
        of IntervalList. The callable must accept one (and only one)
        argument and outputs a single BaseInterval-descendant object.

        >>> ilist = IntervalList([Interval("Chr", 50, 300), Interval("Chr", 350, 475)])
        >>> index = ilist.find_insertion_index_end(Interval("Chr", 280, 350))
        >>> print(index)
        2
        """
        if not (0 <= lower < len(self)):
            lower = 0
        if not (0 <= upper < len(self)):
            upper = len(self)

        node = self._set(interval, setter)
        if self.namespace is not _NULL_NAME and \
           self.namespace != node.interval.namespace:
            return -1
        while lower < upper:
            middle = lower + (upper - lower) // 2
            if node.interval < self._get_node(middle).interval:
                upper = middle
            else:
                lower = middle + 1
        return lower
    

    def find_intersection_index_beg(self, interval, setter=None, lower=0, upper=-1):
        """
        self.find_intersection_index_beg(interval) -> int
        self.find_intersection_index_beg(interval, setter=callable) -> int
        self.find_intersection_index_beg(interval, lower=int, upper=int) -> int

        Return the (inclusive) index of the left-most intersecting
        IntervalList member, or -1 if none.

        The `lower` and `upper` keywords can be used to restrict the
        search space when the lower and upper bounds are known.

        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for querying the IntervalList. This is useful
        when the input is not of the same object class as the members
        of IntervalList. The callable must accept one (and only one)
        argument and outputs a single BaseInterval-descendant object.

        >>> ilist = IntervalList([Interval("Chr", 50, 300), Interval("Chr", 350, 475)])
        >>> index = ilist.find_intersection_index_beg(Interval("Chr", 280, 400))
        >>> print(index)
        0
        """
        if not (0 <= lower < len(self)):
            lower = 0
        if not (0 <= upper < len(self)):
            upper = len(self)

        node = self._set(interval, setter, False)
        index = \
            self.find_index_beg(
                node, 
                setter=remit, 
                lower=lower, 
                upper=upper
            )
        return index \
            if ((lower <= index < upper) and \
                (self._get_node(index).interval.isintersecting(node.interval))) \
            else -1


    def find_intersection_index_end(self, interval, setter=None, lower=0, upper=-1):
        """
        self.find_intersection_index_end(interval) -> int
        self.find_intersection_index_end(interval, setter=callable) -> int
        self.find_intersection_index_end(interval, lower=int, upper=int) -> int

        Return the (exclusive) index of the right-most intersecting
        IntervalList member (i.e., the index of the first non-intersecting 
        member to the right of the input interval), or -1 if none.

        The `lower` and `upper` keywords can be used to restrict the
        search space when the lower and upper bounds are known.

        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for querying the IntervalList. This is useful
        when the input is not of the same object class as the members
        of IntervalList. The callable must accept one (and only one)
        argument and outputs a single BaseInterval-descendant object.

        >>> ilist = IntervalList([Interval("Chr", 50, 300), Interval("Chr", 350, 475)])
        >>> index = ilist.find_intersection_index_end(Interval("Chr", 280, 400))
        >>> print(index)
        2
        """
        if not (0 <= lower < len(self)):
            lower = 0
        if not (0 <= upper < len(self)):
            upper = len(self)

        node = self._set(interval, setter, False)
        index = \
            self.find_index_end(
                node, 
                setter=remit, 
                lower=lower, 
                upper=upper
            )
        return index \
            if ((lower < index <= upper) and \
                (self._get_node(index - 1).interval.isintersecting(node.interval))) \
            else -1
    

    def find_intersection_index_nearest(self, interval, setter=None, lower=0, upper=-1):
        """
        self.find_intersection_index_nearest(interval) -> int
        self.find_intersection_index_nearest(interval, setter=callable) -> int
        self.find_intersection_index_nearest(interval, lower=int, upper=int) -> int

        Return the (inclusive) index of the nearest intersecting 
        IntervalList member, or -1 if none. Returns the left-most 
        index when members are equidistant to the query interval.

        The `lower` and `upper` keywords can be used to restrict the
        search space when the lower and upper bounds are known.

        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for querying the IntervalList. This is useful
        when the input is not of the same object class as the members
        of IntervalList. The callable must accept one (and only one)
        argument and outputs a single BaseInterval-descendant object.

        >>> ilist = IntervalList([Interval("Chr", 50, 350), Interval("Chr", 350, 475)])
        >>> index = ilist.find_intersection_index_nearest(Interval("Chr", 280, 351))
        >>> print(index)
        0
        """
        if not (0 <= lower < len(self)):
            lower = 0
        if not (0 <= upper < len(self)):
            upper = len(self)

        node = self._set(interval, setter, False)
        index = \
            self.find_index_nearest(
                node, 
                setter=remit,
                lower=lower, 
                upper=upper
            )
        return index \
            if ((lower <= index < upper) and \
                (self._get_node(index).interval.isintersecting(node.interval))) \
            else -1


    def find_intersection_index_range(self, intervals, setter=None, lower=0, upper=-1):
        """
        self.find_intersection_index_range(intervals) -> generator
        self.find_intersection_index_range(intervals, setter=callable) -> generator

        An homage to the `range()` callable. Perform an IntervalList 
        overlap search with one or more query interval objects and 
        return a generator object that produces a sequence of integer
        indices between the start (inclusive) and end (exclusive) of
        the overlap range. When an iterable of intervals is inputted,
        indices may not be contiguous. 

        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for querying the IntervalList. This is useful
        when the input is not of the same object class as the members
        of IntervalList. The callable must accept one (and only one)
        argument and outputs a single BaseInterval-descendant object.

        >>> ilist = IntervalList([Interval("Chr", 50, 300), Interval("Chr", 350, 475)])
        >>> indices = ilist.find_intersection_index_range(Interval("Chr", 280, 400))
        >>> print(list(indices))
        [0, 1]
        """
        if not (0 <= lower < len(self)):
            lower = 0
        if not (0 <= upper < len(self)):
            upper = len(self)            

        start = lower
        nodes = map(lambda i: self._set(i, setter, False), _iter(intervals))
        for node in _filter_nested(nodes, sort=_node_pos_nested):
            index = \
                self.find_index_beg(
                    node, 
                    setter=remit, 
                    lower=start, 
                    upper=upper
                )
            while ((lower <= index < upper) and \
                   (self._get_node(index).interval.beg < node.interval.end)):
                if self._get_node(index).interval.isintersecting(node.interval):
                    yield index
                index += 1
            start = index
        
            
    def find_intersection_index_slice(self, intervals, setter=None, lower=0, upper=-1):
        """
        self.find_intersection_index_slice(intervals) -> slice
        self.find_intersection_index_slice(intervals, setter=callable) -> slice

        Perform an IntervalList overlap search with one or more query
        interval objects and return a slice object containing the
        Pythonic range of intersecting items, or `slice(-1, -1)` if
        none.

        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for querying the IntervalList. This is useful
        when the input is not of the same object class as the members
        of IntervalList. The callable must accept one (and only one)
        argument and outputs a single BaseInterval-descendant object.

        >>> ilist = IntervalList([Interval("Chr", 50, 300), Interval("Chr", 350, 475)])
        >>> index_slice = ilist.find_intersection_index_slice(Interval("Chr", 280, 400))
        >>> print(index_slice)
        slice(0, 2, None)
        """
        if not intervals:
            return slice(-1, -1)
        if isiterable(intervals):
            interval = LeftClosedInterval(_POS_INF, _NEG_INF)
            for node in map(lambda i: self._set(i, setter, False), intervals):
                if interval.namespace is _NULL_NAME:
                    interval.namespace = node.interval.namespace
                if interval.namespace != node.interval.namespace:
                    raise ValueError(_BAD_METHOD_NAMESPACE(
                        _caller(1), interval, node.interval
                    ))
                if interval.beg > node.interval.beg:
                    interval.beg = node.interval.beg
                if interval.end < node.interval.end:
                    interval.end = node.interval.end
        else:
            interval = self._set(intervals, setter, False).interval
            
        lower = \
            self.find_intersection_index_beg(
                interval, 
                setter=remit, 
                lower=lower, 
                upper=upper
            )
        upper = \
            self.find_intersection_index_end(
                interval, 
                setter=remit, 
                lower=lower, 
                upper=upper
            )

        if lower < 0 or upper < lower:
            lower = -1
            upper = -1
        return slice(lower, upper)


    def find_intersecting_pairs(self, intervals, setter=None, lower=0, upper=-1):
        """
        self.find_intersecting_pairs(intervals) -> generator
        self.find_intersecting_pairs(intervals, setter=callable) -> generator

        Return a generator object producing 2-tuples for each input 
        interval and each intersecting IntervalList member.

        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for querying the IntervalList. This is useful
        when the input is not of the same object class as the members
        of IntervalList. The callable must accept one (and only one)
        argument and outputs a single BaseInterval-descendant object.

        >>> ilist = IntervalList([Interval("Chr", 20, 60), Interval("Chr", 80, 100)])
        >>> pairs = ilist.find_intersecting_pairs(Interval("Chr", 40, 90))
        >>> print(list(pairs))
        [(Chr:40-90, Chr:20-60), (Chr:40-90, Chr:80-100)]
        """
        if not (0 <= lower < len(self)):
            lower = 0
        if not (0 <= upper < len(self)):
            upper = len(self)

        start = lower
        nodes = map(lambda i: self._set(i, setter, False), _iter(intervals))
        nodes = sorted(nodes, key=_node_pos)
        for node in nodes:
            index = \
                self.find_intersection_index_beg(
                    node, 
                    setter=remit, 
                    lower=start, 
                    upper=upper
                )
            while ((lower <= index < upper) and
                   (self._get_node(index).interval.isintersecting(node.interval))):
                yield (node.instance, self._get_node(index).instance)
                index += 1
            start = index - 1
        
    
    def find_intersecting(self, intervals, setter=None, lower=0, upper=-1):
        """
        self.find_intersecting(intervals) -> generator
        self.find_intersecting(intervals, setter=callable) -> generator

        Return a generator object producing IntervalList members 
        intersected by the input interval object(s).

        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for querying the IntervalList. This is useful
        when the input is not of the same object class as the members
        of IntervalList. The callable must accept one (and only one)
        argument and outputs a single BaseInterval-descendant object.

        >>> ilist = IntervalList([Interval("Chr", 20, 60), Interval("Chr", 80, 100)])
        >>> intersecting = ilist.find_intersecting(Interval("Chr", 40, 90))
        >>> print(list(intersecting))
        [Chr:20-60, Chr:80-100]
        """
        return map(
            self.__getitem__, 
            self.find_intersection_index_range(
                intervals, 
                setter=setter, 
                lower=lower, 
                upper=upper
            )
        )

    
    find_insertion_index_start = find_insertion_index_beg

    find_insertion_index_stop = find_insertion_index_end

    find_insertion_index = find_insertion_index_end
    
    find_intersection_index_start = find_intersection_index_beg

    find_intersection_index_stop = find_intersection_index_end

    find_index_start = find_index_beg

    find_index_stop = find_index_end

    isempty = isnull


    def intersection_length(self, intervals, setter=None):
        """
        self.intersection_length(other) -> int
        self.intersection_length(other, setter=callable) -> int

        Return the length of intersects the input interval or 
        IntervalList object has with the calling IntervalList object.

        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for querying the IntervalList. This is useful
        when the input is not of the same object class as the members
        of IntervalList. The callable must accept one (and only one)
        argument and outputs a single BaseInterval-descendant object.

        >>> ilist = IntervalList([Interval("Chr", 20, 60), Interval("Chr", 80, 100)])
        >>> ilist.intersection_length(Interval("Chr", 40, 70))
        20
        """
        nodes = map(lambda i: self._set(i, setter, False), _iter(intervals))

        upper = 0
        intersection_length = 0
        for node in _filter_nested(nodes, sort=_node_pos_nested):
            index = self.find_index_beg(node, lower=upper, setter=remit)
            while ((0 <= index < len(self)) and \
                   (self._get_node(index).interval.beg < node.interval.end)):
                intersection_length += self._get_node(index).interval.intersection_length(node.interval)
                index += 1
            upper = index
        return intersection_length

    
    def intersection_fraction(self, intervals, query=False, setter=None):
        """
        self.intersection_fraction(other) -> float
        self.intersection_fraction(other, query=bool) -> float
        self.intersection_fraction(other, query=bool, setter=callable) -> float

        Return the fraction of overlap the input interval or 
        IntervalList object has with the calling IntervalList object.

        The `query` keyword argument specifies whether to use the length
        of the input intervals as the numerator (True) or the calling 
        IntervalList as the numerator (False). The default is False.

        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for querying the IntervalList. This is useful
        when the input is not of the same object class as the members
        of IntervalList. The callable must accept one (and only one)
        argument and outputs a single BaseInterval-descendant object.

        >>> ilist = IntervalList([Interval("Chr", 20, 60), Interval("Chr", 80, 100)])
        >>> ilist.intersection_fraction(Interval("Chr", 40, 70))
        0.3333333333333333
        """
        nodes = map(lambda i: self._set(i, setter, False), _iter(intervals)) \
            if   query \
            else self._iter_nodes()
            
        numerator = self.intersection_length(intervals, setter=setter)
        denominator = sum(map(lambda n: len(n.interval), nodes))
        return numerator / float(max(1, denominator))


    
class _Sublist(BaseIntervalCollection, _deque):
    def __init__(self, nodes=None, index=-1, setter=remit):
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
            _repr(self, sep=padding_sep, indent=True)
        )


    def __iter__(self):
        return _deque.__iter__(self)

    
    def __len__(self):
        return _deque.__len__(self)

    
    def __str__(self):
        return _repr(self)


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
        Return the left-most start (inclusive) index for a query 
        interval. IntervalSet members may not necessarily overlap the
        query interval. Guarenteed to return an index 0:L, where L is
        the length. Returns -1 if the query is in the wrong namespace.

        The `lower` and `upper` keywords can be used to restrict the
        search space when the lower and upper bounds are known.

        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for querying the IntervalSet. This is useful 
        when the input is not of the same object class as the members
        of IntervalSet. The callable must accept one (and only one)
        argument and outputs a single BaseInterval-descendant object.
        """
        if self.length < 1 or \
           self[0].interval.namespace != node.interval.namespace:
            return -1            
        if not (0 <= lower < self.length):
            lower = 0
        if not (0 <= upper < self.length):
            upper = self.length
        while lower < upper:
            middle = lower + (upper - lower) // 2
            if self[middle].interval.end <= node.interval.beg:
                lower = middle + 1
            else:
                upper = middle
        return lower

    
    def find_index_end(self, node, lower=0, upper=-1):
        """
        Return the right-most end (exclusive) index for a query
        interval; i.e., the index of the first non-intersecting 
        IntervalSet member. Returns -1 if the query is in the wrong
        namespace.

        The `lower` and `upper` keywords can be used to restrict the
        search space when the lower and upper bounds are known.

        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for querying the IntervalSet. This is useful
        when the input is not of the same object class as the members
        of IntervalSet. The callable must accept one (and only one)
        argument and outputs a single BaseInterval-descendant object.
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
            middle = lower + (upper - lower) // 2
            if node.interval.end <= self[middle].interval.beg:
                upper = middle
            else:
                lower = middle + 1
        return lower  # - 1  # <=[makes inclusive]


    def find_index(self, node, lower=0, upper=-1):
        """
        Return the index for a query interval, or -1 if it doesn't 
        exist. Returns -1 if the query is in the wrong namespace.

        The `lower` and `upper` keywords can be used to restrict the
        search space when the lower and upper bounds are known.

        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for querying the IntervalSet. This is useful
        when the input is not of the same object class as the members
        of IntervalSet. The callable must accept one (and only one)
        argument and outputs a single BaseInterval-descendant object.
        """
        if self.length < 1 or \
           self[0].interval.namespace != node.interval.namespace:
            return -1
        if not (0 <= lower < self.length):
            lower = 0
        if not (0 <= upper < self.length):
            upper = self.length
        while lower < upper:
            middle = lower + (upper - lower) // 2
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

        The `lower` and `upper` keywords can be used to restrict the
        search space when the lower and upper bounds are known.

        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for querying the IntervalSet. This is useful
        when the input is not of the same object class as the members
        of IntervalSet. The callable must accept one (and only one)
        argument and outputs a single BaseInterval-descendant object.
        """
        if self.length < 1 or \
           self[0].interval.namespace != node.interval.namespace:
            return -1            
        if not (0 <= lower < self.length):
            lower = 0
        if not (0 <= upper < self.length):
            upper = self.length
        while lower < upper:
            middle = lower + (upper - lower) // 2
            if self[middle].interval < node.interval:
                lower = middle + 1
            else:
                upper = middle
        if 0 < lower and upper < self.length:
            l = ((abs(self[lower-1].interval.inner_distance(node.interval))) or
                 (-self[lower-1].interval.intersection_length(node.interval)))
            u = ((abs(self[lower].interval.inner_distance(node.interval))) or
                 (-self[lower].interval.intersection_length(node.interval)))
            lower = lower if u < l else lower-1
        return lower
    

    def find_intersection_index_beg(self, node, lower=0, upper=-1):
        """
        Return the start (inclusive) index of the left-most 
        intersecting IntervalSet member, or -1 if none or if the query
        is in the wrong namespace.

        The `lower` and `upper` keywords can be used to restrict the
        search space when the lower and upper bounds are known.

        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for querying the IntervalSet. This is useful 
        when the input is not of the same object class as the members
        of IntervalSet. The callable must accept one (and only one)
        argument and outputs a single BaseInterval-descendant object.
        """
        index = self.find_index_beg(node, lower, upper)
        return index \
            if 0 <= index < self.length and \
               self[index].interval.isintersecting(node.interval) \
            else -1


    def find_intersection_index_end(self, node, lower=0, upper=-1):
        """
        Return the end (exclusive) index of the right-most 
        intersecting IntervalSet member, or -1 if none or if the query
        is in the wronge namespace.

        The `lower` and `upper` keywords can be used to restrict the
        search space when the lower and upper bounds are known.

        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for querying the IntervalSet. This is useful
        when the input is not of the same object class as the members
        of IntervalSet. The callable must accept one (and only one)
        argument and outputs a single BaseInterval-descendant object.
        """
        index = self.find_index_end(node, lower, upper)
        return index \
            if 0 < index <= self._toplist.length and \
               self[index-1].interval.isintersecting(node.interval) \
            else -1
    

    def find_intersection_index_nearest(self, node, lower=0, upper=-1):
        """
        Return the (inclusive) index of the nearest intersecting 
        IntervalSet member, or -1 if none or if the query is in the
        wrong namespace.

        The `lower` and `upper` keywords can be used to restrict the
        search space when the lower and upper bounds are known.

        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for querying the IntervalSet. This is useful
        when the input is not of the same object class as the members
        of IntervalSet. The callable must accept one (and only one)
        argument and outputs a single BaseInterval-descendant object.
        """
        index = self.find_index_nearest(node, lower, upper)
        return index \
            if 0 <= index < self._toplist.length and \
               self[index].interval.isintersecting(node.interval) \
            else -1
 

    def find_intersection_index_range(self, nodes):
        """
        An homage to the `range()` callable. Perform an IntervalSet
        header overlap search with one or more query interval objects
        and return a generator object that produces a sequence of 
        integer indices between the start (inclusive) and end 
        (exclusive) of the overlap range. When an iterable of intervals
        is inputted, indices may not be contiguous. 

        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for querying the IntervalSet. This is useful
        when the input is not of the same object class as the members
        of IntervalSet. The callable must accept one (and only one)
        argument and outputs a single BaseInterval-descendant object.
        """
        upper = 0
        for node in _filter_nested(_iter(nodes), sort=_node_pos_nested):
            index = self.find_index_beg(node, lower=upper)
            while 0 <= index < self.length and \
                  node.interval.isintersecting(self[index].interval):
                yield index
                index += 1
            upper = index


    def find_intersection_index_bounds(self, nodes):
        """
        Perform an IntervalSet header overlap search with one or more
        query interval objects and return a 2-tuple containing the
        Pythonic range of intersecting items, or `(-1, -1)` if none.

        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for querying the IntervalSet. This is useful
        when the input is not of the same object class as the members
        of IntervalSet. The callable must accept one (and only one)
        argument and outputs a single BaseInterval-descendant object.
        """
        lower = -1
        upper = -1
        for node in _filter_nested(_iter(nodes), sort=_node_pos_nested):
            index = self.find_index_beg(node, lower=upper)
            while 0 <= index < self.length and \
                  node.interval.isintersecting(self[index].interval):
                if lower < 0:
                    lower = index
                index += 1
                upper = index
        return lower, upper


    def find_subinterval_index_beg(self, node, lower=0, upper=-1):
        """
        Return the right-most start (inclusive) index for a query
        interval; i.e., the index of the first non-intersecting 
        IntervalSet member. Returns `-1` if the query is in the wrong
        namespace.

        The `lower` and `upper` keywords can be used to restrict the
        search space when the lower and upper bounds are known.

        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for querying the IntervalSet. This is useful
        when the input is not of the same object class as the members
        of IntervalSet. The callable must accept one (and only one)
        argument and outputs a single BaseInterval-descendant object.
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
            middle = lower + (upper - lower) // 2
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

        The `lower` and `upper` keywords can be used to restrict the
        search space when the lower and upper bounds are known.

        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for querying the IntervalSet. This is useful
        when the input is not of the same object class as the members
        of IntervalSet. The callable must accept one (and only one)
        argument and outputs a single BaseInterval-descendant object.
        """
        if self.length < 1 or \
           self[0].interval.namespace != node.interval.namespace:
            return -1
        if not (0 <= lower < self.length):
            lower = 0
        if not (0 <= upper < self.length):
            upper = self.length
        while lower < upper:
            middle = lower + (upper - lower) // 2
            if self[middle].interval.end <= node.interval.end:
                lower = middle + 1
            else:
                upper = middle
        return lower

    
    
class IntervalSet(BaseIntervalCollection):
    """
    Implements and extends the Nested Containment List algorithm
    described in:
    
      Alekseyenko AV, Lee CJ. Nested Containment List (IntervalSet):
      a new algorithm for accelerating interval query of genome
      alignment and interval databases. Bioinformatics. 2007 
      23(11):1386-1393. doi: 10.1093/bioinformatics/btl647. 
      PMID: 17234640.

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

    Find intervals intersecting a query interval:

    >>> list(ncl.find_intersecting(Interval("Chr1", 75, 120)))
    [Interval(Chr1:0-150), Interval(Chr1:10-100)]

    """

    # Constructors
    # ============
    def __init__(self, intervals=[], setter=remit):
        """
        Multiple references to the same object(s) are silently ignored.

        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for querying the IntervalSet. This is useful
        when the input is not of the same object class as the members
        of IntervalSet. The callable must accept one (and only one)
        argument and outputs a single BaseInterval-descendant object.
        """
        BaseIntervalCollection.__init__(self, setter)
        self._set_ncls(map(self._set, intervals))  # calls clear()


    def _set_ncls(self, nodes):
        self.clear()

        # TODO: avoid sorting every time
        nodes = sorted(nodes, key=_node_pos_nested)  
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
            if nodes[i].interval.issubinterval(nodes[p].interval, strict=True):
                if hash(nodes[i]) in visited:
                    i += 1
                    d += 1
                    continue
                
                if nodes[i].interval.issubinterval(nodes[i-1].interval, strict=True):
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
        # intersects from the root (toplist) down (through sublists). This
        # method returns a generator object (via `yield`) that collects 
        # intersecting _Node objects, deferring to wrapper methods
        # that will decide what data to extract.
        toplists = self._toplist
        sublists = self._sublist

        nr = not pairwise
        visited  = set()
        for node in _iter(nodes):
            # Search toplist for top-level overlap; if no intersects,
            # then we are certain there are no sub-intervals with
            # intersects

            toplist = toplists
            toplist.index = toplist.find_intersection_index_beg(node)

            listdeque = _deque()
            listdeque.append(toplist)
            while listdeque:
                toplist = listdeque[0]
                if ((0 <= toplist.index < toplist.length) and
                    (node.interval.isintersecting(toplist[toplist.index].interval))):
                    # The interval intersects another, return result if 
                    # non-redundant (if we haven't seen its hash value)
                    if nr and hash(toplist[toplist.index].instance) in visited:
                        toplist.index += 1
                        continue
                    visited.add(hash(toplist[toplist.index].instance))
                    
                    yield get(node, toplist[toplist.index])

                    if 0 <= toplist[toplist.index].sublist < sublists.length:
                        sublist = sublists[toplist[toplist.index].sublist]
                        sublist.index = sublist.find_intersection_index_beg(node)
                        if 0 <= sublist.index < sublist.length:
                            listdeque.appendleft(sublist)
                    toplist.index += 1
                else:
                    # End of intersection with (sub)list
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
            _repr(self._toplist, sep=padding_hdr, indent=True),
            padding_sep,
            _repr(self._sublist, sep=padding_sub, indent=True)
        )        


    def __str__(self):
        return _repr(self)


    @property
    def namespace(self):
        return _NULL_NAME \
            if   self.isempty() \
            else self._toplist[0].interval.namespace
        
    
    @property
    def beg(self):
        return _NULL_POS \
            if   self.isempty() \
            else self._toplist[0].interval.beg

    @property
    def start(self):
        return self.beg
    

    @property
    def end(self):
        return _NULL_POS \
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
                    "BUG: Record %s" % repr(node.interval)
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
        object. If the interval is not a IntervalSet member, do 
        nothing.

        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for querying the IntervalSet. This is useful
        when the input is not of the same object class as the members
        of IntervalSet. The callable must accept one (and only one)
        argument and output a single BaseInterval-descendant object.
        """
        try:
            self.remove(interval, setter)
        except KeyError:
            pass
        
        
    def insort(self, interval, setter=None):
        """
        Add member object to IntervalSet in sorted position.

        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for querying the IntervalSet. This is useful
        when the input is not of the same object class as the members
        of IntervalSet. The callable must accept one (and only one)
        argument and output a single BaseInterval-descendant object.
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

        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for querying the IntervalSet. This is useful
        when the input is not of the same object class as the members
        of IntervalSet. The callable must accept one (and only one)
        argument and output a single BaseInterval-descendant object.
        """
        self._remove(self._set(interval, setter))

                
    def _remove(self, node):
        toplists = self._toplist
        sublists = self._sublist
        subslots = self._subslot
        toplist  = toplists
        toplist.index = toplist.find_intersection_index_beg(node)
        # .find_intersection_index_beg(node) not ideal, it would be
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
                    sublist.index = sublist.find_intersection_index_beg(node)
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

                    
    def intersection_length(self, intervals, setter=None):
        """
        Returns the length of intersection a query interval or 
        IntervalList object has with this IntervalSet object.

        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for querying the IntervalSet. This is useful
        when the input is not of the same object class as the members
        of IntervalSet. The callable must accept one (and only one)
        argument and outputs a single BaseInterval-descendant object.
        """
        raise NotImplementedError(_NO_METHOD(self,'intersection_length'))

    
    def intersection_fraction(self, intervals, setter=None):
        """
        Returns the fraction of intersection a query interval or 
        IntervalList object shares with this IntervalSet object. 
        Setting `query=True` calculates the overlap fraction with 
        respect to the query length.        

        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for querying the IntervalSet. This is useful
        when the input is not of the same object class as the members
        of IntervalSet. The callable must accept one (and only one)
        argument and outputs a single BaseInterval-descendant object.
        """
        raise NotImplementedError(_NO_METHOD(self,'intersection_fraction'))

    
    def intersecting_pairs(self, intervals, setter=None):
        """
        Preform an inclusive overlap search of IntervalSet with one
        or more query interval objects and return a generator object
        producing 2-tuples of each query interval and its intersecting
        IntervalSet member.

        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for querying the IntervalSet. This is useful
        when the input is not of the same object class as the members
        of IntervalSet. The callable must accept one (and only one)
        argument and outputs a single BaseInterval-descendant object.
        """
        nodes = sorted(
            map(lambda i: self._set(i, setter), _iter(intervals)),
            key=_node_pos
        )
        for i,o in self._find_nodes(nodes, True, remit):
            yield (i.instance, o.instance)
            
                    
    def find_intersecting(self, intervals, setter=None):
        """
        Perform an inclusive overlap search of IntervalSet with one
        or more query interval objects and return a generator object 
        producing IntervalSet members intersecting the input interval
        object(s).

        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for querying the IntervalSet. This is useful
        when the input is not of the same object class as the members
        of IntervalSet. The callable must accept one (and only one)
        argument and outputs a single BaseInterval-descendant object.
        """
        nodes = _filter_nested(
            map(lambda n: self._set(n, setter), _iter(intervals)),
            sort=_node_pos_nested
        )
        return (n.instance for n in self._find_nodes(nodes, False))
    
    
    def subintervals(self, intervals, setter=None):
        raise NotImplementedError(_NO_METHOD(self,'subintervals'))
        

    # Intersection set methods:
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
        raise NotImplementedError(_NO_METHOD(self,'__rsub__'))
    
    
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
            return self.__class__(_iter(other), setter or remit)

    
    def _isintersecting(self, other, setter=remit):
        if not isinstance(other, BaseIntervalCollection):
            return self._isintersecting(
                self.__class__(_iter(other), setter=setter)
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
                if 0 <= getter(lower).find_intersection_index_beg(setter(node)):
                    return True
        return False
    
    
    def isabutting(self, other):
        return Interval.isabutting(self, other)

    
    def isabutting_beg(self, other):
        return Interval.isabutting_beg(self, other)

    
    def isabutting_end(self, other):
        return Interval.isabutting_end(self, other)


    def isdisjoint(self, other):
        return not self.isintersecting(other)

    
    def isempty(self):
        return self._length < 1    

    
    def issuperinterval(self, other, strict=False, intersecting=True):
        """
        strict: require that other is a strict subinterval of self

        intersecting: require intervals in self overlap intervals in
        other
        """
        return (Interval.issuperinterval(self, other, strict) and
                ((not intersecting) or self._isintersecting(other)))

    
    def issubinterval(self, other, strict=False, intersecting=True):
        return (Interval.issubinterval(self, other, strict) and
                ((not intersecting) or self._isintersecting(other)))

    
    def isintersecting(self, other, intersecting=True):
        return (Interval.isintersecting(self, other) and
                ((not intersecting) or self._isintersecting(other)))

    
    def isintersecting_beg(self, other, intersecting=True):
        return (Interval.isintersecting_beg(self, other) and
                ((not intersecting) or self._isintersecting(other)))

    
    def isintersecting_end(self, other, intersecting=True):
        return (Interval.isintersecting_end(self, other) and
                ((not intersecting) or self._isintersecting(other)))

    
    def merge(self, abutting=False):
        """
        self.merge() -> IntervalSet

        Merge intersecting intervals and output a new IntervalSet of
        non-intersecting interval objects. Abutting intervals are not
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
        toplist.append(_Node(LeftClosedInterval(
            namespace=nodes[0].interval.namespace,
            beg=nodes[0].interval.beg,
            end=nodes[0].interval.end
        )))
        intersection = dist.__ge__ if abutting else dist.__gt__
        while i < N:
            if intersection(nodes[i].interval.beg - toplist[p].interval.end):
                # intersection between the two intervals, extend node p:
                toplist[p].interval.end = nodes[i].interval.end
            else:
                # no intersection, add new node p:
                toplist.append(_Node(LeftClosedInterval(
                    namespace=nodes[i].interval.namespace,
                    beg=nodes[i].interval.beg,
                    end=nodes[i].interval.end
                )))
                p += 1
            i += 1
        ncls._length = p + 1
        return ncls


    def merge_update(self, abutting=False):
        """
        self.merge_update() -> None

        Merge intersecting intervals and update self in-place. 
        Abutting intervals are not merged by default, but can be
        when `abutting=True`. Requires O(n) time in the average 
        case.
        
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
            toplist.append(_Node(LeftClosedInterval(
                namespace=self.namespace,
                beg=lower,
                end=self.beg
            )))
            ncls._length += 1
        for i in range(1, self._toplist.length):
            if gapped(nodes[i].interval.beg - nodes[i-1].interval.end):
                # gap between the two intervals, new record:
                toplist.append(_Node(LeftClosedInterval(
                    namespace=nodes[i].interval.namespace,
                    beg=nodes[i-1].interval.end,
                    end=nodes[i].interval.beg
                )))
                ncls._length += 1
        if self.end < upper:
            toplist.append(_Node(LeftClosedInterval(
                namespace=self.namespace,
                beg=self.end,
                end=upper
            )))
            ncls._length += 1
        return ncls


    def complement_update(self, lower=None, upper=None):
        """
        self.complement_update() -> None

        Computes the complement of the intervals contained in self and
        update self in-place. Requires O(n) time in the average case.
        
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
        When `pairwise=False`, only maximal intersection ranges with
        other are returned.

        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for querying the IntervalSet. This is useful
        when the input is not of the same object class as the members
        of IntervalSet. The callable must accept one (and only one)
        argument and output a single BaseInterval-descendant object.
        """
        raise NotImplementedError(_NO_METHOD(self,'difference'))

    
    def difference_update(self, other, pairwise=True, setter=None):
        """
        When `pairwise=False`, only maximal intersection ranges with
        other are returned.

        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for querying the IntervalSet. This is useful
        when the input is not of the same object class as the members
        of IntervalSet. The callable must accept one (and only one)
        argument and output a single BaseInterval-descendant object.
        """
        self._copy_state(self.difference(other, pairwise, setter))

    
    def intersection(self, other, pairwise=True, setter=None):
        """
        self.intersection(other) -> IntervalSet

        Computes all pairwise interval intersections between self and
        other. Requires O(m*log(n)) time in the worst case.

        When `pairwise=False`, only maximal intersection ranges with
        other are returned.

        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for querying the IntervalSet. This is useful
        when the input is not of the same object class as the members
        of IntervalSet. The callable must accept one (and only one)
        argument and output a single BaseInterval-descendant object.
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
            toplist.index = toplist.find_intersection_index_beg(node)

            listdeque = _deque()
            listdeque.append(toplist)
            while listdeque:
                toplist = listdeque[0]
                if ((0 <= toplist.index < toplist.length) and
                    (toplist[toplist.index].interval.beg < node.interval.end)):
                    # member node must intersection query node by search criterion
                    copy = LeftClosedInterval()
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
                    else:  # isintersecting_end of query
                        copy.beg = toplist[toplist.index].interval.beg
                        copy.end = node.interval.end
                    nodes.append(_Node(copy, (toplist[toplist.index].instance, node.instance)))
                    if 0 <= toplist[toplist.index].sublist < sublists.length:
                        sublist = sublists[toplist[toplist.index].sublist]
                        sublist.index = sublist.find_intersection_index_beg(node)
                        listdeque.appendleft(sublist)
                    toplist.index += 1
                else:
                    # no intersection
                    listdeque.popleft()
        ncls._set_ncls(nodes)
        return ncls
        
            
    def intersection_update(self, other, pairwise=True, setter=None):
        """
        self.intersection_update(other) -> None

        Computes all pairwise interval intersections between self and
        other, then updates self. Requires O(m*log(n)) time in the 
        worst case.

        When `pairwise=False`, only maximal intersection ranges with
        other are returned.

        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for querying the IntervalSet. This is useful
        when the input is not of the same object class as the members
        of IntervalSet. The callable must accept one (and only one)
        argument and output a single BaseInterval-descendant object.
        """        
        self._copy_state(self.intersection(other, pairwise, setter))

        
    def symmetric_difference(self, other, pairwise=True, setter=None):
        """
        When `pairwise=False`, only maximal union ranges with other
        are returned.

        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for querying the IntervalSet. This is useful
        when the input is not of the same object class as the members
        of IntervalSet. The callable must accept one (and only one)
        argument and output a single BaseInterval-descendant object.
        """
        raise NotImplementedError(_NO_METHOD(self,'symmetric_difference'))

    
    def symmetric_difference_update(self, other, pairwise=True, setter=None):
        """
        When `pairwise=False`, only maximal union ranges with other
        are returned.

        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for querying the IntervalSet. This is useful
        when the input is not of the same object class as the members
        of IntervalSet. The callable must accept one (and only one)
        argument and output a single BaseInterval-descendant object.
        """
        self._copy_state(self.symmetric_difference(other, pairwise, setter))


    def _scan(self, q, Wq, t, Wt, rev=False):
        i = 0
        L = len(Wt)
        Wo = _deque()
        intersections = []
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
            elif Wt[i].interval.isintersecting(q.interval):
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
    #     sentinel = _Node(Interval(self.namespace, _POS_INF, _NEG_INF))
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

        Setting `abutting=True` allows union of abutting intervals.
        When `pairwise=False`, only maximal union ranges with other
        are returned.

        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for querying the IntervalSet. This is useful
        when the input is not of the same object class as the members
        of IntervalSet. The callable must accept one (and only one)
        argument and output a single BaseInterval-descendant object.
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
        j = 0  # nodes2 current intersection index
        k = 0  # nodes2 first intersection index
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
                    # intersection
                    if ((i+1 < len1) and
                        upstream(nodes2[j].interval.end - nodes1[i+1].interval.beg)):
                        # peek at the next node1 to set k
                        k = j + 1
                    nodes.append(_Node(
                        LeftClosedInterval(
                            namespace=nodes1[i].interval.namespace,
                            beg=min(nodes1[i].interval.beg, nodes2[j].interval.beg),
                            end=max(nodes1[i].interval.end, nodes2[j].interval.end),
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
        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for querying the IntervalSet. This is useful
        when the input is not of the same object class as the members
        of IntervalSet. The callable must accept one (and only one)
        argument and outputs a single BaseInterval-descendant object.
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
        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for querying the IntervalSet. This is useful
        when the input is not of the same object class as the members
        of IntervalSet. The callable must accept one (and only one)
        argument and outputs a single BaseInterval-descendant object.
        """
        other = self._coerce_class(other, setter)
        ncls = self.__class__(setter=self._setter)
        ncls._set_ncls(
            set(self._copy_nodes()) - set(other._copy_nodes())
        )
        return ncls


    def difference_update_set(self, other):
        """
        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for querying the IntervalSet. This is useful
        when the input is not of the same object class as the members
        of IntervalSet. The callable must accept one (and only one)
        argument and outputs a single BaseInterval-descendant object.
        """
        self._copy_state(self.difference_set(other))
            

    def intersection_set(self, other, setter=None):
        """
        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for querying the IntervalSet. This is useful
        when the input is not of the same object class as the members
        of IntervalSet. The callable must accept one (and only one)
        argument and outputs a single BaseInterval-descendant object.
        """
        other = self._coerce_class(other, setter)
        ncls = self.__class__(setter=self._setter)
        ncls._set_ncls(
            set(self._copy_nodes()) & set(other._copy_nodes())
        )
        return ncls

    
    def intersection_update_set(self, other):
        """
        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for querying the IntervalSet. This is useful
        when the input is not of the same object class as the members
        of IntervalSet. The callable must accept one (and only one)
        argument and outputs a single BaseInterval-descendant object.
        """
        self._copy_state(self.intersection_set(other))

    
    def symmetric_difference_set(self, other, setter=None):
        """
        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for querying the IntervalSet. This is useful
        when the input is not of the same object class as the
        members of IntervalSet. The callable must accept one (and only
        one) argument and outputs a single BaseInterval-descendant object.
        """
        other = self._coerce_class(other, setter)
        ncls = self.__class__(setter=self._setter)
        ncls._set_ncls(
            set(self._copy_nodes()) ^ set(other._copy_nodes())
        )
        return ncls

    
    def symmetric_difference_update_set(self, other):
        """
        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for querying the IntervalSet. This is useful
        when the input is not of the same object class as the members
        of IntervalSet. The callable must accept one (and only one)
        argument and outputs a single BaseInterval-descendant object.
        """
        self._copy_state(self.symmetric_difference_set(other))


    def union_set(self, other, setter=None):
        """
        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for querying the IntervalSet. This is useful
        when the input is not of the same object class as the members 
        of IntervalSet. The callable must accept one (and only one)
        argument and outputs a single BaseInterval-descendant object.
        """
        other = self._coerce_class(other, setter)
        ncls = self.__class__(setter=self._setter)
        ncls._set_ncls(
            set(self._copy_nodes()) | set(other._copy_nodes())
        )
        return ncls


    def union_update_set(self, other):
        """
        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for querying the IntervalSet. This is useful
        when the input is not of the same object class as the members 
        of IntervalSet. The callable must accept one (and only one) 
        argument and outputs a single BaseInterval-descendant object.
        """
        self._copy_state(self.union_set(other))


    def update(self, intervals, setter=None):
        """
        The `setter` keyword argument accepts a callable used to 
        extract/construct from the input object a BaseInterval-descendant
        class instance for querying the IntervalSet. This is useful
        when the input is not of the same object class as the members 
        of IntervalSet. The callable must accept one (and only one) 
        argument and outputs a single BaseInterval-descendant object.
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
#
# Performance:
#  1. A collections.deque() is implemented in C and supports O(1) 
#     insert()s and pop()s on either end, and is therefore faster 
#     than a builtin.list() (which is O(n) performance b/c of re-allocs). 
#     See:
#     https://stackoverflow.com/questions/23487307/python-deque-vs-list-performance-comparison
#
# Resources:
# 1. https://github.com/python/cpython/tree/main/Modules
#
# 2. https://github.com/arq5x/chrom_sweep/blob/master/chrom_sweep.py
#
# 3. https://github.com/BioJulia/Bio.jl/issues/340


#TODO: make sure adding max kwarg to _Node hasn't F'd up IntervalSet
