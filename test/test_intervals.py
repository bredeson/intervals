
#TODO: Add test cases for IntervalList methods that accept negative indices
#TODO: Add test cases for negative IntervalList._length

from unittest import TestCase
from intervals import (
    BaseInterval,
    ClosedInterval,
    ClosedPoint,
    LeftClosedInterval,
    LeftClosedPoint,
    Interval,
    Point,
    IntervalList,
)
from intervals.collections import _Node
from collections import deque
from math import isnan, nan, isinf, inf
from copy import copy


class TestCase000_BaseInterval(TestCase):
    constructor = BaseInterval
        
    def test__init__0(self):
        i = self.constructor()
        self.assertIsInstance(i, self.constructor)
        self.assertIsNone(i.namespace)
        self.assertTrue(isnan(i.beg))
        self.assertTrue(isnan(i.end))
            
    def test__init__1(self):
        i = self.constructor(namespace="chr")
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i.namespace, "chr")
        self.assertTrue(isnan(i.beg))
        self.assertTrue(isnan(i.end))        

    def test__init__2(self):
        i = self.constructor(25, 125, namespace="chr")
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i.namespace, "chr")
        self.assertEqual(i.beg, 25)
        self.assertEqual(i.end, 125)
    
    def test_namespace_0(self):
        self.assertTrue(hasattr(self.constructor(), 'namespace'))
    
    def test_beg_0(self):
        self.assertTrue(hasattr(self.constructor(), 'beg'))
        self.assertTrue(hasattr(self.constructor(), 'start'))

    def test_mid_0(self):
        self.assertTrue(hasattr(self.constructor(), 'mid'))

    def test_end_0(self):
        self.assertTrue(hasattr(self.constructor(), 'end'))
        self.assertTrue(hasattr(self.constructor(), 'stop'))

    def test_isnull_0(self):
        self.assertTrue(hasattr(self.constructor(), 'isnull'))

    def test_isempty_0(self):
        self.assertTrue(hasattr(self.constructor(), 'isempty'))

    def test_copy_0(self):
        self.assertTrue(hasattr(self.constructor(), 'copy'))

    def test_to_slice_0(self):
        self.assertTrue(hasattr(self.constructor(), 'to_slice'))

    def test__abs__0(self):
        self.assertTrue(hasattr(self.constructor(), '__abs__'))

    def test__add__0(self):
        self.assertTrue(hasattr(self.constructor(), '__add__'))

    def test__and__0(self):
        self.assertTrue(hasattr(self.constructor(), '__and__'))

    def test__bool__0(self):
        self.assertTrue(hasattr(self.constructor(), '__bool__'))

    def test__ceil__0(self):
        self.assertTrue(hasattr(self.constructor(), '__ceil__'))

    def test__contains__0(self):
        self.assertTrue(hasattr(self.constructor(), '__contains__'))

    def test__eq__0(self):
        self.assertTrue(hasattr(self.constructor(), '__eq__'))

    def test__floor__0(self):
        self.assertTrue(hasattr(self.constructor(), '__floor__'))

    def test__floordiv__0(self):
        self.assertTrue(hasattr(self.constructor(), '__floordiv__'))

    def test__ge__0(self):
        self.assertTrue(hasattr(self.constructor(), '__ge__'))

    def test__gt__0(self):
        self.assertTrue(hasattr(self.constructor(), '__gt__'))

    def test__hash__0(self):
        self.assertTrue(hasattr(self.constructor(), '__hash__'))

    def test__iadd__0(self):
        self.assertTrue(hasattr(self.constructor(), '__iadd__'))

    def test__imul__0(self):
        self.assertTrue(hasattr(self.constructor(), '__imul__'))

    def test__isub__0(self):
        self.assertTrue(hasattr(self.constructor(), '__isub__'))

    def test__le__0(self):
        self.assertTrue(hasattr(self.constructor(), '__le__'))

    def test__len__0(self):
        self.assertTrue(hasattr(self.constructor(), '__len__'))

    def test__lt__0(self):
        self.assertTrue(hasattr(self.constructor(), '__lt__'))

    def test__lshift__0(self):
        self.assertTrue(hasattr(self.constructor(), '__lshift__'))

    def test__mul__0(self):
        self.assertTrue(hasattr(self.constructor(), '__mul__'))

    def test__ne__0(self):
        self.assertTrue(hasattr(self.constructor(), '__ne__'))

    def test__or__0(self):
        self.assertTrue(hasattr(self.constructor(), '__or__'))

    def test_radd_0(self):
        self.assertTrue(hasattr(self.constructor(), '__radd__'))

    def test_rfloordiv_0(self):
        self.assertTrue(hasattr(self.constructor(), '__rfloordiv__'))
        
    def test__rlshift__0(self):
        self.assertTrue(hasattr(self.constructor(), '__rlshift__'))

    def test_rmul_0(self):
        self.assertTrue(hasattr(self.constructor(), '__rmul__'))

    def test__rshift__0(self):
        self.assertTrue(hasattr(self.constructor(), '__rshift__'))

    def test__rsub__0(self):
        self.assertTrue(hasattr(self.constructor(), '__rsub__'))

    def test__rtruediv__0(self):
        self.assertTrue(hasattr(self.constructor(), '__rtruediv__'))

    def test__sub__0(self):
        self.assertTrue(hasattr(self.constructor(), '__sub__'))

    def test__truediv__0(self):
        self.assertTrue(hasattr(self.constructor(), '__truediv__'))

    def test__xor__0(self):
        self.assertTrue(hasattr(self.constructor(), '__xor__'))

    def test_isabutting_beg_0(self):
        self.assertTrue(hasattr(self.constructor(), 'isabutting_beg'))

    def test_isabutting_end_0(self):
        self.assertTrue(hasattr(self.constructor(), 'isabutting_end'))

    def test_issuperinterval_0(self):
        self.assertTrue(hasattr(self.constructor(), 'issuperinterval'))

    def test_difference_0(self):
        self.assertTrue(hasattr(self.constructor(), 'difference'))

    def test_difference_update_0(self):
        self.assertTrue(hasattr(self.constructor(), 'difference_update'))

    def test_inner_distance_0(self):
        self.assertTrue(hasattr(self.constructor(), 'inner_distance'))

    def test_intersection_0(self):
        self.assertTrue(hasattr(self.constructor(), 'intersection'))

    def test_intersection_update_0(self):
        self.assertTrue(hasattr(self.constructor(), 'intersection_update'))

    def test_isdisjoint_0(self):
        self.assertTrue(hasattr(self.constructor(), 'isdisjoint'))

    def test_issubset_0(self):
        self.assertTrue(hasattr(self.constructor(), 'issubset'))
        # just an alias of issubinterval()

    def test_issuperset_0(self):
        self.assertTrue(hasattr(self.constructor(), 'issuperset'))
        # just an alias of issuperinterval()

    def test_jaccard_distance_0(self):
        self.assertTrue(hasattr(self.constructor(), 'jaccard_distance'))

    def test_outer_distance_0(self):
        self.assertTrue(hasattr(self.constructor(), 'outer_distance'))

    def test_intersection_fraction_0(self):
        self.assertTrue(hasattr(self.constructor(), 'intersection_fraction'))

    def test_intersection_length_0(self):
        self.assertTrue(hasattr(self.constructor(), 'intersection_length'))

    def test_isintersecting_0(self):
        self.assertTrue(hasattr(self.constructor(), 'isintersecting'))

    def test_isintersecting_beg_0(self):
        self.assertTrue(hasattr(self.constructor(), 'isintersecting_beg'))

    def test_isintersecting_end_0(self):
        self.assertTrue(hasattr(self.constructor(), 'isintersecting_end'))

    def test_symmetric_difference_0(self):
        self.assertTrue(hasattr(self.constructor(), 'symmetric_difference'))

    def test_symmetric_difference_update_0(self):
        self.assertTrue(hasattr(self.constructor(), 'symmetric_difference_update'))

    def test_to_slice_0(self):
        self.assertTrue(hasattr(self.constructor(), 'to_slice'))

    def test_to_string_0(self):
        self.assertTrue(hasattr(self.constructor(), 'to_string'))

    def test__str__0(self):
        self.assertTrue(hasattr(self.constructor(), '__str__'))

    def test_union_0(self):
        self.assertTrue(hasattr(self.constructor(), 'union'))

    def test_issubinterval_0(self):
        self.assertTrue(hasattr(self.constructor(), 'issubinterval'))


        
class TestCase001_ClosedInterval(TestCase000_BaseInterval):
    constructor = ClosedInterval

        

class TestCase002_LeftClosedInterval(TestCase000_BaseInterval):
    constructor = LeftClosedInterval

        

class TestCase004_Interval(TestCase000_BaseInterval):
    constructor = Interval
            
    def test__init__1(self):
        i = self.constructor("chr")
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i.namespace, "chr")
        self.assertTrue(isnan(i.beg))
        self.assertTrue(isnan(i.end))        

    def test__init__2(self):
        i = self.constructor("chr", 25, 125)
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i.namespace, "chr")
        self.assertEqual(i.beg, 25)
        self.assertEqual(i.end, 125)

    def test_name_0(self):
        self.assertTrue(hasattr(self.constructor(), 'name'))

    def test_name_1(self):
        self.assertTrue(hasattr(self.constructor(), 'name'))        

    def test_name_getter_1(self):
        self.assertIsNone(self.constructor().name)

    def test_name_getter_2(self):
        self.assertEqual(self.constructor("chr1").name, "chr1")
        
    def test_name_setter_1(self):
        i = self.constructor()
        self.assertIsNone(i.name)
        self.assertIsNone(i.namespace)
        i.name = "chr"
        self.assertEqual(i.name, "chr")
        self.assertEqual(i.namespace, "chr")

        
        
class TestCase005_ClosedPoint(TestCase000_BaseInterval):
    constructor = ClosedPoint

    def test__init__1(self):
        i = self.constructor(namespace="chr")
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i.namespace, "chr")
        self.assertTrue(isnan(i.beg))
        self.assertTrue(isnan(i.end))        

    def test__init__2(self):
        i = self.constructor(125, namespace="chr")
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i.namespace, "chr")
        self.assertEqual(i.beg, 125)
        self.assertEqual(i.end, 125)

    def test_pos_0(self):
        self.assertTrue(hasattr(self.constructor(),'pos'))

    
        
        
class TestCase006_LeftClosedPoint(TestCase005_ClosedPoint):
    constructor = LeftClosedPoint
        

        
class TestCase008_Point(TestCase005_ClosedPoint):
    constructor = Point

    def test__init__1(self):
        i = self.constructor("chr")
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i.namespace, "chr")
        self.assertTrue(isnan(i.beg))
        self.assertTrue(isnan(i.end))        

    def test__init__2(self):
        i = self.constructor("chr", 125)
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i.namespace, "chr")
        self.assertEqual(i.beg, 125)
        self.assertEqual(i.end, 126)

    def test_mid_0(self):
        self.assertTrue(hasattr(self.constructor(), 'mid'))


        
        
class TestCase009_BaseInterval(TestCase):
    constructor = BaseInterval
    
    def setUp(self):
        self.interval0  = self.constructor(50, 100)
        self.interval1  = self.constructor(25,  75)
        self.interval2  = self.constructor(70,  75)
        self.interval3  = self.constructor(50,  75)
        self.interval4  = self.constructor( 0, 100)
        self.interval5  = self.constructor( 0,  50)
        self.interval6  = self.constructor(75, 100)
        self.interval7  = self.constructor(75, 125)
        self.interval8  = self.constructor()
        self.interval9  = self.constructor(75, 100, namespace="other")
        self.interval10 = self.constructor(100, 110)
        self.interval11 = self.constructor(50, 90)
        self.interval12 = self.constructor(0, 1000)
        
    def tearDown(self):
        del(self.interval0)
        del(self.interval1)
        del(self.interval2)
        del(self.interval3)
        del(self.interval4)
        del(self.interval5)
        del(self.interval6)
        del(self.interval7)
        del(self.interval8)
        del(self.interval9)
        del(self.interval10)
        del(self.interval11)
        del(self.interval12)

    def test_namespace_getter_1(self):
        self.assertIsNone(self.interval0.namespace)

    def test_namespace_getter_2(self):
        self.assertEqual(self.interval9.namespace, "other")

    def test_namespace_setter_1(self):
        self.assertIsNone(self.interval0.namespace)
        self.interval0.namespace = 3
        self.assertEqual(self.interval0.namespace, 3)
                
    def test_beg_getter_1(self):
        self.assertIsNotNone(self.interval0.beg)
        self.assertIsInstance(self.interval0.beg, int)
        self.assertEqual(self.interval0.beg, 50)
        self.assertEqual(self.interval0.start, 50)

    def test_beg_setter_1(self):
        self.assertEqual(self.interval0.beg, 50)
        self.assertEqual(self.interval0.start, 50)
        self.interval0.beg = 75
        self.assertEqual(self.interval0.beg, 75)
        self.assertEqual(self.interval0.start, 75)

    def test_beg_setter_2(self):
        try:
            self.interval0.beg = nan
        except ValueError:
            pass
        self.assertTrue(isnan(self.interval0.beg))
            
    def test_beg_setter_3(self):
        try:
            self.interval0.beg = inf
        except OverflowError:
            pass
        self.assertTrue(isinf(self.interval0.beg))

    def test_beg_setter_4(self):
        try:
            self.interval0.beg = -inf
        except OverflowError:
            pass
        self.assertTrue(isinf(self.interval0.beg))
            
    def test_mid_1(self):
        self.assertEqual(self.interval6.mid, 87.5)
        
    def test_end_getter_1(self):
        self.assertIsNotNone(self.interval0.end)
        self.assertIsInstance(self.interval0.end, int)
        self.assertEqual(self.interval0.end, 100)
        self.assertEqual(self.interval0.stop, 100)

    def test_end_setter_1(self):
        self.assertEqual(self.interval0.end, 100)
        self.assertEqual(self.interval0.stop, 100)
        self.interval0.end = 175
        self.assertEqual(self.interval0.end, 175)
        self.assertEqual(self.interval0.stop, 175)

    def test_end_setter_2(self):
        try:
            self.interval0.end = nan
        except ValueError:
            pass
        self.assertTrue(isnan(self.interval0.end))

    def test_end_setter_3(self):
        try:
            self.interval0.end = inf
        except OverflowError:
            pass
        self.assertTrue(isinf(self.interval0.end))
        
    def test_end_setter_4(self):
        try:
            self.interval0.end = -inf
        except OverflowError:
            pass
        self.assertTrue(isinf(self.interval0.end))
        
    def test_isnull_1(self):
        i = self.constructor()
        self.assertIsNone(i.namespace)
        self.assertTrue(isnan(i.beg))
        self.assertTrue(isnan(i.end))
        self.assertTrue(i.isnull())

    def test_isnull_2(self):
        i = self.constructor()
        i.end = 19
        self.assertIsNone(i.namespace)
        self.assertTrue(isnan(i.beg))
        self.assertFalse(isnan(i.end))
        self.assertTrue(i.isnull())

    def test_isnull_3(self):
        i = self.constructor()
        i.beg = 19
        self.assertIsNone(i.namespace)
        self.assertFalse(isnan(i.beg))
        self.assertTrue(isnan(i.end))
        self.assertTrue(i.isnull())        

    def test_isempty_1(self):
        self.assertFalse(self.interval0.isempty())
        self.interval0.beg, self.interval0.end \
            = self.interval0.end, self.interval0.beg
        self.assertTrue(self.interval0.isempty())

    def test_isempty_2(self):
        self.interval0.beg = nan
        self.assertTrue(isnan(self.interval0.beg))
        self.assertFalse(isnan(self.interval0.end))
        self.assertTrue(self.interval0.isempty())

    def test_isempty_3(self):
        self.interval0.end = nan
        self.assertFalse(isnan(self.interval0.beg))
        self.assertTrue(isnan(self.interval0.end))
        self.assertTrue(self.interval0.isempty())
        
    def test_copy_1(self):
        i = self.interval0.copy()
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i, self.interval0)
        self.assertNotEqual(hash(i), hash(self.interval0))

    def test_copy_2(self):
        i = self.interval0.copy(deep=True)
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i, self.interval0)
        self.assertNotEqual(hash(i), hash(self.interval0))
        
    def test_to_slice_1(self):
        s = self.interval0.to_slice()
        self.assertIsInstance(s, slice)
        self.assertEqual(s.start, self.interval0.beg)
        self.assertEqual(s.stop, self.interval0.end)

    def test_to_slice_2(self):  ###
        s = self.interval8.to_slice()
        self.assertIsInstance(s, slice)
        self.assertEqual(s.start, -1)
        self.assertEqual(s.stop, -1)
        
    def test__abs__1(self):
        i = self.constructor( -15, -5)
        self.assertEqual(i.beg, -15)
        self.assertEqual(i.end, -5)
        i = abs(i)
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i.beg, 5)
        self.assertEqual(i.end, 15)

    def test__abs__2(self):  ###
        i = abs(self.interval8)
        self.assertIsInstance(i, self.constructor)
        self.assertIs(i.namespace, self.interval8.namespace)
        self.assertTrue(isnan(i.beg))
        self.assertTrue(isnan(i.end))
        
    def test__add__1(self):
        i = self.interval0 + 25
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i, self.interval7)

    def test__add__2(self):
        i = self.interval0 + self.interval1
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i.beg,  75)
        self.assertEqual(i.end, 175)

    def test__add__3(self):  ###
        i = self.interval8 + 100
        self.assertIsInstance(i, self.constructor)
        self.assertTrue(i.isempty())

    def test__add__4(self):
        with self.assertRaises(ValueError):
            self.interval0 + self.interval9

    def test__and__1(self):
        i = self.interval0 & self.interval1
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i, self.interval3)

    def test__and__2(self):
        i = self.interval0 & self.interval2
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i, self.interval2)

    def test__and__3(self):
        i = self.interval0 & self.interval5
        self.assertIsInstance(i, self.constructor)
        self.assertFalse(i.isnull())
        self.assertEqual(len(i), 0)

    def test__and__4(self):  ###
        i = self.interval8 & self.interval0
        self.assertIsInstance(i, self.constructor)
        self.assertTrue(i.isnull())

    def test__and__5(self):  ###
        i = self.interval0 & self.interval8
        self.assertIsInstance(i, self.constructor)
        self.assertTrue(i.isnull())

    def test__and__6(self):
        i = self.interval3 & self.interval9
        self.assertIsInstance(i, self.constructor)
        self.assertTrue(i.isnull())
        
    def test__bool__1(self):
        self.assertTrue(bool(self.interval0))

    def test__bool__2(self):  ###
        self.assertFalse(bool(self.interval8))
        
    def test__ceil__1(self):
        import math
        i = self.constructor( 3.50, 7.75)
        self.assertEqual(i.beg, 3.50)
        self.assertEqual(i.end, 7.75)
        i = math.ceil(i)
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i.beg, 4.0)
        self.assertEqual(i.end, 8.0)

    def test__ceil__2(self):  ###
        import math
        i = math.ceil(self.interval8)
        self.assertIsInstance(i, self.constructor)
        self.assertTrue(i.isempty())
        
    def test__contains__1(self):
        self.assertIn(self.interval2, self.interval1)

    def test__contains__2(self):  ###
        self.assertNotIn(self.interval0, self.interval8)
        
    def test__eq__1(self):
        self.assertEqual(self.interval1, self.interval1)

    def test__eq__2(self):
        self.assertEqual(self.interval0, self.interval0)
        self.assertNotEqual(hash(self.interval0), hash(copy(self.interval0)))

    def test__eq__3(self):
        i = self.interval1.copy()
        i.beg, i.end = i.end, i.beg
        self.assertNotEqual(i, self.interval1)

    def test__eq__4(self):  ###
        # None == None -> True
        # nan == nan -> False
        # True and False -> False always
        i = self.constructor()
        self.assertNotEqual(self.interval8, i)
        self.assertTrue(self.interval8.isempty())
        self.assertTrue(i.isempty())

    def test__eq__5(self):
        self.assertNotEqual(self.interval6, self.interval9)
        
    def test__floor__1(self):
        import math
        i = self.constructor( 3.50, 7.75)
        self.assertEqual(i.beg, 3.50)
        self.assertEqual(i.end, 7.75)
        i = math.floor(i)
        self.assertIsInstance(i, self.constructor)
        self.assertAlmostEqual(i.beg, 3.0)
        self.assertAlmostEqual(i.end, 7.0)

    def test__floor__2(self):  ###
        import math
        i = math.floor(self.interval8)
        self.assertIsInstance(i, self.constructor)
        self.assertNotEqual(i, self.interval8)
        self.assertTrue(self.interval8.isempty())
        self.assertTrue(i.isempty())
        
    def test__floordiv__1(self):
        import math
        i = self.constructor( 3.50, 7.75)
        self.assertEqual(i.beg, 3.50)
        self.assertEqual(i.end, 7.75)
        j = i // 1
        self.assertIsInstance(j, self.constructor)
        self.assertAlmostEqual(j.beg, 3.0)
        self.assertAlmostEqual(j.end, 7.0)

    def test__ge__1(self):        
        self.assertGreaterEqual(self.interval0, self.interval1)

    def test__ge__2(self):
        self.assertGreaterEqual(self.interval0, self.interval3)

    def test__ge__3(self):
        self.assertGreaterEqual(self.interval3, self.interval3)    

    def test__gt__1(self):
        self.assertGreater(self.interval0, self.interval1)

    def test__gt__2(self):
        self.assertGreater(self.interval0, self.interval3)

    def test__gt__3(self):
        self.assertFalse(self.interval9 > self.interval5)
        self.assertFalse(self.interval6 > self.interval9)

    def test__hash__1(self):
        self.assertEqual(hash(self.interval0), hash(self.interval0))
        self.assertIs(self.interval0, self.interval0)

    def test__hash__2(self):
        self.assertNotEqual(hash(self.interval0), hash(copy(self.interval0)))
        self.assertIsNot(self.interval0, copy(self.interval0))

    def test__iadd__1(self):
        self.assertEqual(self.interval0.beg,  50)
        self.assertEqual(self.interval0.end, 100)
        self.interval0 += 10
        self.assertEqual(self.interval0.beg,  60)
        self.assertEqual(self.interval0.end, 110)

    def test__iadd__2(self):
        self.assertEqual(self.interval0.beg,  50)
        self.assertEqual(self.interval0.end, 100)
        self.interval0 += self.interval1
        self.assertIsInstance(self.interval0, self.constructor)
        self.assertEqual(self.interval0.beg,  75)
        self.assertEqual(self.interval0.end, 175)

    def test__iadd__3(self):
        with self.assertRaises(ValueError):
            self.interval0 += self.interval9
        
    def test__imul__1(self):
        self.assertEqual(self.interval0.beg,  50)
        self.assertEqual(self.interval0.end, 100)
        self.interval0 *= 5
        self.assertIsInstance(self.interval0, self.constructor)
        self.assertEqual(self.interval0.beg, 250)
        self.assertEqual(self.interval0.end, 500)

    def test__imul__2(self):
        self.assertEqual(self.interval0.beg,  50)
        self.assertEqual(self.interval0.end, 100)
        self.interval0 *= self.interval3
        self.assertIsInstance(self.interval0, self.constructor)
        self.assertEqual(self.interval0.beg, 2500)
        self.assertEqual(self.interval0.end, 7500)

    def test__imul__3(self):
        with self.assertRaises(ValueError):
            self.interval0 *= self.interval9
        
    def test__isub__1(self):
        self.assertEqual(self.interval0.beg,  50)
        self.assertEqual(self.interval0.end, 100)
        self.interval0 -= 50
        self.assertIsInstance(self.interval0, self.constructor)
        self.assertEqual(self.interval0.beg,  0)
        self.assertEqual(self.interval0.end, 50)

    def test__isub__2(self):
        self.assertEqual(self.interval0.beg,  50)
        self.assertEqual(self.interval0.end, 100)
        self.interval0 -= self.interval3
        self.assertIsInstance(self.interval0, self.constructor)
        self.assertEqual(self.interval0.beg,  0)
        self.assertEqual(self.interval0.end, 25)

    def test__isub__3(self):
        with self.assertRaises(ValueError):
            self.interval0 -= self.interval9

    def test__le__1(self):
        self.assertLessEqual(self.interval1, self.interval0)

    def test__le__2(self):
        self.assertLessEqual(self.interval3, self.interval0)

    def test__le__3(self):
        self.assertLessEqual(self.interval0, self.interval0)

    def test__len__1(self):
        self.assertEqual(len(self.interval0), 50)
        self.assertEqual(len(self.interval1), 50)
        self.assertEqual(len(self.interval2),  5)
        self.assertEqual(len(self.interval3), 25)

    def test__lt__1(self):
        self.assertLess(self.interval1, self.interval0)

    def test__lt__2(self):
        self.assertLess(self.interval3, self.interval0)

    def test__lt__3(self):
        self.assertFalse(self.interval5 < self.interval9)
        self.assertFalse(self.interval9 < self.interval10)
        
    def test__lshift__1(self):
        j = self.constructor( 2, 4)
        i = j << 1
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i.beg, 4)
        self.assertEqual(i.end, 8)

    def test__lshift__2(self):
        j = self.constructor( 2, 4)
        i = j << self.constructor( 1, 2)
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i.beg,  4)
        self.assertEqual(i.end, 16)
        
    def test__mul__1(self):
        self.assertEqual(self.interval0.beg,  50)
        self.assertEqual(self.interval0.end, 100)
        i = self.interval0 * 5
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i.beg, 250)
        self.assertEqual(i.end, 500)

    def test__mul__2(self):
        self.assertEqual(self.interval0.beg,  50)
        self.assertEqual(self.interval0.end, 100)
        i = self.interval0 * self.constructor( 2, 5)
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i.beg, 100)
        self.assertEqual(i.end, 500)
        
    def test__ne__1(self):
        self.assertNotEqual(self.interval0, self.interval1)

    def test__ne__2(self):
        self.assertNotEqual(self.interval0, self.interval3)

    def test__ne__3(self):
        self.assertNotEqual(self.interval0, self.constructor(0, 100))

    def test__ne__4(self):
        self.assertNotEqual(self.interval6, self.interval9)
        
    def test__or__1(self):
        # i0:  50 *================* 100
        # i2:       70 *===* 75        
        i = self.interval0 | self.interval2
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i, self.interval0)

    def test__or__2(self):
        # i0:  50 *================* 100
        # i3:  50 *============* 75        
        i = self.interval0 | self.interval3
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i, self.interval0)

    def test__or__3(self):
        # i0:  50 *================* 100
        # i6:          75 *========* 100
        i = self.interval0 | self.interval6
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i, self.interval0)
        
    def test__or__4(self):
        # i0:           50 *================* 100
        # i1:  25 *================* 75
        i = self.interval0 | self.interval1
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i.beg,  25)
        self.assertEqual(i.end, 100)

    def test__or__5(self):
        # i0:  50 *================* 100
        # i7:           75 *================* 125
        i = self.interval0 | self.interval7
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i.beg, 50)
        self.assertEqual(i.end, 125)

    def test__or__6(self):
        # i3:           50 *======* 75
        # i5: 0 *==========* 50
        i = self.interval3 | self.interval5
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i.beg, 0)
        self.assertEqual(i.end, 75)

    def test__or__7(self):
        # i3:  50 *======* 75
        # i6:         75 *======* 100
        i = self.interval3 | self.interval6
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i.beg, 50)
        self.assertEqual(i.end, 100)
        
    def test__or__8(self):
        # i2:                     70 *====* 75
        # i5:  0 *===============* 50
        i = self.interval2 | self.interval5
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.constructor)
        self.assertIsInstance(i[1], self.constructor)
        self.assertEqual(i[0], self.interval2)
        self.assertEqual(i[1], self.interval5)

    def test__or__9(self):
        # i5:  0 *===============* 50
        # i2:                     70 *====* 75
        i = self.interval5 | self.interval2
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.constructor)
        self.assertIsInstance(i[1], self.constructor)
        self.assertEqual(i[0], self.interval5)
        self.assertEqual(i[1], self.interval2)

    def test__or__10(self):
        i = self.interval6 | self.interval9
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.constructor)
        self.assertIsInstance(i[1], self.constructor)
        self.assertEqual(i[0], self.interval6)
        self.assertEqual(i[1], self.interval9)        
        
    def test__radd__1(self):
        self.assertEqual(self.interval0.beg,  50)
        self.assertEqual(self.interval0.end, 100)
        i = 5 + self.interval0
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i.beg,  55)
        self.assertEqual(i.end, 105)

    def test__rfloordiv__1(self):
        i = 1000000 // self.interval0
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i.beg, 10000)
        self.assertEqual(i.end, 20000)
        
    def test__rlshift__1(self):
        i = 1 << self.constructor(2,4)
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i.beg,  4)
        self.assertEqual(i.end, 16)
        
    def test__rmul__1(self):
        i = 5 * self.interval0
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i.beg, 250)
        self.assertEqual(i.end, 500)

    def test__rshift__1(self):
        i = self.constructor( 2, 16) >> 1
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i.beg, 1)
        self.assertEqual(i.end, 8)

    def test__rsub__1(self):
        i = 10000 - self.constructor( 1000, 10000)
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i.beg, 0)
        self.assertEqual(i.end, 9000)

    def test__rtruediv__1(self):
        i = 5.0 / self.constructor( 2.0, 5.0)
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i.beg, 1)
        self.assertEqual(i.end, 2.5)

    def test__sub__1(self):
        i = self.interval0 - 50
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i.beg,  0)
        self.assertEqual(i.end, 50)

    def test__sub__2(self):
        i = self.interval0 - self.interval3
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i.beg, -25)
        self.assertEqual(i.end, 50)
        
    def test__truediv__1(self):
        i = self.interval1 / 100.0
        self.assertIsInstance(i, self.interval1.__class__)
        self.assertAlmostEqual(i.beg, 0.25)
        self.assertAlmostEqual(i.end, 0.75)

    def test__truediv__2(self):
        i = self.interval1 / self.constructor(100.0, 100.0)
        self.assertIsInstance(i, self.interval1.__class__)
        self.assertAlmostEqual(i.beg, 0.25)
        self.assertAlmostEqual(i.end, 0.75)

    def test__truediv__3(self):
        with self.assertRaises(ValueError):
            self.interval6 / self.interval9
        
    def test__xor__1(self):
        # i5:  0 *========o 50
        # i1:      25 *========o 75
        i = self.interval5 ^ self.interval1
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.constructor)
        self.assertIsInstance(i[1], self.constructor)
        self.assertEqual(i[0], self.constructor(  0, 25))
        self.assertEqual(i[1], self.constructor( 50, 75))

    def test__xor__2(self):
        # i1:      25 *========o 75
        # i5:  0 *========o 50
        i = self.interval1 ^ self.interval5
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.constructor)
        self.assertIsInstance(i[1], self.constructor)
        self.assertEqual(i[0], self.constructor( 50, 75))
        self.assertEqual(i[1], self.constructor(  0, 25))
        
    def test__xor__3(self):
        # i0:  50 *================o 100
        # i2:       70 *========o 75        
        i = self.interval0 ^ self.interval2
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.constructor)
        self.assertIsInstance(i[1], self.constructor)
        self.assertEqual(i[0], self.constructor( 50,  70))
        self.assertEqual(i[1], self.constructor( 75, 100))

    def test__xor__4(self):
        # i0:  50 *================o 100
        # i0:  50 *================o 100
        i = self.interval0 ^ self.interval0
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)        
        self.assertIsInstance(i[0], self.constructor)
        self.assertIsInstance(i[1], self.constructor)
        self.assertTrue(i[0].isempty())
        self.assertTrue(i[1].isempty())

    def test__xor__5(self):
        # i5:  0 *========o 50
        # i3:          50 *====o 75        
        i = self.interval5 ^ self.interval3
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.constructor)
        self.assertIsInstance(i[1], self.constructor)
        self.assertEqual(i[0], self.interval5)
        self.assertEqual(i[1], self.interval3)

    def test__xor__6(self):  
        # i3:          50 *====o 75
        # i5:  0 *========o 50        
        i = self.interval3 ^ self.interval5
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.constructor)
        self.assertIsInstance(i[1], self.constructor)
        self.assertEqual(i[0], self.interval3)
        self.assertEqual(i[1], self.interval5)
        
    def test__xor__7(self):
        # i0:  50 *========o 100
        # i3:  50 *====o 75
        i = self.interval0 ^ self.interval3
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.constructor)
        self.assertIsInstance(i[1], self.constructor)
        self.assertEqual(i[0], self.interval6)
        self.assertTrue(i[1].isempty())

    def test__xor__8(self):
        # i1:  25 *==========o 75
        # i3:       50 *=====o 75
        i = self.interval1 ^ self.interval3
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.constructor)
        self.assertIsInstance(i[1], self.constructor)
        self.assertEqual(i[0].beg, 25)
        self.assertEqual(i[0].end, 50)
        self.assertTrue(i[1].isempty())

    def test__xor__9(self):
        i = self.interval6 ^ self.interval9
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.constructor)
        self.assertIsInstance(i[1], self.constructor)
        self.assertEqual(i[0], self.interval6)
        self.assertEqual(i[1], self.interval9)
        
    def test_isabutting_beg_1(self):
        self.assertTrue(self.interval5.isabutting_beg(self.interval3))

    def test_isabutting_beg_2(self):
        self.assertFalse(self.interval5.isabutting_beg(self.interval2))

    def test_isabutting_beg_3(self):
        self.assertFalse(self.interval3.isabutting_beg(self.interval5))

    def test_isabutting_beg_4(self):
        self.assertFalse(self.interval3.isabutting_beg(self.interval9))
        
    def test_isabutting_end_1(self):
        self.assertTrue(self.interval3.isabutting_end(self.interval5))

    def test_isabutting_end_2(self):
        self.assertFalse(self.interval2.isabutting_end(self.interval5))

    def test_isabutting_end_3(self):
        self.assertFalse(self.interval5.isabutting_end(self.interval3))

    def test_isabutting_end_4(self):
        self.assertFalse(self.interval9.isabutting_end(self.interval3))
        
    def test_issuperinterval_1(self):
        self.assertTrue(self.interval0.issuperinterval(self.interval2))

    def test_issuperinterval_2(self):
        self.assertTrue(self.interval0.issuperinterval(self.interval3))

    def test_issuperinterval_3(self):
        self.assertTrue(self.interval0.issuperinterval(self.interval6))

    def test_issuperinterval_4(self):
        self.assertTrue(self.interval0.issuperinterval(self.interval2))

    def test_issuperinterval_5(self):
        self.assertFalse(self.interval0.issuperinterval(self.interval1))

    def test_issuperinterval_6(self):
        self.assertFalse(self.interval1.issuperinterval(self.interval0))
        
    def test_issuperinterval_7(self):
        self.assertFalse(self.interval6.issuperinterval(self.interval0))

    def test_issuperinterval_8(self):
        self.assertTrue(self.interval0.issuperinterval(self.interval0, strict=False))
        self.assertFalse(self.interval0.issuperinterval(self.interval0, strict=True))

    def test_issuperinterval_9(self):
        self.assertFalse(self.interval12.issuperinterval(self.interval9))
        
    def test_difference_1(self):
        i = self.interval0.difference(self.interval6)
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i, self.interval3)
        
    def test_difference_2(self):
        i = self.interval0.difference(self.interval3)
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i, self.interval6)
        
    def test_difference_3(self):
        i = self.interval2.difference(self.interval0)
        self.assertIsInstance(i, self.constructor)
        self.assertTrue(i.isnull())

    def test_difference_4(self):
        i = self.interval0.difference(self.interval2)
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.constructor)
        self.assertIsInstance(i[1], self.constructor)
        self.assertEqual(i[0].beg,  50)
        self.assertEqual(i[0].end,  70)
        self.assertEqual(i[1].beg,  75)
        self.assertEqual(i[1].end, 100)

    def test_difference_5(self):
        i = self.interval5.difference(self.interval2)
        self.assertEqual(i, self.interval5)

    def test_difference_6(self):
        i = self.interval4.difference(self.interval9)
        self.assertEqual(i, self.interval4)
        
    def test_difference_update_1(self):
        with self.assertRaises(NotImplementedError):
            self.interval0.difference_update(self.interval0)

    def test_inner_distance_1(self):
        self.assertEqual(self.interval0.inner_distance(self.interval2), 0)

    def test_inner_distance_2(self):
        self.assertEqual(self.interval5.inner_distance(self.interval3), 0)

    def test_inner_distance_3(self):
        self.assertEqual(self.interval7.inner_distance(self.interval3), 0)

    def test_inner_distance_4(self):
        self.assertEqual(self.interval5.inner_distance(self.interval7), 25)

    def test_inner_distance_5(self):
        self.assertEqual(self.interval7.inner_distance(self.interval5), -25)

    def test_inner_distance_6(self):
        self.assertTrue(isinf(self.interval6.inner_distance(self.interval9)))
        
    def test_intersection_1(self):
        i = self.interval0.intersection(self.interval2)
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i, self.interval2)

    def test_intersection_2(self):
        i = self.interval0.intersection(self.interval3)
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i, self.interval3)

    def test_intersection_3(self):
        i = self.interval0.intersection(self.interval6)
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i, self.interval6)

    def test_intersection_4(self):
        i = self.interval0.intersection(self.interval1)
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i.beg, 50)
        self.assertEqual(i.end, 75)

    def test_intersection_5(self):
        i = self.interval0.intersection(self.interval7)
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i.beg,  75)
        self.assertEqual(i.end, 100)
        
    def test_intersection_6(self):
        i = self.interval0.intersection(self.interval5)
        self.assertIsInstance(i, self.constructor)
        self.assertFalse(i.isnull())
        self.assertEqual(len(i), 0)

    def test_intersection_7(self):
        i = self.interval1.intersection(self.interval7)
        self.assertIsInstance(i, self.constructor)
        self.assertFalse(i.isnull())
        self.assertEqual(len(i), 0)

    def test_intersection_8(self):
        i = self.interval6.intersection(self.interval9)
        self.assertIsInstance(i, self.constructor)
        self.assertTrue(i.isnull())
        self.assertEqual(len(i), 0)

    def test_intersection_update_1(self):
        self.interval0.intersection_update(self.interval2)
        self.assertIsInstance(self.interval0, self.constructor)
        self.assertEqual(self.interval0, self.interval2)

    def test_intersection_update_2(self):
        self.interval0.intersection_update(self.interval3)
        self.assertIsInstance(self.interval0, self.constructor)
        self.assertEqual(self.interval0, self.interval3)

    def test_intersection_update_3(self):
        self.interval0.intersection_update(self.interval6)
        self.assertIsInstance(self.interval0, self.constructor)
        self.assertEqual(self.interval0, self.interval6)

    def test_intersection_update_4(self):
        self.interval0.intersection_update(self.interval1)
        self.assertIsInstance(self.interval0, self.constructor)
        self.assertEqual(self.interval0.beg, 50)
        self.assertEqual(self.interval0.end, 75)

    def test_intersection_update_5(self):
        self.interval0.intersection_update(self.interval7)
        self.assertIsInstance(self.interval0, self.constructor)
        self.assertEqual(self.interval0.beg,  75)
        self.assertEqual(self.interval0.end, 100)
        
    def test_intersection_update_6(self):
        self.interval0.intersection_update(self.interval5)
        self.assertIsInstance(self.interval0, self.constructor)
        self.assertFalse(self.interval0.isnull())
        self.assertEqual(len(self.interval0), 0)

    def test_intersection_update_7(self):
        self.interval1.intersection_update(self.interval7)
        self.assertIsInstance(self.interval0, self.constructor)
        self.assertFalse(self.interval0.isnull())
        self.assertEqual(len(self.interval0), 50)

    def test_intersection_update_8(self):
        self.interval6.intersection_update(self.interval9)
        self.assertIsInstance(self.interval6, self.constructor)
        self.assertTrue(self.interval6.isnull())
        self.assertEqual(len(self.interval6), 0)
        
    def test_isdisjoint_1(self):
        self.assertTrue(self.interval5.isdisjoint(self.interval2))

    def test_isdisjoint_2(self):
        self.assertFalse(self.interval5.isdisjoint(self.interval3))

    def test_isdisjoint_3(self):
        self.assertFalse(self.interval3.isdisjoint(self.interval5))

    def test_isdisjoint_4(self):
        self.assertTrue(self.interval2.isdisjoint(self.interval5))

    def test_isdisjoint_5(self):
        self.assertFalse(self.interval3.isdisjoint(self.interval2))

    def test_isdisjoint_6(self):
        self.assertFalse(self.interval0.isdisjoint(self.interval3))

    def test_isdisjoint_7(self):
        self.assertTrue(self.interval6.isdisjoint(self.interval9))
        

    def test_jaccard_distance_1(self):
        self.assertAlmostEqual(
            self.interval0.jaccard_distance(self.interval0), 0.0,
            places=6
        )

    def test_jaccard_distance_2(self):
        self.assertAlmostEqual(
            self.interval5.jaccard_distance(self.interval2), 1.0,
            places=6
        )

    def test_jaccard_distance_3(self):
        self.assertAlmostEqual(
            self.interval2.jaccard_distance(self.interval5), 1.0,
            places=6
        )

    def test_jaccard_distance_4(self):
        self.assertAlmostEqual(
            self.interval5.jaccard_distance(self.interval0), 1.0,
            places=6
        )

    def test_jaccard_distance_5(self):
        self.assertAlmostEqual(
            self.interval5.jaccard_distance(self.interval0), 1.0,
            places=6
        )

    def test_jaccard_distance_6(self):
        self.assertAlmostEqual(
            self.interval4.jaccard_distance(self.interval7), 0.8,
            places=6
        )

    def test_jaccard_distance_7(self):
        self.assertAlmostEqual(
            self.interval6.jaccard_distance(self.interval9), 1.0,
            places=6
        )
        
    def test_outer_distance_1(self):
        self.assertEqual(
            self.interval0.outer_distance(self.interval2, True), 50
        )

    def test_outer_distance_2(self):
        self.assertEqual(
            self.interval0.outer_distance(self.interval3, True), 50
        )

    def test_outer_distance_3(self):
        self.assertEqual(
            self.interval0.outer_distance(self.interval6, True), 50
        )

    def test_outer_distance_4(self):
        self.assertEqual(
            self.interval5.outer_distance(self.interval0, True), 100
        )

    def test_outer_distance_5(self):
        self.assertEqual(
            self.interval3.outer_distance(self.interval7, True), 75
        )

    def test_outer_distance_6(self):
        self.assertEqual(
            self.interval0.outer_distance(self.interval5, True), -100
        )

    def test_outer_distance_7(self):
        self.assertEqual(
            self.interval5.outer_distance(self.interval7, True), 125
        )       

    def test_outer_distance_8(self):
        self.assertEqual(
            self.interval7.outer_distance(self.interval5, True), -125
        )

    def test_outer_distance_8(self):
        self.assertTrue(isinf(
            self.interval6.outer_distance(self.interval9, True)
        ))
        
    def test_intersection_fraction_1(self):
        self.assertAlmostEqual(
            self.interval0.intersection_fraction(self.interval2), 0.10,
            places=6
        )

    def test_intersection_fraction_2(self):
        self.assertAlmostEqual(
            self.interval2.intersection_fraction(self.interval0), 1.0,
            places=6
        )

    def test_intersection_fraction_3(self):
        self.assertAlmostEqual(
            self.interval0.intersection_fraction(self.interval3), 0.5,
            places=6
        )
        
    def test_intersection_fraction_4(self):
        self.assertAlmostEqual(
            self.interval0.intersection_fraction(self.interval6), 0.5,
            places=6
        )
        
    def test_intersection_fraction_5(self):
        self.assertAlmostEqual(
            self.interval0.intersection_fraction(self.interval5), 0.0,
            places=6
        )

    def test_intersection_fraction_6(self):
        self.assertAlmostEqual(
            self.interval5.intersection_fraction(self.interval3), 0.0,
            places=6
        )

    def test_intersection_fraction_7(self):
        self.assertAlmostEqual(
            self.interval6.intersection_fraction(self.interval9), 0.0,
            places=6
        )
        
    def test_intersection_length_1(self):
        self.assertEqual(
            self.interval0.intersection_length(self.interval2), 5
        )

    def test_intersection_length_2(self):
        self.assertEqual(
            self.interval2.intersection_length(self.interval0), 5
        )

    def test_intersection_length_3(self):
        self.assertEqual(
            self.interval0.intersection_length(self.interval3), 25
        )
        
    def test_intersection_length_4(self):
        self.assertEqual(
            self.interval0.intersection_length(self.interval6), 25
        )
        
    def test_intersection_length_5(self):
        self.assertEqual(
            self.interval0.intersection_length(self.interval5), 0
        )

    def test_intersection_length_6(self):
        self.assertEqual(
            self.interval5.intersection_length(self.interval3), 0
        )

    def test_intersection_length_9(self):
        self.assertEqual(
            self.interval6.intersection_length(self.interval9), 0
        )
        
    def test_isintersecting_1(self):
        self.assertTrue(self.interval0.isintersecting(self.interval2))

    def test_isintersecting_2(self):
        self.assertTrue(self.interval0.isintersecting(self.interval3))

    def test_isintersecting_3(self):
        self.assertTrue(self.interval0.isintersecting(self.interval6))

    def test_isintersecting_4(self):
        self.assertTrue(self.interval0.isintersecting(self.interval1))

    def test_isintersecting_5(self):
        self.assertTrue(self.interval0.isintersecting(self.interval7))

    def test_isintersecting_6(self):
        self.assertTrue(self.interval0.isintersecting(self.interval5))

    def test_isintersecting_7(self):
        self.assertTrue(self.interval3.isintersecting(self.interval7))

    def test_isintersecting_8(self):
        self.assertFalse(self.interval5.isintersecting(self.interval2))

    def test_isintersecting_9(self):
        self.assertFalse(self.interval6.isintersecting(self.interval9))

    def test_isintersecting_beg_1(self):
        self.assertTrue(self.interval1.isintersecting_beg(self.interval0))

    def test_isintersecting_beg_2(self):
        self.assertTrue(self.interval3.isintersecting_beg(self.interval0))

    def test_isintersecting_beg_3(self):
        self.assertFalse(self.interval2.isintersecting_beg(self.interval0))

    def test_isintersecting_beg_4(self):
        self.assertTrue(self.interval5.isintersecting_beg(self.interval0))

    def test_isintersecting_beg_5(self):
        self.assertFalse(self.interval11.isintersecting_beg(self.interval9))
        
    def test_isintersecting_end_1(self):
        self.assertTrue(self.interval1.isintersecting_end(self.interval5))

    def test_isintersecting_end_2(self):
        self.assertTrue(self.interval7.isintersecting_end(self.interval0))

    def test_isintersecting_end_3(self):
        self.assertFalse(self.interval2.isintersecting_end(self.interval0))    

    def test_isintersecting_end_4(self):
        self.assertTrue(self.interval7.isintersecting_end(self.interval1))

    def test_isintersecting_end_5(self):
        self.assertFalse(self.interval9.isintersecting_end(self.interval11))
        
    def test_symmetric_difference_1(self):
        # i5:  0 *========o 50
        # i1:      25 *========o 75
        i = self.interval5.symmetric_difference(self.interval1)
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.constructor)
        self.assertIsInstance(i[1], self.constructor)
        self.assertEqual(i[0], self.constructor(  0, 25))
        self.assertEqual(i[1], self.constructor( 50, 75))

    def test_symmetric_difference_2(self):
        # i1:      25 *========o 75
        # i5:  0 *========o 50
        i = self.interval1.symmetric_difference(self.interval5)
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.constructor)
        self.assertIsInstance(i[1], self.constructor)
        self.assertEqual(i[0], self.constructor( 50, 75))
        self.assertEqual(i[1], self.constructor(  0, 25))
        
    def test_symmetric_difference_3(self):
        # i0:  50 *================o 100
        # i2:       70 *========o 75
        i = self.interval0.symmetric_difference(self.interval2)
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.constructor)
        self.assertIsInstance(i[1], self.constructor)
        self.assertEqual(i[0], self.constructor( 50,  70))
        self.assertEqual(i[1], self.constructor( 75, 100))

    def test_symmetric_difference_4(self):
        # i0:  50 *================o 100
        # i0:  50 *================o 100
        i = self.interval0.symmetric_difference(self.interval0)
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)        
        self.assertIsInstance(i[0], self.constructor)
        self.assertIsInstance(i[1], self.constructor)
        self.assertTrue(i[0].isempty())
        self.assertTrue(i[1].isempty())

    def test_symmetric_difference_5(self):
        # i5:  0 *========o 50
        # i3:          50 *====o 75
        i = self.interval5.symmetric_difference(self.interval3)
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.constructor)
        self.assertIsInstance(i[1], self.constructor)
        self.assertEqual(i[0], self.interval5)
        self.assertEqual(i[1], self.interval3)

    def test_symmetric_difference_6(self):  
        # i3:          50 *====o 75
        # i5:  0 *========o 50        
        i = self.interval3.symmetric_difference(self.interval5)
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.constructor)
        self.assertIsInstance(i[1], self.constructor)
        self.assertEqual(i[0], self.interval3)
        self.assertEqual(i[1], self.interval5)
        
    def test_symmetric_difference_7(self):
        # i0:  50 *========o 100
        # i3:  50 *====o 75
        i = self.interval0.symmetric_difference(self.interval3)
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.constructor)
        self.assertIsInstance(i[1], self.constructor)
        self.assertEqual(i[0], self.interval6)
        self.assertTrue(i[1].isempty())

    def test_symmetric_difference_8(self):
        # i1:  25 *==========o 75
        # i3:       50 *=====o 75
        i = self.interval1.symmetric_difference(self.interval3)
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.constructor)
        self.assertIsInstance(i[1], self.constructor)
        self.assertEqual(i[0].beg, 25)
        self.assertEqual(i[0].end, 50)
        self.assertTrue(i[1].isempty())

    def test_symmetric_difference_8(self):
        # i1:  25 *==========o 75
        # i3:       50 *=====o 75
        i = self.interval6.symmetric_difference(self.interval9)
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.constructor)
        self.assertIsInstance(i[1], self.constructor)
        self.assertEqual(i[0], self.interval6)
        self.assertEqual(i[1], self.interval9)

    def test_symmetric_difference_update_1(self):
        with self.assertRaises(NotImplementedError):
            self.interval0.symmetric_difference_update(self.interval0)

    def test_to_slice_1(self):
        s = self.interval0.to_slice()
        self.assertIsInstance(s, slice)
        self.assertEqual(s.start, self.interval0.beg)
        self.assertEqual(s.stop, self.interval0.end)

    def test_to_string_1(self):
        s = self.interval0.to_string()
        self.assertIsInstance(s, str)
        self.assertEqual(s, "[50, 100, namespace=None]")

    def test_to_string_2(self):
        s = self.constructor(3.5, 10.5).to_string()
        self.assertIsInstance(s, str)
        self.assertEqual(s, "[3.5, 10.5, namespace=None]")

    def test__str__1(self):
        s = str(self.interval0)
        self.assertIsInstance(s, str)
        self.assertEqual(s, "[50, 100, namespace=None]")

    def test__str__2(self):
        s = str(self.constructor(3.5, 10.5))
        self.assertIsInstance(s, str)
        self.assertEqual(s, "[3.5, 10.5, namespace=None]")
        
    def test_union_1(self):
        # i0:  50 *================o 100
        # i2:       70 *===o 75
        i = self.interval0.union(self.interval2)
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i, self.interval0)

    def test_union_2(self):
        # i0:  50 *================o 100
        # i3:  50 *============o 75
        i = self.interval0.union(self.interval3)
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i, self.interval0)

    def test_union_3(self):
        # i0:  50 *================o 100
        # i6:          75 *========o 100
        i = self.interval0.union(self.interval6)
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i, self.interval0)
        
    def test_union_4(self):
        # i0:           50 *================o 100
        # i1:  25 *================o 75
        i = self.interval0.union(self.interval1)
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i.beg,  25)
        self.assertEqual(i.end, 100)

    def test_union_5(self):
        # i0:  50 *================o 100
        # i7:           75 *================o 125
        i = self.interval0.union(self.interval7)
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i.beg,  50)
        self.assertEqual(i.end, 125)

    def test_union_6(self):
        # i3:           50 *======* 75
        # i5: 0 *==========* 50
        i = self.interval3.union(self.interval5)
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i.beg, 0)
        self.assertEqual(i.end, 75)

    def test_union_7(self):
        # i3:  50 *======o 75
        # i6:         75 *======o 100
        i = self.interval3.union(self.interval6)
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i.beg, 50)
        self.assertEqual(i.end, 100)
        
    def test_union_8(self):
        # i2:                     70 *====o 75
        # i5:  0 *===============o 50
        i = self.interval2.union(self.interval5)
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.constructor)
        self.assertIsInstance(i[1], self.constructor)
        self.assertEqual(i[0], self.interval2)
        self.assertEqual(i[1], self.interval5)

    def test_union_9(self):
        # i5:  0 *===============o 50
        # i2:                     70 *====o 75
        i = self.interval5.union(self.interval2)
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.constructor)
        self.assertIsInstance(i[1], self.constructor)
        self.assertEqual(i[0], self.interval5)
        self.assertEqual(i[1], self.interval2)

    def test_union_10(self):
        # i5:  0 *===============o 50
        # i2:                     70 *====o 75
        i = self.interval6.union(self.interval9)
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.constructor)
        self.assertIsInstance(i[1], self.constructor)
        self.assertEqual(i[0], self.interval6)
        self.assertEqual(i[1], self.interval9)

    def test_issubinterval_1(self):
        self.assertTrue(self.interval2.issubinterval(self.interval0))

    def test_issubinterval_2(self):
        self.assertTrue(self.interval3.issubinterval(self.interval0))

    def test_issubinterval_3(self):
        self.assertTrue(self.interval6.issubinterval(self.interval0))

    def test_issubinterval_4(self):
        self.assertTrue(self.interval0.issubinterval(self.interval0))
        
    def test_issubinterval_5(self):
        self.assertTrue(self.interval3.issubinterval(self.interval0))

    def test_issubinterval_6(self):
        self.assertFalse(self.interval7.issubinterval(self.interval0))

    def test_issubinterval_7(self):
        self.assertFalse(self.interval5.issubinterval(self.interval3))

    def test_issubinterval_8(self):
        self.assertFalse(self.interval6.issubinterval(self.interval3))

    def test_issubinterval_9(self):
        self.assertTrue(self.interval0.issubinterval(self.interval0, strict=False))
        self.assertFalse(self.interval0.issubinterval(self.interval0, strict=True))

    def test_issubinterval_10(self):
        self.assertFalse(self.interval9.issubinterval(self.interval12))


class TestCase010_LeftClosedInterval(TestCase009_BaseInterval):
    constructor = LeftClosedInterval
    
    def setUp(self):
        self.interval0  = self.constructor(50, 100)
        self.interval1  = self.constructor(25,  75)
        self.interval2  = self.constructor(70,  75)
        self.interval3  = self.constructor(50,  75)
        self.interval4  = self.constructor( 0, 100)
        self.interval5  = self.constructor( 0,  50)
        self.interval6  = self.constructor(75, 100)
        self.interval7  = self.constructor(75, 125)
        self.interval8  = self.constructor()
        self.interval9  = self.constructor(75, 100, namespace="other")
        self.interval10 = self.constructor(100, 110)
        self.interval11 = self.constructor(50, 90)
        self.interval12 = self.constructor(0, 1000)

    def test__and__3(self):
        i = self.interval0 & self.interval5
        self.assertIsInstance(i, self.constructor)
        self.assertTrue(i.isnull())

    def test_intersection_6(self):
        i = self.interval0.intersection(self.interval5)
        self.assertIsInstance(i, self.constructor)
        self.assertTrue(i.isnull())        
        
    def test_intersection_7(self):
        i = self.interval1.intersection(self.interval7)
        self.assertIsInstance(i, self.constructor)
        self.assertTrue(i.isnull())

    def test_intersection_update_6(self):
        self.interval0.intersection_update(self.interval5)
        self.assertIsInstance(self.interval0, self.constructor)
        self.assertTrue(self.interval0.isnull())
        self.assertEqual(len(self.interval0), 0)
        
    def test_isdisjoint_2(self):
        self.assertTrue(self.interval5.isdisjoint(self.interval3))

    def test_isdisjoint_3(self):
        self.assertTrue(self.interval3.isdisjoint(self.interval5))

    def test_isintersecting_6(self):
        self.assertFalse(self.interval0.isintersecting(self.interval5))

    def test_isintersecting_7(self):
        self.assertFalse(self.interval3.isintersecting(self.interval7))

    def test_isintersecting_beg_4(self):
        self.assertFalse(self.interval5.isintersecting_beg(self.interval0))

    def test_isintersecting_end_4(self):
        self.assertFalse(self.interval7.isintersecting_end(self.interval1))

    def test__or__6(self):
        # i3:           50 *======o 75
        # i5: 0 *==========o 50
        i = self.interval3 | self.interval5
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.constructor)
        self.assertIsInstance(i[1], self.constructor)
        self.assertEqual(i[0], self.interval3)
        self.assertEqual(i[1], self.interval5)

    def test__or__7(self):
        # i3:  50 *======o 75
        # i6:         75 *======o 100
        i = self.interval3 | self.interval6
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.constructor)
        self.assertIsInstance(i[1], self.constructor)
        self.assertEqual(i[0], self.interval3)
        self.assertEqual(i[1], self.interval6)

    def test_union_6(self):
        # i3:           50 *======o 75
        # i5: 0 *==========o 50
        i = self.interval3.union(self.interval5)
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.constructor)
        self.assertIsInstance(i[1], self.constructor)
        self.assertEqual(i[0], self.interval3)
        self.assertEqual(i[1], self.interval5)

    def test_union_7(self):
        # i3:  50 *======o 75
        # i6:         75 *======o 100
        i = self.interval3.union(self.interval6)
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.constructor)
        self.assertIsInstance(i[1], self.constructor)
        self.assertEqual(i[0], self.interval3)
        self.assertEqual(i[1], self.interval6)

        

class TestCase011_ClosedInterval(TestCase009_BaseInterval):
    constructor = ClosedInterval
    
    def setUp(self):
        self.interval0  = self.constructor(50, 100, "Chr1")
        self.interval1  = self.constructor(25,  75, "Chr1")
        self.interval2  = self.constructor(70,  75, "Chr1")
        self.interval3  = self.constructor(50,  75, "Chr1")
        self.interval4  = self.constructor(50, 100, "Chr2")
        self.interval5  = self.constructor( 0,  50, "Chr1")
        self.interval6  = self.constructor(75, 100, "Chr1")
        self.interval7  = self.constructor(75, 125, "Chr1")
        self.interval8  = self.constructor()
        self.interval9  = self.constructor(75, 100, "other")
        self.interval10 = self.constructor(100, 110, "Chr1")
        self.interval11 = self.constructor(50, 90, "Chr1")
        self.interval12 = self.constructor(0, 1000, "Chr1")

    def tearDown(self):
        del(self.interval0)
        del(self.interval1)
        del(self.interval2)
        del(self.interval3)
        del(self.interval4)
        del(self.interval5)
        del(self.interval6)
        del(self.interval7)
        del(self.interval8)
        del(self.interval9)
        del(self.interval10)
        del(self.interval11)
        del(self.interval12)

    def test_namespace_getter_0(self):
        self.assertTrue(hasattr(self.interval0, 'namespace'))

    def test_namespace_getter_1(self):
        self.assertEqual(self.interval0.namespace, "Chr1")

    def test_namespace_setter_0(self):
        self.assertTrue(hasattr(self.interval0, 'namespace'))

    def test_namespace_setter_1(self):
        self.assertEqual(self.interval0.namespace, "Chr1")
        self.interval0.namespace = 3
        self.assertEqual(self.interval0.namespace, 3)

    def test_mid_1(self):
        self.assertEqual(self.interval6.mid, 87.5)
        
    def test_to_string_1(self):
        s = self.interval0.to_string()
        self.assertIsInstance(s, str)
        self.assertEqual(s, '[50, 100, namespace=Chr1]')

    def test_to_string_2(self):
        s = self.constructor(2, 50, 100).to_string()
        self.assertIsInstance(s, str)
        self.assertEqual(s, '[2, 50, namespace=100]')

    def test__str__1(self):
        s = str(self.interval0)
        self.assertIsInstance(s, str)
        self.assertEqual(s, '[50, 100, namespace=Chr1]')

    def test__str__2(self):
        s = str(self.constructor(50, 100, 2))
        self.assertIsInstance(s, str)
        self.assertEqual(s, '[50, 100, namespace=2]')

    def test_isempty_4(self):
        self.assertFalse(self.interval0.isempty())
        self.interval0.end = self.interval0.beg - 1
        self.assertTrue(self.interval0.isempty())
        
    def test__abs__1(self):
        i = self.constructor(-15, -5, "Chr1")
        self.assertEqual(i.namespace, "Chr1")
        self.assertEqual(i.beg, -15)
        self.assertEqual(i.end, -5)
        i = abs(i)
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i.namespace, "Chr1")
        self.assertEqual(i.beg, 5)
        self.assertEqual(i.end, 15)
        
    def test__add__3(self):
        with self.assertRaises(ValueError):
            i = self.interval0 + self.interval4

    def test__add__4(self):
        i = self.interval0 + Interval("Chr1", 25, 25)
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i, self.interval7)

    def test__bool__2(self):
        self.interval0.beg = nan
        self.interval0.end = nan
        self.assertFalse(bool(self.interval0))

    def test__eq__4(self):
        i = self.constructor(50, 100, "Chr1")
        self.assertNotEqual(i, self.interval4)

    def test__ceil__1(self):
        pass

    def test__floor__1(self):
        pass

    def test__floordiv__1(self):
        import math
        i = self.constructor(1000, 2000, "Chr1")
        self.assertEqual(i.beg, 1000)
        self.assertEqual(i.end, 2000)
        j = i // 10
        self.assertIsInstance(j, self.constructor)
        self.assertEqual(j.beg, 100)
        self.assertEqual(j.end, 200)
        
    def test__rtruediv__1(self):
        i = 5.0 / self.constructor(2.0, 5.0, "Chr1")
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i.beg, "Chr1")
        self.assertEqual(i.beg, 2)
        self.assertEqual(i.end, 1)

    def test__truediv__1(self):
        i = self.interval0 / 50
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i.namespace, "Chr1")
        self.assertEqual(i.beg, 1)
        self.assertEqual(i.end, 2)

    def test__truediv__2(self):
        i = self.interval0 / self.constructor(50, 50, "Chr1")
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i.beg, 1)
        self.assertEqual(i.end, 2)
        
    def test__iadd__3(self):
        with self.assertRaises(ValueError):
            self.interval0 += self.interval4

    def test__iadd__4(self):
        self.interval0 += Interval("Chr1", 25, 25)
        self.assertIsInstance(self.interval0, self.interval1.__class__)
        self.assertEqual(self.interval0, self.interval7)

    def test__imul__3(self):
        with self.assertRaises(ValueError):
            self.interval0 *= self.interval4

    def test__imul__4(self):
        self.assertEqual(self.interval0.beg,  50)
        self.assertEqual(self.interval0.end, 100)
        self.interval0 *= Interval("Chr1", 50, 75)
        self.assertIsInstance(self.interval0, self.constructor)
        self.assertEqual(self.interval0.beg, 2500)
        self.assertEqual(self.interval0.end, 7500)

    def test__isub__3(self):
        with self.assertRaises(ValueError):
            self.interval0 -= self.interval4

    def test__isub__4(self):
        self.assertEqual(self.interval0.beg,  50)
        self.assertEqual(self.interval0.end, 100)
        self.interval0 -= Interval("Chr1", 50, 75)
        self.assertIsInstance(self.interval0, self.constructor)
        self.assertEqual(self.interval0.beg,  0)
        self.assertEqual(self.interval0.end, 25)

    def test__lshift__1(self):
        j = self.constructor(2, 4, "Chr1")
        i = j << 1
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i.namespace, "Chr1")
        self.assertEqual(i.beg, 4)
        self.assertEqual(i.end, 8)

    def test__lshift__2(self):
        j = self.constructor(2, 4, "Chr1")
        i = j << self.constructor(1, 2, "Chr1")
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i.namespace, "Chr1")
        self.assertEqual(i.beg,  4)
        self.assertEqual(i.end, 16)

    def test__lshift__3(self):
        with self.assertRaises(ValueError):
            i = self.interval0 << self.interval4
    
    def test__lshift__4(self):
        j = self.constructor(2, 4, "Chr1")
        i = j << Interval("Chr1", 1, 2)
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i.namespace, "Chr1")
        self.assertEqual(i.beg,  4)
        self.assertEqual(i.end, 16)

    def test__mul__2(self):
        self.assertEqual(self.interval0.beg,  50)
        self.assertEqual(self.interval0.end, 100)
        i = self.interval0 * self.constructor(2, 5, "Chr1")
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i.namespace, "Chr1")
        self.assertEqual(i.beg, 100)
        self.assertEqual(i.end, 500)
        
    def test__mul__3(self):
        with self.assertRaises(ValueError):
            i = self.interval0 * self.interval4

    def test__mul__4(self):
        self.assertEqual(self.interval0.beg,  50)
        self.assertEqual(self.interval0.end, 100)
        i = self.interval0 * Interval("Chr1", 2, 5)
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i.namespace, "Chr1")
        self.assertEqual(i.beg, 100)
        self.assertEqual(i.end, 500)

    def test__rlshift__1(self):
        i = 1 << self.constructor(2, 4, "Chr1")
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i.beg,  4)
        self.assertEqual(i.end, 16)

    def test__rshift__1(self):
        i = self.constructor(2, 16, "Chr1") >> 1
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i.namespace, "Chr1")
        self.assertEqual(i.beg, 1)
        self.assertEqual(i.end, 8)

    def test__rsub__1(self):
        i = 10000 - self.constructor(1000, 10000, "Chr1")
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i.namespace, "Chr1")
        self.assertEqual(i.beg, 0)
        self.assertEqual(i.end, 9000)

    def test__rtruediv__1(self):
        i = 10000 / self.constructor(10, 20, "Chr1")
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i.beg, 500)
        self.assertEqual(i.end, 1000)
        
    def test__sub__3(self):
        with self.assertRaises(ValueError):
            i = self.interval0 - self.interval4

    def test__sub__4(self):
        i = self.interval0 - Interval("Chr1", 50, 75)
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i.beg, -25)
        self.assertEqual(i.end, 50)

    def test__truediv__3(self):
        with self.assertRaises(ValueError):
            i = self.interval0 / self.interval4

    def test__truediv__4(self):
        i = self.interval0 / Interval("Chr1", 50, 50)
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i.beg, 1)
        self.assertEqual(i.end, 2)

    def test__xor__1(self):
        # i5:  0 *========o 50
        # i1:      25 *========o 75        
        i = self.interval5 ^ self.interval1
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.constructor)
        self.assertIsInstance(i[1], self.constructor)
        self.assertEqual(i[0], self.constructor( 0, 25, "Chr1"))
        self.assertEqual(i[1], self.constructor(50, 75, "Chr1"))

    def test__xor__2(self):
        # i1:      25 *========o 75
        # i5:  0 *========o 50        
        i = self.interval1 ^ self.interval5
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.constructor)
        self.assertIsInstance(i[1], self.constructor)
        self.assertEqual(i[0], self.constructor(50, 75, "Chr1"))
        self.assertEqual(i[1], self.constructor( 0, 25, "Chr1"))
        
    def test__xor__3(self):
        # i0:  50 *================o 100
        # i2:       70 *========o 75
        i = self.interval0 ^ self.interval2
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.constructor)
        self.assertIsInstance(i[1], self.constructor)
        self.assertEqual(i[0], self.constructor(50,  70, "Chr1"))
        self.assertEqual(i[1], self.constructor(75, 100, "Chr1"))

    def test__xor__9(self):
        # i0:  50 *================o 100 Chr1
        # i4:    (different namespace)   Chr2
        i = self.interval0 ^ self.interval4
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.constructor)
        self.assertIsInstance(i[1], self.constructor)
        self.assertEqual(i[0], self.interval0)
        self.assertEqual(i[1], self.interval4)

    def test_difference_6(self):
        i = self.interval0.difference(self.interval4)
        self.assertIsInstance(i, self.constructor)
        self.assertEqual(i, self.interval0)

    def test_inner_distance_5(self):
        self.assertEqual(self.interval0.inner_distance(self.interval4), inf)

    def test_inner_distance_6(self):
        self.assertEqual(self.interval4.inner_distance(self.interval0), inf)

    def test_intersection_8(self):
        i = self.interval1.intersection(self.interval4)
        self.assertIsInstance(i, self.constructor)
        self.assertTrue(i.isnull())

    def test_isdisjoint_7(self):
        self.assertTrue(self.interval0.isdisjoint(self.interval4))

    def test_jaccard_distance_6(self):
        self.assertAlmostEqual(
            self.interval0.jaccard_distance(self.interval7), 2/3,
            places=6
        )
        
    def test_outer_distance_9(self):
        self.assertEqual(
            self.interval0.outer_distance(self.interval4, True), inf
        )

    def test_outer_distance_10(self):
        self.assertEqual(
            self.interval4.outer_distance(self.interval0, True), inf
        )

    def test_intersection_fraction_7(self):
        self.assertEqual(
            self.interval0.intersection_fraction(self.interval4), 0.0
        )

    def test_intersection_length_7(self):
        self.assertEqual(
            self.interval0.intersection_length(self.interval4), 0
        )

    def test_isintersecting_9(self):
        self.assertFalse(self.interval0.isintersecting(self.interval4))

    def test_isintersecting_beg_5(self):
        self.assertFalse(self.interval1.isintersecting_beg(self.interval4))

    def test_isintersecting_end_5(self):
        self.assertFalse(self.interval7.isintersecting_end(self.interval4))

    def test_symmetric_difference_1(self):
        # i5:  0 *========o 50
        # i1:      25 *========o 75
        i = self.interval5.symmetric_difference(self.interval1)
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.constructor)
        self.assertIsInstance(i[1], self.constructor)
        self.assertEqual(i[0], self.constructor( 0, 25, "Chr1"))
        self.assertEqual(i[1], self.constructor(50, 75, "Chr1"))

    def test_symmetric_difference_2(self):
        # i1:      25 *========o 75
        # i5:  0 *========o 50        
        i = self.interval1.symmetric_difference(self.interval5)
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.constructor)
        self.assertIsInstance(i[1], self.constructor)
        self.assertEqual(i[0], self.constructor(50, 75, "Chr1"))
        self.assertEqual(i[1], self.constructor( 0, 25, "Chr1"))
        
    def test_symmetric_difference_3(self):
        # i0:  50 *================o 100
        # i2:       70 *========o 75        
        i = self.interval0.symmetric_difference(self.interval2)
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.constructor)
        self.assertIsInstance(i[1], self.constructor)
        self.assertEqual(i[0], self.constructor(50,  70, "Chr1"))
        self.assertEqual(i[1], self.constructor(75, 100, "Chr1"))

    def test_symmetric_difference_9(self):
        # i0:  50 *================o 100 Chr1
        # i4:    (different namespace)   Chr2
        i = self.interval0.symmetric_difference(self.interval4)
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.constructor)
        self.assertIsInstance(i[1], self.constructor)
        self.assertEqual(i[0], self.interval0)
        self.assertEqual(i[1], self.interval4)

    def test_union_10(self):
        # i0:  50 *================o 100 Chr1
        # i4:    (different namespace)   Chr2
        i = self.interval0 | self.interval4
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.constructor)
        self.assertIsInstance(i[1], self.constructor)
        self.assertEqual(i[0], self.interval0)
        self.assertEqual(i[1], self.interval4)

    def test_issubinterval_8(self):
        self.assertFalse(self.interval2.issubinterval(self.interval4))



class TestCase013_Interval(TestCase):
    constructor = Interval
    
    def setUp(self):
        self.interval0  = self.constructor("Chr1", 50, 100)
        self.interval1  = self.constructor("Chr1", 25,  75)
        self.interval2  = self.constructor("Chr1", 70,  75)
        self.interval3  = self.constructor("Chr1", 50,  75)
        self.interval4  = self.constructor("Chr2", 50, 100)
        self.interval5  = self.constructor("Chr1",  0,  50)
        self.interval6  = self.constructor("Chr1", 75, 100)
        self.interval7  = self.constructor("Chr1", 75, 125)
        self.interval8  = self.constructor()
        self.interval9  = self.constructor("other", 75, 100)
        self.interval10 = self.constructor("Chr1",100, 110)
        self.interval11 = self.constructor("Chr1", 50, 90)
        self.interval12 = self.constructor("Chr1",  0, 1000)


    def test_isempty_4(self):
        self.assertFalse(self.interval0.isempty())
        self.interval0.end = self.interval0.beg
        self.assertTrue(self.interval0.isempty())
        
    def test_mid_1(self):
        self.assertEqual(self.interval6.mid, 87)

    def test__and__3(self):
        i = self.interval0 & self.interval5
        self.assertIsInstance(i, self.constructor)
        self.assertTrue(i.isnull())

    def test_intersection_6(self):
        i = self.interval0.intersection(self.interval5)
        self.assertIsInstance(i, self.constructor)
        self.assertTrue(i.isnull())        
        
    def test_intersection_7(self):
        i = self.interval1.intersection(self.interval7)
        self.assertIsInstance(i, self.constructor)
        self.assertTrue(i.isnull())

    def test_isdisjoint_2(self):
        self.assertTrue(self.interval5.isdisjoint(self.interval3))

    def test_isdisjoint_3(self):
        self.assertTrue(self.interval3.isdisjoint(self.interval5))

    def test_isintersecting_6(self):
        self.assertFalse(self.interval0.isintersecting(self.interval5))

    def test_isintersecting_7(self):
        self.assertFalse(self.interval3.isintersecting(self.interval7))

    def test_isintersecting_beg_4(self):
        self.assertFalse(self.interval5.isintersecting_beg(self.interval0))

    def test_isintersecting_end_4(self):
        self.assertFalse(self.interval7.isintersecting_end(self.interval1))

    def test__or__6(self):
        # i3:           50 *======o 75
        # i5: 0 *==========o 50
        i = self.interval3 | self.interval5
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.constructor)
        self.assertIsInstance(i[1], self.constructor)
        self.assertEqual(i[0], self.interval3)
        self.assertEqual(i[1], self.interval5)

    def test__or__7(self):
        # i3:  50 *======o 75
        # i6:         75 *======o 100
        i = self.interval3 | self.interval6
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.constructor)
        self.assertIsInstance(i[1], self.constructor)
        self.assertEqual(i[0], self.interval3)
        self.assertEqual(i[1], self.interval6)

    def test_union_6(self):
        # i3:           50 *======o 75
        # i5: 0 *==========o 50
        i = self.interval3.union(self.interval5)
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.constructor)
        self.assertIsInstance(i[1], self.constructor)
        self.assertEqual(i[0], self.interval3)
        self.assertEqual(i[1], self.interval5)

    def test_union_7(self):
        # i3:  50 *======o 75
        # i6:         75 *======o 100
        i = self.interval3.union(self.interval6)
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.constructor)
        self.assertIsInstance(i[1], self.constructor)
        self.assertEqual(i[0], self.interval3)
        self.assertEqual(i[1], self.interval6)

    def test_to_string_2(self):
        s = self.constructor(2, 50, 100).to_string()
        self.assertIsInstance(s, str)
        self.assertEqual(s, '2:50-100')


        
class TestCase014_ClosedPoint(TestCase):
    constructor = ClosedPoint
    
    def setUp(self):
        self.point0 = self.constructor()
        self.point1 = self.constructor(56)

    def test_pos_getter_0(self):
        self.assertTrue(isnan(self.point0.pos))
        self.assertEqual(self.point1.pos, 56)
        
    def test_pos_setter_0(self):
        self.assertEqual(self.point1.pos, 56)
        self.point1.pos = 23
        self.assertEqual(self.point1.pos, 23)



class TestCase014_LeftClosedPoint(TestCase014_ClosedPoint):
    constructor = LeftClosedPoint
    
    def setUp(self):
        self.point0 = self.constructor()
        self.point1 = self.constructor(56)    



# class TestCase014_IntLeftClosedPoint(TestCase014_ClosedPoint):
#     def setUp(self):
#         self.point0 = IntLeftClosedPoint()
#         self.point1 = IntLeftClosedPoint(56)
        
        
class TestCase014__Node(TestCase):
    def test__init__0(self):
        with self.assertRaisesRegex(
                TypeError,
                r"missing \d+ required positional argument"):
            _Node()

    def test__init__1(self):
        node = _Node(
            Interval("Chr", 2, 5)
        )
        self.assertIsInstance(node, _Node)

    def test__init__2(self):
        node = _Node(
            Interval("Chr", 2, 5),
            Interval("Chr", 2, 5)
        )
        self.assertIsInstance(node, _Node)

    def test__init__3(self):
        node = _Node(
            Interval("Chr", 2, 5),
            Interval("Chr", 5, 8)
        )
        self.assertIsInstance(node, _Node)

        
class TestCase015__Node(TestCase):
    def setUp(self):
        self.interval0 = Interval("Chr", 2, 5)
        self.interval1 = Interval("Chr", 5, 8)
        self.intervalNode0 = _Node(self.interval0)
        self.intervalNode1 = _Node(self.interval0, self.interval1)

    def tearDown(self):
        del(self.interval0)
        del(self.interval1)
        del(self.intervalNode0)
        del(self.intervalNode1)
        
    def test_interval_getter_0(self):
        self.assertTrue(hasattr(self.intervalNode0, 'interval'))

    def test_interval_getter_1(self):
        self.assertEqual(self.intervalNode0.interval, self.interval0)

    def test_interval_getter_2(self):
        self.assertEqual(self.intervalNode1.interval, self.interval0)

    def test_interval_setter_0(self):
        self.assertEqual(self.intervalNode0.interval, self.interval0)
        self.intervalNode0.interval = self.interval1
        self.assertEqual(self.intervalNode0.interval, self.interval1)
        
    def test_instance_getter_0(self):
        self.assertTrue(hasattr(self.intervalNode0, 'instance'))

    def test_instance_getter_1(self):
        self.assertEqual(self.intervalNode0.instance, self.interval0)

    def test_instance_getter_2(self):
        self.assertEqual(self.intervalNode1.instance, self.interval1)

    def test_instance_setter_0(self):
        self.assertEqual(self.intervalNode0.instance, self.interval0)
        self.intervalNode0.instance = self.interval1
        self.assertEqual(self.intervalNode0.instance, self.interval1)
        
        
                                  
class TestCase016_IntervalList(TestCase):
    def setUp(self):
        self.constructor = IntervalList
        
    def test__add__0(self):
        self.assertTrue(hasattr(self.constructor(), '__add__'))
        
    def test__bool__0(self):
        self.assertTrue(hasattr(self.constructor(), '__bool__'))

    def test__class__0(self):
        self.assertTrue(hasattr(self.constructor(), '__class__'))

    def test__contains__0(self):
        self.assertTrue(hasattr(self.constructor(), '__contains__'))

    def test__copy__0(self):
        self.assertTrue(hasattr(self.constructor(), '__copy__'))

    def test__delitem__0(self):
        self.assertTrue(hasattr(self.constructor(), '__delitem__'))

    def test__eq__0(self):
        self.assertTrue(hasattr(self.constructor(), '__eq__'))

    def test__format__0(self):
        self.assertTrue(hasattr(self.constructor(), '__format__'))

    def test__ge__0(self):
        self.assertTrue(hasattr(self.constructor(), '__ge__'))

    def test__getitem__0(self):
        self.assertTrue(hasattr(self.constructor(), '__getitem__'))

    def test__gt__0(self):
        self.assertTrue(hasattr(self.constructor(), '__gt__'))

    def test__iadd__0(self):
        self.assertTrue(hasattr(self.constructor(), '__iadd__'))

    def test__imul__0(self):
        self.assertTrue(hasattr(self.constructor(), '__imul__'))

    def test__init__0(self):
        self.assertTrue(hasattr(self.constructor(), '__init__'))
        
    def test__init__1(self):
        ilist = self.constructor()
        self.assertIsInstance(ilist, self.constructor)
        self.assertEqual(len(ilist), 0)
        self.assertEqual(len(ilist), deque.__len__(ilist))

    def test__init__1(self):
        mysetter = lambda i: i
        ilist = self.constructor(setter=mysetter)
        self.assertIsInstance(ilist, self.constructor)
        self.assertEqual(len(ilist), 0)
        self.assertEqual(len(ilist), deque.__len__(ilist))
        self.assertIs(ilist._setter, mysetter)
        
    def test__iter__0(self):
        self.assertTrue(hasattr(self.constructor(), '__iter__'))

    def test__le__0(self):
        self.assertTrue(hasattr(self.constructor(), '__le__'))

    def test__len__0(self):
        self.assertTrue(hasattr(self.constructor(), '__len__'))

    def test__lt__0(self):
        self.assertTrue(hasattr(self.constructor(), '__lt__'))

    def test__mul__0(self):
        self.assertTrue(hasattr(self.constructor(), '__mul__'))

    def test__ne__0(self):
        self.assertTrue(hasattr(self.constructor(), '__ne__'))

    def test__repr__0(self):
        self.assertTrue(hasattr(self.constructor(), '__repr__'))

    def test__reversed__0(self):
        self.assertTrue(hasattr(self.constructor(), '__reversed__'))

    def test__rmul__0(self):
        self.assertTrue(hasattr(self.constructor(), '__rmul__'))

    def test__setitem__(self):
        self.assertTrue(hasattr(self.constructor(), '__setitem__'))

    def test__str__0(self):
        self.assertTrue(hasattr(self.constructor(), '__str__'))
        
    def test_append_0(self):
        self.assertTrue(hasattr(self.constructor(), 'append'))

    def test_appendleft_0(self):
        self.assertTrue(hasattr(self.constructor(), 'appendleft'))        

    def test_beg_0(self):
        self.assertTrue(hasattr(self.constructor(), 'beg'))
        
    def test_clear_0(self):
        self.assertTrue(hasattr(self.constructor(), 'clear'))
            
    def test_copy_0(self):
        self.assertTrue(hasattr(self.constructor(), 'copy'))

    def test_count_0(self):
        self.assertTrue(hasattr(self.constructor(), 'count'))

    def test_end_0(self):
        self.assertTrue(hasattr(self.constructor(), 'end'))
        
    def test_extend_0(self):
        self.assertTrue(hasattr(self.constructor(), 'extend'))

    def test_extendleft_0(self):
        self.assertTrue(hasattr(self.constructor(), 'extendleft'))

    def test_hull_0(self):
        self.assertTrue(hasattr(self.constructor(), 'hull'))
        
    def test_index_0(self):
        self.assertTrue(hasattr(self.constructor(), 'index'))

    def test_insert_0(self):
        self.assertTrue(hasattr(self.constructor(), 'insert'))

    def test_insort_0(self):
        self.assertTrue(hasattr(self.constructor(), 'insort'))

    def test_insortleft_0(self):
        self.assertTrue(hasattr(self.constructor(), 'insortleft'))

    def test_isempty_0(self):
        self.assertTrue(hasattr(self.constructor(), 'isempty'))

    def test_isfinite_0(self):
        self.assertTrue(hasattr(self.constructor(), 'isfinite'))

    def test_isnull_0(self):
        self.assertTrue(hasattr(self.constructor(), 'isnull'))

    def test_namespace_0(self):
        self.assertTrue(hasattr(self.constructor(), 'namespace'))

    def test_pop_0(self):
        self.assertTrue(hasattr(self.constructor(), 'pop'))

    def test_popleft_0(self):
        self.assertTrue(hasattr(self.constructor(), 'popleft'))

    def test_remove_0(self):
        self.assertTrue(hasattr(self.constructor(), 'remove'))

    def test_reverse_0(self):
        self.assertTrue(hasattr(self.constructor(), 'reverse'))

    def test_rotate_0(self):
        self.assertTrue(hasattr(self.constructor(), 'rotate'))

    def test_start_0(self):
        self.assertTrue(hasattr(self.constructor(), 'start'))

    def test_stop_0(self):
        self.assertTrue(hasattr(self.constructor(), 'stop'))

    def test_update_0(self):
        self.assertTrue(hasattr(self.constructor(), 'update'))

    def test_updateleft_0(self):
        self.assertTrue(hasattr(self.constructor(), 'updateleft'))

    def test_find_index_beg_0(self):
        self.assertTrue(hasattr(self.constructor(), 'find_index_beg'))

    def test_find_index_start_0(self):
        self.assertTrue(hasattr(self.constructor(), 'find_index_start'))
        
    def test_find_index_end_0(self):
        self.assertTrue(hasattr(self.constructor(), 'find_index_end'))

    def test_find_index_stop_0(self):
        self.assertTrue(hasattr(self.constructor(), 'find_index_stop'))        
        
    def test_find_index_nearest_0(self):
        self.assertTrue(hasattr(self.constructor(), 'find_index_nearest'))

    def test_find_insertion_index_beg_0(self):
        self.assertTrue(hasattr(self.constructor(), 'find_insertion_index_beg'))

    def test_find_insertion_index_start_0(self):
        self.assertTrue(hasattr(self.constructor(), 'find_insertion_index_start'))        

    def test_find_insertion_index_end_0(self):
        self.assertTrue(hasattr(self.constructor(), 'find_insertion_index_end'))

    def test_find_insertion_index_stop_0(self):
        self.assertTrue(hasattr(self.constructor(), 'find_insertion_index_stop'))        

    def test_find_insertion_index_0(self):
        self.assertTrue(hasattr(self.constructor(), 'find_insertion_index'))
        
    def test_find_intersection_index_beg_0(self):
        self.assertTrue(hasattr(self.constructor(), 'find_intersection_index_beg'))

    def test_find_intersection_index_start_0(self):
        self.assertTrue(hasattr(self.constructor(), 'find_intersection_index_start'))
        
    def test_find_intersection_index_end_0(self):
        self.assertTrue(hasattr(self.constructor(), 'find_intersection_index_end'))

    def test_find_intersection_index_stop_0(self):
        self.assertTrue(hasattr(self.constructor(), 'find_intersection_index_stop'))        

    def test_find_intersection_index_nearest_0(self):
        self.assertTrue(hasattr(self.constructor(), 'find_intersection_index_nearest'))
        
    def test_find_intersection_index_range_0(self):
        self.assertTrue(hasattr(self.constructor(), 'find_intersection_index_range'))
        
    def test_find_intersection_index_slice_0(self):
        self.assertTrue(hasattr(self.constructor(), 'find_intersection_index_slice'))
        
    def test_intersection_length_0(self):
        self.assertTrue(hasattr(self.constructor(), 'intersection_length'))
        
    def test_intersection_fraction_0(self):
        self.assertTrue(hasattr(self.constructor(), 'intersection_fraction'))

    def test_find_intersecting_0(self):
        self.assertTrue(hasattr(self.constructor(), 'find_intersecting'))


        
class TestCase017_IntervalList(TestCase):
    constructor = IntervalList
    def setUp(self):
        self.interval0  = Interval("Chr", 0, 4)
        self.interval10 = Interval("Chr", 0, 50)
        self.interval9  = Interval("Chr", 0, 5000)
        self.interval1  = Interval("Chr", 1, 5)
        self.interval2  = Interval("Chr", 1, 5)
        self.interval8  = Interval("Chr", 5, 15)
        self.interval3  = Interval("Chr", 10, 25)
        self.interval4  = Interval("Chr", 25, 50)
        self.interval5  = Interval("Chr", 20, 35)
        self.interval12 = Interval("Chr", 35, 97)
        self.interval11 = Interval("Chr", 40,100)
        self.interval6  = Interval("Chr", 45, 95)
        self.interval7  = Interval("Chr", 100, 110)
        self.interval13 = Interval("X", 100, 110)

        self.instance1 = self.constructor()
        self.instance2 = self.constructor([
            self.interval1,  # Chr:1-5
            self.interval3,  # Chr:10-25
            self.interval5   # Chr:20-35
        ])
        self.instance3 = self.constructor([
            self.interval0,  # 0-4
            self.interval1,  # 1-5
            self.interval8,  # 5-15
            self.interval4,  # 25-50
            self.interval11, # 40-100
            self.interval6,  # 45-95
            self.interval7   # 100-110
        ])

    def tearDown(self):
        del(self.interval0)
        del(self.interval1)
        del(self.interval2)
        del(self.interval3)
        del(self.interval4)
        del(self.interval5)
        del(self.interval6)
        del(self.interval7)
        del(self.interval8)
        del(self.interval9)
        del(self.interval10)
        del(self.interval11)
        del(self.interval12)
        del(self.interval13)
        del(self.instance1)
        del(self.instance2)
        del(self.instance3)
        
    def test__init__0(self):
        ilist = self.constructor([self.interval0])
        self.assertIsInstance(ilist, self.constructor)
        self.assertEqual(len(ilist), 1)
        self.assertEqual(len(ilist), deque.__len__(ilist))
        self.assertEqual(ilist[0], self.interval0)
        self.assertEqual(ilist._get_node(0).max, self.interval0.end)
        
    def test__init__1(self):
        intervals = [(5, self.interval0)]
        ilist = self.constructor(intervals, setter=lambda i: i[1])
        self.assertIsInstance(ilist, self.constructor)
        self.assertEqual(len(ilist), len(intervals))
        self.assertEqual(len(ilist), deque.__len__(ilist))
        self.assertEqual(list(ilist), intervals)
        self.assertEqual(ilist._get_node(0).max, self.interval0.end)
        
    def test__init__2(self):
        intervals = [
            (4, self.interval0),
            (5, self.interval1),
            (15, self.interval8)
        ]
        ilist = self.constructor(intervals, setter=lambda i: i[1])
        self.assertIsInstance(ilist, self.constructor)
        self.assertEqual(len(ilist), len(intervals))
        self.assertEqual(len(ilist), deque.__len__(ilist))
        self.assertEqual(list(ilist), intervals)
        for i in range(len(intervals)):
            self.assertEqual(ilist._get_node(i).max, intervals[i][0])
        
    def test__init__3(self):
        expected_max = [5, 25, 35]
        observed_max = [
            self.instance2._get_node(i).max \
            for i in range(len(self.instance2))
        ]
        self.assertEqual(observed_max, expected_max)
        
    def test__init__4(self):
        expected_max = [4, 5, 15, 50, 100, 100, 110]
        observed_max = [
            self.instance3._get_node(i).max \
            for i in range(len(self.instance3))
        ]
        self.assertEqual(observed_max, expected_max)

    def test__init__5(self):
        with self.assertRaises(ValueError):
            self.constructor([self.interval0, self.interval13])

    def test__setitem__0(self):
        num_items = len(self.instance2)
        self.instance2[2] = self.interval12  # 35-97
        self.assertEqual(len(self.instance2), num_items)
        self.assertEqual(len(self.instance2), deque.__len__(self.instance2))
        self.assertIs(self.instance2[2], self.interval12)
        expected_max = [5, 25, 97]
        observed_max = [
            self.instance2._get_node(i).max \
            for i in range(len(self.instance2))
        ]
        self.assertEqual(observed_max, expected_max)

    def test__setitem__1(self):
        num_items = len(self.instance2)
        self.instance2[1] = self.interval8  # 5-15
        self.assertEqual(len(self.instance2), num_items)
        self.assertEqual(len(self.instance2), deque.__len__(self.instance2))
        self.assertIs(self.instance2[1], self.interval8)
        expected_max = [5, 15, 35]
        observed_max = [
            self.instance2._get_node(i).max \
            for i in range(len(self.instance2))
        ]
        self.assertEqual(observed_max, expected_max)
        
    def test__setitem__2(self):
        num_items = len(self.instance2)
        self.instance2[1] = interval = Interval("Chr",10,40)
        self.assertEqual(len(self.instance2), num_items)
        self.assertEqual(len(self.instance2), deque.__len__(self.instance2))
        self.assertIs(self.instance2[1], interval)
        expected_max = [5, 40, 40]
        observed_max = [
            self.instance2._get_node(i).max \
            for i in range(len(self.instance2))
        ]
        self.assertEqual(observed_max, expected_max)

    def test__setitem__3(self):
        num_items = len(self.instance3)
        self.instance3[5] = interval = Interval("Chr",41,99)
        self.assertEqual(len(self.instance3), num_items)
        self.assertEqual(len(self.instance3), deque.__len__(self.instance3))
        self.assertIs(self.instance3[5], interval)
        expected_max = [4, 5, 15, 50, 100, 100, 110]
        observed_max = [
            self.instance3._get_node(i).max \
            for i in range(len(self.instance3))
        ]
        self.assertEqual(observed_max, expected_max)

    def test__setitem__4(self):
        num_items = len(self.instance3)
        self.instance3[4] = interval = Interval("Chr",40,55)
        self.assertEqual(len(self.instance3), num_items)
        self.assertEqual(len(self.instance3), deque.__len__(self.instance3))
        self.assertIs(self.instance3[4], interval)
        expected_max = [4, 5, 15, 50, 55, 95, 110]
        observed_max = [
            self.instance3._get_node(i).max \
            for i in range(len(self.instance3))
        ]
        self.assertEqual(observed_max, expected_max)

    def test__setitem__5(self):
        num_items = len(self.instance3)
        self.instance3[4] = interval = Interval("Chr",40,45)
        self.assertEqual(len(self.instance3), num_items)
        self.assertEqual(len(self.instance3), deque.__len__(self.instance3))
        self.assertIs(self.instance3[4], interval)
        expected_max = [4, 5, 15, 50, 50, 95, 110]
        observed_max = [
            self.instance3._get_node(i).max \
            for i in range(len(self.instance3))
        ]
        self.assertEqual(observed_max, expected_max)

    def test__str__0(self):
        self.assertIsInstance(str(self.instance1), str)
        self.assertEqual(str(self.instance1),'[]')

    def test__str__1(self):
        string = '[%s, %s, %s]' % (
            str(self.interval1),
            str(self.interval3),
            str(self.interval5)
        )
        self.assertEqual(str(self.instance2), string)
        
    def test_append_0(self):
        num_items = len(self.instance1)
        self.assertEqual(num_items, deque.__len__(self.instance1))
        self.instance1.append(self.interval6)
        self.assertEqual(len(self.instance1), num_items+1)
        self.assertEqual(len(self.instance1), deque.__len__(self.instance1))
        self.assertIs(self.instance1[-1], self.interval6)

    def test_append_1(self):
        num_items = len(self.instance2)
        self.assertEqual(num_items, deque.__len__(self.instance2))
        self.instance2.append(self.interval6)
        self.assertEqual(len(self.instance2), num_items+1)
        self.assertEqual(len(self.instance2), deque.__len__(self.instance2))
        self.assertIs(self.instance2[-1], self.interval6)
        
    def test_append_2(self):
        expected_max = [5, 25, 35, 95]
        self.instance2.append(self.interval6)

        observed_max = [
            self.instance2._get_node(i).max \
            for i in range(len(self.instance2))
        ]
        self.assertEqual(observed_max, expected_max)

    def test_append_3(self):
        expected_max = [5, 25, 35, 50]
        self.instance2.append(self.interval4)

        observed_max = [
            self.instance2._get_node(i).max \
            for i in range(len(self.instance2))
        ]
        self.assertEqual(observed_max, expected_max)

    def test_append_4(self):
        expected_max = [5, 25, 35, 35]
        self.instance2.append(Interval("Chr", 21, 30))

        observed_max = [
            self.instance2._get_node(i).max \
            for i in range(len(self.instance2))
        ]
        self.assertEqual(observed_max, expected_max)        
                    
    def test_appendleft_0(self):
        num_items = len(self.instance1)
        self.assertEqual(num_items, deque.__len__(self.instance1))
        self.instance1.appendleft(self.interval6)
        self.assertEqual(len(self.instance1), num_items+1)
        self.assertEqual(len(self.instance1), deque.__len__(self.instance1))
        self.assertIs(self.instance1[0], self.interval6)

    def test_appendleft_1(self):
        num_items = len(self.instance2)
        self.assertEqual(num_items, deque.__len__(self.instance2))
        self.instance2.appendleft(self.interval6)
        self.assertEqual(len(self.instance2), num_items+1)
        self.assertEqual(len(self.instance2), deque.__len__(self.instance2))
        self.assertIs(self.instance2[0], self.interval6)
        
    def test_appendleft_2(self):
        expected_max = [1, 5, 25, 35]
        self.instance2.appendleft(Interval("Chr",0,1))

        observed_max = [
            self.instance2._get_node(i).max \
            for i in range(len(self.instance2))
        ]
        self.assertEqual(observed_max, expected_max)
        
    def test_appendleft_3(self):
        expected_max = [4, 5, 25, 35]
        self.instance2.appendleft(self.interval0)

        observed_max = [
            self.instance2._get_node(i).max \
            for i in range(len(self.instance2))
        ]
        self.assertEqual(observed_max, expected_max)

    def test_appendleft_4(self):
        expected_max = [50, 50, 50, 50, 50, 100, 100, 110]
        self.instance3.appendleft(self.interval10)

        observed_max = [
            self.instance3._get_node(i).max \
            for i in range(len(self.instance3))
        ]
        self.assertEqual(observed_max, expected_max)

    def test_clear_1(self):
        ilist = self.constructor([self.interval0])
        self.assertIsInstance(ilist, self.constructor)
        self.assertEqual(len(ilist), 1)
        self.assertEqual(len(ilist), deque.__len__(ilist))
        ilist.clear()
        self.assertEqual(len(ilist), 0)
        self.assertEqual(len(ilist), deque.__len__(ilist))
        
    def test_extend_0(self):
        num_items = len(self.instance2)
        self.assertEqual(num_items, deque.__len__(self.instance2))
        self.instance2.extend([self.interval0])
        self.assertEqual(len(self.instance2), num_items+1)
        self.assertEqual(len(self.instance2), deque.__len__(self.instance2))
        self.assertIs(self.instance2[-1], self.interval0)

    def test_extend_1(self):
        expected_max = [5, 25, 35, 95, 110]
        self.instance2.extend([
            self.interval6,
            self.interval7
        ])

        observed_max = [
            self.instance2._get_node(i).max \
            for i in range(len(self.instance2))
        ]
        self.assertEqual(observed_max, expected_max)

    def test_extend_2(self):
        expected_max = [5, 25, 35, 35, 95]
        self.instance2.extend([
            Interval("Chr",25,30),
            self.interval6
        ])

        observed_max = [
            self.instance2._get_node(i).max \
            for i in range(len(self.instance2))
        ]
        self.assertEqual(observed_max, expected_max)

    def test_extend_3(self):
        expected_max = [5, 25, 35, 35, 100, 100]
        self.instance2.extend([
            Interval("Chr",25,30),
            self.interval11,
            self.interval6
        ])

        observed_max = [
            self.instance2._get_node(i).max \
            for i in range(len(self.instance2))
        ]
        self.assertEqual(observed_max, expected_max)
        
    def test_extendleft_0(self):
        num_items = len(self.instance2)
        self.assertEqual(num_items, deque.__len__(self.instance2))
        self.instance2.extendleft([self.interval6])
        self.assertEqual(len(self.instance2), num_items+1)
        self.assertEqual(len(self.instance2), deque.__len__(self.instance2))
        self.assertIs(self.instance2[0], self.interval6)

    def test_extendleft_1(self):
        expected_max = [4, 5, 25, 35]
        self.instance2.extendleft([
            self.interval0
        ])

        observed_max = [
            self.instance2._get_node(i).max \
            for i in range(len(self.instance2))
        ]
        self.assertEqual(observed_max, expected_max)        

    def test_extendleft_2(self):
        expected_max = [50, 50, 50, 50, 50, 100, 100, 110]
        self.instance3.extendleft([
            self.interval10
        ])

        observed_max = [
            self.instance3._get_node(i).max \
            for i in range(len(self.instance3))
        ]
        self.assertEqual(observed_max, expected_max)
        
    def test_extendleft_3(self):
        expected_max = [50, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000]
        self.instance3.extendleft([
            self.interval9,
            self.interval10
        ])

        observed_max = [
            self.instance3._get_node(i).max \
            for i in range(len(self.instance3))
        ]
        self.assertEqual(observed_max, expected_max)        
        
    def test_insert_0(self):
        num_items = len(self.instance2)
        self.assertEqual(num_items, deque.__len__(self.instance2))
        self.instance2.insert(2, self.interval4)
        self.assertEqual(len(self.instance2), num_items+1)
        self.assertEqual(len(self.instance2), deque.__len__(self.instance2))
        self.assertEqual(
            list(self.instance2),
            [self.interval1, self.interval3, self.interval4, self.interval5]
        )

    def test_insert_1(self):
        expected_max = [5, 15, 25, 35]
        self.instance2.insert(1, self.interval8)  # 5-15

        observed_max = [
            self.instance2._get_node(i).max \
            for i in range(len(self.instance2))
        ]
        self.assertEqual(observed_max, expected_max)        

    def test_insert_2(self):
        expected_max = [50, 50, 50, 50, 50, 100, 100, 110]
        self.instance3.insert(0, self.interval10)

        observed_max = [
            self.instance3._get_node(i).max \
            for i in range(len(self.instance3))
        ]
        self.assertEqual(observed_max, expected_max)        

    def test_insert_3(self):
        expected_max = [4, 50, 50, 50, 50, 100, 100, 110]
        self.instance3.insert(1, self.interval10)

        observed_max = [
            self.instance3._get_node(i).max \
            for i in range(len(self.instance3))
        ]
        self.assertEqual(observed_max, expected_max)

    def test_insert_4(self):
        expected_max = [50, 50, 50]
        ilist = self.constructor([
            self.interval10,  # 0-50
            self.interval4,   # 25-50
        ])
        num_items = len(ilist)
        self.assertEqual(num_items, deque.__len__(ilist))
        ilist.insert(1, self.interval5)
        self.assertEqual(len(ilist), num_items+1)
        self.assertEqual(len(ilist), deque.__len__(ilist))
        observed_max = [
            ilist._get_node(i).max \
            for i in range(len(ilist))
        ]
        self.assertEqual(observed_max, expected_max)
        
    def test_update_1(self):
        num_items = len(self.instance2)
        answer = [
            self.interval1,
            self.interval2,
            self.interval3,
            self.interval5,
            self.interval6,
            self.interval7
        ]
        self.assertEqual(num_items, deque.__len__(self.instance2))
        self.instance2.update([self.interval6, self.interval2, self.interval7])
        self.assertEqual(len(self.instance2), num_items+3)
        self.assertEqual(len(self.instance2), deque.__len__(self.instance2))
        self.assertEqual(list(self.instance2), answer)
        self.assertIs(self.instance2[0], self.interval1)
        self.assertIs(self.instance2[1], self.interval2)

    def test_updateleft_1(self):
        num_items = len(self.instance2)
        answer = [
            self.interval0,
            self.interval2,
            self.interval1,
            self.interval3,
            self.interval5,
            self.interval7
        ]
        self.assertEqual(num_items, deque.__len__(self.instance2))
        self.instance2.updateleft([self.interval0, self.interval2, self.interval7])
        self.assertEqual(len(self.instance2), num_items+3)
        self.assertEqual(len(self.instance2), deque.__len__(self.instance2))
        self.assertEqual(list(self.instance2), answer)
        self.assertIs(self.instance2[1], self.interval2)
        self.assertIs(self.instance2[2], self.interval1)
        
    def test_popleft_1(self):
        num_items = len(self.instance2)
        self.assertEqual(num_items, deque.__len__(self.instance2))
        item1 = self.instance2[0]
        item2 = self.instance2.popleft()
        self.assertEqual(len(self.instance2), num_items-1)
        self.assertEqual(len(self.instance2), deque.__len__(self.instance2))
        self.assertIs(item1, item2)

    def test_popleft_2(self):
        expected_max = [25, 35]
        item = self.instance2.popleft()

        observed_max = [
            self.instance2._get_node(i).max \
            for i in range(len(self.instance2))
        ]
        self.assertEqual(observed_max, expected_max)

    def test_popleft_3(self):
        expected_max = [5, 15, 50, 100, 100, 110]
        item = self.instance3.popleft()

        observed_max = [
            self.instance3._get_node(i).max \
            for i in range(len(self.instance3))
        ]
        self.assertEqual(observed_max, expected_max)

    def test_popleft_4(self):
        expected_max = [50, 50, 50, 50, 100, 100, 110]
        ilist = self.constructor([
            self.interval10,
            self.interval1,
            self.interval8,
            self.interval4,
            self.interval11,
            self.interval6,
            self.interval7
        ])
        observed_max = [
            ilist._get_node(i).max \
            for i in range(len(ilist))
        ]
        self.assertEqual(observed_max, expected_max)

        item = ilist.popleft()
        expected_max = [5, 15, 50, 100, 100, 110]
        observed_max = [
            ilist._get_node(i).max \
            for i in range(len(ilist))
        ]
        self.assertEqual(observed_max, expected_max)
        
    def test_pop_1(self):
        num_items = len(self.instance2)
        self.assertEqual(num_items, deque.__len__(self.instance2))
        item1 = self.instance2[-1]
        item2 = self.instance2.pop()
        self.assertEqual(len(self.instance2), num_items-1)
        self.assertEqual(len(self.instance2), deque.__len__(self.instance2))
        self.assertIs(item1, item2)

    def test_pop_2(self):
        expected_max = [4, 5, 15, 50, 100, 100]
        item = self.instance3.pop()

        observed_max = [
            self.instance3._get_node(i).max \
            for i in range(len(self.instance3))
        ]
        self.assertEqual(observed_max, expected_max)

    def test_pop_3(self):
        expected_max = [5, 25]
        item = self.instance2.pop()

        observed_max = [
            self.instance2._get_node(i).max \
            for i in range(len(self.instance2))
        ]
        self.assertEqual(observed_max, expected_max)
        
    def test_pop_4(self):
        expected_max = [50, 50, 100, 100]
        ilist = self.constructor([
            self.interval10,
            self.interval3,
            self.interval11,
            self.interval6
        ])

        observed_max = [
            ilist._get_node(i).max \
            for i in range(len(ilist))
        ]
        self.assertEqual(observed_max, expected_max)

        item = ilist.pop()
        expected_max = [50, 50, 100]
        observed_max = [
            ilist._get_node(i).max \
            for i in range(len(ilist))
        ]
        self.assertEqual(observed_max, expected_max)
    
    def test_rotate_1(self):
        self.instance2 = self.constructor([
            self.interval3, self.interval4, self.interval5
        ])
        num_items = len(self.instance2)
        item1 = self.instance2[0]
        item2 = self.instance2[1]
        item3 = self.instance2[-1]
        self.instance2.rotate(-1)  # pull leftward
        self.assertEqual(len(self.instance2), num_items)
        self.assertEqual(len(self.instance2), deque.__len__(self.instance2))
        self.assertIs(self.instance2[0], item2)
        self.assertIs(self.instance2[-2], item3)
        self.assertIs(self.instance2[-1], item1)
        
    def test_rotate_2(self):
        self.instance2 = self.constructor([
            self.interval3, self.interval4, self.interval5
        ])
        num_items = len(self.instance2)
        item1 = self.instance2[0]
        item2 = self.instance2[-2]
        item3 = self.instance2[-1]
        self.instance2.rotate(+1)  # pull rightward
        self.assertEqual(len(self.instance2), num_items)
        self.assertEqual(len(self.instance2), deque.__len__(self.instance2))
        self.assertIs(self.instance2[0], item3)
        self.assertIs(self.instance2[1], item1)
        self.assertIs(self.instance2[-1], item2)        

    def test_remove_1(self):
        num_items = len(self.instance3)
        answer = [
            self.interval0,
            self.interval1,
            self.interval8,
            self.interval4,
            self.interval6,
            self.interval7
        ]
        self.assertEqual(num_items, deque.__len__(self.instance3))
        self.instance3.remove(self.interval11)
        self.assertEqual(len(self.instance3), num_items-1)
        self.assertEqual(len(self.instance3), deque.__len__(self.instance3))
        self.assertEqual(list(self.instance3), answer)

    def test_remove_2(self):
        num_items = len(self.instance3)
        answer = [
            self.interval1,
            self.interval8,
            self.interval4,
            self.interval11,
            self.interval6,
            self.interval7
        ]
        self.assertEqual(num_items, deque.__len__(self.instance3))
        self.instance3.remove(self.interval0)
        self.assertEqual(len(self.instance3), num_items-1)
        self.assertEqual(len(self.instance3), deque.__len__(self.instance3))
        self.assertEqual(list(self.instance3), answer)

    def test_remove_3(self):
        num_items = len(self.instance3)
        answer = [
            self.interval0,
            self.interval1,
            self.interval8,
            self.interval4,
            self.interval11,
            self.interval6,
        ]
        self.assertEqual(num_items, deque.__len__(self.instance3))
        self.instance3.remove(self.interval7)
        self.assertEqual(len(self.instance3), num_items-1)
        self.assertEqual(len(self.instance3), deque.__len__(self.instance3))
        self.assertEqual(list(self.instance3), answer)        
        
    def test_remove_4(self):
        expected_max = [4, 5, 15, 50, 100, 100, 110]
        observed_max = [
            self.instance3._get_node(i).max \
            for i in range(len(self.instance3))
        ]
        self.assertEqual(observed_max, expected_max)

        self.instance3.remove(self.interval6)
        
        expected_max = [4, 5, 15, 50, 100, 110]
        observed_max = [
            self.instance3._get_node(i).max \
            for i in range(len(self.instance3))
        ]
        self.assertEqual(observed_max, expected_max)

    def test_remove_5(self):
        expected_max = [4, 5, 15, 50, 100, 100, 110]
        observed_max = [
            self.instance3._get_node(i).max \
            for i in range(len(self.instance3))
        ]
        self.assertEqual(observed_max, expected_max)

        self.instance3.remove(self.interval11)
        
        expected_max = [4, 5, 15, 50, 95, 110]
        observed_max = [
            self.instance3._get_node(i).max \
            for i in range(len(self.instance3))
        ]
        self.assertEqual(observed_max, expected_max)

    def test_remove_6(self):
        expected_max = [97, 100, 100]
        ilist = self.constructor([
            self.interval12,  # 35-97
            self.interval11,  # 40-100
            self.interval6    # 45-95
        ])
        observed_max = [
            ilist._get_node(i).max \
            for i in range(len(ilist))
        ]
        self.assertEqual(observed_max, expected_max)

        ilist.remove(self.interval11)

        expected_max = [97, 97]
        observed_max = [
            ilist._get_node(i).max \
            for i in range(len(ilist))
        ]
        self.assertEqual(observed_max, expected_max)
        
    def test_find_index_beg_1(self):
        index = self.instance2.find_index_beg(Interval("Chr", 0, 1))
        self.assertEqual(index, 0)

    def test_find_index_beg_2(self):
        index = self.instance2.find_index_beg(Interval("Chr", 1, 2))
        self.assertEqual(index, 0)
        
    def test_find_index_beg_3(self):
        index = self.instance2.find_index_beg(Interval("Chr", 4, 5))
        self.assertEqual(index, 0)

    def test_find_index_beg_4(self):
        index = self.instance2.find_index_beg(Interval("Chr", 5, 6))
        self.assertEqual(index, 1)

    def test_find_index_beg_5(self):
        index = self.instance2.find_index_beg(Interval("Chr", 9, 10))
        self.assertEqual(index, 1)

    def test_find_index_beg_6(self):
        index = self.instance2.find_index_beg(Interval("Chr", 10, 11))
        self.assertEqual(index, 1)

    def test_find_index_beg_7(self):
        index = self.instance2.find_index_beg(Interval("Chr", 19, 20))
        self.assertEqual(index, 1)
        
    def test_find_index_beg_8(self):
        index = self.instance2.find_index_beg(Interval("Chr", 20, 21))
        self.assertEqual(index, 1)

    def test_find_index_beg_9(self):
        index = self.instance2.find_index_beg(Interval("Chr", 24, 25))
        self.assertEqual(index, 1)

    def test_find_index_beg_10(self):
        index = self.instance2.find_index_beg(Interval("Chr", 25, 26))
        self.assertEqual(index, 2)

    def test_find_index_beg_11(self):
        index = self.instance2.find_index_beg(Interval("Chr", 34, 35))
        self.assertEqual(index, 2)

    def test_find_index_beg_12(self):
        index = self.instance2.find_index_beg(Interval("Chr", 35, 36))
        self.assertEqual(index, 3)

    def test_find_index_beg_13(self):
        ilist = self.constructor([
            self.interval9,  #   0-5000
            self.interval3,  #  10-25
            self.interval7   # 100-110
        ])
        for i in range(len(ilist)):
            self.assertEqual(ilist._get_node(i).max, 5000)
            
        index = ilist.find_index_beg(self.interval5)  # 20-35
        self.assertEqual(index, 0)

    def test_find_index_beg_14(self):
        ilist = self.constructor([
            self.interval9,  #   0-5000
            self.interval3,  #  10-25
            self.interval7   # 100-110
        ])
        for i in range(len(ilist)):
            self.assertEqual(ilist._get_node(i).max, 5000)
        
        index = ilist.find_index_beg(self.interval6)  # 45-95
        self.assertEqual(index, 0)

    def test_find_index_beg_15(self):
        index = self.instance3.find_index_beg(Interval("Chr",95,100))
        self.assertEqual(index, 4)
        
    def test_find_index_end_1(self):
        index = self.instance2.find_index_end(Interval("Chr", 0, 1))
        self.assertEqual(index, 0)

    def test_find_index_end_2(self):
        index = self.instance2.find_index_end(Interval("Chr", 1, 2))
        self.assertEqual(index, 1)
        
    def test_find_index_end_3(self):
        index = self.instance2.find_index_end(Interval("Chr", 4, 5))
        self.assertEqual(index, 1)

    def test_find_index_end_4(self):
        index = self.instance2.find_index_end(Interval("Chr", 5, 6))
        self.assertEqual(index, 1)

    def test_find_index_end_5(self):
        index = self.instance2.find_index_end(Interval("Chr", 9, 10))
        self.assertEqual(index, 1)

    def test_find_index_end_6(self):
        index = self.instance2.find_index_end(Interval("Chr", 10, 11))
        self.assertEqual(index, 2)

    def test_find_index_end_7(self):
        index = self.instance2.find_index_end(Interval("Chr", 19, 20))
        self.assertEqual(index, 2)
        
    def test_find_index_end_8(self):
        index = self.instance2.find_index_end(Interval("Chr", 20, 21))
        self.assertEqual(index, 3)
        
    def test_find_index_end_9(self):
        index = self.instance2.find_index_end(Interval("Chr", 24, 25))
        self.assertEqual(index, 3)

    def test_find_index_end_10(self):
        index = self.instance2.find_index_end(Interval("Chr", 25, 26))
        self.assertEqual(index, 3)

    def test_find_index_end_11(self):
        index = self.instance2.find_index_end(Interval("Chr", 34, 35))
        self.assertEqual(index, 3)

    def test_find_index_end_12(self):
        index = self.instance2.find_index_end(Interval("Chr", 35, 36))
        self.assertEqual(index, 3)        

    def test_find_index_end_13(self):
        ilist = self.constructor([
            self.interval9,  #   0-5000
            self.interval3,  #  10-25
            self.interval7   # 100-110
        ])
        index = ilist.find_index_end(self.interval5)  # 20-35
        self.assertEqual(index, 2)

    def test_find_index_end_14(self):
        ilist = self.constructor([
            self.interval9,  #   0-5000
            self.interval3,  #  10-25
            self.interval7   # 100-110
        ])
        index = ilist.find_index_end(self.interval6)  # 45-95
        self.assertEqual(index, 2)

    def test_find_index_end_15(self):
        ilist = self.constructor([
            self.interval9,  #   0-5000
            self.interval3,  #  10-25
            self.interval4,  #  25-50
            self.interval7   # 100-110
        ])
        index = ilist.find_index_end(Interval("Chr",49,101))
        self.assertEqual(index, 4)
        
    def test_find_index_nearest_1(self):
        index = self.instance2.find_index_nearest(Interval("Chr",0,1))
        self.assertEqual(index, 0)

    def test_find_index_nearest_2(self):
        index = self.instance2.find_index_nearest(Interval("Chr",1,2))
        self.assertEqual(index, 0)

    def test_find_index_nearest_3(self):
        index = self.instance2.find_index_nearest(Interval("Chr",4,5))
        self.assertEqual(index, 0)

    def test_find_index_nearest_4(self):
        index = self.instance2.find_index_nearest(Interval("Chr",5,6))
        self.assertEqual(index, 0)

    def test_find_index_nearest_5(self):
        index = self.instance2.find_index_nearest(Interval("Chr",6,7))
        self.assertEqual(index, 0)

    def test_find_index_nearest_6(self):
        # equidinstant features return left-most index
        index = self.instance2.find_index_nearest(Interval("Chr",7,8))
        self.assertEqual(index, 0)

    def test_find_index_nearest_7(self):
        index = self.instance2.find_index_nearest(Interval("Chr",8,9))
        self.assertEqual(index, 1)

    def test_find_index_nearest_8(self):
        index = self.instance2.find_index_nearest(Interval("Chr",9,10))
        self.assertEqual(index, 1)

    def test_find_index_nearest_9(self):
        index = self.instance2.find_index_nearest(Interval("Chr",10,11))
        self.assertEqual(index, 1)
        
    def test_find_index_nearest_10(self):
        index = self.instance2.find_index_nearest(Interval("Chr",24,25))
        self.assertEqual(index, 2)

    def test_find_index_nearest_11(self):
        index = self.instance2.find_index_nearest(Interval("Chr",25,26))
        self.assertEqual(index, 2)

    def test_find_index_nearest_12(self):
        index = self.instance2.find_index_nearest(Interval("Chr",50,51))
        self.assertEqual(index, 2)

    def test_find_insertion_index_beg_1(self):
        index = self.instance1.find_insertion_index_beg(Interval("Chr", 50,51))
        self.assertEqual(index, 0)

    def test_find_insertion_index_beg_2(self):
        index = self.instance2.find_insertion_index_beg(Interval("Chr",5,10))
        self.assertEqual(index, 1)

    def test_find_insertion_index_beg_3(self):
        index = self.instance2.find_insertion_index_beg(Interval("Chr",15,20))
        self.assertEqual(index, 2)

    def test_find_insertion_index_beg_4(self):
        index = self.instance2.find_insertion_index_beg(Interval("Chr",40,50))
        self.assertEqual(index, 3)
        
    def test_find_insertion_index_beg_5(self):
        index = self.instance2.find_insertion_index_beg(Interval("Chr",1,5))
        self.assertEqual(index, 0)

    def test_find_insertion_index_beg_6(self):
        index = self.instance2.find_insertion_index_beg(Interval("Chr",10,25))
        self.assertEqual(index, 1)

    def test_find_insertion_index_beg_7(self):
        index = self.instance2.find_insertion_index_beg(Interval("Chr",20,35))
        self.assertEqual(index, 2)

    def test_find_insertion_index_end_1(self):
        index = self.instance1.find_insertion_index_end(Interval("Chr", 50,51))
        self.assertEqual(index, 0)

    def test_find_insertion_index_end_2(self):
        index = self.instance2.find_insertion_index_end(Interval("Chr",5,10))
        self.assertEqual(index, 1)

    def test_find_insertion_index_end_3(self):
        index = self.instance2.find_insertion_index_end(Interval("Chr",15,20))
        self.assertEqual(index, 2)

    def test_find_insertion_index_end_4(self):
        index = self.instance2.find_insertion_index_end(Interval("Chr",40,50))
        self.assertEqual(index, 3)
        
    def test_find_insertion_index_end_5(self):
        index = self.instance2.find_insertion_index_end(Interval("Chr",1,5))
        self.assertEqual(index, 1)

    def test_find_insertion_index_end_6(self):
        index = self.instance2.find_insertion_index_end(Interval("Chr",10,25))
        self.assertEqual(index, 2)

    def test_find_insertion_index_end_7(self):
        index = self.instance2.find_insertion_index_end(Interval("Chr",20,35))
        self.assertEqual(index, 3)
        
    def test_find_intersection_index_beg_1(self):
        index = self.instance2.find_intersection_index_beg(Interval("Chr", 0, 1))
        self.assertEqual(index, -1)

    def test_find_intersection_index_beg_2(self):
        index = self.instance2.find_intersection_index_beg(Interval("Chr", 1, 2))
        self.assertEqual(index, 0)
        
    def test_find_intersection_index_beg_3(self):
        index = self.instance2.find_intersection_index_beg(Interval("Chr", 4, 5))
        self.assertEqual(index, 0)

    def test_find_intersection_index_beg_4(self):
        index = self.instance2.find_intersection_index_beg(Interval("Chr", 5, 6))
        self.assertEqual(index, -1)

    def test_find_intersection_index_beg_5(self):
        index = self.instance2.find_intersection_index_beg(Interval("Chr", 9, 10))
        self.assertEqual(index, -1)

    def test_find_intersection_index_beg_6(self):
        index = self.instance2.find_intersection_index_beg(Interval("Chr", 10, 11))
        self.assertEqual(index, 1)

    def test_find_intersection_index_beg_7(self):
        index = self.instance2.find_intersection_index_beg(Interval("Chr", 19, 20))
        self.assertEqual(index, 1)
        
    def test_find_intersection_index_beg_8(self):
        index = self.instance2.find_intersection_index_beg(Interval("Chr", 20, 21))
        self.assertEqual(index, 1)
        
    def test_find_intersection_index_beg_9(self):
        index = self.instance2.find_intersection_index_beg(Interval("Chr", 24, 25))
        self.assertEqual(index, 1)

    def test_find_intersection_index_beg_10(self):
        index = self.instance2.find_intersection_index_beg(Interval("Chr", 25, 26))
        self.assertEqual(index, 2)

    def test_find_intersection_index_beg_11(self):
        index = self.instance2.find_intersection_index_beg(Interval("Chr", 34, 35))
        self.assertEqual(index, 2)

    def test_find_intersection_index_beg_12(self):
        index = self.instance2.find_intersection_index_beg(Interval("Chr", 35, 36))
        self.assertEqual(index, -1)

    def test_find_intersection_index_beg_13(self):
        ilist = self.constructor([
            self.interval9,  #   0-5000
            self.interval3,  #  10-25
            self.interval7   # 100-110
        ])
        index = ilist.find_intersection_index_beg(self.interval5)  # 20-35
        self.assertEqual(index, 0)

    def test_find_intersection_index_beg_14(self):
        ilist = self.constructor([
            self.interval9,  #   0-5000
            self.interval3,  #  10-25
            self.interval7   # 100-110
        ])
        index = ilist.find_intersection_index_beg(self.interval6)  # 45-95
        self.assertEqual(index, 0)

    def test_find_intersection_index_beg_15(self):
        index = self.instance3.find_intersection_index_beg(Interval("Chr",95,100))
        self.assertEqual(index, 4)
        
    def test_find_intersection_index_end_1(self):
        index = self.instance2.find_intersection_index_end(Interval("Chr", 0, 1))
        self.assertEqual(index, -1)

    def test_find_intersection_index_end_2(self):
        index = self.instance2.find_intersection_index_end(Interval("Chr", 1, 2))
        self.assertEqual(index, 1)
        
    def test_find_intersection_index_end_3(self):
        index = self.instance2.find_intersection_index_end(Interval("Chr", 4, 5))
        self.assertEqual(index, 1)

    def test_find_intersection_index_end_4(self):
        index = self.instance2.find_intersection_index_end(Interval("Chr", 5, 6))
        self.assertEqual(index, -1)

    def test_find_intersection_index_end_5(self):
        index = self.instance2.find_intersection_index_end(Interval("Chr", 9, 10))
        self.assertEqual(index, -1)

    def test_find_intersection_index_end_6(self):
        index = self.instance2.find_intersection_index_end(Interval("Chr", 10, 11))
        self.assertEqual(index, 2)

    def test_find_intersection_index_end_7(self):
        index = self.instance2.find_intersection_index_end(Interval("Chr", 19, 20))
        self.assertEqual(index, 2)
        
    def test_find_intersection_index_end_8(self):
        index = self.instance2.find_intersection_index_end(Interval("Chr", 20, 21))
        self.assertEqual(index, 3)
        
    def test_find_intersection_index_end_9(self):
        index = self.instance2.find_intersection_index_end(Interval("Chr", 24, 25))
        self.assertEqual(index, 3)

    def test_find_intersection_index_end_10(self):
        index = self.instance2.find_intersection_index_end(Interval("Chr", 25, 26))
        self.assertEqual(index, 3)

    def test_find_intersection_index_end_11(self):
        index = self.instance2.find_intersection_index_end(Interval("Chr", 34, 35))
        self.assertEqual(index, 3)

    def test_find_intersection_index_end_12(self):
        index = self.instance2.find_intersection_index_end(Interval("Chr", 35, 36))
        self.assertEqual(index, -1)        
        
    def test_find_intersection_index_nearest_1(self):
        index = self.instance2.find_intersection_index_nearest(Interval("Chr",0,1))
        self.assertEqual(index, -1)

    def test_find_intersection_index_nearest_2(self):
        index = self.instance2.find_intersection_index_nearest(Interval("Chr",1,2))
        self.assertEqual(index, 0)

    def test_find_intersection_index_nearest_3(self):
        index = self.instance2.find_intersection_index_nearest(Interval("Chr",4,5))
        self.assertEqual(index, 0)

    def test_find_intersection_index_nearest_4(self):
        index = self.instance2.find_intersection_index_nearest(Interval("Chr",5,6))
        self.assertEqual(index, -1)

    def test_find_intersection_index_nearest_5(self):
        index = self.instance2.find_intersection_index_nearest(Interval("Chr",6,7))
        self.assertEqual(index, -1)

    def test_find_intersection_index_nearest_6(self):
        # equidinstant features return left-most index
        index = self.instance2.find_intersection_index_nearest(Interval("Chr",7,8))
        self.assertEqual(index, -1)

    def test_find_intersection_index_nearest_7(self):
        index = self.instance2.find_intersection_index_nearest(Interval("Chr",8,9))
        self.assertEqual(index, -1)

    def test_find_intersection_index_nearest_8(self):
        index = self.instance2.find_intersection_index_nearest(Interval("Chr",9,10))
        self.assertEqual(index, -1)

    def test_find_intersection_index_nearest_9(self):
        index = self.instance2.find_intersection_index_nearest(Interval("Chr",10,11))
        self.assertEqual(index, 1)

    def test_find_intersection_index_nearest_10(self):
        index = self.instance2.find_intersection_index_nearest(Interval("Chr",19,20))
        self.assertEqual(index, 1)

    def test_find_intersection_index_nearest_11(self):
        index = self.instance2.find_intersection_index_nearest(Interval("Chr",20,21))
        self.assertEqual(index, 1)
        
    def test_find_intersection_index_nearest_12(self):
        index = self.instance2.find_intersection_index_nearest(Interval("Chr",24,25))
        self.assertEqual(index, 2)
        
    def test_find_intersection_index_nearest_13(self):
        index = self.instance2.find_intersection_index_nearest(Interval("Chr",25,26))
        self.assertEqual(index, 2)

    def test_find_intersection_index_nearest_14(self):
        index = self.instance2.find_intersection_index_nearest(Interval("Chr",50,51))
        self.assertEqual(index, -1)
        
    def test_find_intersection_index_range_1(self):
        indices = list(self.instance2.find_intersection_index_range(Interval("Chr", 0, 1)))
        self.assertEqual(indices, [])

    def test_find_intersection_index_range_2(self):
        indices = list(self.instance2.find_intersection_index_range(Interval("Chr", 0, 2)))
        self.assertEqual(indices, [0])

    def test_find_intersection_index_range_3(self):
        indices = list(self.instance2.find_intersection_index_range(Interval("Chr", 2, 8)))
        self.assertEqual(indices, [0])

    def test_find_intersection_index_range_4(self):
        indices = list(self.instance2.find_intersection_index_range(Interval("Chr", 0, 20)))
        self.assertEqual(indices, [0, 1])

    def test_find_intersection_index_range_5(self):
        indices = list(self.instance2.find_intersection_index_range(Interval("Chr", 0, 22)))
        self.assertEqual(indices, [0, 1, 2])

    def test_find_intersection_index_range_6(self):
        indices = list(self.instance2.find_intersection_index_range(Interval("Chr", 15, 22)))
        self.assertEqual(indices, [1, 2])

    def test_find_intersection_index_range_7(self):
        indices = list(self.instance2.find_intersection_index_range(Interval("Chr", 22, 50)))
        self.assertEqual(indices, [1, 2])

    def test_find_intersection_index_range_8(self):
        indices = list(self.instance2.find_intersection_index_range(Interval("Chr", 25, 50)))
        self.assertEqual(indices, [2])

    def test_find_intersection_index_range_9(self):
        indices = list(self.instance2.find_intersection_index_range(Interval("Chr", 40, 50)))
        self.assertEqual(indices, [])

    def test_find_intersection_index_range_10(self):
        ilist = self.constructor([
            self.interval9,  #   0-5000
            self.interval3,  #  10-25
            self.interval5,  #  20-35
            self.interval6,  #  45-95
        ])
        index = list(ilist.find_intersection_index_range(Interval("Chr",25,40)))
        self.assertEqual(index, [0,2])

    def test_find_intersection_index_range_11(self):
        ilist = self.constructor([
            self.interval9,  #   0-5000
            self.interval3,  #  10-25
            self.interval5,  #  20-35
            self.interval6,  #  45-95
        ])
        index = list(ilist.find_intersection_index_range(self.interval4))  # 25-50
        self.assertEqual(index, [0,2,3])

    def test_find_intersection_index_slice_1(self):
        indices = self.instance2.find_intersection_index_slice(Interval("Chr", 0, 1))
        self.assertEqual(indices, slice(-1, -1))

    def test_find_intersection_index_slice_2(self):
        indices = self.instance2.find_intersection_index_slice(Interval("Chr", 0, 2))
        self.assertEqual(indices, slice(0, 1))

    def test_find_intersection_index_slice_3(self):
        indices = self.instance2.find_intersection_index_slice(Interval("Chr", 2, 8))
        self.assertEqual(indices, slice(0, 1))

    def test_find_intersection_index_slice_4(self):
        indices = self.instance2.find_intersection_index_slice(Interval("Chr", 0, 20))
        self.assertEqual(indices, slice(0, 2))

    def test_find_intersection_index_slice_5(self):
        indices = self.instance2.find_intersection_index_slice(Interval("Chr", 0, 22))
        self.assertEqual(indices, slice(0, 3))

    def test_find_intersection_index_slice_6(self):
        indices = self.instance2.find_intersection_index_slice(Interval("Chr", 15, 22))
        self.assertEqual(indices, slice(1, 3))

    def test_find_intersection_index_slice_7(self):
        indices = self.instance2.find_intersection_index_slice(Interval("Chr", 22, 50))
        self.assertEqual(indices, slice(1, 3))

    def test_find_intersection_index_slice_8(self):
        indices = self.instance2.find_intersection_index_slice(Interval("Chr", 25, 50))
        self.assertEqual(indices, slice(2, 3))

    def test_find_intersection_index_slice_9(self):
        indices = self.instance2.find_intersection_index_slice(Interval("Chr", 40, 50))
        self.assertEqual(indices, slice(-1, -1))
        
    def test_find_intersection_index_slice_10(self):
        ilist = self.constructor([
            self.interval9,  #   0-5000
            self.interval3,  #  10-25
            self.interval5,  #  20-35
            self.interval6,  #  45-95
        ])
        index = ilist.find_intersection_index_slice(Interval("Chr",25,40))
        self.assertEqual(index, slice(0, 3))

    def test_find_intersection_index_slice_11(self):
        ilist = self.constructor([
            self.interval9,  #   0-5000
            self.interval3,  #  10-25
            self.interval5,  #  20-35
            self.interval6,  #  45-95
        ])
        index = ilist.find_intersection_index_slice(self.interval4)  # 25-50
        self.assertEqual(index, slice(0, 4))
        
    def test_intersection_length_1(self):
        length = self.instance2.intersection_length(Interval("Chr", 0, 5))
        self.assertEqual(length, 4)

    def test_intersection_length_2(self):
        length = self.instance2.intersection_length(Interval("Chr", 2, 4))
        self.assertEqual(length, 2)

    def test_intersection_length_3(self):
        length = self.instance2.intersection_length(Interval("Chr", 0, 20))
        self.assertEqual(length, 14)

    def test_intersection_length_4(self):
        length = self.instance2.intersection_length(Interval("Chr", 10, 50))
        self.assertEqual(length, 30)
        
    def test_intersection_fraction_1(self):
        length = self.instance2.intersection_fraction(Interval("Chr", 0, 5))
        self.assertAlmostEqual(length, 4/34.0, 2)
        
    def test_intersection_fraction_2(self):
        length = self.instance2.intersection_fraction(Interval("Chr", 2, 4))
        self.assertAlmostEqual(length, 2/34.0, 2)

    def test_intersection_fraction_3(self):
        length = self.instance2.intersection_fraction(Interval("Chr", 0, 20))
        self.assertAlmostEqual(length, 14/34.0, 2)

    def test_intersection_fraction_4(self):
        length = self.instance2.intersection_fraction(Interval("Chr", 10, 50))
        self.assertAlmostEqual(length, 30/34.0, 2)

    def test_intersection_fraction_5(self):
        length = self.instance2.intersection_fraction(Interval("Chr", 0, 5), query=True)
        self.assertAlmostEqual(length, 4/5.0, 2)
        
    def test_find_intersecting_1(self):
        intersections = list(self.instance2.find_intersecting(Interval("Chr", 0, 1)))
        self.assertEqual(intersections, [])

    def test_find_intersecting_2(self):
        intersections = list(self.instance2.find_intersecting(Interval("Chr", 2, 4)))
        self.assertEqual(intersections, [self.instance2[0]])

    def test_find_intersecting_3(self):
        intersections = list(self.instance2.find_intersecting(Interval("Chr", 2, 15)))
        self.assertEqual(intersections, [self.instance2[0], self.instance2[1]])

    def test_find_intersecting_4(self):
        intersections = list(self.instance2.find_intersecting(Interval("Chr", 15, 22)))
        self.assertEqual(intersections, [self.instance2[1], self.instance2[2]])

    def test_find_intersecting_5(self):
        intersections = list(self.instance2.find_intersecting(Interval("Chr", 25, 50)))
        self.assertEqual(intersections, [self.instance2[2]])

    def test_find_intersecting_6(self):
        intersections = list(self.instance2.find_intersecting(Interval("Chr", 40, 50)))
        self.assertEqual(intersections, [])


# TEST IntervalSet.insort() exhaustively!!!
# TEST IntervalSet.remove() exhaustively!!!
# TEST IntervalSet: test interval set operations after _remove() and _insert()

# TODO: need to perform union() boundary checks
# def test_union_1(self):
#     n = IntervalSet((Interval("Chr",100,150), Interval("Chr",500,800), Interval("Chr",900,1000)))
#     m = IntervalSet((Interval("Chr",0,10), Interval("Chr",180,300), Interval("Chr",850,900)))
#     u = m.union(n)
#     self.assertEqual(len(u), 6)

# def test_union_2(self):
#     # test symmetry:
#     n = IntervalSet((Interval("Chr",100,150), Interval("Chr",500,800), Interval("Chr",900,1000)))
#     m = IntervalSet((Interval("Chr",0,125), Interval("Chr",125,300), Interval("Chr",850,900)))
#     u = n.union(m)
#     v = m.union(n)
#     self.assertEqual(u, v)

# def test_untion_2(self):
#     n = IntervalSet((Interval("Chr",100,150), Interval("Chr",500,800), Interval("Chr",900,1000)))
#     m = IntervalSet((Interval("Chr",0,10), Interval("Chr",125,300), Interval("Chr",850,900)))
#     self.assertEqual(len(m.union(n)), 5)
    
