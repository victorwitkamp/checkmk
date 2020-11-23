#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# yapf: disable
# type: ignore



checkname = 'liebert_system_events'


info = [
    ['Ambient Air Temperature Sensor Issue', 'Inactive Event'],
    ['Supply Fluid Over Temp', 'Inactive Event'],
    ['Supply Fluid Under Temp', 'Inactive Event'],
    ['Supply Fluid Temp Sensor Issue', 'Active Warning'],
]


discovery = {
    '': [
        (None, {}),
    ],
}


checks = {
    '': [
        (None, {}, [
            (2, 'Supply Fluid Temp Sensor Issue: Active Warning', []),
        ]),
    ],
}
