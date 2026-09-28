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

from .constants import NULL_NAMESPACE as _NULL_NAME
from .constants import NULL_POSITION as _NULL_POS
from .interfaces import (
    _IntervalArithmeticInterface,
    _IntervalIdentityInterface,
    _IntervalIntegerInterface,
    _IntervalSetInterface,
    _numeric,
    _int
)


    
class BaseInterval(
        _IntervalSetInterface,
        _IntervalIdentityInterface,
        _IntervalArithmeticInterface
    ):
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



class Interval(_IntervalIntegerInterface, LeftClosedInterval):
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
        self._beg = _numeric(beg)
        self._end = _numeric(beg)

        
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
        self._beg = _numeric(end)
        self._end = _numeric(end)
    
    
    @property
    def mid(self):
        """
        self.mid -> value

        Return self's midpoint value.

        >>> print(point.mid)
        412
        """        
        return _NULL_POS if self.isempty() else self.beg


    @property
    def pos(self):
        """
        self.pos -> value

        Return self's position value. Alias for beg/start and end,
        since they are equal for a point.
        """
        return self.beg


    @pos.setter
    def pos(self, pos):
        self.beg = pos

        
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
        self._beg = _numeric(beg)
        self._end = _numeric(beg)


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
        self._beg = _numeric(end)
        self._end = _numeric(end)

        
    @property
    def pos(self):
        return self.beg


    @pos.setter
    def pos(self, pos):
        self.beg = pos
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



class Point(_IntervalIntegerInterface, LeftClosedPoint):
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
