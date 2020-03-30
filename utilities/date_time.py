#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time    : 2/18/2020 11:52 AM
# @Author  : Xin He
# @File    : date_time.py
# @Desc    : 

import arrow


def get_delta_datetime(**kwarg):
    """
    获取几天之后的utc时间
    Args:
        kwarg: 偏移时间, 例如, days=1, months=-2, years=99

    Returns:
        utc_time: 例如, 2020-02-18T03:44:55.458000Z

    """

    date = arrow.utcnow().shift(**kwarg)
    utc_time = date.format('YYYY-MM-DDTHH:mm:ss.SSS') + '000Z'

    return utc_time
