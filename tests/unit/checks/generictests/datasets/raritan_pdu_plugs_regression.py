#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# yapf: disable
# type: ignore

checkname = 'raritan_pdu_plugs'

info = [['1', '', '7'], ['36', 'FooName', '7']]

discovery = {
    '': [
        ('1', {'discovered_state': 'on'}),
        ('36', {'discovered_state': 'on'}),
    ]
}

checks = {
    '': [
        ('1', 'on', [
            (0, 'Status: on', []),
        ]),
        ('36', 'on', [
            (0, 'FooName', []),
            (0, 'Status: on', []),
        ]),
        ('1', 'on', [
            (0, 'Status: on', []),
            ]),
        ('36', 5, [
            (0, 'FooName', []),
            (0, 'Status: on', []),
            (2, 'Expected: above upper warning', []),
        ]),
    ]
}
