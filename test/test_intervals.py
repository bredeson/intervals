
from unittest import TestCase
from intervals import (
    BaseInterval,
    Interval,
    IntervalList,
)
from intervals.collections import _Node
from math import isnan, nan, isinf, inf

class TestCase001_BaseInterval(TestCase):
    def setUp(self):
        self.interval  = BaseInterval(50, 100)
        self.interval0 = BaseInterval(50, 100)
        self.interval1 = BaseInterval(25,  75)
        self.interval2 = BaseInterval(70,  75)
        self.interval3 = BaseInterval(50,  75)
        self.interval4 = BaseInterval( 0, 100)
        self.interval5 = BaseInterval( 0,  50)
        self.interval6 = BaseInterval(75, 100)
        self.interval7 = BaseInterval(75, 125)
        self.interval8 = BaseInterval()
        
    def tearDown(self):
        del(self.interval)
        del(self.interval0)
        del(self.interval1)
        del(self.interval2)
        del(self.interval3)
        del(self.interval4)
        del(self.interval5)
        del(self.interval6)
        del(self.interval7)
        del(self.interval8)

    def test_namespace_getter_0(self):
        self.assertTrue(hasattr(self.interval, 'namespace'))

    def test_namespace_getter_1(self):
        self.assertIsNone(self.interval.namespace)

    def test_namespace_setter_0(self):
        self.assertTrue(hasattr(self.interval, 'namespace'))

    def test_namespace_setter_1(self):
        self.assertIsNone(self.interval.namespace)
        self.interval.namespace = 3
        self.assertEqual(self.interval.namespace, 3)
        
    def test_beg_getter_0(self):
        self.assertTrue(hasattr(self.interval, 'beg'))
        self.assertTrue(hasattr(self.interval, 'start'))
        
    def test_beg_getter_1(self):
        self.assertIsNotNone(self.interval.beg)
        self.assertIsInstance(self.interval.beg, int)
        self.assertEqual(self.interval.beg, 50)
        self.assertEqual(self.interval.start, 50)

    def test_beg_setter_0(self):
        self.assertTrue(hasattr(self.interval, 'beg'))
        self.assertTrue(hasattr(self.interval, 'start'))

    def test_beg_setter_1(self):
        self.assertEqual(self.interval.beg, 50)
        self.assertEqual(self.interval.start, 50)
        self.interval.beg = 75
        self.assertEqual(self.interval.beg, 75)
        self.assertEqual(self.interval.start, 75)

    def test_beg_setter_2(self):
        try:
            self.interval.beg = nan
        except ValueError:
            pass
        self.assertTrue(isnan(self.interval.beg))
            
    def test_beg_setter_3(self):
        try:
            self.interval.beg = inf
        except OverflowError:
            pass
        self.assertTrue(isinf(self.interval.beg))

    def test_beg_setter_4(self):
        try:
            self.interval.beg = -inf
        except OverflowError:
            pass
        self.assertTrue(isinf(self.interval.beg))
            
    def test_mid_0(self):
        self.assertTrue(hasattr(self.interval, 'mid'))

    def test_mid_1(self):
        self.assertEqual(self.interval6.mid, 87.5)
        
    def test_end_getter_0(self):
        self.assertTrue(hasattr(self.interval, 'end'))
        self.assertTrue(hasattr(self.interval, 'stop'))

    def test_end_getter_1(self):
        self.assertIsNotNone(self.interval.end)
        self.assertIsInstance(self.interval.end, int)
        self.assertEqual(self.interval.end, 100)
        self.assertEqual(self.interval.stop, 100)

    def test_end_setter_0(self):
        self.assertTrue(hasattr(self.interval, 'end'))
        self.assertTrue(hasattr(self.interval, 'stop'))

    def test_end_setter_1(self):
        self.assertEqual(self.interval.end, 100)
        self.assertEqual(self.interval.stop, 100)
        self.interval.end = 175
        self.assertEqual(self.interval.end, 175)
        self.assertEqual(self.interval.stop, 175)

    def test_end_setter_2(self):
        try:
            self.interval.end = nan
        except ValueError:
            pass
        self.assertTrue(isnan(self.interval.end))

    def test_end_setter_3(self):
        try:
            self.interval.end = inf
        except OverflowError:
            pass
        self.assertTrue(isinf(self.interval.end))
        
    def test_end_setter_4(self):
        try:
            self.interval.end = -inf
        except OverflowError:
            pass
        self.assertTrue(isinf(self.interval.end))
        
    def test_isnull_0(self):
        self.assertTrue(hasattr(self.interval, 'isnull'))

    def test_isnull_1(self):
        i = self.interval.__class__()
        self.assertIsNone(i.namespace)
        self.assertTrue(isnan(i.beg))
        self.assertTrue(isnan(i.end))
        self.assertTrue(i.isnull())

    def test_isnull_2(self):
        i = self.interval.__class__()
        i.end = 19
        self.assertIsNone(i.namespace)
        self.assertTrue(isnan(i.beg))
        self.assertFalse(isnan(i.end))
        self.assertTrue(i.isnull())

    def test_isnull_3(self):
        i = self.interval.__class__()
        i.beg = 19
        self.assertIsNone(i.namespace)
        self.assertFalse(isnan(i.beg))
        self.assertTrue(isnan(i.end))
        self.assertTrue(i.isnull())        

    def test_isempty_0(self):
        self.assertTrue(hasattr(self.interval, 'isempty'))

    def test_isempty_1(self):
        self.assertFalse(self.interval.isempty())
        self.interval.beg, self.interval.end \
            = self.interval.end, self.interval.beg
        self.assertTrue(self.interval.isempty())

    def test_isempty_2(self):
        self.interval.beg = nan
        self.assertTrue(isnan(self.interval.beg))
        self.assertFalse(isnan(self.interval.end))
        self.assertTrue(self.interval.isempty())

    def test_isempty_3(self):
        self.interval.end = nan
        self.assertFalse(isnan(self.interval.beg))
        self.assertTrue(isnan(self.interval.end))
        self.assertTrue(self.interval.isempty())
        
    def test_copy_0(self):
        self.assertTrue(hasattr(self.interval, 'copy'))

    def test_copy_1(self):
        i = self.interval0.copy()
        self.assertIsInstance(i, self.interval.__class__)
        self.assertEqual(i, self.interval0)
        self.assertNotEqual(hash(i), hash(self.interval0))

    def test_copy_2(self):
        i = self.interval0.copy(deep=True)
        self.assertIsInstance(i, self.interval.__class__)
        self.assertEqual(i, self.interval0)
        self.assertNotEqual(hash(i), hash(self.interval0))
        
    def test_to_slice_0(self):
        self.assertTrue(hasattr(self.interval, 'to_slice'))

    def test_to_slice_1(self):
        s = self.interval.to_slice()
        self.assertIsInstance(s, slice)
        self.assertEqual(s.start, self.interval.beg)
        self.assertEqual(s.stop, self.interval.end)

    def test_to_slice_2(self):  ###
        s = self.interval8.to_slice()
        self.assertIsInstance(s, slice)
        self.assertEqual(s.start, 0)
        self.assertEqual(s.stop, 0)
        
    def test_abs_0(self):
        self.assertTrue(hasattr(self.interval, '__abs__'))

    def test_abs_1(self):
        i = self.interval.__class__( -15, -5)
        self.assertEqual(i.beg, -15)
        self.assertEqual(i.end, -5)
        i = abs(i)
        self.assertIsInstance(i, self.interval.__class__)
        self.assertEqual(i.beg, 15)
        self.assertEqual(i.end, 5)

    def test_abs_2(self):  ###
        i = abs(self.interval8)
        self.assertIsInstance(i, self.interval.__class__)
        self.assertIs(i.namespace, self.interval8.namespace)
        self.assertTrue(isnan(i.beg))
        self.assertTrue(isnan(i.end))
        
    def test_add_0(self):
        self.assertTrue(hasattr(self.interval, '__add__'))

    def test_add_1(self):
        i = self.interval + 25
        self.assertIsInstance(i, self.interval.__class__)
        self.assertEqual(i, self.interval7)

    def test_add_2(self):
        i = self.interval0 + self.interval1
        self.assertIsInstance(i, self.interval.__class__)
        self.assertEqual(i.beg,  75)
        self.assertEqual(i.end, 175)

    def test_add_3(self):  ###
        i = self.interval8 + 100
        self.assertIsInstance(i, self.interval.__class__)
        self.assertTrue(i.isempty())
        
    def test_and_0(self):
        self.assertTrue(hasattr(self.interval, '__and__'))

    def test_and_1(self):
        i = self.interval0 & self.interval1
        self.assertIsInstance(i, self.interval.__class__)
        self.assertEqual(i, self.interval3)

    def test_and_2(self):
        i = self.interval0 & self.interval2
        self.assertIsInstance(i, self.interval.__class__)
        self.assertEqual(i, self.interval2)

    def test_and_3(self):
        i = self.interval0 & self.interval5
        self.assertIsInstance(i, self.interval.__class__)
        self.assertTrue(i.isnull())

    def test_and_4(self):  ###
        i = self.interval8 & self.interval0
        self.assertIsInstance(i, self.interval.__class__)
        self.assertTrue(i.isnull())

    def test_and_5(self):  ###
        i = self.interval0 & self.interval8
        self.assertIsInstance(i, self.interval.__class__)
        self.assertTrue(i.isnull())
        
    def test_bool_0(self):
        self.assertTrue(hasattr(self.interval, '__bool__'))

    def test_bool_1(self):
        self.assertTrue(bool(self.interval))

    def test_bool_2(self):  ###
        self.assertFalse(bool(self.interval8))
        
    def test_ceil_0(self):
        self.assertTrue(hasattr(self.interval, '__ceil__'))

    def test_ceil_1(self):
        import math
        i = self.interval.__class__( 3.50, 7.75)
        self.assertEqual(i.beg, 3.50)
        self.assertEqual(i.end, 7.75)
        i = math.ceil(i)
        self.assertIsInstance(i, self.interval.__class__)
        self.assertEqual(i.beg, 4.0)
        self.assertEqual(i.end, 8.0)

    def test_ceil_2(self):  ###
        import math
        i = math.ceil(self.interval8)
        self.assertIsInstance(i, self.interval.__class__)
        self.assertTrue(i.isempty())
        
    def test_in_0(self):
        self.assertTrue(hasattr(self.interval, '__contains__'))

    def test_in_1(self):
        self.assertIn(self.interval2, self.interval1)

    def test_in_2(self):  ###
        self.assertNotIn(self.interval0, self.interval8)
        
    def test_eq_0(self):
        self.assertTrue(hasattr(self.interval, '__eq__'))

    def test_eq_1(self):
        self.assertEqual(self.interval1, self.interval1)

    def test_eq_2(self):
        self.assertEqual(self.interval0, self.interval)
        self.assertNotEqual(hash(self.interval0), hash(self.interval))

    def test_eq_3(self):
        i = self.interval1.copy()
        i.beg, i.end = i.end, i.beg
        self.assertNotEqual(i, self.interval1)

    def test_eq_4(self):  ###
        # None == None -> True
        # nan == nan -> False
        # True and False -> False always
        i = self.interval.__class__()
        self.assertNotEqual(self.interval8, i)
        self.assertTrue(self.interval8.isempty())
        self.assertTrue(i.isempty())
        
    def test_floor_0(self):
        self.assertTrue(hasattr(self.interval, '__floor__'))

    def test_floor_1(self):
        import math
        i = self.interval.__class__( 3.50, 7.75)
        self.assertEqual(i.beg, 3.50)
        self.assertEqual(i.end, 7.75)
        i = math.floor(i)
        self.assertIsInstance(i, self.interval.__class__)
        self.assertEqual(i.beg, 3.0)
        self.assertEqual(i.end, 7.0)

    def test_floor_2(self):  ###
        import math
        i = math.floor(self.interval8)
        self.assertIsInstance(i, self.interval.__class__)
        self.assertNotEqual(i, self.interval8)
        self.assertTrue(self.interval8.isempty())
        self.assertTrue(i.isempty())
        
    def test_floordiv_0(self):
        self.assertTrue(hasattr(self.interval, '__floordiv__'))

    def test_floordiv_1(self):
        import math
        i = self.interval.__class__( 3.50, 7.75)
        self.assertEqual(i.beg, 3.50)
        self.assertEqual(i.end, 7.75)
        j = i // 1
        self.assertIsInstance(j, self.interval.__class__)
        self.assertEqual(j.beg, 3.0)
        self.assertEqual(j.end, 7.0)

    def test_ge_0(self):
        self.assertTrue(hasattr(self.interval, '__ge__'))

    def test_ge_1(self):        
        self.assertGreaterEqual(self.interval0, self.interval1)

    def test_ge_2(self):
        self.assertGreaterEqual(self.interval0, self.interval3)

    def test_ge_3(self):
        self.assertGreaterEqual(self.interval3, self.interval3)    

    def test_gt_0(self):
        self.assertTrue(hasattr(self.interval, '__gt__'))

    def test_gt_1(self):
        self.assertGreater(self.interval0, self.interval1)

    def test_gt_2(self):
        self.assertGreater(self.interval0, self.interval3)

    def test_hash_0(self):
        self.assertTrue(hasattr(self.interval, '__hash__'))

    def test_hash_1(self):
        self.assertEqual(hash(self.interval0), hash(self.interval0))
        self.assertIs(self.interval0, self.interval0)

    def test_hash_2(self):
        self.assertNotEqual(hash(self.interval0), hash(self.interval))
        self.assertIsNot(self.interval0, self.interval)

    def test_iadd_0(self):
        self.assertTrue(hasattr(self.interval, '__iadd__'))

    def test_iadd_1(self):
        self.assertEqual(self.interval0.beg,  50)
        self.assertEqual(self.interval0.end, 100)
        self.interval0 += 10
        self.assertEqual(self.interval0.beg,  60)
        self.assertEqual(self.interval0.end, 110)

    def test_iadd_2(self):
        self.assertEqual(self.interval0.beg,  50)
        self.assertEqual(self.interval0.end, 100)
        self.interval0 += self.interval1
        self.assertIsInstance(self.interval0, self.interval.__class__)
        self.assertEqual(self.interval0.beg,  75)
        self.assertEqual(self.interval0.end, 175)
        
    def test_imul_0(self):
        self.assertTrue(hasattr(self.interval, '__imul__'))

    def test_imul_1(self):
        self.assertEqual(self.interval0.beg,  50)
        self.assertEqual(self.interval0.end, 100)
        self.interval0 *= 5
        self.assertIsInstance(self.interval0, self.interval.__class__)
        self.assertEqual(self.interval0.beg, 250)
        self.assertEqual(self.interval0.end, 500)

    def test_imul_2(self):
        self.assertEqual(self.interval0.beg,  50)
        self.assertEqual(self.interval0.end, 100)
        self.interval0 *= self.interval3
        self.assertIsInstance(self.interval0, self.interval.__class__)
        self.assertEqual(self.interval0.beg, 2500)
        self.assertEqual(self.interval0.end, 7500)
        
    def test_isub_0(self):
        self.assertTrue(hasattr(self.interval, '__isub__'))

    def test_isub_1(self):
        self.assertEqual(self.interval0.beg,  50)
        self.assertEqual(self.interval0.end, 100)
        self.interval0 -= 50
        self.assertIsInstance(self.interval0, self.interval.__class__)
        self.assertEqual(self.interval0.beg,  0)
        self.assertEqual(self.interval0.end, 50)

    def test_isub_2(self):
        self.assertEqual(self.interval0.beg,  50)
        self.assertEqual(self.interval0.end, 100)
        self.interval0 -= self.interval3
        self.assertIsInstance(self.interval0, self.interval.__class__)
        self.assertEqual(self.interval0.beg,  0)
        self.assertEqual(self.interval0.end, 25)
        
    def test_le_0(self):
        self.assertTrue(hasattr(self.interval, '__le__'))

    def test_le_1(self):
        self.assertLessEqual(self.interval1, self.interval0)

    def test_le_2(self):
        self.assertLessEqual(self.interval3, self.interval0)

    def test_le_3(self):
        self.assertLessEqual(self.interval0, self.interval)

    def test_len_0(self):
        self.assertTrue(hasattr(self.interval, '__len__'))

    def test_len_1(self):
        self.assertEqual(len(self.interval0), 50)
        self.assertEqual(len(self.interval1), 50)
        self.assertEqual(len(self.interval2),  5)
        self.assertEqual(len(self.interval3), 25)

    def test_lt_0(self):
        self.assertTrue(hasattr(self.interval, '__lt__'))

    def test_lt_1(self):
        self.assertLess(self.interval1, self.interval0)

    def test_lt_2(self):
        self.assertLess(self.interval3, self.interval0)

    def test_lshift_0(self):
        self.assertTrue(hasattr(self.interval, '__lshift__'))

    def test_lshift_1(self):
        j = self.interval0.__class__( 2, 4)
        i = j << 1
        self.assertIsInstance(i, self.interval.__class__)
        self.assertEqual(i.beg, 4)
        self.assertEqual(i.end, 8)

    def test_lshift_2(self):
        j = self.interval0.__class__( 2, 4)
        i = j << self.interval0.__class__( 1, 2)
        self.assertIsInstance(i, self.interval.__class__)
        self.assertEqual(i.beg,  4)
        self.assertEqual(i.end, 16)
        
    def test_mul_0(self):
        self.assertTrue(hasattr(self.interval, '__mul__'))

    def test_mul_1(self):
        self.assertEqual(self.interval0.beg,  50)
        self.assertEqual(self.interval0.end, 100)
        i = self.interval0 * 5
        self.assertIsInstance(i, self.interval.__class__)
        self.assertEqual(i.beg, 250)
        self.assertEqual(i.end, 500)

    def test_mul_2(self):
        self.assertEqual(self.interval0.beg,  50)
        self.assertEqual(self.interval0.end, 100)
        i = self.interval0 * self.interval0.__class__( 2, 5)
        self.assertIsInstance(i, self.interval.__class__)
        self.assertEqual(i.beg, 100)
        self.assertEqual(i.end, 500)
        
    def test_ne_0(self):
        self.assertTrue(hasattr(self.interval, '__ne__'))

    def test_ne_1(self):
        self.assertNotEqual(self.interval0, self.interval1)

    def test_ne_2(self):
        self.assertNotEqual(self.interval0, self.interval3)

    def test_ne_3(self):
        self.assertNotEqual(self.interval0, self.interval0.__class__(0, 100))
        
    def test_or_0(self):
        self.assertTrue(hasattr(self.interval, '__or__'))

    def test_or_1(self):
        # i0:  50 *================o 100
        # i2:       70 *===o 75        
        i = self.interval0 | self.interval2
        self.assertIsInstance(i, self.interval.__class__)
        self.assertEqual(i, self.interval0)

    def test_or_2(self):
        # i0:  50 *================o 100
        # i3:  50 *============o 75        
        i = self.interval0 | self.interval3
        self.assertIsInstance(i, self.interval.__class__)
        self.assertEqual(i, self.interval0)

    def test_or_3(self):
        # i0:  50 *================o 100
        # i6:          75 *========o 100
        i = self.interval0 | self.interval6
        self.assertIsInstance(i, self.interval.__class__)
        self.assertEqual(i, self.interval0)
        
    def test_or_4(self):
        # i0:           50 *================o 100
        # i1:  25 *================o 75
        i = self.interval0 | self.interval1
        self.assertIsInstance(i, self.interval.__class__)
        self.assertEqual(i.beg,  25)
        self.assertEqual(i.end, 100)

    def test_or_5(self):
        # i0:  50 *================o 100
        # i7:           75 *================o 125
        i = self.interval0 | self.interval7
        self.assertIsInstance(i, self.interval.__class__)
        self.assertEqual(i.beg,  50)
        self.assertEqual(i.end, 125)

    def test_or_6(self):
        # i3:           50 *======o 75
        # i5: 0 *==========o 50
        i = self.interval3 | self.interval5
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.interval.__class__)
        self.assertIsInstance(i[1], self.interval.__class__)
        self.assertEqual(i[0], self.interval3)
        self.assertEqual(i[1], self.interval5)

    def test_or_7(self):
        # i3:  50 *======o 75
        # i6:         75 *======o 100
        i = self.interval3 | self.interval6
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.interval.__class__)
        self.assertIsInstance(i[1], self.interval.__class__)
        self.assertEqual(i[0], self.interval3)
        self.assertEqual(i[1], self.interval6)
        
    def test_or_8(self):
        # i2:                     70 *====o 75
        # i5:  0 *===============o 50
        i = self.interval2 | self.interval5
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.interval.__class__)
        self.assertIsInstance(i[1], self.interval.__class__)
        self.assertEqual(i[0], self.interval2)
        self.assertEqual(i[1], self.interval5)

    def test_or_9(self):
        # i5:  0 *===============o 50
        # i2:                     70 *====o 75
        i = self.interval5 | self.interval2
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.interval.__class__)
        self.assertIsInstance(i[1], self.interval.__class__)
        self.assertEqual(i[0], self.interval5)
        self.assertEqual(i[1], self.interval2)
        
    def test_radd_0(self):
        self.assertTrue(hasattr(self.interval, '__radd__'))

    def test_radd_1(self):
        self.assertEqual(self.interval0.beg,  50)
        self.assertEqual(self.interval0.end, 100)
        i = 5 + self.interval0
        self.assertIsInstance(i, self.interval.__class__)
        self.assertEqual(i.beg,  55)
        self.assertEqual(i.end, 105)

    def test_rfloordiv_0(self):
        self.assertTrue(hasattr(self.interval, '__rfloordiv__'))

    def test_rfloordiv_1(self):
        i = 1000000 // self.interval0
        self.assertIsInstance(i, self.interval.__class__)
        self.assertEqual(i.beg, 20000)
        self.assertEqual(i.end, 10000)
        
    def test_rlshift_0(self):
        self.assertTrue(hasattr(self.interval, '__rlshift__'))

    def test_rlshift_1(self):
        i = 1 << self.interval0.__class__(2,4)
        self.assertIsInstance(i, self.interval.__class__)
        self.assertEqual(i.beg,  4)
        self.assertEqual(i.end, 16)
        
    def test_rmul_0(self):
        self.assertTrue(hasattr(self.interval, '__rmul__'))

    def test_rmul_1(self):
        i = 5 * self.interval0
        self.assertIsInstance(i, self.interval.__class__)
        self.assertEqual(i.beg, 250)
        self.assertEqual(i.end, 500)

    def test_rshift_0(self):
        self.assertTrue(hasattr(self.interval, '__rshift__'))

    def test_rshift_1(self):
        i = self.interval0.__class__( 2, 16) >> 1
        self.assertIsInstance(i, self.interval.__class__)
        self.assertEqual(i.beg, 1)
        self.assertEqual(i.end, 8)

    def test_rsub_0(self):
        self.assertTrue(hasattr(self.interval, '__rsub__'))

    def test_rsub_1(self):
        i = 10000 - self.interval0.__class__( 1000, 10000)
        self.assertIsInstance(i, self.interval.__class__)
        self.assertEqual(i.beg, 9000)
        self.assertEqual(i.end, 0)

    def test_rtruediv_0(self):
        self.assertTrue(hasattr(self.interval, '__rtruediv__'))

    def test_rtruediv_1(self):
        i = 5.0 / self.interval0.__class__( 2.0, 5.0)
        self.assertIsInstance(i, self.interval.__class__)
        self.assertEqual(i.beg, 2.5)
        self.assertEqual(i.end, 1)

    def test_sub_0(self):
        self.assertTrue(hasattr(self.interval, '__sub__'))

    def test_sub_1(self):
        i = self.interval0 - 50
        self.assertIsInstance(i, self.interval0.__class__)
        self.assertEqual(i.beg,  0)
        self.assertEqual(i.end, 50)

    def test_sub_2(self):
        i = self.interval0 - self.interval3
        self.assertIsInstance(i, self.interval0.__class__)
        self.assertEqual(i.beg,  0)
        self.assertEqual(i.end, 25)
        
    def test_truediv_0(self):
        self.assertTrue(hasattr(self.interval, '__truediv__'))

    def test_truediv_1(self):
        i = self.interval1 / 100.0
        self.assertIsInstance(i, self.interval1.__class__)
        self.assertEqual(i.beg, 0.25)
        self.assertEqual(i.end, 0.75)

    def test_truediv_2(self):
        i = self.interval1 / self.interval.__class__(100.0, 100.0)
        self.assertIsInstance(i, self.interval1.__class__)
        self.assertEqual(i.beg, 0.25)
        self.assertEqual(i.end, 0.75)
        
    def test_xor_0(self):
        self.assertTrue(hasattr(self.interval, '__xor__'))

    def test_xor_1(self):
        # i5:  0 *========o 50
        # i1:      25 *========o 75
        i = self.interval5 ^ self.interval1
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.interval.__class__)
        self.assertIsInstance(i[1], self.interval.__class__)
        self.assertEqual(i[0], self.interval.__class__(  0, 25))
        self.assertEqual(i[1], self.interval.__class__( 50, 75))

    def test_xor_2(self):
        # i1:      25 *========o 75
        # i5:  0 *========o 50
        i = self.interval1 ^ self.interval5
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.interval.__class__)
        self.assertIsInstance(i[1], self.interval.__class__)
        self.assertEqual(i[0], self.interval.__class__( 50, 75))
        self.assertEqual(i[1], self.interval.__class__(  0, 25))
        
    def test_xor_3(self):
        # i0:  50 *================o 100
        # i2:       70 *========o 75        
        i = self.interval0 ^ self.interval2
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.interval.__class__)
        self.assertIsInstance(i[1], self.interval.__class__)
        self.assertEqual(i[0], self.interval.__class__( 50,  70))
        self.assertEqual(i[1], self.interval.__class__( 75, 100))

    def test_xor_4(self):
        # i0:  50 *================o 100
        # i0:  50 *================o 100
        i = self.interval0 ^ self.interval0
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)        
        self.assertIsInstance(i[0], self.interval.__class__)
        self.assertIsInstance(i[1], self.interval.__class__)
        self.assertTrue(i[0].isempty())
        self.assertTrue(i[1].isempty())

    def test_xor_5(self):
        # i5:  0 *========o 50
        # i3:          50 *====o 75        
        i = self.interval5 ^ self.interval3
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.interval.__class__)
        self.assertIsInstance(i[1], self.interval.__class__)
        self.assertEqual(i[0], self.interval5)
        self.assertEqual(i[1], self.interval3)

    def test_xor_6(self):  
        # i3:          50 *====o 75
        # i5:  0 *========o 50        
        i = self.interval3 ^ self.interval5
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.interval.__class__)
        self.assertIsInstance(i[1], self.interval.__class__)
        self.assertEqual(i[0], self.interval3)
        self.assertEqual(i[1], self.interval5)
        
    def test_xor_7(self):
        # i0:  50 *========o 100
        # i3:  50 *====o 75
        i = self.interval0 ^ self.interval3
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.interval.__class__)
        self.assertIsInstance(i[1], self.interval.__class__)
        self.assertEqual(i[0], self.interval6)
        self.assertTrue(i[1].isempty())

    def test_xor_8(self):
        # i1:  25 *==========o 75
        # i3:       50 *=====o 75
        i = self.interval1 ^ self.interval3
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.interval.__class__)
        self.assertIsInstance(i[1], self.interval.__class__)
        self.assertEqual(i[0].beg, 25)
        self.assertEqual(i[0].end, 50)
        self.assertTrue(i[1].isempty())

    def test_isabutting_beg_0(self):
        self.assertTrue(hasattr(self.interval, 'isabutting_beg'))

    def test_isabutting_beg_1(self):
        self.assertTrue(self.interval5.isabutting_beg(self.interval3))

    def test_isabutting_beg_2(self):
        self.assertFalse(self.interval5.isabutting_beg(self.interval2))

    def test_isabutting_beg_3(self):
        self.assertFalse(self.interval3.isabutting_beg(self.interval5))
        
    def test_isabutting_end_0(self):
        self.assertTrue(hasattr(self.interval, 'isabutting_end'))

    def test_isabutting_end_1(self):
        self.assertTrue(self.interval3.isabutting_end(self.interval5))

    def test_isabutting_end_2(self):
        self.assertFalse(self.interval2.isabutting_end(self.interval5))

    def test_isabutting_end_3(self):
        self.assertFalse(self.interval5.isabutting_end(self.interval3))
        
    def test_issuperinterval_0(self):
        self.assertTrue(hasattr(self.interval, 'issuperinterval'))

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

    def test_issubinterval_8(self):
        self.assertTrue(self.interval.issuperinterval(self.interval0, proper=False))
        self.assertFalse(self.interval.issuperinterval(self.interval0, proper=True))
        
    def test_difference_0(self):
        self.assertTrue(hasattr(self.interval, 'difference'))

    def test_difference_1(self):
        i = self.interval0.difference(self.interval6)
        self.assertIsInstance(i, self.interval.__class__)
        self.assertEqual(i, self.interval3)
        
    def test_difference_2(self):
        i = self.interval0.difference(self.interval3)
        self.assertIsInstance(i, self.interval.__class__)
        self.assertEqual(i, self.interval6)
        
    def test_difference_3(self):
        i = self.interval2.difference(self.interval0)
        self.assertIsInstance(i, self.interval.__class__)
        self.assertTrue(i.isnull())

    def test_difference_4(self):
        i = self.interval0.difference(self.interval2)
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.interval.__class__)
        self.assertIsInstance(i[1], self.interval.__class__)
        self.assertEqual(i[0].beg,  50)
        self.assertEqual(i[0].end,  70)
        self.assertEqual(i[1].beg,  75)
        self.assertEqual(i[1].end, 100)

    def test_difference_5(self):
        i = self.interval5.difference(self.interval2)
        self.assertEqual(i, self.interval5)
        
    def test_difference_update_0(self):
        self.assertTrue(hasattr(self.interval, 'difference_update'))

    def test_difference_update_1(self):
        with self.assertRaises(NotImplementedError):
            self.interval0.difference_update(self.interval0)

    def test_inner_distance_0(self):
        self.assertTrue(hasattr(self.interval, 'inner_distance'))

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
        
    def test_intersection_0(self):
        self.assertTrue(hasattr(self.interval, 'intersection'))

    def test_intersection_1(self):
        i = self.interval0.intersection(self.interval2)
        self.assertIsInstance(i, self.interval.__class__)
        self.assertEqual(i, self.interval2)

    def test_intersection_2(self):
        i = self.interval0.intersection(self.interval3)
        self.assertIsInstance(i, self.interval.__class__)
        self.assertEqual(i, self.interval3)

    def test_intersection_3(self):
        i = self.interval0.intersection(self.interval6)
        self.assertIsInstance(i, self.interval.__class__)
        self.assertEqual(i, self.interval6)

    def test_intersection_4(self):
        i = self.interval0.intersection(self.interval1)
        self.assertIsInstance(i, self.interval.__class__)
        self.assertEqual(i.beg, 50)
        self.assertEqual(i.end, 75)

    def test_intersection_5(self):
        i = self.interval0.intersection(self.interval7)
        self.assertIsInstance(i, self.interval.__class__)
        self.assertEqual(i.beg,  75)
        self.assertEqual(i.end, 100)
        
    def test_intersection_6(self):
        i = self.interval0.intersection(self.interval5)
        self.assertIsInstance(i, self.interval.__class__)
        self.assertTrue(i.isnull())        

    def test_intersection_7(self):
        i = self.interval1.intersection(self.interval7)
        self.assertIsInstance(i, self.interval.__class__)
        self.assertTrue(i.isnull())

    def test_intersection_update_0(self):
        self.assertTrue(hasattr(self.interval, 'intersection_update'))

    def test_intersection_update_1(self):
        with self.assertRaises(NotImplementedError):
            self.interval0.intersection_update(self.interval0)

    def test_isdisjoint_0(self):
        self.assertTrue(hasattr(self.interval, 'isdisjoint'))

    def test_isdisjoint_1(self):
        self.assertTrue(self.interval5.isdisjoint(self.interval2))

    def test_isdisjoint_2(self):
        self.assertTrue(self.interval5.isdisjoint(self.interval3))

    def test_isdisjoint_3(self):
        self.assertTrue(self.interval3.isdisjoint(self.interval5))

    def test_isdisjoint_4(self):
        self.assertTrue(self.interval2.isdisjoint(self.interval5))

    def test_isdisjoint_5(self):
        self.assertFalse(self.interval3.isdisjoint(self.interval2))

    def test_isdisjoint_6(self):
        self.assertFalse(self.interval0.isdisjoint(self.interval3))
        
    def test_issubset_0(self):
        self.assertTrue(hasattr(self.interval, 'issubset'))
        # just an alias of issubinterval()

    def test_issuperset_0(self):
        self.assertTrue(hasattr(self.interval, 'issuperset'))
        # just an alias of issuperinterval()

    def test_outer_distance_0(self):
        self.assertTrue(hasattr(self.interval, 'outer_distance'))

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
        
    def test_overlap_fraction_0(self):
        self.assertTrue(hasattr(self.interval, 'overlap_fraction'))

    def test_overlap_fraction_1(self):
        self.assertEqual(
            self.interval0.overlap_fraction(self.interval2), 0.10
        )

    def test_overlap_fraction_2(self):
        self.assertEqual(
            self.interval2.overlap_fraction(self.interval0), 1.0
        )

    def test_overlap_fraction_3(self):
        self.assertEqual(
            self.interval0.overlap_fraction(self.interval3), 0.5
        )
        
    def test_overlap_fraction_4(self):
        self.assertEqual(
            self.interval0.overlap_fraction(self.interval6), 0.5
        )
        
    def test_overlap_fraction_5(self):
        self.assertEqual(
            self.interval0.overlap_fraction(self.interval5), 0.0
        )

    def test_overlap_fraction_6(self):
        self.assertEqual(
            self.interval5.overlap_fraction(self.interval3), 0.0
        )

    def test_overlap_length_0(self):
        self.assertTrue(hasattr(self.interval, 'overlap_length'))

    def test_overlap_length_1(self):
        self.assertEqual(
            self.interval0.overlap_length(self.interval2), 5
        )

    def test_overlap_length_2(self):
        self.assertEqual(
            self.interval2.overlap_length(self.interval0), 5
        )

    def test_overlap_length_3(self):
        self.assertEqual(
            self.interval0.overlap_length(self.interval3), 25
        )
        
    def test_overlap_length_4(self):
        self.assertEqual(
            self.interval0.overlap_length(self.interval6), 25
        )
        
    def test_overlap_length_5(self):
        self.assertEqual(
            self.interval0.overlap_length(self.interval5), 0
        )

    def test_overlap_length_6(self):
        self.assertEqual(
            self.interval5.overlap_length(self.interval3), 0
        )
        
    def test_isoverlapping_0(self):
        self.assertTrue(hasattr(self.interval, 'isoverlapping'))

    def test_isoverlapping_1(self):
        self.assertTrue(self.interval0.isoverlapping(self.interval2))

    def test_isoverlapping_2(self):
        self.assertTrue(self.interval0.isoverlapping(self.interval3))

    def test_isoverlapping_3(self):
        self.assertTrue(self.interval0.isoverlapping(self.interval6))

    def test_isoverlapping_4(self):
        self.assertTrue(self.interval0.isoverlapping(self.interval1))

    def test_isoverlapping_5(self):
        self.assertTrue(self.interval0.isoverlapping(self.interval7))

    def test_isoverlapping_6(self):
        self.assertFalse(self.interval0.isoverlapping(self.interval5))

    def test_isoverlapping_7(self):
        self.assertFalse(self.interval3.isoverlapping(self.interval7))

    def test_isoverlapping_8(self):
        self.assertFalse(self.interval5.isoverlapping(self.interval2))

    def test_isoverlapping_beg_0(self):
        self.assertTrue(hasattr(self.interval, 'isoverlapping_beg'))

    def test_isoverlapping_beg_1(self):
        self.assertTrue(self.interval1.isoverlapping_beg(self.interval0))

    def test_isoverlapping_beg_2(self):
        self.assertTrue(self.interval3.isoverlapping_beg(self.interval0))

    def test_isoverlapping_beg_3(self):
        self.assertFalse(self.interval2.isoverlapping_beg(self.interval0))

    def test_isoverlapping_beg_4(self):
        self.assertFalse(self.interval5.isoverlapping_beg(self.interval0))
        
    def test_isoverlapping_end_0(self):
        self.assertTrue(hasattr(self.interval, 'isoverlapping_end'))

    def test_isoverlapping_end_1(self):
        self.assertTrue(self.interval1.isoverlapping_end(self.interval5))

    def test_isoverlapping_end_2(self):
        self.assertTrue(self.interval7.isoverlapping_end(self.interval0))

    def test_isoverlapping_end_3(self):
        self.assertFalse(self.interval2.isoverlapping_end(self.interval0))    

    def test_isoverlapping_end_4(self):
        self.assertFalse(self.interval7.isoverlapping_end(self.interval1))
        
    def test_symmetric_difference_0(self):
        self.assertTrue(hasattr(self.interval, 'symmetric_difference'))

    def test_symmetric_difference_1(self):
        # i5:  0 *========o 50
        # i1:      25 *========o 75
        i = self.interval5.symmetric_difference(self.interval1)
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.interval.__class__)
        self.assertIsInstance(i[1], self.interval.__class__)
        self.assertEqual(i[0], self.interval.__class__(  0, 25))
        self.assertEqual(i[1], self.interval.__class__( 50, 75))

    def test_symmetric_difference_2(self):
        # i1:      25 *========o 75
        # i5:  0 *========o 50
        i = self.interval1.symmetric_difference(self.interval5)
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.interval.__class__)
        self.assertIsInstance(i[1], self.interval.__class__)
        self.assertEqual(i[0], self.interval.__class__( 50, 75))
        self.assertEqual(i[1], self.interval.__class__(  0, 25))
        
    def test_symmetric_difference_3(self):
        # i0:  50 *================o 100
        # i2:       70 *========o 75
        i = self.interval0.symmetric_difference(self.interval2)
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.interval.__class__)
        self.assertIsInstance(i[1], self.interval.__class__)
        self.assertEqual(i[0], self.interval.__class__( 50,  70))
        self.assertEqual(i[1], self.interval.__class__( 75, 100))

    def test_symmetric_difference_4(self):
        # i0:  50 *================o 100
        # i0:  50 *================o 100
        i = self.interval0.symmetric_difference(self.interval0)
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)        
        self.assertIsInstance(i[0], self.interval.__class__)
        self.assertIsInstance(i[1], self.interval.__class__)
        self.assertTrue(i[0].isempty())
        self.assertTrue(i[1].isempty())

    def test_symmetric_difference_5(self):
        # i5:  0 *========o 50
        # i3:          50 *====o 75
        i = self.interval5.symmetric_difference(self.interval3)
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.interval.__class__)
        self.assertIsInstance(i[1], self.interval.__class__)
        self.assertEqual(i[0], self.interval5)
        self.assertEqual(i[1], self.interval3)

    def test_symmetric_difference_6(self):  
        # i3:          50 *====o 75
        # i5:  0 *========o 50        
        i = self.interval3.symmetric_difference(self.interval5)
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.interval.__class__)
        self.assertIsInstance(i[1], self.interval.__class__)
        self.assertEqual(i[0], self.interval3)
        self.assertEqual(i[1], self.interval5)
        
    def test_symmetric_difference_7(self):
        # i0:  50 *========o 100
        # i3:  50 *====o 75
        i = self.interval0.symmetric_difference(self.interval3)
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.interval.__class__)
        self.assertIsInstance(i[1], self.interval.__class__)
        self.assertEqual(i[0], self.interval6)
        self.assertTrue(i[1].isempty())

    def test_symmetric_difference_8(self):
        # i1:  25 *==========o 75
        # i3:       50 *=====o 75
        i = self.interval1.symmetric_difference(self.interval3)
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.interval.__class__)
        self.assertIsInstance(i[1], self.interval.__class__)
        self.assertEqual(i[0].beg, 25)
        self.assertEqual(i[0].end, 50)
        self.assertTrue(i[1].isempty())
        
    def test_symmetric_difference_update_0(self):
        self.assertTrue(hasattr(self.interval, 'symmetric_difference_update'))

    def test_symmetric_difference_update_1(self):
        with self.assertRaises(NotImplementedError):
            self.interval0.symmetric_difference_update(self.interval0)

    def test_to_slice_0(self):
        self.assertTrue(hasattr(self.interval, 'to_slice'))

    def test_to_slice_1(self):
        s = self.interval.to_slice()
        self.assertIsInstance(s, slice)
        self.assertEqual(s.start, self.interval.beg)
        self.assertEqual(s.stop, self.interval.end)

    def test_to_string_0(self):
        self.assertTrue(hasattr(self.interval, 'to_string'))

    def test_to_string_1(self):
        s = self.interval0.to_string()
        self.assertIsInstance(s, str)
        self.assertEqual(s, "[50, 100, namespace=None]")

    def test_to_string_2(self):
        s = BaseInterval(3.5, 10.5).to_string()
        self.assertIsInstance(s, str)
        self.assertEqual(s, "[3.5, 10.5, namespace=None]")

    def test_str_0(self):
        self.assertTrue(hasattr(self.interval, '__str__'))

    def test_str_1(self):
        s = str(self.interval0)
        self.assertIsInstance(s, str)
        self.assertEqual(s, "[50, 100, namespace=None]")

    def test_str_2(self):
        s = str(BaseInterval(3.5, 10.5))
        self.assertIsInstance(s, str)
        self.assertEqual(s, "[3.5, 10.5, namespace=None]")
        
    def test_union_0(self):
        self.assertTrue(hasattr(self.interval, 'union'))

    def test_union_1(self):
        # i0:  50 *================o 100
        # i2:       70 *===o 75
        i = self.interval0.union(self.interval2)
        self.assertIsInstance(i, self.interval.__class__)
        self.assertEqual(i, self.interval0)

    def test_union_2(self):
        # i0:  50 *================o 100
        # i3:  50 *============o 75
        i = self.interval0.union(self.interval3)
        self.assertIsInstance(i, self.interval.__class__)
        self.assertEqual(i, self.interval0)

    def test_union_3(self):
        # i0:  50 *================o 100
        # i6:          75 *========o 100
        i = self.interval0.union(self.interval6)
        self.assertIsInstance(i, self.interval.__class__)
        self.assertEqual(i, self.interval0)
        
    def test_union_4(self):
        # i0:           50 *================o 100
        # i1:  25 *================o 75
        i = self.interval0.union(self.interval1)
        self.assertIsInstance(i, self.interval.__class__)
        self.assertEqual(i.beg,  25)
        self.assertEqual(i.end, 100)

    def test_union_5(self):
        # i0:  50 *================o 100
        # i7:           75 *================o 125
        i = self.interval0.union(self.interval7)
        self.assertIsInstance(i, self.interval.__class__)
        self.assertEqual(i.beg,  50)
        self.assertEqual(i.end, 125)

    def test_union_6(self):
        # i3:           50 *======o 75
        # i5: 0 *==========o 50
        i = self.interval3.union(self.interval5)
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.interval.__class__)
        self.assertIsInstance(i[1], self.interval.__class__)
        self.assertEqual(i[0], self.interval3)
        self.assertEqual(i[1], self.interval5)

    def test_union_7(self):
        # i3:  50 *======o 75
        # i6:         75 *======o 100
        i = self.interval3.union(self.interval6)
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.interval.__class__)
        self.assertIsInstance(i[1], self.interval.__class__)
        self.assertEqual(i[0], self.interval3)
        self.assertEqual(i[1], self.interval6)
        
    def test_union_8(self):
        # i2:                     70 *====o 75
        # i5:  0 *===============o 50
        i = self.interval2.union(self.interval5)
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.interval.__class__)
        self.assertIsInstance(i[1], self.interval.__class__)
        self.assertEqual(i[0], self.interval2)
        self.assertEqual(i[1], self.interval5)

    def test_union_9(self):
        # i5:  0 *===============o 50
        # i2:                     70 *====o 75
        i = self.interval5.union(self.interval2)
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.interval.__class__)
        self.assertIsInstance(i[1], self.interval.__class__)
        self.assertEqual(i[0], self.interval5)
        self.assertEqual(i[1], self.interval2)
        
    def test_issubinterval_0(self):
        self.assertTrue(hasattr(self.interval, 'issubinterval'))

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
        self.assertTrue(self.interval.issubinterval(self.interval0, proper=False))
        self.assertFalse(self.interval.issubinterval(self.interval0, proper=True))
        
        
class TestCase002_Interval(TestCase001_BaseInterval):
    def setUp(self):
        self.interval  = Interval("Chr1", 50, 100)
        self.interval0 = Interval("Chr1", 50, 100)
        self.interval1 = Interval("Chr1", 25,  75)
        self.interval2 = Interval("Chr1", 70,  75)
        self.interval3 = Interval("Chr1", 50,  75)
        self.interval4 = Interval("Chr2", 50, 100)
        self.interval5 = Interval("Chr1",  0,  50)
        self.interval6 = Interval("Chr1", 75, 100)
        self.interval7 = Interval("Chr1", 75, 125)
        self.interval8 = Interval()

    def tearDown(self):
        del(self.interval)
        del(self.interval0)
        del(self.interval1)
        del(self.interval2)
        del(self.interval3)
        del(self.interval4)
        del(self.interval5)
        del(self.interval6)
        del(self.interval7)
        del(self.interval8)

    def test_namespace_getter_0(self):
        self.assertTrue(hasattr(self.interval, 'namespace'))

    def test_namespace_getter_1(self):
        self.assertEqual(self.interval.namespace, "Chr1")

    def test_namespace_setter_0(self):
        self.assertTrue(hasattr(self.interval, 'namespace'))

    def test_namespace_setter_1(self):
        self.assertEqual(self.interval.namespace, "Chr1")
        self.interval.namespace = 3
        self.assertEqual(self.interval.namespace, 3)

    def test_mid_1(self):
        self.assertEqual(self.interval6.mid, 87)
        
    def test_to_string_1(self):
        s = self.interval0.to_string()
        self.assertIsInstance(s, str)
        self.assertEqual(s, 'Chr1:50-100')

    def test_to_string_2(self):
        s = Interval(2, 50, 100).to_string()
        self.assertIsInstance(s, str)
        self.assertEqual(s, '2:50-100')

    def test_str_1(self):
        s = str(self.interval0)
        self.assertIsInstance(s, str)
        self.assertEqual(s, 'Chr1:50-100')

    def test_str_2(self):
        s = str(Interval(2, 50, 100))
        self.assertIsInstance(s, str)
        self.assertEqual(s, '2:50-100')

    def test_isempty_4(self):
        self.assertFalse(self.interval.isempty())
        self.interval.end = self.interval.beg
        self.assertTrue(self.interval.isempty())
        
    def test_abs_1(self):
        i = self.interval.__class__("Chr1", -15, -5)
        self.assertEqual(i.namespace, "Chr1")
        self.assertEqual(i.beg, -15)
        self.assertEqual(i.end, -5)
        i = abs(i)
        self.assertIsInstance(i, self.interval.__class__)
        self.assertEqual(i.namespace, "Chr1")
        self.assertEqual(i.beg, 15)
        self.assertEqual(i.end, 5)
        
    def test_add_3(self):
        with self.assertRaises(ValueError):
            i = self.interval0 + self.interval4

    def test_add_4(self):
        i = self.interval0 + Interval("Chr1", 25, 25)
        self.assertIsInstance(i, self.interval0.__class__)
        self.assertEqual(i, self.interval7)

    def test_bool_2(self):
        self.interval.beg = nan
        self.interval.end = nan
        self.assertFalse(bool(self.interval))

    def test_eq_4(self):
        i = self.interval.__class__("Chr1", 50, 100)
        self.assertNotEqual(i, self.interval4)

    def test_ceil_1(self):
        pass

    def test_floor_1(self):
        pass

    def test_floordiv_1(self):
        import math
        i = self.interval.__class__("Chr1", 1000, 2000)
        self.assertEqual(i.beg, 1000)
        self.assertEqual(i.end, 2000)
        j = i // 10
        self.assertIsInstance(j, self.interval.__class__)
        self.assertEqual(j.beg, 100)
        self.assertEqual(j.end, 200)
        
    def test_rtruediv_1(self):
        i = 5.0 / self.interval.__class__("Chr1", 2.0, 5.0)
        self.assertIsInstance(i, self.interval.__class__)
        self.assertEqual(i.beg, "Chr1")
        self.assertEqual(i.beg, 2)
        self.assertEqual(i.end, 1)

    def test_truediv_1(self):
        i = self.interval0 / 50
        self.assertIsInstance(i, self.interval.__class__)
        self.assertEqual(i.namespace, "Chr1")
        self.assertEqual(i.beg, 1)
        self.assertEqual(i.end, 2)

    def test_truediv_2(self):
        i = self.interval0 / self.interval.__class__("Chr1", 50, 50)
        self.assertIsInstance(i, self.interval.__class__)
        self.assertEqual(i.beg, 1)
        self.assertEqual(i.end, 2)
        
    def test_iadd_3(self):
        with self.assertRaises(ValueError):
            self.interval0 += self.interval4

    def test_iadd_4(self):
        self.interval0 += Interval("Chr1", 25, 25)
        self.assertIsInstance(self.interval0, self.interval1.__class__)
        self.assertEqual(self.interval0, self.interval7)

    def test_imul_3(self):
        with self.assertRaises(ValueError):
            self.interval0 *= self.interval4

    def test_imul_4(self):
        self.assertEqual(self.interval0.beg,  50)
        self.assertEqual(self.interval0.end, 100)
        self.interval0 *= Interval("Chr1", 50, 75)
        self.assertIsInstance(self.interval0, self.interval.__class__)
        self.assertEqual(self.interval0.beg, 2500)
        self.assertEqual(self.interval0.end, 7500)

    def test_isub_3(self):
        with self.assertRaises(ValueError):
            self.interval0 -= self.interval4

    def test_isub_4(self):
        self.assertEqual(self.interval0.beg,  50)
        self.assertEqual(self.interval0.end, 100)
        self.interval0 -= Interval("Chr1", 50, 75)
        self.assertIsInstance(self.interval0, self.interval.__class__)
        self.assertEqual(self.interval0.beg,  0)
        self.assertEqual(self.interval0.end, 25)

    def test_lshift_1(self):
        j = self.interval0.__class__("Chr1", 2, 4)
        i = j << 1
        self.assertIsInstance(i, self.interval.__class__)
        self.assertEqual(i.namespace, "Chr1")
        self.assertEqual(i.beg, 4)
        self.assertEqual(i.end, 8)

    def test_lshift_2(self):
        j = self.interval0.__class__("Chr1", 2, 4)
        i = j << self.interval0.__class__("Chr1", 1, 2)
        self.assertIsInstance(i, self.interval.__class__)
        self.assertEqual(i.namespace, "Chr1")
        self.assertEqual(i.beg,  4)
        self.assertEqual(i.end, 16)

    def test_lshift_3(self):
        with self.assertRaises(ValueError):
            i = self.interval0 << self.interval4
    
    def test_lshift_4(self):
        j = self.interval0.__class__("Chr1", 2, 4)
        i = j << Interval("Chr1", 1, 2)
        self.assertIsInstance(i, self.interval.__class__)
        self.assertEqual(i.namespace, "Chr1")
        self.assertEqual(i.beg,  4)
        self.assertEqual(i.end, 16)

    def test_mul_2(self):
        self.assertEqual(self.interval0.beg,  50)
        self.assertEqual(self.interval0.end, 100)
        i = self.interval0 * self.interval0.__class__("Chr1", 2, 5)
        self.assertIsInstance(i, self.interval.__class__)
        self.assertEqual(i.namespace, "Chr1")
        self.assertEqual(i.beg, 100)
        self.assertEqual(i.end, 500)
        
    def test_mul_3(self):
        with self.assertRaises(ValueError):
            i = self.interval0 * self.interval4

    def test_mul_4(self):
        self.assertEqual(self.interval0.beg,  50)
        self.assertEqual(self.interval0.end, 100)
        i = self.interval0 * Interval("Chr1", 2, 5)
        self.assertIsInstance(i, self.interval.__class__)
        self.assertEqual(i.namespace, "Chr1")
        self.assertEqual(i.beg, 100)
        self.assertEqual(i.end, 500)

    def test_rlshift_1(self):
        i = 1 << self.interval0.__class__("Chr1", 2, 4)
        self.assertIsInstance(i, self.interval.__class__)
        self.assertEqual(i.beg,  4)
        self.assertEqual(i.end, 16)

    def test_rshift_1(self):
        i = self.interval0.__class__("Chr1", 2, 16) >> 1
        self.assertIsInstance(i, self.interval.__class__)
        self.assertEqual(i.namespace, "Chr1")
        self.assertEqual(i.beg, 1)
        self.assertEqual(i.end, 8)

    def test_rsub_1(self):
        i = 10000 - self.interval0.__class__("Chr1", 1000, 10000)
        self.assertIsInstance(i, self.interval.__class__)
        self.assertEqual(i.namespace, "Chr1")
        self.assertEqual(i.beg, 9000)
        self.assertEqual(i.end, 0)

    def test_rtruediv_1(self):
        i = 10000 / self.interval0.__class__("Chr1", 10, 20)
        self.assertIsInstance(i, self.interval.__class__)
        self.assertEqual(i.beg, 1000)
        self.assertEqual(i.end,  500)
        
    def test_sub_3(self):
        with self.assertRaises(ValueError):
            i = self.interval0 - self.interval4

    def test_sub_4(self):
        i = self.interval0 - Interval("Chr1", 50, 75)
        self.assertIsInstance(i, self.interval.__class__)
        self.assertEqual(i.beg,  0)
        self.assertEqual(i.end, 25)

    def test_truediv_3(self):
        with self.assertRaises(ValueError):
            i = self.interval0 / self.interval4

    def test_truediv_4(self):
        i = self.interval0 / Interval("Chr1", 50, 50)
        self.assertIsInstance(i, self.interval.__class__)
        self.assertEqual(i.beg, 1)
        self.assertEqual(i.end, 2)

    def test_xor_1(self):
        # i5:  0 *========o 50
        # i1:      25 *========o 75        
        i = self.interval5 ^ self.interval1
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.interval.__class__)
        self.assertIsInstance(i[1], self.interval.__class__)
        self.assertEqual(i[0], self.interval.__class__("Chr1",  0, 25))
        self.assertEqual(i[1], self.interval.__class__("Chr1", 50, 75))

    def test_xor_2(self):
        # i1:      25 *========o 75
        # i5:  0 *========o 50        
        i = self.interval1 ^ self.interval5
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.interval.__class__)
        self.assertIsInstance(i[1], self.interval.__class__)
        self.assertEqual(i[0], self.interval.__class__("Chr1", 50, 75))
        self.assertEqual(i[1], self.interval.__class__("Chr1",  0, 25))
        
    def test_xor_3(self):
        # i0:  50 *================o 100
        # i2:       70 *========o 75
        i = self.interval0 ^ self.interval2
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.interval.__class__)
        self.assertIsInstance(i[1], self.interval.__class__)
        self.assertEqual(i[0], self.interval.__class__("Chr1", 50,  70))
        self.assertEqual(i[1], self.interval.__class__("Chr1", 75, 100))

    def test_xor_9(self):
        # i0:  50 *================o 100 Chr1
        # i4:    (different namespace)   Chr2
        i = self.interval0 ^ self.interval4
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.interval.__class__)
        self.assertIsInstance(i[1], self.interval.__class__)
        self.assertEqual(i[0], self.interval0)
        self.assertEqual(i[1], self.interval4)

    def test_difference_6(self):
        i = self.interval0.difference(self.interval4)
        self.assertIsInstance(i, self.interval.__class__)
        self.assertEqual(i, self.interval0)

    def test_inner_distance_5(self):
        self.assertEqual(self.interval0.inner_distance(self.interval4), inf)

    def test_inner_distance_6(self):
        self.assertEqual(self.interval4.inner_distance(self.interval0), inf)

    def test_intersection_8(self):
        i = self.interval1.intersection(self.interval4)
        self.assertIsInstance(i, self.interval.__class__)
        self.assertTrue(i.isnull())

    def test_isdisjoint_7(self):
        self.assertTrue(self.interval0.isdisjoint(self.interval4))

    def test_outer_distance_9(self):
        self.assertEqual(
            self.interval0.outer_distance(self.interval4, True), inf
        )

    def test_outer_distance_10(self):
        self.assertEqual(
            self.interval4.outer_distance(self.interval0, True), inf
        )

    def test_overlap_fraction_7(self):
        self.assertEqual(
            self.interval0.overlap_fraction(self.interval4), 0.0
        )

    def test_overlap_length_7(self):
        self.assertEqual(
            self.interval0.overlap_length(self.interval4), 0
        )

    def test_isoverlapping_9(self):
        self.assertFalse(self.interval0.isoverlapping(self.interval4))

    def test_isoverlapping_beg_5(self):
        self.assertFalse(self.interval1.isoverlapping_beg(self.interval4))

    def test_isoverlapping_end_5(self):
        self.assertFalse(self.interval7.isoverlapping_end(self.interval4))

    def test_symmetric_difference_1(self):
        # i5:  0 *========o 50
        # i1:      25 *========o 75
        i = self.interval5.symmetric_difference(self.interval1)
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.interval.__class__)
        self.assertIsInstance(i[1], self.interval.__class__)
        self.assertEqual(i[0], self.interval.__class__("Chr1",  0, 25))
        self.assertEqual(i[1], self.interval.__class__("Chr1", 50, 75))

    def test_symmetric_difference_2(self):
        # i1:      25 *========o 75
        # i5:  0 *========o 50        
        i = self.interval1.symmetric_difference(self.interval5)
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.interval.__class__)
        self.assertIsInstance(i[1], self.interval.__class__)
        self.assertEqual(i[0], self.interval.__class__("Chr1", 50, 75))
        self.assertEqual(i[1], self.interval.__class__("Chr1",  0, 25))
        
    def test_symmetric_difference_3(self):
        # i0:  50 *================o 100
        # i2:       70 *========o 75        
        i = self.interval0.symmetric_difference(self.interval2)
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.interval.__class__)
        self.assertIsInstance(i[1], self.interval.__class__)
        self.assertEqual(i[0], self.interval.__class__("Chr1", 50,  70))
        self.assertEqual(i[1], self.interval.__class__("Chr1", 75, 100))

    def test_symmetric_difference_9(self):
        # i0:  50 *================o 100 Chr1
        # i4:    (different namespace)   Chr2
        i = self.interval0.symmetric_difference(self.interval4)
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.interval.__class__)
        self.assertIsInstance(i[1], self.interval.__class__)
        self.assertEqual(i[0], self.interval0)
        self.assertEqual(i[1], self.interval4)

    def test_union_10(self):
        # i0:  50 *================o 100 Chr1
        # i4:    (different namespace)   Chr2
        i = self.interval0 | self.interval4
        self.assertIsInstance(i, tuple)
        self.assertEqual(len(i), 2)
        self.assertIsInstance(i[0], self.interval.__class__)
        self.assertIsInstance(i[1], self.interval.__class__)
        self.assertEqual(i[0], self.interval0)
        self.assertEqual(i[1], self.interval4)

    def test_issubinterval_8(self):
        self.assertFalse(self.interval2.issubinterval(self.interval4))


class TestCase003__Node(TestCase):
    def test_init_0(self):
        with self.assertRaisesRegex(
                TypeError,
                "missing \d+ required positional argument"):
            _Node()

    def test_init_1(self):
        node = _Node(
            Interval("Chr", 2, 5)
        )
        self.assertIsInstance(node, _Node)

    def test_init_2(self):
        node = _Node(
            Interval("Chr", 2, 5),
            Interval("Chr", 2, 5)
        )
        self.assertIsInstance(node, _Node)

    def test_init_3(self):
        node = _Node(
            Interval("Chr", 2, 5),
            Interval("Chr", 5, 8)
        )
        self.assertIsInstance(node, _Node)

        
class TestCase004__Node(TestCase):
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
        
        
                                  
class TestCase005_IntervalList(TestCase):
    def setUp(self):
        self.interval0 = Interval("Chr", 2, 5)

    def tearDown(self):
        del(self.interval0)
        
    def test_init_0(self):
        ilist = IntervalList()
        self.assertIsInstance(ilist, IntervalList)
        self.assertEqual(len(ilist), 0)
        
    def test_init_1(self):
        ilist = IntervalList([self.interval0])
        self.assertIsInstance(ilist, IntervalList)
        self.assertEqual(len(ilist), 1)
        

class TestCase006_IntervalList(TestCase):
    def setUp(self):
        self.interval0 = Interval("Chr", 0, 4)
        self.interval1 = Interval("Chr", 1, 5)
        self.interval2 = Interval("Chr", 1, 5)
        self.interval8 = Interval("Chr", 5, 15)
        self.interval3 = Interval("Chr", 10, 25)
        self.interval4 = Interval("Chr", 25, 50)
        self.interval5 = Interval("Chr", 20, 35)
        self.interval6 = Interval("Chr", 45, 95)
        self.interval7 = Interval("Chr", 100, 110)
        self.intervalList = IntervalList([
            self.interval1,  # Chr:1-5
            self.interval3,  # Chr:10-25
            self.interval5   # Chr:20-35
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
        del(self.intervalList)

    def test_append(self):
        num_items = len(self.intervalList)
        self.intervalList.append(self.interval0)
        self.assertEqual(len(self.intervalList), num_items+1)
        self.assertIs(self.intervalList[-1], self.interval0)

    def test_appendleft(self):
        num_items = len(self.intervalList)
        self.intervalList.appendleft(self.interval6)
        self.assertEqual(len(self.intervalList), num_items+1)
        self.assertIs(self.intervalList[0], self.interval6)
        
    def test_extend(self):
        num_items = len(self.intervalList)
        self.intervalList.extend([self.interval0])
        self.assertEqual(len(self.intervalList), num_items+1)
        self.assertIs(self.intervalList[-1], self.interval0)

    def test_extendleft(self):
        num_items = len(self.intervalList)
        self.intervalList.extendleft([self.interval6])
        self.assertEqual(len(self.intervalList), num_items+1)
        self.assertIs(self.intervalList[0], self.interval6)
        
    def test_insert(self):
        num_items = len(self.intervalList)
        self.intervalList.insert(2, self.interval4)
        self.assertEqual(len(self.intervalList), num_items+1)
        self.assertEqual(
            list(self.intervalList),
            [self.interval1, self.interval3, self.interval4, self.interval5]
        )

    def test_update(self):
        num_items = len(self.intervalList)
        answer = [
            self.interval1,
            self.interval2,
            self.interval3,
            self.interval5,
            self.interval6,
            self.interval7
        ]
        self.intervalList.update([self.interval6, self.interval2, self.interval7])
        self.assertEqual(len(self.intervalList), num_items+3)
        self.assertEqual(list(self.intervalList), answer)
        self.assertIs(self.intervalList[0], self.interval1)
        self.assertIs(self.intervalList[1], self.interval2)

    def test_updateleft(self):
        num_items = len(self.intervalList)
        answer = [
            self.interval0,
            self.interval2,
            self.interval1,
            self.interval3,
            self.interval5,
            self.interval7
        ]
        self.intervalList.updateleft([self.interval0, self.interval2, self.interval7])
        self.assertEqual(len(self.intervalList), num_items+3)
        self.assertEqual(list(self.intervalList), answer)
        self.assertIs(self.intervalList[1], self.interval2)
        self.assertIs(self.intervalList[2], self.interval1)
        
    def test_popleft(self):
        num_items = len(self.intervalList)
        item1 = self.intervalList[0]
        item2 = self.intervalList.popleft()
        self.assertEqual(len(self.intervalList), num_items-1)
        self.assertIs(item1, item2)

    def test_pop(self):
        num_items = len(self.intervalList)
        item1 = self.intervalList[-1]
        item2 = self.intervalList.pop()
        self.assertEqual(len(self.intervalList), num_items-1)
        self.assertIs(item1, item2)
        
    def test_rotate_0(self):
        self.intervalList = IntervalList([
            self.interval3, self.interval4, self.interval5
        ])
        num_items = len(self.intervalList)
        item1 = self.intervalList[0]
        item2 = self.intervalList[1]
        item3 = self.intervalList[-1]
        self.intervalList.rotate(-1)  # pull leftward
        self.assertEqual(len(self.intervalList), num_items)
        self.assertIs(self.intervalList[0], item2)
        self.assertIs(self.intervalList[-2], item3)
        self.assertIs(self.intervalList[-1], item1)
        
    def test_rotate_1(self):
        self.intervalList = IntervalList([
            self.interval3, self.interval4, self.interval5
        ])
        num_items = len(self.intervalList)
        item1 = self.intervalList[0]
        item2 = self.intervalList[-2]
        item3 = self.intervalList[-1]
        self.intervalList.rotate(+1)  # pull rightward
        self.assertEqual(len(self.intervalList), num_items)
        self.assertIs(self.intervalList[0], item3)
        self.assertIs(self.intervalList[1], item1)
        self.assertIs(self.intervalList[-1], item2)        

    def test_find_index_beg_0(self):
        self.assertTrue(hasattr(self.intervalList, 'find_index_beg'))

    def test_find_index_beg_1(self):
        index = self.intervalList.find_index_beg(Interval("Chr", 0, 1))
        self.assertEqual(index, 0)

    def test_find_index_beg_2(self):
        index = self.intervalList.find_index_beg(Interval("Chr", 1, 2))
        self.assertEqual(index, 0)
        
    def test_find_index_beg_3(self):
        index = self.intervalList.find_index_beg(Interval("Chr", 4, 5))
        self.assertEqual(index, 0)

    def test_find_index_beg_4(self):
        index = self.intervalList.find_index_beg(Interval("Chr", 5, 6))
        self.assertEqual(index, 1)

    def test_find_index_beg_5(self):
        index = self.intervalList.find_index_beg(Interval("Chr", 9, 10))
        self.assertEqual(index, 1)

    def test_find_index_beg_6(self):
        index = self.intervalList.find_index_beg(Interval("Chr", 10, 11))
        self.assertEqual(index, 1)

    def test_find_index_beg_7(self):
        index = self.intervalList.find_index_beg(Interval("Chr", 19, 20))
        self.assertEqual(index, 1)
        
    def test_find_index_beg_8(self):
        index = self.intervalList.find_index_beg(Interval("Chr", 20, 21))
        self.assertEqual(index, 1)

    def test_find_index_beg_9(self):
        index = self.intervalList.find_index_beg(Interval("Chr", 24, 25))
        self.assertEqual(index, 1)

    def test_find_index_beg_10(self):
        index = self.intervalList.find_index_beg(Interval("Chr", 25, 26))
        self.assertEqual(index, 2)

    def test_find_index_beg_11(self):
        index = self.intervalList.find_index_beg(Interval("Chr", 34, 35))
        self.assertEqual(index, 2)

    def test_find_index_beg_12(self):
        index = self.intervalList.find_index_beg(Interval("Chr", 35, 36))
        self.assertEqual(index, 3)
        
    def test_find_index_end_0(self):
        self.assertTrue(hasattr(self.intervalList, 'find_index_end'))

    def test_find_index_end_1(self):
        index = self.intervalList.find_index_end(Interval("Chr", 0, 1))
        self.assertEqual(index, 0)

    def test_find_index_end_2(self):
        index = self.intervalList.find_index_end(Interval("Chr", 1, 2))
        self.assertEqual(index, 1)
        
    def test_find_index_end_3(self):
        index = self.intervalList.find_index_end(Interval("Chr", 4, 5))
        self.assertEqual(index, 1)

    def test_find_index_end_4(self):
        index = self.intervalList.find_index_end(Interval("Chr", 5, 6))
        self.assertEqual(index, 1)

    def test_find_index_end_5(self):
        index = self.intervalList.find_index_end(Interval("Chr", 9, 10))
        self.assertEqual(index, 1)

    def test_find_index_end_6(self):
        index = self.intervalList.find_index_end(Interval("Chr", 10, 11))
        self.assertEqual(index, 2)

    def test_find_index_end_7(self):
        index = self.intervalList.find_index_end(Interval("Chr", 19, 20))
        self.assertEqual(index, 2)
        
    def test_find_index_end_8(self):
        index = self.intervalList.find_index_end(Interval("Chr", 20, 21))
        self.assertEqual(index, 3)
        
    def test_find_index_end_9(self):
        index = self.intervalList.find_index_end(Interval("Chr", 24, 25))
        self.assertEqual(index, 3)

    def test_find_index_end_10(self):
        index = self.intervalList.find_index_end(Interval("Chr", 25, 26))
        self.assertEqual(index, 3)

    def test_find_index_end_11(self):
        index = self.intervalList.find_index_end(Interval("Chr", 34, 35))
        self.assertEqual(index, 3)

    def test_find_index_end_12(self):
        index = self.intervalList.find_index_end(Interval("Chr", 35, 36))
        self.assertEqual(index, 3)        
        
    def test_find_index_nearest_0(self):
        self.assertTrue(hasattr(self.intervalList, 'find_index_nearest'))

    def test_find_index_nearest_1(self):
        index = self.intervalList.find_index_nearest(Interval("Chr",0,1))
        self.assertEqual(index, 0)

    def test_find_index_nearest_2(self):
        index = self.intervalList.find_index_nearest(Interval("Chr",1,2))
        self.assertEqual(index, 0)

    def test_find_index_nearest_3(self):
        index = self.intervalList.find_index_nearest(Interval("Chr",4,5))
        self.assertEqual(index, 0)

    def test_find_index_nearest_4(self):
        index = self.intervalList.find_index_nearest(Interval("Chr",5,6))
        self.assertEqual(index, 0)

    def test_find_index_nearest_5(self):
        index = self.intervalList.find_index_nearest(Interval("Chr",6,7))
        self.assertEqual(index, 0)

    def test_find_index_nearest_6(self):
        # equidinstant features return left-most index
        index = self.intervalList.find_index_nearest(Interval("Chr",7,8))
        self.assertEqual(index, 0)

    def test_find_index_nearest_7(self):
        index = self.intervalList.find_index_nearest(Interval("Chr",8,9))
        self.assertEqual(index, 1)

    def test_find_index_nearest_8(self):
        index = self.intervalList.find_index_nearest(Interval("Chr",9,10))
        self.assertEqual(index, 1)

    def test_find_index_nearest_9(self):
        index = self.intervalList.find_index_nearest(Interval("Chr",10,11))
        self.assertEqual(index, 1)
        
    def test_find_index_nearest_10(self):
        index = self.intervalList.find_index_nearest(Interval("Chr",24,25))
        self.assertEqual(index, 2)

    def test_find_index_nearest_11(self):
        index = self.intervalList.find_index_nearest(Interval("Chr",25,26))
        self.assertEqual(index, 2)

    def test_find_index_nearest_12(self):
        index = self.intervalList.find_index_nearest(Interval("Chr",50,51))
        self.assertEqual(index, 2)

    def test_find_overlap_index_beg_0(self):
        self.assertTrue(hasattr(self.intervalList, 'find_overlap_index_beg'))

    def test_find_overlap_index_beg_1(self):
        index = self.intervalList.find_overlap_index_beg(Interval("Chr", 0, 1))
        self.assertEqual(index, -1)

    def test_find_overlap_index_beg_2(self):
        index = self.intervalList.find_overlap_index_beg(Interval("Chr", 1, 2))
        self.assertEqual(index, 0)
        
    def test_find_overlap_index_beg_3(self):
        index = self.intervalList.find_overlap_index_beg(Interval("Chr", 4, 5))
        self.assertEqual(index, 0)

    def test_find_overlap_index_beg_4(self):
        index = self.intervalList.find_overlap_index_beg(Interval("Chr", 5, 6))
        self.assertEqual(index, -1)

    def test_find_overlap_index_beg_5(self):
        index = self.intervalList.find_overlap_index_beg(Interval("Chr", 9, 10))
        self.assertEqual(index, -1)

    def test_find_overlap_index_beg_6(self):
        index = self.intervalList.find_overlap_index_beg(Interval("Chr", 10, 11))
        self.assertEqual(index, 1)

    def test_find_overlap_index_beg_7(self):
        index = self.intervalList.find_overlap_index_beg(Interval("Chr", 19, 20))
        self.assertEqual(index, 1)
        
    def test_find_overlap_index_beg_8(self):
        index = self.intervalList.find_overlap_index_beg(Interval("Chr", 20, 21))
        self.assertEqual(index, 1)
        
    def test_find_overlap_index_beg_9(self):
        index = self.intervalList.find_overlap_index_beg(Interval("Chr", 24, 25))
        self.assertEqual(index, 1)

    def test_find_overlap_index_beg_10(self):
        index = self.intervalList.find_overlap_index_beg(Interval("Chr", 25, 26))
        self.assertEqual(index, 2)

    def test_find_overlap_index_beg_11(self):
        index = self.intervalList.find_overlap_index_beg(Interval("Chr", 34, 35))
        self.assertEqual(index, 2)

    def test_find_overlap_index_beg_12(self):
        index = self.intervalList.find_overlap_index_beg(Interval("Chr", 35, 36))
        self.assertEqual(index, -1)
        
    def test_find_overlap_index_end_0(self):
        self.assertTrue(hasattr(self.intervalList, 'find_overlap_index_end'))

    def test_find_overlap_index_end_1(self):
        index = self.intervalList.find_overlap_index_end(Interval("Chr", 0, 1))
        self.assertEqual(index, -1)

    def test_find_overlap_index_end_2(self):
        index = self.intervalList.find_overlap_index_end(Interval("Chr", 1, 2))
        self.assertEqual(index, 1)
        
    def test_find_overlap_index_end_3(self):
        index = self.intervalList.find_overlap_index_end(Interval("Chr", 4, 5))
        self.assertEqual(index, 1)

    def test_find_overlap_index_end_4(self):
        index = self.intervalList.find_overlap_index_end(Interval("Chr", 5, 6))
        self.assertEqual(index, -1)

    def test_find_overlap_index_end_5(self):
        index = self.intervalList.find_overlap_index_end(Interval("Chr", 9, 10))
        self.assertEqual(index, -1)

    def test_find_overlap_index_end_6(self):
        index = self.intervalList.find_overlap_index_end(Interval("Chr", 10, 11))
        self.assertEqual(index, 2)

    def test_find_overlap_index_end_7(self):
        index = self.intervalList.find_overlap_index_end(Interval("Chr", 19, 20))
        self.assertEqual(index, 2)
        
    def test_find_overlap_index_end_8(self):
        index = self.intervalList.find_overlap_index_end(Interval("Chr", 20, 21))
        self.assertEqual(index, 3)
        
    def test_find_overlap_index_end_9(self):
        index = self.intervalList.find_overlap_index_end(Interval("Chr", 24, 25))
        self.assertEqual(index, 3)

    def test_find_overlap_index_end_10(self):
        index = self.intervalList.find_overlap_index_end(Interval("Chr", 25, 26))
        self.assertEqual(index, 3)

    def test_find_overlap_index_end_11(self):
        index = self.intervalList.find_overlap_index_end(Interval("Chr", 34, 35))
        self.assertEqual(index, 3)

    def test_find_overlap_index_end_12(self):
        index = self.intervalList.find_overlap_index_end(Interval("Chr", 35, 36))
        self.assertEqual(index, -1)        
        
    def test_find_overlap_index_nearest_0(self):
        self.assertTrue(hasattr(self.intervalList, 'find_overlap_index_nearest'))

    def test_find_overlap_index_nearest_1(self):
        index = self.intervalList.find_overlap_index_nearest(Interval("Chr",0,1))
        self.assertEqual(index, -1)

    def test_find_overlap_index_nearest_2(self):
        index = self.intervalList.find_overlap_index_nearest(Interval("Chr",1,2))
        self.assertEqual(index, 0)

    def test_find_overlap_index_nearest_3(self):
        index = self.intervalList.find_overlap_index_nearest(Interval("Chr",4,5))
        self.assertEqual(index, 0)

    def test_find_overlap_index_nearest_4(self):
        index = self.intervalList.find_overlap_index_nearest(Interval("Chr",5,6))
        self.assertEqual(index, -1)

    def test_find_overlap_index_nearest_5(self):
        index = self.intervalList.find_overlap_index_nearest(Interval("Chr",6,7))
        self.assertEqual(index, -1)

    def test_find_overlap_index_nearest_6(self):
        # equidinstant features return left-most index
        index = self.intervalList.find_overlap_index_nearest(Interval("Chr",7,8))
        self.assertEqual(index, -1)

    def test_find_overlap_index_nearest_7(self):
        index = self.intervalList.find_overlap_index_nearest(Interval("Chr",8,9))
        self.assertEqual(index, -1)

    def test_find_overlap_index_nearest_8(self):
        index = self.intervalList.find_overlap_index_nearest(Interval("Chr",9,10))
        self.assertEqual(index, -1)

    def test_find_overlap_index_nearest_9(self):
        index = self.intervalList.find_overlap_index_nearest(Interval("Chr",10,11))
        self.assertEqual(index, 1)

    def test_find_overlap_index_nearest_10(self):
        index = self.intervalList.find_overlap_index_nearest(Interval("Chr",19,20))
        self.assertEqual(index, 1)

    def test_find_overlap_index_nearest_11(self):
        index = self.intervalList.find_overlap_index_nearest(Interval("Chr",20,21))
        self.assertEqual(index, 1)
        
    def test_find_overlap_index_nearest_12(self):
        index = self.intervalList.find_overlap_index_nearest(Interval("Chr",24,25))
        self.assertEqual(index, 2)
        
    def test_find_overlap_index_nearest_13(self):
        index = self.intervalList.find_overlap_index_nearest(Interval("Chr",25,26))
        self.assertEqual(index, 2)

    def test_find_overlap_index_nearest_14(self):
        index = self.intervalList.find_overlap_index_nearest(Interval("Chr",50,51))
        self.assertEqual(index, -1)
        
    def test_find_overlap_index_range_0(self):
        self.assertTrue(hasattr(self.intervalList, 'find_overlap_index_range'))

    def test_find_overlap_index_range_1(self):
        indices = list(self.intervalList.find_overlap_index_range(Interval("Chr", 0, 1)))
        self.assertEqual(indices, [])

    def test_find_overlap_index_range_2(self):
        indices = list(self.intervalList.find_overlap_index_range(Interval("Chr", 0, 2)))
        self.assertEqual(indices, [0])

    def test_find_overlap_index_range_3(self):
        indices = list(self.intervalList.find_overlap_index_range(Interval("Chr", 2, 8)))
        self.assertEqual(indices, [0])

    def test_find_overlap_index_range_4(self):
        indices = list(self.intervalList.find_overlap_index_range(Interval("Chr", 0, 20)))
        self.assertEqual(indices, [0, 1])

    def test_find_overlap_index_range_5(self):
        indices = list(self.intervalList.find_overlap_index_range(Interval("Chr", 0, 22)))
        self.assertEqual(indices, [0, 1, 2])

    def test_find_overlap_index_range_6(self):
        indices = list(self.intervalList.find_overlap_index_range(Interval("Chr", 15, 22)))
        self.assertEqual(indices, [1, 2])

    def test_find_overlap_index_range_7(self):
        indices = list(self.intervalList.find_overlap_index_range(Interval("Chr", 22, 50)))
        self.assertEqual(indices, [1, 2])

    def test_find_overlap_index_range_8(self):
        indices = list(self.intervalList.find_overlap_index_range(Interval("Chr", 25, 50)))
        self.assertEqual(indices, [2])

    def test_find_overlap_index_range_9(self):
        indices = list(self.intervalList.find_overlap_index_range(Interval("Chr", 40, 50)))
        self.assertEqual(indices, [])
        
    def test_find_overlap_index_bounds_0(self):
        self.assertTrue(hasattr(self.intervalList, 'find_overlap_index_bounds'))

    def test_find_overlap_index_bounds_1(self):
        indices = self.intervalList.find_overlap_index_bounds(Interval("Chr", 0, 1))
        self.assertEqual(indices, (-1, -1))

    def test_find_overlap_index_bounds_2(self):
        indices = self.intervalList.find_overlap_index_bounds(Interval("Chr", 0, 2))
        self.assertEqual(indices, (0, 1))

    def test_find_overlap_index_bounds_3(self):
        indices = self.intervalList.find_overlap_index_bounds(Interval("Chr", 2, 8))
        self.assertEqual(indices, (0, 1))

    def test_find_overlap_index_bounds_4(self):
        indices = self.intervalList.find_overlap_index_bounds(Interval("Chr", 0, 20))
        self.assertEqual(indices, (0, 2))

    def test_find_overlap_index_bounds_5(self):
        indices = self.intervalList.find_overlap_index_bounds(Interval("Chr", 0, 22))
        self.assertEqual(indices, (0, 3))

    def test_find_overlap_index_bounds_6(self):
        indices = self.intervalList.find_overlap_index_bounds(Interval("Chr", 15, 22))
        self.assertEqual(indices, (1, 3))

    def test_find_overlap_index_bounds_7(self):
        indices = self.intervalList.find_overlap_index_bounds(Interval("Chr", 22, 50))
        self.assertEqual(indices, (1, 3))

    def test_find_overlap_index_bounds_8(self):
        indices = self.intervalList.find_overlap_index_bounds(Interval("Chr", 25, 50))
        self.assertEqual(indices, (2, 3))

    def test_find_overlap_index_bounds_9(self):
        indices = self.intervalList.find_overlap_index_bounds(Interval("Chr", 40, 50))
        self.assertEqual(indices, (-1, -1))
        
    def test_find_overlap_length_0(self):
        self.assertTrue(hasattr(self.intervalList, 'find_overlap_length'))

    def test_find_overlap_length_1(self):
        length = self.intervalList.find_overlap_length(Interval("Chr", 0, 5))
        self.assertEqual(length, 4)

    def test_find_overlap_length_2(self):
        length = self.intervalList.find_overlap_length(Interval("Chr", 2, 4))
        self.assertEqual(length, 2)

    def test_find_overlap_length_3(self):
        length = self.intervalList.find_overlap_length(Interval("Chr", 0, 20))
        self.assertEqual(length, 14)

    def test_find_overlap_length_4(self):
        length = self.intervalList.find_overlap_length(Interval("Chr", 10, 50))
        self.assertEqual(length, 30)
        
    def test_find_overlap_fraction_0(self):
        self.assertTrue(hasattr(self.intervalList, 'find_overlap_fraction'))

    def test_find_overlap_fraction_1(self):
        length = self.intervalList.find_overlap_fraction(Interval("Chr", 0, 5))
        self.assertAlmostEqual(length, 4/34.0, 2)
        
    def test_find_overlap_fraction_2(self):
        length = self.intervalList.find_overlap_fraction(Interval("Chr", 2, 4))
        self.assertAlmostEqual(length, 2/34.0, 2)

    def test_find_overlap_fraction_3(self):
        length = self.intervalList.find_overlap_fraction(Interval("Chr", 0, 20))
        self.assertAlmostEqual(length, 14/34.0, 2)

    def test_find_overlap_fraction_4(self):
        length = self.intervalList.find_overlap_fraction(Interval("Chr", 10, 50))
        self.assertAlmostEqual(length, 30/34.0, 2)

    def test_find_overlap_fraction_5(self):
        length = self.intervalList.find_overlap_fraction(Interval("Chr", 0, 5), query=True)
        self.assertAlmostEqual(length, 4/5.0, 2)
        
    def test_find_overlaps_0(self):
        self.assertTrue(hasattr(self.intervalList, 'find_overlaps'))

    def test_find_overlaps_1(self):
        overlaps = list(self.intervalList.find_overlaps(Interval("Chr", 0, 1)))
        self.assertEqual(overlaps, [])

    def test_find_overlaps_2(self):
        overlaps = list(self.intervalList.find_overlaps(Interval("Chr", 2, 4)))
        self.assertEqual(overlaps, [self.intervalList[0]])

    def test_find_overlaps_3(self):
        overlaps = list(self.intervalList.find_overlaps(Interval("Chr", 2, 15)))
        self.assertEqual(overlaps, [self.intervalList[0], self.intervalList[1]])

    def test_find_overlaps_4(self):
        overlaps = list(self.intervalList.find_overlaps(Interval("Chr", 15, 22)))
        self.assertEqual(overlaps, [self.intervalList[1], self.intervalList[2]])

    def test_find_overlaps_5(self):
        overlaps = list(self.intervalList.find_overlaps(Interval("Chr", 25, 50)))
        self.assertEqual(overlaps, [self.intervalList[2]])

    def test_find_overlaps_6(self):
        overlaps = list(self.intervalList.find_overlaps(Interval("Chr", 40, 50)))
        self.assertEqual(overlaps, [])
    

                
class TestCase007_IntervalList(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

# TEST IntervalSet.insort() exhaustively!!!
# TEST IntervalSet.remove() exhaustively!!!
# TEST IntervalSet: test interval set operations after _remove() and _insert()


class TestCase009_IntervalSet(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

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
    
