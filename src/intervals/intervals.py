"""
Module for representing genomic intervals

All class methods assume a 0-index coordinate system unless otherwise
specified. Classes represent "open" or "closed" intervals in the context
of intersection.

About mathematical and genomic intervals:
  1. https://en.wikipedia.org/wiki/Interval_(mathematics)#Terminology
  2. https://en.wikipedia.org/wiki/Interval_arithmetic
  3. http://genome.ucsc.edu/blog/the-ucsc-genome-browser-coordinate-counting-systems/

"""

from math import isnan as _isnull
from math import isinf as _isinf
from math import isfinite as _isfinite
from copy import copy as _copy
from copy import deepcopy as _deepcopy
from .constants import NULL_NAMESPACE as _NULL_NAME
from .constants import NULL_POSITION as _NULL_POS
from .constants import POS_INF as _POS_INF
from .constants import NEG_INF as _NEG_INF
from .errors import _BAD_OPERAND_TYPE, _BAD_OPERAND_NAMESPACE, _ILL_DEFINED



def _0s(x):
    return (0, 0)


def _1s(x):
    return (1, 1)


def _nulls(x):
    return (_NULL_POS, _NULL_POS)


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



class _IntervalIndexInterface(object):
    __slots__ = ()
    
    @property
    def beg(self):
        """
        self.beg -> value

        Return self's start numeric value (0-based).

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
        self.mid -> value

        Return self's midpoint value.

        >>> print(self.mid)
        412
        """        
        return _NULL_POS \
            if   self.isempty() \
            else self.beg + ((self.end - self.beg) >> 1)
        

    @property
    def end(self):
        """
        self.end -> value

        Return self's end value (1-based).

        >>> interval.end = 500
        >>> print(interval.end)
        500
        """        
        return self._end


    @end.setter
    def end(self, end):
        self._end = _int(end)

        
    def isempty(self):
        """
        self.isempty() -> bool

        Return a boolean indicating whether self is a valid interval range.
        If either self.beg or self.end values are nan, this method returns
        True.
        """
        return not (self.beg < self.end)


    def issingleton(self):
        """
        self.issingleton() -> bool

        Return a boolean indicating whether self is a singleton interval.
        """
        return ((self.end - self.beg) == 1)



class _IntervalArithmeticInterface(object):
    __slots__ = ()
    
    def __rvalue_get(self, other, op=None, i=_0s):
        if isinstance(other, BaseInterval):
            if other.isnull():
                return i(other)
            if self.namespace != other.namespace:
                raise ValueError(_BAD_OPERAND_NAMESPACE(op, other, self)) \
                    from None
            beg = other.beg
            end = other.end
        elif isinstance(other, (float, int)):
            beg = end = other
        else:
            raise TypeError(_BAD_OPERAND_TYPE(op, other, self)) from None
        return (beg, end)


    def __lvalue_get(self, other, op=None, i=_0s):
        if isinstance(other, BaseInterval):
            if other.isnull():
                return i(other)
            if self.namespace != other.namespace:
                raise ValueError(_BAD_OPERAND_NAMESPACE(op, self, other)) \
                    from None
            beg = other.beg
            end = other.end
        elif isinstance(other, (float, int)):
            beg = end = other
        else:
            raise TypeError(_BAD_OPERAND_TYPE(op, self, other)) from None
        return (beg, end)
    

    def __abs__(self):
        """
        abs(self) -> interval

        Return a copy of self with absolute start and end values.
        """
        copy = self.copy()
        copy.beg = min(abs(self.beg),abs(self.end))
        copy.end = max(abs(self.beg),abs(self.end))
        return copy
    

    def __add__(self, value):
        """
        self + value -> interval

        Return a copy of self with start and end values shifted by
        the amount given via the input value argument, where the value
        argument is a numeric primitive or BaseInterval-descendant
        class instance.
        """
        copy = self.copy()
        beg, end = self.__lvalue_get(value, op='+', i=_0s)
        copy.beg = self.beg + beg
        copy.end = self.end + end
        return copy


    def __ceil__(self):
        """
        math.ceil(self) -> interval

        Return a copy of self with start and end values ceilinged.
        """
        copy = self.copy()
        copy.beg = _ceil(self.beg)
        copy.end = _ceil(self.end)
        return copy


    def __float__(self):
        """
        float(self) -> float

        Return a copy of self with start and end values cast to 
        floating-point values.
        """
        copy = self.copy()
        copy.beg *= 1.0
        copy.end *= 1.0
        return copy
    

    def __floor__(self):
        """
        math.floor(self) -> interval

        Return a copy of self with start and end values floored.
        """
        copy = self.copy()
        copy.beg = _floor(self.beg, 1)
        copy.end = _floor(self.end, 1)
        return copy
    

    def __floordiv__(self, value):
        """
        self // value -> interval

        Return a copy of self with start and end values divided by the
        amount given via the input value argument then floored, where
        the value argument is a numeric primitive or BaseInterval
        -descendant class instance.
        """
        copy = self.copy()
        beg, end = self.__lvalue_get(value, op='//', i=_1s)
        if beg == 0 and end == 0:
            raise ZeroDivisionError("division by zero")
        elif beg == 0:
            copy.beg = min(self.beg / end, self.end / end)
            copy.end = _POS_INF
        elif end == 0:
            copy.beg = _NEG_INF
            copy.end = max(self.beg / beg, self.end / beg)
        else:
            copy.beg = min(self.beg / beg, self.end / beg,
                           self.beg / end, self.end / end)
            copy.end = max(self.beg / beg, self.end / beg,
                           self.beg / end, self.end / end)
        copy.beg = _floor(copy.beg, 1)
        copy.end = _floor(copy.end, 1)
        return copy


    def __iadd__(self, value):
        """
        self += value -> interval

        In-place addition. Shift self's start and end values by the
        amount given via the input value argument, where the value
        argument is a numeric primitive or BaseInterval-descendant
        class instance.
        """
        beg, end = self.__lvalue_get(value, op='+=', i=_0s)
        self.beg += beg
        self.end += end
        return self
    

    def __imul__(self, value):
        """
        self *= value -> interval

        In-place multiplication. Scale self's start and end values by the
        amount given via the input value argument, where the value
        argument is a numeric primitive or BaseInterval-descendant
        class instance.
        """
        beg, end = self.__lvalue_get(value, op='*=', i=_0s)
        _beg = min(self.beg * beg, self.beg * end,
                   self.end * beg, self.end * end)
        _end = max(self.beg * beg, self.beg * end,
                   self.end * beg, self.end * end)
        self.beg = _beg
        self.end = _end
        return self
            

    def __int__(self):
        """
        int(self) -> interval

        Return a copy of self with start and end values cast to integer
        values.
        """
        copy = self.copy()
        copy.beg = _int(self.beg)
        copy.end = _int(self.end)
        return copy

    
    def __isub__(self, value):
        """
        self -= value -> interval

        In-place subtraction. Shift self's start and end values by the
        amount given via the input value argument, where the value
        argument is a numeric primitive or BaseInterval-descendant
        class instance.
        """
        beg, end = self.__lvalue_get(value, op='-=', i=_0s)
        self.beg -= beg
        self.end -= end
        return self
            

    def __lshift__(self, value):
        """
        self << value -> interval

        Return a copy of self with start and end values bitwise left-shifted
        by the amount given via the input value argument, where the value
        argument is a numeric primitive or BaseInterval-descendant class
        instance.
        """
        copy = self.copy()
        beg, end = self.__lvalue_get(value, op='<<', i=_0s)
        copy.beg = self.beg << beg
        copy.end = self.end << end
        return copy


    def __mod__(self, value):
        """
        self % value -> interval

        Return a copy of self with start and end values modulo'd by the 
        amount given via the input value argument, where the value argument
        is a numeric primitive or BaseInterval-descendant class instance.
        """
        copy = self.copy()
        beg, end = self.__lvalue_get(value, op='<<', i=_0s)
        copy.beg = min(self.beg % beg, self.beg % end,
                       self.end % beg, self.end % end)
        copy.end = min(self.beg % beg, self.beg % end,
                       self.end % beg, self.end % end)
        return copy
    
    
    def __mul__(self, value):
        """
        self * value -> interval

        Return a copy of self with start and end values multiplied by the
        amount given via the input value argument, where the value argument
        is a numeric primitive or BaseInterval-descendant class instance.
        """
        copy = self.copy()
        beg, end = self.__lvalue_get(value, op='*', i=_0s)
        copy.beg = min(self.beg * beg, self.beg * end,
                       self.end * beg, self.end * end)
        copy.end = max(self.beg * beg, self.beg * end,
                       self.end * beg, self.end * end)
        return copy


    def __neg__(self):
        """
        -self -> interval

        Return a copy of self with the numeric signs of start and end values
        negated.
        """
        copy = self.copy()
        copy.beg = -1 * self.end
        copy.end = -1 * self.beg
        return copy


    def __pos__(self):
        """
        +self -> interval
        
        Return a copy of self with the numeric signs of start and end values
        unchanged.
        """
        return self.copy()


    def __pow__(self, value):
        """
        self**mod -> interval
        pow(self, mod) -> interval

        Return a copy of self with the start and end values raised to the
        power of the input value argument, where the value argument is
        a numeric primitive or BaseInterval-descendant class instance. 
        
        The result is ill-defined if an input interval contains negative
        values and the exponent is a non-integer, in which case a ValueError
        is raised.
        """
        copy = self.copy()
        beg, end = self.__lvalue_get(value, op='*', i=_0s)
        copy.beg = min(pow(self.beg, beg), pow(self.beg, end),
                       pow(self.end, beg), pow(self.end, end))
        copy.end = max(pow(self.beg, beg), pow(self.beg, end),
                       pow(self.end, beg), pow(self.end, end))
        return copy

    
    def __radd__(self, value):
        """
        value + self -> interval

        Right-side addtion. Return a copy of self with the start and end
        values shifted by the amount given via the input value argument,
        where the value argument is a numeric primitive.
        """
        copy = self.copy()
        beg, end = self.__rvalue_get(value, op='+', i=_0s)
        copy.beg = beg + self.beg
        copy.end = end + self.end
        return copy
    

    def __rfloordiv__(self, value):
        """
        value // self -> Interval

        Right-side floor division. Return a copy of self with the start
        and end values divided by the amount given via the input value
        argument and then floored, where the value argument is a numeric
        primitive.

        The result is ill-defined if self contains 0, in which case a
        ZeroDivisionError is raised.
        """
        copy = self.copy()
        value, _ = self.__rvalue_get(value, op='//', i=_nulls)
        if self.beg == 0 and self.end == 0:
            raise ZeroDivisionError("division by zero")
        elif self.beg == 0:
            copy.beg = value / self.end
            copy.end = _POS_INF
        elif self.end == 0:
            copy.beg = _NEG_INF
            copy.end = value / self.beg
        else:
            copy.beg = min(value / self.beg, value / self.end)
            copy.end = max(value / self.beg, value / self.end)
        copy.beg = _floor(copy.beg, 1)
        copy.end = _floor(copy.end, 1)
        return copy


    def __rlshift__(self, value):
        """
        value << self -> interval

        Right-side bitwise left-shift. Return a copy of self with the input
        value argument bitwise left-shifted by the amount of self's start
        and end values, where the value argument is a numeric primitive.
        """        
        copy = self.copy()
        beg, end = self.__rvalue_get(value, op='<<', i=_0s)
        copy.beg = beg << self.beg
        copy.end = end << self.end
        return copy


    def __rmul__(self, value):
        """
        value * self -> interval

        Right-side multiplication. Return a copy of self with the start
        and end values multiplied by the amount given via the input value
        argument, where the value argument is a numeric primitive.
        """
        copy = self.copy()
        value, _ = self.__rvalue_get(value, op='*', i=_0s)
        copy.beg = min(value * self.beg, value * self.end)
        copy.end = max(value * self.beg, value * self.end)
        return copy


    def __rmod__(self, value):
        """
        value % self -> interval

        Right-side modulo. Return a copy of self with the input value
        argument module'd by the amount of self's start and end values,
        where the value argument is a numeric primitive.
        """
        copy = self.copy()
        value, _ = self.__rvalue_get(value, op='%', i=_0s)
        copy.beg = min(value % self.beg, value % self.end)
        copy.end = max(value % self.beg, value % self.end)
        return copy
    

    def __round__(self, ndigits=None):
        """
        round(self, ndigits) -> interval

        Return a copy of self with the start and end values rounded to 
        ndigits. Performs banker's rounding, same as built-in `round()`.
        """
        copy = self.copy()
        copy.beg = round(self.beg, ndigits)
        copy.end = round(self.end, ndigits)
        return copy

    
    def __rrshift__(self, value):
        """
        value >> self -> interval

        Right-side bitwise right-shift. Return a copy of self with the input
        value argument bitwise right-shifted by the amount of self's start
        and end values, where the value argument is a numeric primitive.
        """
        copy = self.copy()
        value, _ = self.__rvalue_get(value, op='>>', i=_0s)
        copy.beg = min(value >> self.beg, value >> self.end)
        copy.end = max(value >> self.beg, value >> self.end)
        return copy
    

    def __rshift__(self, value):
        """
        self >> value -> interval

        Return a copy of self with the start and end values bitwise right-
        shifted by the amount given via the input value argument, where the
        value argument is a numeric primitive or BaseInterval-descendant class
        instance.
        """
        copy = self.copy()
        beg, end = self.__lvalue_get(value, op='>>', i=_0s)
        copy.beg = self.beg >> beg
        copy.end = self.end >> end
        return copy


    def __rsub__(self, value):
        """
        value - self -> interval

        Right-side subtraction. Return a copy of self with the start and
        end values subtracted from the input value argument, where the
        value argument is a numeric primitive.
        """        
        copy = self.copy()
        value, _ = self.__rvalue_get(value, op='-', i=_0s)
        copy.beg = min(value - self.beg, value - self.end)
        copy.end = max(value - self.beg, value - self.end)
        return copy


    def __rtruediv__(self, value):
        """
        value / self -> interval

        Right-side division. Return a copy of self with the start and
        end values divided into the input value argument, where the
        value argument is a numeric primitive.
        """
        copy = self.copy()
        value, _ = self.__rvalue_get(value, op='/', i=_nulls)
        if self.beg == 0 and self.end == 0:
            raise ZeroDivisionError("division by zero")
        elif self.beg == 0:
            copy.beg = value / self.end
            copy.end = _POS_INF
        elif self.end == 0:
            copy.beg = _NEG_INF
            copy.end = value / self.beg
        else:
            copy.beg = min(value / self.beg, value / self.end)
            copy.end = max(value / self.beg, value / self.end)
        return copy
    

    def __sub__(self, value):
        """
        self - value -> interval

        Return a copy of self with the start and end values subtracted by
        the amount given via the input value argument, where input value
        is a numeric primitive or an BaseInterval-descendant class instance.
        """
        copy = self.copy()
        beg, end = self.__lvalue_get(value, op='-', i=_0s)
        copy.beg = self.beg - end
        copy.end = self.end - beg
        return copy


    def __truediv__(self, value):
        """
        self / value -> interval

        Return a copy of self with the start and end values divided by
        the amount given via the input value argument, where input value
        is a numeric primitive or BaseInterval-descendant class instance.

        The result is ill-defined if the input value contains 0, in which
        case a ZeroDivisionError is raised.
        """
        copy = self.copy()
        beg, end = self.__lvalue_get(value, op='/', i=_1s)
        if beg == 0 and end == 0:
            raise ZeroDivisionError("division by zero")
        elif beg == 0:
            copy.beg = min(self.beg / end, self.end / end)
            copy.end = _POS_INF
        elif end == 0:
            copy.beg = _NEG_INF
            copy.end = max(self.beg / beg, self.end / beg)
        else:
            copy.beg = min(self.beg / beg, self.end / beg,
                           self.beg / end, self.end / end)
            copy.end = max(self.beg / beg, self.end / beg,
                           self.beg / end, self.end / end)
        return copy


    def __trunc__(self):
        """
        Return a copy of self with the start and end values truncated to
        the Integral closest to x between 0 and x.
        """
        copy = self.copy()
        copy.beg = _int(self.beg)
        copy.end = _int(copy.end)
        return copy



class _IntervalSetInterface(object):
    __slots__ = ()
    
    # Interval and set methods
    def empty(self):
        """
        self.empty() -> None

        In-place empty. Set self's start and end values to 0.
        
        >>> interval = Interval("Chr", 15, 55)
        >>> interval.empty()
        >>> print(interval)
        Chr:0-0
        """
        self.beg = 0
        self.end = 0


    def null(self):
        """
        self.null() -> None

        In-place null. Set self's start and end values to nan and namespace
        to None.
        
        >>> interval = Interval("Chr", 15, 55)
        >>> interval.null()
        >>> print(interval)
        None:nan-nan
        """
        self.__init__()

        
    def __and__(self, other):
        """
        self & other -> Interval
        self.intersection(other) -> Interval

        Return an interval object of the same type as self representing
        the intersection of self and other. Disjoint intervals return a
        null object.

        >>> I1 = Interval("Chr", 1, 60)
        >>> I2 = Interval("Chr", 45, 80)
        >>> I1 & I2
        Interval(Chr:45-60)
        """
        return self.intersection(other)

    
    def __iand__(self, value):
        """
        self &= other -> None
        self.intersection_update(other) -> None

        In-place intersection. Update self with the intersection of itself
        and other.
        """
        self.intersection_update(value)


    def __rand__(self, other):
        """Raises TypeError"""
        raise TypeError(_BAD_OPERAND_TYPE('&',other,self))
        

    def __contains__(self, other):
        """
        other in self -> bool

        Returns a boolean indicating whether self is a superinterval of
        other.

        See `issuperinterval()` method documentation for more information.
        """
        return self.issuperinterval(other)


    def __or__(self, other):
        """
        self | other -> interval or 2-tuple
        self.union(other) -> interval or 2-tuple

        Return an interval object of the same type as self representing
        the union (inclusive OR) of self and other. If the two intervals
        are disjoint, return a 2-tuple containing the result intervals. 
        If the two intervals are abutting and `abutting=True`, return a
        single interval object.

        >>> Interval("Chr", 0, 60) | Interval("Chr", 45, 80)
        Interval(Chr:0-80)
        """
        return self.union(other)


    def __ior__(self, other):
        """Raises NotImplementedError."""
        self.union_update(other)
    

    def __ror__(self, other):
        """Raises TypeError"""
        raise TypeError(_BAD_OPERAND_TYPE('|',other,self))
        
        
    def __xor__(self, other):
        """
        self ^ other -> 2-tuple of Intervals
        self.symmetric_difference(other) -> 2-tuple of Intervals

        Returns a 2-tuple of interval objects representing the symmetric
        difference (exclusive OR, XOR) of self and other. The left-side
        and right-side objects are returned as the same class type(s) as
        the inputs, unless one interval is subinterval of another, then
        both objects returned are of the superinterval's type.

        >>> I1 = Interval("Chr", 1, 60)
        >>> I2 = Interval("Chr", 45, 80)
        >>> I1.symmetric_difference(I2)
        (Interval(Chr:1-45), Interval(Chr:60-80))
        """
        return self.symmetric_difference(other)


    def __ixor__(self, other):
        """Raises NotImplementedError."""
        self.symmetric_difference_update(other)
    

    def __rxor__(self, other):
        """Raises TypeError"""
        raise TypeError(_BAD_OPERAND_TYPE('^',other,self))

        
    def isabutting(self, other):
        """
        self.isabutting(other) -> bool

        Return a boolean indicating whether self is abutting the start
        or end of other.

        >>> Interval("Chr", 30, 40).isabutting(Interval("Chr", 40, 60))
        True
        """
        return self.isabutting_beg(other) or self.isabutting_end(other)
    

    def isabutting_beg(self, other):
        """
        self.isabutting_beg(other) -> bool

        Return a boolean indicating whether self abutts the start of other.

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

        Return a boolean indicating whether self abutts the end of other.

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

        Return a boolean indicating whether self is a superinterval of 
        other. When `strict=True`, evaluate to True only when self is a
        strict superinterval of other, i.e. when:
        self.start < other.start and other.end < self.end

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

        Return a boolean indicating whether self is a subinterval of 
        other. When `strict=True`, evaluate to True only when self is
        a strict subinterval of other, i.e. when:
        other.start < self.start and self.end < other.end

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
        return other.issuperinterval(self, strict=strict)


    def isintersecting(self, other):
        """
        self.isintersecting(other) -> bool

        Return a boolean indicating whether self intersects other.

        >>> Interval("Chr", 20, 60).isintersecting(Interval("Chr", 40, 80))
        True
        """
        return ((self.namespace == other.namespace) and
                (other.beg <= self.end and self.beg <= other.end))
    

    def isintersecting_beg(self, other):
        """
        self.isintersecting_beg(other) -> bool

        Return a boolean indicating whether other's start value is
        contained within self's interval range.

        >>> Interval("Chr", 20, 60).isintersecting_beg(Interval("Chr", 40, 80))
        True
        >>> Interval("Chr", 40, 80).isintersecting_beg(Interval("Chr", 20, 60))
        False
        """
        # self.beg *=========* self.end
        #      other.beg *==============* other.end
        return ((self.namespace == other.namespace) and
                (self.beg <= other.beg <= self.end <= other.end))


    def isintersecting_end(self, other):
        """
        self.isintersecting_end(other) -> bool

        Return a boolean indicating whether other's end value is
        contained within self's interval range.

        >>> Interval("Chr", 40, 80).isintersecting_end(Interval("Chr", 20, 60))
        True
        >>> Interval("Chr", 20, 60).isintersecting_end(Interval("Chr", 40, 80))
        False
        """
        #           self.beg *=========* self.end
        # other.beg *==============* other.end            
        return ((self.namespace == other.namespace) and
                (other.beg <= self.beg <= other.end <= self.end))


    def intersection_length(self, other):
        """
        self.intersection_length(other) -> value

        Return the intersection length between two intervals, or 0 if none.

        >>> Interval("Chr", 20, 60).intersection_length(Interval("Chr", 40, 70))
        20
        """
        if self.namespace == other.namespace:
            return max(0, min(self.end, other.end) - max(self.beg, other.beg))
        return 0
        

    def intersection_fraction(self, other):
        """
        self.intersection_fraction(other) -> float

        Return the intersection length as a fraction of self, or 0 if none.

        >>> I1 = Interval("Chr", 20, 60)
        >>> I2 = Interval("Chr", 40, 70)
        >>> I1.intersection_fraction(I2)
        0.5
        """
        return float(self.intersection_length(other)) / max(1, self.end - self.beg)
    
    
    def inner_distance(self, other):
        """
        self.inner_distance(other) -> value

        Return the minimum distance between the start values and end 
        values of self and other. Negative distances indicate other is
        upstream of self. Abutting and intersecting intervals return 0.

        >>> I1 = Interval("Chr", 10, 20)
        >>> I2 = Interval("Chr", 45, 80)
        >>> I1.inner_distance(I2)
        25
        >>> I2.inner_distance(I1)
        -25
        """
        if self.isnull() or other.isnull():
            return _POS_INF
        if self.isintersecting(other):
            return 0
        if self < other:
            return other.beg - self.end
        if self > other:
            return other.end - self.beg
        return _POS_INF


    def jaccard_distance(self, other):
        """
        self.jaccard_distance(other) -> value

        Returns the Jaccard distance (1 - Jaccard similarity) between
        self and other.

        >>> I1 = Interval("Chr", 10, 20)
        >>> I2 = Interval("Chr", 15, 30)
        >>> I1.jaccard_distance(I2)
        0.75
        """
        intersection_length = float(self.intersection_length(other))
        return 1.0 - intersection_length / (
            (self.end - self.beg) + (other.end - other.beg)
            - intersection_length
        )

    
    def outer_distance(self, other, maxrange=False):
        """
        self.outer_distance(other) -> value
        self.outer_distance(other, maxrange=True) -> value

        Return the maximum distance between the start values and end
        values of self and other. Negative distances indicate other
        is upstream of self.

        >>> I1 = Interval("Chr", 10, 17)
        >>> I2 = Interval("Chr", 5, 8)
        >>> I1.outer_distance(I2)
        -12

        If `maxrange=True`, the outer distance of intersecting
        intervals is calculated as min(self.start, other.start) and 
        max(self.end, other.end).

        >>> I1 = Interval("Chr", 10, 20)
        >>> I2 = Interval("Chr", 15, 18)
        >>> I1.outer_distance(I2)
        8
        >>> I1.outer_distance(I2, maxrange=True)
        10
        """
        if self.isnull() or other.isnull():
            return _POS_INF
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
        return _POS_INF
    

    def difference(self, other):
        """
        self - other -> interval or 2-tuple
        self.difference(other) -> interval or 2-tuple
        
        Return an interval, or 2-tuple of intervals, of the same type 
        as self representing the difference of self and other. 
    
        If self and other are disjoint, return a copy of self. 
        If self contains other, return a tuple containing two intervals. 
        If self is a subinterval of other, return a null interval object.

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
            copy.null()
        elif other.isintersecting_beg(self):
            copy.beg = other.end
        elif other.isintersecting_end(self):
            copy.end = other.beg            
        elif other.issubinterval(self):
            copy.end = other.beg
            kopy = self.copy()
            kopy.beg = other.end
            return (copy, kopy)
        return copy


    def difference_update(self, other):
        """Raises NotImplementedError."""
        raise NotImplementedError(_ILL_DEFINED('difference'))
        

    def hull(self, other=None):
        """
        self.hull() -> interval
        self.hull(other) -> interval

        Return an interval object the same type as self represeting the
        smallest interval closure of self (and, optionally, other). 
        """
        copy = self.copy()
        if other and self.namespace == other.namespace:
            copy.beg = min(copy.beg, other.beg)
            copy.end = max(copy.end, other.end)
        return copy
    
        
    def intersection(self, other):
        """
        self & other -> interval
        self.intersection(other) -> interval

        Return an interval object the same type as self representing the
        intersection of self and other. Disjoint intervals return a null
        object.

        >>> I1 = Interval("Chr", 1, 60)
        >>> I2 = Interval("Chr", 45, 80)
        >>> I1.intersection(I2)
        Interval(Chr:45-60)
        """
        copy = self.copy()
        if self.isintersecting(other):
            copy.beg = max(self.beg, other.beg)
            copy.end = min(self.end, other.end)
        elif self.namespace == other.namespace:
            copy.beg = _NULL_POS
            copy.end = _NULL_POS
        else:
            copy.null()
        return copy


    def intersection_update(self, other):
        """
        self &= other -> None
        self.intersection_update(other) -> None

        In-place intersection. Update self with the intersection of 
        itself and other.
        """
        copy = self.intersection(other)
        self.namespace = copy.namespace
        self.beg = copy.beg
        self.end = copy.end


    def symmetric_difference(self, other):
        """
        self ^ other -> 2-tuple of intervals
        self.symmetric_difference(other) -> 2-tuple of intervals

        Return a 2-tuple of interval objects representing the symmetric
        difference (exclusive OR, XOR) of self and other. The left- and
        right-side objects are returned as the same types as self and
        other, respectively, unless one interval is a subinterval of 
        another, in which case both objects returned are of the 
        superinterval's type.

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
        raise NotImplementedError(_ILL_DEFINED('symmetric_difference'))
    

    def union(self, other, abutting=False):
        """
        self | other -> Interval or 2-tuple
        self.union(other) -> Interval or 2-tuple

        Return an interval object the same type as self representing
        the union (inclusive OR) of self and other. If the two intervals
        are disjoint, return a tuple containing two intervals with left-
        and right-side objects the same types as self and other, 
        respectively. If self and other are abutting and `abutting=True`,
        return a single interval object.

        >>> Interval("Chr", 0, 60).union(Interval("Chr", 45, 80))
        Interval(Chr:0-80)
        """
        if self.isempty():
            return other.copy()
        if other.isempty():
            return self.copy()
        copy = self.copy()
        if self.isintersecting(other):
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
        raise NotImplementedError(_ILL_DEFINED('union'))

    
    def isdisjoint(self, other):
        """
        self.isdisjoint(other) -> bool

        Return a boolean indicating whether self and other are disjoint
        (non-intersecting) intervals.

        >>> Interval("Chr", 0, 20).isdisjoint(Interval("Chr", 45, 80))
        True
        >>> Interval("Chr", 0, 60).isdisjoint(Interval("Chr", 45, 80))
        False
        """
        return not self.isintersecting(other)
    

    def isempty(self):
        """
        self.isempty() -> bool

        Return a boolean indicating whether self is an invalid interval
        range. If self is null this method will return True.
        """
        return not (self.beg <= self.end)


    def isfinite(self):
        """
        self.isfinite() -> bool

        Return a boolean indicating whether self is a finite interval.
        """
        return _isfinite(self.beg) and _isfinite(self.end)

    
    def isnull(self):
        """
        self.isnull() -> bool

        Return a boolean indicating whether either start or end are
        null (nan) values.
        """
        return _isnull(self.beg) or _isnull(self.end)


    def issingleton(self):
        """
        self.issingleton() -> bool

        Return a boolean indicating whether start == end.
        """
        # nan == nan -> False
        return self.beg == self.end


    clear = null
    
    isabutting_start = isabutting_beg

    isabutting_stop = isabutting_end
    
    isintersecting_start = isintersecting_beg

    isintersecting_stop = isintersecting_end

    issubset = issubinterval

    issuperset = issuperinterval

    update = union_update

    

class _IntervalIdentityInterface(object):
    __slots__ = ()
    
    def __bool__(self):
        """
        bool(self) -> bool

        Return a boolean indicating whether self is non-empty.
        
        >>> bool(Interval("Chr", 350, 475))
        True
        >>> bool(Interval())
        False
        """
        return (self.beg < self.end)


    def __hash__(self):
        """
        hash(self) -> int

        Return a runtime-unique id for self.
        
        >>> hash(Interval("Chr", 350, 475))
        4465105936
        """
        return id(self)
        

    def __repr__(self):
        """
        repr(self) -> str

        Return a string representation of self.
        
        >>> repr(Interval("Chr", 350, 475))
        'BaseInterval([350, 475, namespace=Chr])'
        """
        return "%s(%s)" % (self.__class__.__name__, str(self))

    
    def __str__(self):
        """
        str(self) -> str

        Return a string representation of self.
        
        >>> str(Interval("Chr", 350,475))
        '[350, 475, namespace=None]'
        """
        return "[%s, %s, namespace=%s]" %(
            str(self.beg), str(self.end), str(self.namespace)
        )

    
    def __eq__(self, other):
        """
        self == other -> bool

        Return a boolean indicating whether self is positionally equal
        to other. Null objects are always non-equal. If self and other
        are in different namespaces, return False.
        """
        return ((self.namespace == other.namespace) and
                (self.beg == other.beg) and
                (self.end == other.end))
    

    def __gt__(self, other):
        """
        self > other -> bool

        Return a boolean indicating whether self is positionally 
        greater-than other. If self and other are in different 
        namespaces, return False.
        """
        return ((self.namespace == other.namespace) and
                ((self.beg > other.beg) or
                 (self.beg == other.beg) and
                 (self.end > other.end)))


    def __ge__(self, other):
        """
        self >= other -> bool

        Return a boolean indicating whether self is positionally 
        greater-than or equal-to other. If self and other are in
        different namespaces, return False.
        """
        return self == other or self > other
    

    def __lt__(self, other):
        """
        self < other -> bool

        Return a boolean indicating whether self is positionally 
        less-than other. If self and other are in different 
        namespaces, return False.
        """
        return ((self.namespace == other.namespace) and
                ((self.beg < other.beg) or
                 (self.beg == other.beg) and
                 (self.end < other.end)))


    def __le__(self, other):
        """
        self <= other -> bool

        Return a boolean indicating whether self is positionally 
        less-than or equal-to other. If self and other are in different 
        namespaces, return False.
        """
        return self == other or self < other


    def __ne__(self, other):
        """
        self != other -> bool

        Return a boolean indicating whether self is not positionally
        equal to other. If self and other are in different namespaces,
        return True.
        """
        return not (self == other)


    def to_string(self):
        return self.__str__()


    
class BaseInterval(
        _IntervalSetInterface,
        _IntervalIdentityInterface,
        _IntervalArithmeticInterface):
    """
    Base class representing generic one-dimensional intervals.

    The `self.namespace` attribute provides an abstraction allowing 
    this module access to a stable id or name and enable comparions
    between objects in potentially different namespaces (X, Y, or Z
    dimensions, sequence names, etc.).
    """
    # To maintain memory and speed efficiency, every child object
    # must also define __slots__ = ()
    __slots__ = ('namespace','_beg','_end')
    
    # Constructor, descriptor, and introspection methods:
    def __init__(self, beg=_NULL_POS, end=_NULL_POS, namespace=_NULL_NAME):
        self.namespace = namespace
        self.beg = beg  # sets self._beg
        self.end = end  # sets self._end


    @property
    def beg(self):
        """
        self.beg -> value

        Return self's start numeric value (0-based).

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

        Return self's start numeric value (0-based).
        
        >>> interval.start = 350
        >>> print(interval.start)
        350
        """
        return self._beg


    @start.setter
    def start(self, start):
        self._beg = start


    @property
    def mid(self):
        """
        self.mid -> value

        Return self's midpoint value.
        
        >>> print(self.mid)
        412.5
        """
        return _NULL_POS \
            if   self.isempty() \
            else (self.beg + (self.end - self.beg) / 2.0)


    @property
    def end(self):
        """
        self.end -> value

        Return self's end value (1-based).
        
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
        
        Return self's end value (1-based).
        
        >>> interval.stop = 500
        >>> print(interval.stop)
        500
        """
        return self._end


    @stop.setter
    def stop(self, stop):
        self._end = stop
        

    def __len__(self):
        """
        len(self) -> value

        Return the length of the interval.
        """
        return 0 if self.isempty() else (self.end - self.beg)

        
    def copy(self, deep=False):
        """
        self.copy() -> interval
        self.copy(deep=True) -> interval

        Return a copy of self.

        If `deep=False`, return a shallow copy of the interval object.
        If `deep=True`, return a deep copy of the interval object.

        >>> interval = Interval("Chr", 350, 475)
        >>> interval.copy() is interval
        False
        """
        return _deepcopy(self) if deep else _copy(self)
        

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
   

    
class ClosedInterval(BaseInterval):
    """
    Class representing a generic fully-closed continuous interval; 
    i.e., start and end coordinates may be floating-point
    values, and are inclusive in interval intersection.

    The `self.namespace` attribute provides an abstraction allowing 
    this module access to a stable id or name and enable comparions
    between objects in potentially different namespaces (X, Y, or Z
    dimensions, sequence names, etc.).
    """
    # To maintain memory and speed efficiency, every child object
    # must also define __slots__ = ()
    __slots__ = ()
    
    def __init__(self, beg=_NULL_POS, end=_NULL_POS, namespace=_NULL_NAME):
        """
        >>> ClosedInterval("Chr1", 15, 37) -> ClosedInterval
        """
        super().__init__(beg=beg, end=end, namespace=namespace)

    

class LeftClosedInterval(BaseInterval):
    """
    Class representing a generic left-closed, right-open continuous
    interval; i.e., start and end coordinates may be
    floating-point values, with start inclusive in interval
    intersection and exclusive end.

    The `self.namespace` attribute provides an abstraction allowing 
    this module access to a stable id or name and enable comparions
    between objects in potentially different namespaces (X, Y, or Z
    dimensions, sequence names, etc.).
    """
    __slots__ = ()

    def issuperinterval(self, other, strict=False):
        """
        self.issuperinterval(other) -> bool

        Return a boolean indicating whether self is a superinterval of other.
        When `strict=True`, evaluate to True only when self is a strict 
        superinterval of other, i.e. when:
        self.start < other.start and other.end < self.end

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

        Return a boolean indicating whether self is a subinterval of other. 
        When `strict=True`, evaluate to True only when self is a strict
        subinterval of other, i.e. when:
        other.start < self.start and self.end < other.end

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

    
    def isintersecting(self, other):
        """
        self.isintersecting(other) -> bool

        Return a boolean indicating whether self intersects other.

        >>> Interval("Chr", 20, 60).isintersecting(Interval("Chr", 40, 80))
        True
        """
        return ((self.namespace == other.namespace) and
                (other.beg < self.end and self.beg < other.end))


    def isintersecting_beg(self, other):
        """
        self.isintersecting_beg(other) -> bool

        Return a boolean indicating whether other's start value is
        contained within self's interval range.

        >>> Interval("Chr", 20, 60).isintersecting_beg(Interval("Chr", 40, 80))
        True
        >>> Interval("Chr", 40, 80).isintersecting_beg(Interval("Chr", 20, 60))
        False
        """
        # self.beg *=========o self.end
        #      other.beg *==============o other.end
        return ((self.namespace == other.namespace) and
                (self.beg <= other.beg < self.end < other.end))


    def isintersecting_end(self, other):
        """
        self.isintersecting_end(other) -> bool

        Return a boolean indicating whether other's end value is
        contained within self's interval range.

        >>> Interval("Chr", 40, 80).isintersecting_end(Interval("Chr", 20, 60))
        True
        >>> Interval("Chr", 20, 60).isintersecting_end(Interval("Chr", 40, 80))
        False
        """
        #           self.beg *=========o self.end
        # other.beg *==============o other.end            
        return ((self.namespace == other.namespace) and
                (other.beg < self.beg < other.end <= self.end))

    
    isintersecting_start = isintersecting_beg

    isintersecting_stop = isintersecting_end

    issubset = issubinterval

    issuperset = issuperinterval



class Interval(_IntervalIndexInterface, LeftClosedInterval):
    """
    Class representing a generic left-closed, right-open discrete
    interval; i.e., start and end coordinates only permit
    integer values, with start (0-based) inclusive in interval
    intersection and exclusive end (1-based).

    The `self.namespace` attribute provides an abstraction allowing 
    this module access to a stable id or name and enable comparions
    between objects in potentially different namespaces (X, Y, or Z
    dimensions, sequence names, etc.).
    """
    __slots__ = ()
    
    def __init__(self, name=_NULL_NAME, beg=_NULL_POS, end=_NULL_POS):
        """
        >>> Interval("Chr1", 15, 37) -> Interval
        """
        super().__init__(namespace=name, beg=beg, end=end)

        
    def __str__(self):
        """
        str(self) -> str

        Return a string representation of self.

        >>> str(Interval("Chr", 350,475))
        'Chr:350-475'
        """
        return "%s:%s-%s" % (str(self.namespace), str(self.beg), str(self.end))


    @property
    def name(self):
        """
        self.name -> value

        Return the namespace attribute of self.
        
        In an inheriting child class, if the `namespace` attribute
        is best defined by another attribute (e.g., as `self.contig`, 
        `self.scaff`, `self.chrom`, etc.) for the purpose of the class,
        the `self.namespace` attribute will require initializization
        in the `__init__()` method.

        For example: 
            def __init__(self, chrom, beg, end):
                super().__init__(namespace=chrom, beg=beg, end=end)
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



class ClosedPoint(ClosedInterval):
    __slots__ = ()
    
    def __init__(self, pos=_NULL_POS, namespace=_NULL_NAME):
        """
        >>> ClosedPoint("Chr1", 37) -> ClosedPoint
        """
        super().__init__(beg=pos, end=pos, namespace=namespace)


    def __bool__(self):
        return not self.isempty()
        

    def __index__(self):
        return self.beg

    
    @property
    def beg(self):
        """
        self.beg -> value

        Return self's start numeric value.

        >>> point.beg = 350
        >>> print(point.beg)
        350
        """
        return self._beg


    @beg.setter
    def beg(self, beg):
        self._beg = beg
        self._end = beg

        
    @property
    def end(self):
        """
        self.end -> value

        Return self's end value.

        >>> point.end = 500
        >>> print(point.end)
        500
        """
        return self._end


    @end.setter
    def end(self, end):
        self._beg = end
        self._end = end
    
    
    @property
    def mid(self):
        """
        self.mid -> value

        Return self's midpoint value.

        >>> print(point.mid)
        412
        """        
        return _NULL_POS if self.isempty() else self.end


    @property
    def pos(self):
        """
        self.pos -> value

        Return self's position value. Alias for beg/start and end,
        since they are equal for a point.
        """
        return self.end


    @pos.setter
    def pos(self, pos):
        self.end = pos

        
    def isempty(self):
        return self.isnull()
        

    def issingleton(self):
        """
        self.issingleton() -> True

        Return a boolean indicating whether self is a singleton interval.

        A point is a singleton, so always returns True.
        """
        return True
    


class LeftClosedPoint(LeftClosedInterval):
    __slots__ = ()
    
    def __init__(self, pos=_NULL_POS, namespace=_NULL_NAME):
        """
        >>> LeftClosedPoint("Chr1", 37) -> LeftClosedPoint
        """
        super().__init__(namespace=namespace)
        self.pos = pos

        
    @property
    def pos(self):
        return self.end


    @pos.setter
    def pos(self, pos):
        self.beg = pos
        self.end = pos



class Point(_IntervalIndexInterface, LeftClosedPoint):
    """
    Class representing a generic left-closed, right-open discrete
    point; i.e., start and end coordinates only permit
    integer values, with start (0-based) inclusive in interval
    intersection and exclusive end (1-based).

    The `self.namespace` attribute provides an abstraction allowing 
    this module access to a stable id or name and enable comparions
    between objects in potentially different namespaces (X, Y, or Z
    dimensions, sequence names, etc.).
    """    
    __slots__ = ()

    def __init__(self, name=_NULL_NAME, pos=_NULL_POS):
        """
        >>> Point("Chr1", 37) -> Point
        """
        super().__init__(pos=pos, namespace=name)
        

    def __str__(self):
        """
        str(self) -> str

        Return a string representation of the object.

        >>> str(Point("Chr", 350,475))
        'Chr:350-475'
        """
        return "%s:%s" % (str(self.namespace), str(self.end))

        
    @property
    def beg(self):
        """
        self.beg -> int

        The beginning (0-based) coordinate of the point.

        >>> point.beg = 350
        >>> print(point.beg)
        350
        >>> print(point.end)
        351
        """
        return self._beg

    
    @beg.setter
    def beg(self, beg):
        self._beg = _int(beg)
        self._end = _int(beg) + 1

        
    @property
    def end(self):
        """
        self.end -> int

        The ending (1-based) coordinate of the point.

        >>> point.end = 500
        >>> print(point.beg)
        499
        >>> print(point.end)
        500
        """        
        return self._end

    
    @end.setter
    def end(self, end):
        self._beg = _int(end) - 1
        self._end = _int(end)
    
    
    @property
    def pos(self):
        return self.beg


    @pos.setter
    def pos(self, pos):
        self.beg = pos


    @property
    def name(self):
        """
        self.name -> value
        
        Return the namespace attribute of self.

        In an inheriting child class, if the `namespace` attribute
        is best defined by another attribute (e.g., as `self.contig`, 
        `self.scaff`, `self.chrom`, etc.) for the purpose of the class,
        the `self.namespace` attribute will require initializization
        in the `__init__()` method.

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


        
#       10        20        30        40        50        60        70        80
#---+----|----+----|----+----|----+----|----+----|----+----|----+----|----+----|



# NOTES:
# - builtin numeric types all have a .real, .imag, and .conjugate attributes
#
# - Bounded intervals are bounded sets, in the sense that their diameter 
#   (which is equal to the absolute difference between the endpoints) is 
#   finite. The diameter may be called the length, width, measure, range,
#   or size of the interval. The size of unbounded intervals is usually 
#   defined as +∞, and the size of the empty interval may be defined as 0
#   (or left undefined).
