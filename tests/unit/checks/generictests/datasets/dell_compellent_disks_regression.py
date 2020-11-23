#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# yapf: disable
# type: ignore


checkname = 'dell_compellent_disks'

info = [[
    ['1', '1', '1', '', '1'],
    ['2', '999', '1', '', '1'],
    ['3', '1', '999', '', '1'],
    ['4', '1', '0', 'ATTENTION', '1'],
    ['5', '1', '999', 'ATTENTION', '1'],
    ['10', '2', '0', 'KAPUTT', '1'],
], [
    ['serial1'], ['serial2'], ['serial3'], ['serial4'], ['serial5'], ['serial10']
]]

discovery = {
    '': [('1', None), ('2', None), ('3', None), ('4', None), ('5', None), ('10', None)]
}

checks = {
    '': [
        ('1', {}, [
            (0, 'Status: UP', []),
            (0, 'Location: Enclosure 1', []),
            (0, "Serial number: serial1", []),
        ]),
        ('2', {}, [
            (3, 'Status: unknown[999]', []),
            (0, 'Location: Enclosure 1', []),
            (0, "Serial number: serial2", []),
        ]),
        ('3', {}, [
            (0, 'Status: UP', []),
            (0, 'Location: Enclosure 1', []),
            (0, "Serial number: serial3", []),
        ]),
        ('4', {}, [
            (0, 'Status: UP', []),
            (0, 'Location: Enclosure 1', []),
            (0, "Serial number: serial4", []),
            (2, 'Health: not healthy, Reason: ATTENTION', []),
        ]),
        ('5', {}, [
            (0, 'Status: UP', []),
            (0, 'Location: Enclosure 1', []),
            (0, "Serial number: serial5", []),
            (3, 'Health: unknown[999], Reason: ATTENTION', []),
        ]),
        ('10', {}, [
            (2, 'Status: DOWN', []),
            (0, 'Location: Enclosure 1', []),
            (0, "Serial number: serial10", []),
            (2, 'Health: not healthy, Reason: KAPUTT', []),
        ]),
    ]
}
