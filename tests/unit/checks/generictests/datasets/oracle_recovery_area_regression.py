#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# yapf: disable
# type: ignore



checkname = 'oracle_recovery_area'


info = [['AIMDWHD1', '300', '51235', '49000', '300']]


discovery = {'': [('AIMDWHD1', {})]}


checks = {'': [('AIMDWHD1',
                {'levels': (70.0, 90.0)},
                [(2,
                  '47.85 GB out of 50.03 GB used (95.1%, warn/crit at 70.0%/90.0%), 300.00 MB reclaimable',
                  [('used', 49000, 35864.5, 46111.5, 0, 51235),
                   ('reclaimable', 300, None, None, None, None)])]),
               ]}
