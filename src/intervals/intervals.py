"""
Module for representing genomic intervals

All class methods assume a 0-index coordinate system unless otherwise
specified.

About mathematical and genomic intervals:
  1. https://en.wikipedia.org/wiki/Interval_(mathematics)#Terminology
  2. http://genome.ucsc.edu/blog/the-ucsc-genome-browser-coordinate-counting-systems/

"""

from math import isnan as _isnull
from math import isinf as _isinf
from math import isfinite as _isfinite
from copy import copy as _copy
from copy import deepcopy as _deepcopy
from .constants import NULL_NAMESPACE as _NULL_NS
from .constants import NULL_BEG as _NULL_BEG
from .constants import NULL_END as _NULL_END
from .constants import inf as _INF

_bad_operand_type = \
    "unsupported operand type(s) for {0:s}: '{1}' and '{2}'".format
_bad_operand_name = \
    "mismatched operand namespaces for {0:s}: '{1}' and '{2}'".format
_ill_defined = \
    "Result ill-defined, use {0:s}() instead".format


def _0s(x):
    return (0, 0)


def _1s(x):
    return (1, 1)


def _nulls(x):
    return (_NULL_BEG, _NULL_END)


def _0div(x):
    raise ZeroDivisionError("denominator an empty interval")


def _int(x):
    try:
        return int(x)
    except (ValueError, OverflowError):
        return x


def _ceil(x):
    return x if _isinf(x) else -1 * ((-1 * x) // 1)


def _floor(x, y):
    return x if _isinf(x) else x // y

    

class BaseInterval(object):
    """
    Base class for 0-indexed generic mathematical intervals. Assumes
    interval coordinates are fully-open (specifically, left-closed 
    right-open), same as Pythonic slice notation.

    The `self.namespace` attribute provides an abstraction allowing 
    this module access to a stable id or name and enable comparions
    between objects in potentially different namespaces (X, Y, or Z
    dimensions, sequence names, etc.).
    """
    # To maintain memory and speed efficiency, every child object
    # must also define __slots__ = ()
    __slots__ = ('namespace','_beg','_end')
    
    # Constructor, descriptor, and introspection methods:
    def __init__(self, beg=_NULL_BEG, end=_NULL_END, namespace=_NULL_NS):
        self.namespace = namespace
        self.beg = beg  # sets self._beg
        self.end = end  # sets self._end


    def __bool__(self):
        """
        bool(self) -> bool

        Test if an Interval is non-empty.
        
        >>> bool(Interval("Chr", 350, 475))
        True
        >>> bool(Interval())
        False
        """
        return not self.isempty()


    def __hash__(self):
        """
        hash(self) -> int

        Return a runtime-unique id for the Interval object.
        
        >>> hash(Interval("Chr", 350, 475))
        4465105936
        """
        return id(self)
        

    def __len__(self):
        """
        len(self) -> value

        Return the length of the interval.
        """
        return 0 if self.isempty() else (self.end - self.beg)

    
    def __repr__(self):
        return "%s(%s)" % (
            self.__class__.__name__, str(self))

    
    def __str__(self):
        """
        str(self) -> str

        Return a string representation of the Interval object.
        
        >>> str(Interval("Chr", 350,475))
        '[350, 475, namespace=None]'
        """
        return "[%s, %s, namespace=%s]" %(
            str(self.beg), str(self.end), str(self.namespace)
        )


    @property
    def beg(self):
        """
        self.beg -> value

        The beginning (0-based) coordinate of the Interval.
        
        >>> interval.beg = 350
        >>> print(interval.beg)
        350
        """
        return self._beg


    @beg.setter
    def beg(self, beg):
        self._beg = beg


    @property
    def start(self):
        """
        self.start -> value

        Alias for the `beg` attribute.
        
        >>> interval.start = 350
        >>> print(interval.start)
        350
        """
        return self.beg


    @start.setter
    def start(self, start):
        self.beg = start


    @property
    def mid(self):
        """
        self.mid -> value

        The midpoint of the interval.
        
        >>> print(self.mid)
        412.5
        """
        return _NULL_BEG \
            if   self.isempty() \
            else float(self.beg + self.end) / 2


    @property
    def end(self):
        """
        self.end -> value

        The ending (1-based) coordinate of the interval.
        
        >>> interval.end = 500
        >>> print(interval.end)
        500
        """
        return self._end


    @end.setter
    def end(self, end):
        self._end = end


    @property
    def stop(self):
        """
        self.stop -> value
        
        Alias for `end` attribute.
        
        >>> interval.stop = 500
        >>> print(interval.stop)
        500
        """
        return self.end


    @stop.setter
    def stop(self, stop):
        self.end = stop
        

    def empty(self):
        """
        self.empty() -> None

        Empty the Interval object.
        
        >>> interval = Interval("Chr", 15, 55)
        >>> interval.empty()
        >>> print(interval)
        None:nan-nan
        """
        self.namespace = _NULL_NS
        self.beg = _NULL_BEG
        self.end = _NULL_END

        
    def copy(self, deep=False):
        """
        self.copy() -> Interval
        self.copy(deep=True) -> Interval

        If `deep=False`, return a shallow copy of the Interval object.
        If `deep=True`, return a deep copy of the Interval object.

        >>> interval.copy() is interval
        False
        """
        return _deepcopy(self) if deep else _copy(self)
        

    def to_slice(self):
        """
        self.to_slice() -> slice

        Return the interval as a slice object for use with lists, 
        strings, or other list-like objects. Returns slice(0, 0)
        if null.
        
        >>> string = 'abcdefghijklmnopqrstuvwxyz'
        >>> interval = Interval("Chr", 2, 10)
        >>> print(string[interval.to_slice()])
        cdefghij
        """
        if self.isempty():
            return slice(0, 0)
        return slice(self.beg, self.end)


    # Equality and comparison methods:
    def __eq__(self, other):
        """
        self == other -> bool

        Test for interval equality. Null objects are always not equal.
        """
        return ((self.namespace == other.namespace) and
                (self.beg == other.beg) and
                (self.end == other.end))
    

    def __gt__(self, other):
        """
        self > other -> bool

        Test if self Interval is greater-than other.
        """
        return ((self.namespace == other.namespace) and
                ((self.beg > other.beg) or
                 (self.beg == other.beg) and
                 (self.end > other.end)))


    def __ge__(self, other):
        """
        self >= other -> bool

        Test if self Interval is greater-than or equal-to other: 
        """
        return self == other or self > other
    

    def __lt__(self, other):
        """
        self < other -> bool

        Test if self Interval is less-than other.
        """
        return ((self.namespace == other.namespace) and
                ((self.beg < other.beg) or
                 (self.beg == other.beg) and
                 (self.end < other.end)))


    def __le__(self, other):
        """
        self <= other -> bool

        Test if self Interval is less-than or equal-to other.
        """
        return self == other or self < other


    def __ne__(self, other):
        """
        self != other -> bool

        Test for interval inequality.
        """
        return not (self == other)
    

    # Arithmetic methods
    def __rvalue_get(self, other, op=None, i=_0s):
        if isinstance(other, BaseInterval):
            if other.isnull():
                return i(other)
            if self.namespace != other.namespace:
                raise ValueError(_bad_operand_name(
                    op, other.namespace, self.namespace
                )) from None
            beg = other.beg
            end = other.end
        elif isinstance(other, (float, int)):
            beg = end = other
        else:
            raise TypeError(
                _bad_operand_type(op, type(other), type(self))
            )
        return (beg, end)


    def __lvalue_get(self, other, op=None, i=_0s):
        if isinstance(other, BaseInterval):
            if other.isnull():
                return i(other)
            if self.namespace != other.namespace:
                raise ValueError(_bad_operand_name(
                    op, self.namespace, other.namespace
                )) from None
            beg = other.beg
            end = other.end
        elif isinstance(other, (float, int)):
            beg = end = other
        else:
            raise TypeError(
                _bad_operand_type(op, type(self), type(other))
            )
        return (beg, end)
    

    def __abs__(self):
        """
        abs(self) -> Interval

        Return the absolute value of an interval's beginning-/end-
        points.
        """
        copy = self.copy()
        copy.beg = abs(self.beg)
        copy.end = abs(self.end)
        return copy
    

    def __add__(self, value):
        """
        self + value -> Interval

        Shift self Interval beginning-/end-points by value, where 
        value can be any numeric primitive or BaseInterval-
        descendant class instance.
        """
        copy = self.copy()
        beg, end = self.__lvalue_get(value, op='+', i=_0s)
        copy.beg = self.beg + beg
        copy.end = self.end + end
        return copy


    def __ceil__(self):
        """
        math.ceil(self) -> Interval

        Take the ceiling of an interval's beginning-/end-points. 
        """
        copy = self.copy()
        copy.beg = _ceil(self.beg)
        copy.end = _ceil(self.end)
        return copy


    def __float__(self):
        """
        float(self) -> float

        Cast the beginning-/end-points of an interval to floating-
        point values.
        """
        copy = self.copy()
        copy.beg *= 1.0
        copy.end *= 1.0
        return copy
    

    def __floor__(self):
        """
        math.floor(self) -> Interval

        Floor an interval's beginning-/end-points.
        """
        copy = self.copy()
        copy.beg = _floor(self.beg, 1)
        copy.end = _floor(self.end, 1)
        return copy
    

    def __floordiv__(self, value):
        """
        self // value -> Interval

        Divide and floor interval beginning-/end-points by value, 
        where value can be any numeric primitive or BaseInterval-
        descendant class instance.
        """
        copy = self.copy()
        beg, end = self.__lvalue_get(value, op='//', i=_0div)
        copy.beg = _floor(self.beg, beg)
        copy.end = _floor(self.end, end)
        return copy


    def __iadd__(self, value):
        """
        self += value -> Interval

        In-place addition. Shift interval beginning-/end-points by 
        value, where value can be any numeric primitive or
        BaseInterval-descendant class instance.
        """
        beg, end = self.__lvalue_get(value, op='+=', i=_0s)
        self.beg += beg
        self.end += end
        return self


    def __imul__(self, value):
        """
        self *= value -> Interval

        In-place multiplication. Scale interval beginning-/end-points 
        by value, where value can be any numeric primitive or
        BaseInterval-descendant class instance.
        """
        beg, end = self.__lvalue_get(value, op='*=', i=_0s)
        self.beg *= beg
        self.end *= end
        return self
            

    def __int__(self):
        """
        int(self) -> Interval

        Cast the interval beginning-/end-points to integer values.
        """
        copy = self.copy()
        copy.beg = _int(self.beg)
        copy.end = _int(self.end)
        return copy

    
    def __isub__(self, value):
        """
        self -= value -> Interval

        In-place subtraction. Shift interval beginning-/end-points 
        by value, where value can be any numeric primitive or
        BaseInterval-descendant class instance.
        """
        beg, end = self.__lvalue_get(value, op='-=', i=_0s)
        self.beg -= beg
        self.end -= end
        return self
            

    def __lshift__(self, value):
        """
        self << value -> Interval

        Bitwise left-shift interval beginning-/end-points by value,
        where value can be any numeric primitive or BaseInterval-
        descendant class instance.
        """
        copy = self.copy()
        beg, end = self.__lvalue_get(value, op='<<', i=_0s)
        copy.beg = self.beg << beg
        copy.end = self.end << end
        return copy


    def __mod__(self, value):
        """
        self % value -> Interval

        Module the interval beginning-/end-points by value, where
        value can be any numeric primitive or BaseInterval-
        descendant class instance.
        """
        copy = self.copy()
        beg, end = self.__lvalue_get(value, op='<<', i=_0s)
        copy.beg = self.beg % beg
        copy.end = self.end % end
        return copy
    
    
    def __mul__(self, value):
        """
        self * value -> Interval

        Multiply interval beginning-/end-points by value, where
        value can be any numeric primitive or BaseInterval-
        descendant class instance.
        """
        copy = self.copy()
        beg, end = self.__lvalue_get(value, op='*', i=_0s)
        copy.beg = self.beg * beg
        copy.end = self.end * end
        return copy


    def __neg__(self):
        """
        -self -> value

        Change the numeric sign of the interval beginning-/end-points.
        """
        copy = self.copy()
        copy.beg *= -1
        copy.end *= -1
        return copy


    def __pos__(self):
        """
        +self -> value
        
        Returns a copy of the calling object with beginning-/end-points
        numeric signs unchanged.
        """
        return self.copy()


    def __pow__(self, mod):
        """
        self**mod -> Interval
        pow(self, mod) -> Interval

        Obtain self to the power of mod for the beginning-/end-points
        of the interval.
        """
        copy = self.copy()
        beg, end = self.__lvalue_get(value, op='*', i=_0s)
        copy.beg = pow(self.beg, beg)
        copy.end = pow(self.end, end)
        return copy

    
    def __radd__(self, value):
        """
        value + self -> Interval

        Right-side addtion. Shift a value by interval beginning-/end-
        points, where value can be any numeric primitive.
        """
        copy = self.copy()
        beg, end = self.__rvalue_get(value, op='+', i=_0s)
        copy.beg = beg + self.beg
        copy.end = end + self.end
        return copy
    

    def __rfloordiv__(self, value):
        """
        value // self -> Interval

        Divide and floor value by interval, where value can be any 
        numeric primitive.
        """
        copy = self.copy()
        beg, end = self.__rvalue_get(value, op='//', i=_0s)
        copy.beg = _floor(beg, self.beg)
        copy.end = _floor(end, self.end)
        return copy


    def __rlshift__(self, value):
        """
        value << self -> Interval

        Bitwise left-shift value by the beginning-/end-points of self, 
        where value can be any numeric primitive.
        """
        copy = self.copy()
        beg, end = self.__rvalue_get(value, op='<<', i=_0s)
        copy.beg = beg << self.beg
        copy.end = end << self.end
        return copy


    def __rmul__(self, value):
        """
        value * self -> Interval

        Multiply value by self, where value can be any numeric
        primitive.
        """
        copy = self.copy()
        beg, end = self.__rvalue_get(value, op='*', i=_0s)
        copy.beg = beg * self.beg
        copy.end = end * self.end
        return copy


    def __rmod__(self, value):
        """
        value % self -> Interval

        Modulo value by self, where value can be any numeric
        primitive.
        """
        copy = self.copy()
        beg, end = self.__rvalue_get(value, op='%', i=_0s)
        copy.beg = beg % self.beg
        copy.end = end % self.end
        return copy
    

    def __round__(self, ndigits=None):
        """
        round(self, ndigits) -> Interval

        Round the beginning-/end-points of an interval to `ndigits`.
        Performs banker's rounding, same as built-in `round()`.
        """
        copy = self.copy()
        copy.beg = round(self.beg, ndigits)
        copy.end = round(self.end, ndigits)
        return copy

    
    def __rrshift__(self, value):
        """
        value >> self -> Interval

        Bitwise right-shift value by the beginning-/end-points of self, 
        where value can be any numeric primitive.
        """
        copy = self.copy()
        beg, end = self.__rvalue_get(value, op='>>', i=_0s)
        copy.beg = beg >> self.beg
        copy.end = end >> self.end
        return copy
    

    def __rshift__(self, value):
        """
        self >> value -> Interval

        Bitwise right-shift the beginning-/end-points of self by value, 
        where value can be any numeric primitive or BaseInterval-
        descendant class instance.
        """
        copy = self.copy()
        beg, end = self.__lvalue_get(value, op='>>', i=_0s)
        copy.beg = self.beg >> beg
        copy.end = self.end >> end
        return copy


    def __rsub__(self, value):
        """
        value - self -> Interval

        Right-side subtraction. Shift interval beginning-/end-points
        by value, where value can be any numeric primitive.
        """        
        copy = self.copy()
        beg, end = self.__rvalue_get(value, op='-', i=_0s)
        copy.beg = beg - self.beg
        copy.end = end - self.end
        return copy


    def __rtruediv__(self, value):
        """
        value / self -> Interval

        Divide value by beginning-/end-points of self, where value
        can be any numeric primitive.
        """
        copy = self.copy()
        beg, end = self.__rvalue_get(value, op='/', i=_nulls)
        copy.beg = beg / self.beg
        copy.end = end / self.end
        return copy
    

    def __sub__(self, value):
        """
        self - value -> Interval

        Shift interval beginning-/end-points by value, where value can
        be any numeric primitive or an BaseInterval-descendant class
        instance.
        """
        copy = self.copy()
        beg, end = self.__lvalue_get(value, op='-', i=_0s)
        copy.beg = self.beg - beg
        copy.end = self.end - end
        return copy


    def __truediv__(self, value):
        """
        self / value -> Interval

        Divided interval beginning-/end-points by value, where value
        can be any numeric primitive or BaseInterval-descendant class
        instance.
        """
        copy = self.copy()
        beg, end = self.__lvalue_get(value, op='/', i=_1s)
        copy.beg = self.beg / beg
        copy.end = self.end / end
        return copy


    def __trunc__(self):
        copy = self.copy()
        copy.beg = _int(self.beg)
        copy.end = _int(copy.end)
        return copy
    

    # Interval and set methods
    def __and__(self, other):
        """
        self & other -> Interval or None

        Return the intersection interval of two Intervals. See the
        `intersection()` method documentation for more information.
        """
        return self.intersection(other)


    def __contains__(self, other):
        """
        other in self -> bool

        Test if other is contained within self. See the `issuperinterval()`
        method documentation for more information.
        """
        return self.issuperinterval(other)


    def __or__(self, other):
        """
        self | other -> Interval or 2-tuple

        Return the union interval of two Intervals. See the `union()`
        method documentation for more information.
        """
        return self.union(other)
    

    def __xor__(self, other):
        """
        self ^ other -> 2-tuple of Intervals
        
        Returns the (xor) symmetric difference intervals wrapped in 
        a tuple. The right-side and left-side objects are returned
        as the same class type(s) as their inputs, unless one object
        is contained within another, then both objects returned are 
        of the larger type.
        """
        return self.symmetric_difference(other)


    def isabutting(self, other):
        """
        self.isabutting(other) -> bool

        Test whether self is abutting the beginning or end of other.

        >>> Interval("Chr", 30, 40).isabutting(Interval("Chr", 40, 60))
        True
        """
        return self.isabutting_beg(other) or self.isabutting_end(other)
    

    def isabutting_beg(self, other):
        """
        self.isabutting_beg(other) -> bool

        Test whether self is abutting the beginning of other.

        >>> Interval("Chr", 30, 40).isabutting_beg(Interval("Chr", 40, 60))
        True
        """
        return ((self.namespace == other.namespace) and
                (self.end == other.beg) and
                (other.beg < other.end) and
                (self.beg < other.end))


    def isabutting_end(self, other):
        """
        self.isabutting_end(other) -> bool

        Test whether self is abutting the end of other.

        >>> Interval("Chr", 60, 80).isabutting_end(Interval("Chr", 40, 60))
        True
        """
        return ((self.namespace == other.namespace) and
                (other.end == self.beg) and
                (other.beg < other.end) and
                (self.beg < self.end))


    def issuperinterval(self, other, strict=False):
        """
        self.issuperinterval(other) -> bool

        Test whether self is containing other (whether self is a 
        superinterval of self). When `strict=True`, evaluate to True
        only when self is a strict superinterval of other.

        >>> i1 = Interval("Chr", 20, 80)
        >>> i2 = Interval("Chr", 40, 60)
        >>> i1.issuperinterval(i2)
        True
        >>> i2.issuperinterval(i1)
        False
        >>> i1.issuperinterval(i1, strict=False)
        True
        >>> i1.issuperinterval(i1, strict=True)
        False
        """
        strict = strict and (self.beg == other.beg) and (self.end == other.end)
        return ((self.namespace == other.namespace) and
                (self.beg <= other.beg <= other.end <= self.end) and
                (not strict))


    def issubinterval(self, other, strict=False):
        """
        self.issubinterval(other) -> bool

        Test whether self is contained within other (whether self is
        a subinterval of other). When `strict=True`, evaluate to True
        only when self is a strict subinterval of other.

        >>> i1 = Interval("Chr", 20, 80)
        >>> i2 = Interval("Chr", 40, 60)
        >>> i1.issubinterval(i2)
        False
        >>> i2.issubinterval(i1)
        True
        >>> i1.issubinterval(i1, strict=False)
        True
        >>> i1.issubinterval(i1, strict=True)
        False
        """
        strict = strict and (self.beg == other.beg) and (self.end == other.end)
        return ((self.namespace == other.namespace) and 
                (other.beg <= self.beg <= self.end <= other.end) and
                (not strict))


    def isoverlapping(self, other):
        """
        self.isoverlapping(other) -> bool

        Test whether self has any kind of overlap with other.

        >>> Interval("Chr", 20, 60).isoverlapping(Interval("Chr", 40, 80))
        True
        """
        return ((self.namespace == other.namespace) and
                (other.beg <= self.end and self.beg <= other.end))
    

    def isoverlapping_beg(self, other):
        """
        self.isoverlapping_beg(other) -> bool

        Test whether self isoverlapping the left-most edge of other.

        >>> Interval("Chr", 20, 60).isoverlapping_beg(Interval("Chr", 40, 80))
        True
        >>> Interval("Chr", 40, 80).isoverlapping_beg(Interval("Chr", 20, 60))
        False
        """
        # self.beg *=========* self.end
        #      other.beg *==============* other.end
        return ((self.namespace == other.namespace) and
                (self.beg <= other.beg <= self.end <= other.end))


    def isoverlapping_end(self, other):
        """
        self.isoverlapping_end(other) -> bool

        Test whether self isoverlapping the right-most edge of other.

        >>> Interval("Chr", 40, 80).isoverlapping_end(Interval("Chr", 20, 60))
        True
        >>> Interval("Chr", 20, 60).isoverlapping_end(Interval("Chr", 40, 80))
        False
        """
        #           self.beg *=========* self.end
        # other.beg *==============* other.end            
        return ((self.namespace == other.namespace) and
                (other.beg <= self.beg <= other.end <= self.end))


    def overlap_length(self, other):
        """
        self.overlap_length(other) -> value

        Returns the overlap length between two intervals.

        >>> Interval("Chr", 20, 60).overlap_length(Interval("Chr", 40, 70))
        20
        """
        if self.namespace == other.namespace:
            return max(0, min(self.end, other.end) - max(self.beg, other.beg))
        return 0
        

    def overlap_fraction(self, other):
        """
        self.overlap_fraction(other) -> float

        Calculates overlap length as a fraction of self.

        >>> I1 = Interval("Chr", 20, 60)
        >>> I2 = Interval("Chr", 40, 70)
        >>> I1.overlap_fraction(I2)
        0.5
        """
        return float(self.overlap_length(other)) / max(1, len(self))


    def inner_distance(self, other):
        """
        self.inner_distance(other) -> value

        Returns the distance between the inner-most coordinates of two 
        intervals. A negative distances indicates that self is downstream
        of other. Abutting and overlapping intervals return `0`.

        >>> I1 = Interval("Chr", 10, 20)
        >>> I2 = Interval("Chr", 45, 80)
        >>> I1.inner_distance(I2)
        25
        >>> I2.inner_distance(I1)
        -25
        """
        if self.isnull() or other.isnull():
            return _INF
        if self.isoverlapping(other):
            return 0
        if self < other:
            return other.beg - self.end
        if self > other:
            return other.end - self.beg
        return _INF

    
    def outer_distance(self, other, maxrange=False):
        """
        self.outer_distance(other) -> value
        self.outer_distance(other, maxrange=True) -> value

        Returns the distance between the outer-most points of two 
        intervals. A negative distance indicates that self is downstream
        of other.

        >>> I1 = Interval("Chr", 10, 17)
        >>> I2 = Interval("Chr", 5, 8)
        >>> I1.outer_distance(I2)
        -12

        If maxrange=True, then the outer distance of overlapping
        intervals is calculated as min(self.beg, other.beg) and 
        max(self.end, other.end).

        >>> I1 = Interval("Chr", 10, 20)
        >>> I2 = Interval("Chr", 15, 18)
        >>> I1.outer_distance(I2)
        8
        >>> I1.outer_distance(I2, maxrange=True)
        10
        """
        if self.isnull() or other.isnull():
            return _INF
        if self.namespace == other.namespace:
            if maxrange:
                beg = min(self.beg, other.beg)
                end = max(self.end, other.end)
            elif self.mid <= other.mid:
                beg = self.beg
                end = other.end
            else:
                beg = other.beg
                end = self.end
            if self.beg <= other.beg:
                return end - beg
            else:
                return beg - end
        return _INF
    

    def difference(self, other):
        """
        self.difference(other) -> Interval or 2-tuple
        
        Returns the difference interval(s) of the same type as the 
        left-side/calling object. If either interval is contained
        within the other, return a tuple containing the two result
        intervals.

        >>> I1 = Interval("Chr", 1, 60)
        >>> I2 = Interval("Chr", 45, 80)
        >>> I1.difference(I2)
        Interval(Chr:1-45)
        """
        copy = self.copy()
        if self.isempty():
            return copy
        if other.isempty():
            return copy
        elif other.issuperinterval(self):
            copy.empty()
        elif other.isoverlapping_beg(self):
            copy.beg = other.end
        elif other.isoverlapping_end(self):
            copy.end = other.beg            
        elif other.issubinterval(self):
            copy.end = other.beg
            kopy = self.copy()
            kopy.beg = other.end
            return (copy, kopy)
        return copy


    def difference_update(self, other):
        """Raises NotImplementedError."""
        raise NotImplementedError(_ill_defined('difference'))
        

    def hull(self, other=None):
        """
        self.hull() -> Interval
        self.hull(other) -> Interval

        Returns the smallest interval closure of self (and, optionally,
        other).
        """
        copy = self.copy()
        if copy.isempty():
            copy.empty()
        if other:
            if other.isempty():
                other = Interval()
            if copy.namespace == other.namespace:
                copy.beg = min(copy.beg, other.beg)
                copy.end = max(copy.end, other.end)
        return copy
    
        
    def intersection(self, other):
        """
        self & other -> Interval
        self.intersection(other) -> Interval

        Returns the intersection interval of the same type as the 
        left-side/calling object. Disjoint intervals return a null
        object.

        >>> I1 = Interval("Chr", 1, 60)
        >>> I2 = Interval("Chr", 45, 80)
        >>> I1.intersection(I2)
        Interval(Chr:45-60)
        """
        copy = self.copy()
        if self.isoverlapping(other):
            copy.beg = max(self.beg, other.beg)
            copy.end = min(self.end, other.end)
        else:
            copy.empty()
        return copy


    def intersection_update(self, other):
        """Raises NotImplementedError."""
        raise NotImplementedError(_ill_defined('intersection'))


    def symmetric_difference(self, other):
        """
        self ^ other -> 2-tuple of Intervals
        self.symmetric_difference(other) -> 2-tuple of Intervals

        Returns the (xor) symmetric difference Intervals wrapped in 
        a tuple. The right-side and left-side objects are returned
        as the same class type(s) as their inputs, unless one object
        is contained within another, then both objects returned are 
        of the larger type.

        >>> I1 = Interval("Chr", 1, 60)
        >>> I2 = Interval("Chr", 45, 80)
        >>> I1.symmetric_difference(I2)
        (Interval(Chr:1-45), Interval(Chr:60-80))
        """
        if self.isnull() or other.isnull():
            return (self.copy(), other.copy())
        i1 = self.difference(other)
        i2 = other.difference(self)
        if isinstance(i1, tuple):
            return i1
        if isinstance(i2, tuple):
            return i2
        return (i1, i2)


    def symmetric_difference_update(self, other):
        """Raises NotImplementedError."""
        raise NotImplementedError(_ill_defined('symmetric_difference'))
    

    def union(self, other, abutting=False):
        """
        self | other -> Interval or 2-tuple
        self.union(other) -> Interval or 2-tuple

        Returns the union (inclusive or) interval(s) of the same type
        as the left-side/calling object possibly wrapped in a tuple 
        object.

        >>> Interval("Chr", 0, 60).union(Interval("Chr", 45, 80))
        Interval(Chr:0-80)
        """
        if self.isempty():
            return other.copy()
        if other.isempty():
            return self.copy()
        copy = self.copy()
        if self.isoverlapping(other):
            copy.beg = min(self.beg, other.beg)
            copy.end = max(self.end, other.end)
        elif abutting and self.isabbutting(other):
            copy.beg = min(self.beg, other.beg)
            copy.end = max(self.end, other.end)
        else:
            kopy = other.copy()
            return (copy, kopy)
        return copy
    

    def union_update(self, other):
        """Raises NotImplementedError."""
        raise NotImplementedError(_ill_defined('union_update'))

    
    def isdisjoint(self, other):
        """
        self.isdisjoint(other) -> bool

        Test whether self and other are disjoint (non-overlapping).

        >>> Interval("Chr", 0, 20).isdisjoint(Interval("Chr", 45, 80))
        True
        >>> Interval("Chr", 0, 60).isdisjoint(Interval("Chr", 45, 80))
        False
        """
        return not self.isoverlapping(other)
    

    def isempty(self):
        """
        self.isempty() -> bool

        Test whether self is a valid interval range. If self is null
        this method will also return True.
        """
        return not (self.beg <= self.end)


    def isfinite(self):
        """
        self.isfinite() -> bool

        Test whether self is a finite interval.
        """
        return _isfinite(self.beg) and _isfinite(self.end)

    
    def isnull(self):
        """
        self.isnull() -> bool

        Test whether self.beg or self.end are null (nan) values.
        """
        return _isnull(self.beg) or _isnull(self.end)


    def issingleton(self):
        """
        self.issingleton() -> bool

        Test whether self.beg == self.end
        """
        return self.beg == self.end
    

    # Method aliases
    clear = empty
    
    to_string = __str__

    isabutting_start = isabutting_beg

    isabutting_stop = isabutting_end
    
    isoverlapping_start = isoverlapping_beg

    isoverlapping_stop = isoverlapping_end

    issubset = issubinterval

    issuperset = issuperinterval


    
class LeftClosedInterval(BaseInterval):
    """
    Class for 0-indexed generic mathematical intervals. Assumes
    interval coordinates are half-open (specifically, left-closed 
    right-open), same as Pythonic slice notation.

    The `self.namespace` attribute provides an abstraction allowing 
    this module access to a stable id or name and enable comparions
    between objects in potentially different namespaces (X, Y, or Z
    dimensions, sequence names, etc.).
    """
    __slots__ = ()
    
    def issuperinterval(self, other, strict=False):
        """
        self.issuperinterval(other) -> bool
        
        Test whether self is containing other (whether self is a 
        superinterval of self). When `strict=True`, evaluate to True
        only when self is a strict superinterval of other.

        >>> i1 = Interval("Chr", 20, 80)
        >>> i2 = Interval("Chr", 40, 60)
        >>> i1.issuperinterval(i2)
        True
        >>> i2.issuperinterval(i1)
        False
        >>> i1.issuperinterval(i1, strict=False)
        True
        >>> i1.issuperinterval(i1, strict=True)
        False
        """
        strict = strict and (self.beg == other.beg) and (self.end == other.end)
        return ((self.namespace == other.namespace) and
                (self.beg <= other.beg < other.end <= self.end) and
                (not strict))

    
    def issubinterval(self, other, strict=False):
        """
        self.issubinterval(other) -> bool

        Test whether self is contained within other (whether self is
        a subinterval of other). When `strict=True`, evaluate to True
        only when self is a strict subinterval of other.

        >>> i1 = Interval("Chr", 20, 80)
        >>> i2 = Interval("Chr", 40, 60)
        >>> i1.issubinterval(i2)
        False
        >>> i2.issubinterval(i1)
        True
        >>> i1.issubinterval(i1, strict=False)
        True
        >>> i1.issubinterval(i1, strict=True)
        False
        """
        strict = strict and (self.beg == other.beg) and (self.end == other.end)
        return ((self.namespace == other.namespace) and 
                (other.beg <= self.beg < self.end <= other.end) and
                (not strict))

    
    def isoverlapping(self, other):
        """
        self.isoverlapping(other) -> bool

        Test whether self has any kind of overlap with other.

        >>> Interval("Chr", 20, 60).isoverlapping(Interval("Chr", 40, 80))
        True
        """
        return ((self.namespace == other.namespace) and
                (other.beg < self.end and self.beg < other.end))


    def isoverlapping_beg(self, other):
        """
        self.isoverlapping_beg(other) -> bool

        Test whether self isoverlapping the left-most edge of other.

        >>> Interval("Chr", 20, 60).isoverlapping_beg(Interval("Chr", 40, 80))
        True
        >>> Interval("Chr", 40, 80).isoverlapping_beg(Interval("Chr", 20, 60))
        False
        """
        # self.beg *=========o self.end
        #      other.beg *==============o other.end
        return ((self.namespace == other.namespace) and
                (self.beg <= other.beg < self.end < other.end))


    def isoverlapping_end(self, other):
        """
        self.isoverlapping_end(other) -> bool

        Test whether self isoverlapping the right-most edge of other.

        >>> Interval("Chr", 40, 80).isoverlapping_end(Interval("Chr", 20, 60))
        True
        >>> Interval("Chr", 20, 60).isoverlapping_end(Interval("Chr", 40, 80))
        False
        """
        #           self.beg *=========o self.end
        # other.beg *==============o other.end            
        return ((self.namespace == other.namespace) and
                (other.beg < self.beg < other.end <= self.end))

    
    isoverlapping_start = isoverlapping_beg

    isoverlapping_stop = isoverlapping_end

    issubset = issubinterval

    issuperset = issuperinterval



class ClosedInterval(BaseInterval):
    """
    Class representing a fully-closed interval, i.e., start/begin 
    and stop/end coordinates are inclusive (0-based).
    """
    # To maintain memory and speed efficiency, every child object
    # must also define __slots__ = ()
    __slots__ = ()
    
    def __init__(self, name=_NULL_NS, beg=_NULL_BEG, end=_NULL_END):
        """
        >>> Interval("Chr1", 15, 37) -> Interval
        """
        super().__init__(namespace=name, beg=beg, end=end)


    def __str__(self):
        """
        str(self) -> str

        Return a string representation of the object.

        >>> str(Interval("Chr", 350,475))
        'Chr:350-475'
        """
        return "%s:%s-%s" % (str(self.namespace), str(self.beg), str(self.end))


    to_string = __str__



class Interval(LeftClosedInterval):
    """
    Class representing a generic left-closed, right-open interval,
    i.e., start/begin coordinates are inclusive (0-based) and stop/end
    coordinates are exclusive (or 1-based).
    """
    # To maintain memory and speed efficiency, every child object
    # must also define __slots__ = ()
    __slots__ = ()
    
    def __init__(self, name=_NULL_NS, beg=_NULL_BEG, end=_NULL_END):
        """
        >>> Interval("Chr1", 15, 37) -> Interval
        """
        super().__init__(namespace=name, beg=beg, end=end)
        

    def __str__(self):
        """
        str(self) -> str

        Return a string representation of the object.

        >>> str(Interval("Chr", 350,475))
        'Chr:350-475'
        """
        return "%s:%s-%s" % (str(self.namespace), str(self.beg), str(self.end))

    
    @property
    def name(self):
        """
        self.name -> value
        
        In an inheriting child class, if the `namespace` attribute is
        best defined by another attribute (e.g., as `self.contig`, 
        `self.scaff`, `self.chrom`, etc.) for the purpose of the class,
        the `self.namespace` attribute will require initializization in
        the `__init__()` method.

        For example: 
            def __init__(self, chrom, beg, end):
                Interval.__init__(self, chrom, beg, end)
            @property
            def chrom(self):
                return self.namespace
            @chrom.setter
            def chrom(self, chrom):
                self.namespace = chrom

        """
        return self.namespace


    @name.setter
    def name(self, name):
        self.namespace = name
        
    
    @property
    def beg(self):
        """
        self.beg -> int

        The beginning (0-based) coordinate of the interval.

        >>> interval.beg = 350
        >>> print(interval.beg)
        350
        """
        return self._beg


    @beg.setter
    def beg(self, beg):
        self._beg = _int(beg)


    @property
    def mid(self):
        """
        self.mid -> int

        The midpoint of the interval.

        >>> print(self.mid)
        412
        """        
        return (self.beg + self.end) // 2
        

    @property
    def end(self):
        return self._end


    @end.setter
    def end(self, end):
        """
        self.end -> int

        The ending (1-based) coordinate of the interval.

        >>> interval.end = 500
        >>> print(interval.end)
        500
        """        
        self._end = _int(end)

        
    def isempty(self):
        """
        self.isempty() -> bool

        Test whether self is a valid interval range. If either self.beg
        or self.end are nan, this method returns True.
        """
        return not (self.beg < self.end)


    def issingleton(self):
        """
        self.issingleton() -> bool

        Test whether self.end - self.beg == 1
        """
        return ((self.end - self.beg) == 1)


    to_string = __str__



class ClosedPoint(ClosedInterval):
    __slots__ = ()
    
    def __init__(self, name=_NULL_NS, pos=_NULL_BEG):
        """
        >>> Point("Chr1", 37) -> Point
        """
        super().__init__(namespace=name, beg=pos, end=pos)


    @property
    def beg(self):
        """
        self.beg -> int

        The beginning (0-based) coordinate of the interval.

        >>> interval.beg = 350
        >>> print(interval.beg)
        350
        """
        return self._beg


    @beg.setter
    def beg(self, beg):
        self._beg = beg
        self._end = beg

        
    @property
    def end(self):
        return self._end


    @end.setter
    def end(self, end):
        """
        self.end -> int

        The ending (1-based) coordinate of the interval.

        >>> interval.end = 500
        >>> print(interval.end)
        500
        """
        self._beg = end
        self._end = end
    
    
    @property
    def mid(self):
        """
        self.mid -> int

        The midpoint of the interval.

        >>> print(self.mid)
        412
        """        
        return self.end


    @property
    def pos(self):
        return self.end


    @pos.setter
    def pos(self, pos):
        self.end = pos


    def issingleton(self):
        """
        self.issingleton() -> bool

        Test whether self.end - self.beg == 1
        """
        return True



class Point(Interval):
    __slots__ = ()
    
    def __init__(self, name=_NULL_NS, pos=_NULL_BEG):
        """
        >>> Point("Chr1", 37) -> Point
        """
        super().__init__(namespace=name, beg=pos, end=pos)


    @property
    def beg(self):
        """
        self.beg -> int

        The beginning (0-based) coordinate of the interval.

        >>> interval.beg = 350
        >>> print(interval.beg)
        350
        """
        return self._beg


    @beg.setter
    def beg(self, beg):
        self._beg = _int(beg)
        self._end = _int(beg) + 1

        
    @property
    def end(self):
        return self._end


    @end.setter
    def end(self, end):
        """
        self.end -> int

        The ending (1-based) coordinate of the interval.

        >>> interval.end = 500
        >>> print(interval.end)
        500
        """
        self._beg = _int(end) - 1
        self._end = _int(end)
    
    
    @property
    def mid(self):
        """
        self.mid -> int

        The midpoint of the interval.

        >>> print(self.mid)
        412
        """        
        return self.end


    @property
    def pos(self):
        return self.end


    @pos.setter
    def pos(self, pos):
        self.end = pos


    @property
    def pos0(self):
        return self.beg


    @pos0.setter
    def pos0(self, pos0):
        self.beg = pos0

        
    def issingleton(self):
        """
        self.issingleton() -> bool

        Test whether self.end - self.beg == 1
        """
        return True



#       10        20        30        40        50        60        70        80
#---+----|----+----|----+----|----+----|----+----|----+----|----+----|----+----|



# NOTES:
# - builtin numeric types all have a .real, .imag, and .conjugate attributes
