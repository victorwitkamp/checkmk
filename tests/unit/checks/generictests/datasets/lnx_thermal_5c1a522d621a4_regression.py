#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# yapf: disable
# type: ignore



checkname = 'lnx_thermal'


info = [['thermal_zone0',
         'enabled',
         'acpitz',
         '8300',
         '31300',
         'critical',
         '9800',
         'passive'],
        ['thermal_zone1',
         '-',
         'pkg-temp-0',
         '',
         '35000',
         '0',
         'passive',
         '0',
         'passive'],
        ['thermal_zone2',
         '-',
         'pkg-temp-1',
         '',
         '40000',
         '0',
         'passive',
         '0',
         'passive']]


discovery = {'': [('Zone 0', {})]}


checks = {'': [('Zone 0',
                {'device_levels_handling': 'devdefault', 'levels': (70.0, 80.0)},
                [(0, '8.3 \xb0C', [('temp', 8.3, 9.8, 31.3, None, None)])])]}
