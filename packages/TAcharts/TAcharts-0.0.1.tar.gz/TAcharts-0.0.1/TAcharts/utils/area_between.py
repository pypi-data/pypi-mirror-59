#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

import numpy as np
from .wrappers import pd_series_to_np_array


@pd_series_to_np_array
def area_between(line1, line2):
    ''' Return the area between line1 and line2 '''

    diff = line1 - line2
    x1 = diff[:-1]
    x2 = diff[1:]

    triangle_area = abs(x2 - x1) * .5
    square_area = np.amin(zip(x1, x2), axis=1)

    return np.sum([triangle_area, square_area])
