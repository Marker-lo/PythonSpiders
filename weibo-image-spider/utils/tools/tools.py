#!/usr/bin python
# coding:utf-8
# Created by yubiao.luo at 2020/9/10
import decimal
import sys
import traceback

TWO_POINT_DECIMAL = decimal.Decimal('0.00')
FOUR_POINT_DECIMAL = decimal.Decimal('0.0000')
EIGHT_POINT_DECIMAL = decimal.Decimal('0.00000000')
NINE_POINT_DECIMAL = decimal.Decimal('0.000000000')
TEN_POINT_DECIMAL = decimal.Decimal('0.0000000000')
SIXTEEN_POINT_DECIMAL = decimal.Decimal('0.0000000000000000')


def to_decimal(f, precision=FOUR_POINT_DECIMAL):
    if isinstance(f, (int, float)):
        d = decimal.Decimal.from_float(f)
    elif isinstance(f, decimal.Decimal):
        d = f
    else:
        d = decimal.Decimal(f)
    return d.quantize(precision)


def get_traceback(n=4):
    exType, exVal, exStack = sys.exc_info()
    ss = traceback.format_exception(exType, exVal, exStack)
    lines = []
    for s1 in ss:
        s2 = s1.split('\n')
        for s3 in s2:
            s4 = s3.strip()
            if len(s4) > 0:
                lines.append(s4)
            # end if
        # end for
    # end for
    return " ==> ".join(lines[-n:])


def chunkify(count, number):
    return [count[n::number] for n in range(number)]
