#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# yapf: disable
# type: ignore



checkname = 'printer_input'


info = [
    ['1.1', 'Printer 1', 'MP Tray', '19', '8', '150', '0'],
    ['1.2', 'Custom Printer Name 1', 'Cassette 1', '4', '8', '500', '400'],
    ['1.3', '', 'Cassette 2', '0', '8', '300', '150'],
    ['1.4', '', 'Option Feeder Lower', '', '', '', ''],
]


discovery = {
    '': [
        ('Cassette 2', {}),
        ('Custom Printer Name 1', {}),
        ('Option Feeder Lower', {}),
    ],
}


checks = {
    '': [
        ('Cassette 2', {'capacity_levels': (0.0, 0.0)}, [
            (0, 'Cassette 2', []),
            (0, 'Status: Available and Idle', []),
            (0, 'Capacity: 50.00% of 300 sheets remaining', []),
        ]),
        ('Custom Printer Name 1', {'capacity_levels': (0.0, 0.0)}, [
            (0, 'Cassette 1', []),
            (0, 'Status: Available and Active', []),
            (0, 'Capacity: 80.00% of 500 sheets remaining', []),
        ]),
        ('Option Feeder Lower', {'capacity_levels': (0.0, 0.0)}, [
            (0, 'Option Feeder Lower', []),
            (0, 'Status: Available and Idle', []),
            (0, 'Capacity: 0', []),
        ]),
    ],
}
