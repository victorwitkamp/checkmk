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
         '27800',
         '105000',
         'critical',
         '80000',
         'active',
         '55000',
         'active',
         '500',
         '00',
         'active',
         '45000',
         'active',
         '40000',
         'active'],
        ['thermal_zone1',
         'enabled',
         'acpitz',
         '29800',
         '105000',
         'critical',
         '108000',
         'passive']]


discovery = {'': [('Zone 1', {})]}


checks = {'': [('Zone 1',
                {'device_levels_handling': 'devdefault', 'levels': (70.0, 80.0)},
                [(0, '29.8 \xb0C', [('temp', 29.8, 108.0, 105.0, None, None)])])]}
