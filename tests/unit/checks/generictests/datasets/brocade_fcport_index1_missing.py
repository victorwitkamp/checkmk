#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# yapf: disable
# type: ignore

checkname = 'brocade_fcport'

info = [
    [
        [
            '45', '6', '1', '1', '2905743640', '886676077', '925307562',
            '12463206', '3618162349', '0', '0', '0', '0', '', 'port44'
        ],
        [
            '46', '6', '1', '1', '3419046246', '972264932',
            '3137901401', '544788281', '569031932', '0', '0', '0', '82',
            '', 'port45'
        ],
        [
            '47', '6', '1', '1', '1111764110', '2429196329',
            '4259150384', '1651642909', '569031932', '0', '0', '0', '6',
            '', 'port46'
        ],
        [
            '48', '6', '1', '1', '1832010527', '3916222665',
            '596751007', '1430959330', '3618162349', '0', '0', '0', '0',
            '', 'port47'
        ]
    ], [['45', '512'], ['46', '512'], ['47', '512'], ['48', '512']],
    [
        ['805306369', '6', '100'], ['805306370', '24', '0'],
        ['805306371', '131', '0'], ['805306372', '1', '0'],
        ['805306373', '1', '0'], ['805306374', '1', '0'],
        ['805306375', '1', '0'], ['805306376', '1', '0'],
        ['805306377', '1', '0'], ['805306378', '1', '0'],
        ['1073741868', '56', '16000'], ['1073741869', '56', '16000'],
        ['1073741870', '56', '16000'], ['1073741871', '56', '16000']
    ], []
]

discovery = {
    '': [
        (
            '44 ISL port44',
            '{ "phystate": [6], "opstate": [1], "admstate": [1] }'
        ),
        (
            '45 ISL port45',
            '{ "phystate": [6], "opstate": [1], "admstate": [1] }'
        ),
        (
            '46 ISL port46',
            '{ "phystate": [6], "opstate": [1], "admstate": [1] }'
        ),
        (
            '47 ISL port47',
            '{ "phystate": [6], "opstate": [1], "admstate": [1] }'
        )
    ]
}

checks = {
    '': [
        (
            '44 ISL port44', {
                'assumed_speed': 2.0,
                'phystate': [6],
                'notxcredits': (3.0, 20.0),
                'opstate': [1],
                'c3discards': (3.0, 20.0),
                'admstate': [1],
                'rxencinframes': (3.0, 20.0),
                'rxcrcs': (3.0, 20.0),
                'rxencoutframes': (3.0, 20.0)
            }, [
                (
                    0,
                    'ISL speed: 16 Gbit/s, In: 0.00 B/s, Out: 0.00 B/s, Physical: in sync, Operational: online, Administrative: online',
                    [
                        ('in', 0.0, None, None, 0, 1600000000.0),
                        ('out', 0.0, None, None, 0, 1600000000.0),
                        ('rxframes', 0.0, None, None, None, None),
                        ('txframes', 0.0, None, None, None, None),
                        ('rxcrcs', 0.0, None, None, None, None),
                        ('rxencoutframes', 0.0, None, None, None, None),
                        ('rxencinframes', 0.0, None, None, None, None),
                        ('c3discards', 0.0, None, None, None, None),
                        ('notxcredits', 0.0, None, None, None, None)
                    ]
                )
            ]
        ),
        (
            '45 ISL port45', {
                'assumed_speed': 2.0,
                'phystate': [6],
                'notxcredits': (3.0, 20.0),
                'opstate': [1],
                'c3discards': (3.0, 20.0),
                'admstate': [1],
                'rxencinframes': (3.0, 20.0),
                'rxcrcs': (3.0, 20.0),
                'rxencoutframes': (3.0, 20.0)
            }, [
                (
                    0,
                    'ISL speed: 16 Gbit/s, In: 0.00 B/s, Out: 0.00 B/s, Physical: in sync, Operational: online, Administrative: online',
                    [
                        ('in', 0.0, None, None, 0, 1600000000.0),
                        ('out', 0.0, None, None, 0, 1600000000.0),
                        ('rxframes', 0.0, None, None, None, None),
                        ('txframes', 0.0, None, None, None, None),
                        ('rxcrcs', 0.0, None, None, None, None),
                        ('rxencoutframes', 0.0, None, None, None, None),
                        ('rxencinframes', 0.0, None, None, None, None),
                        ('c3discards', 0.0, None, None, None, None),
                        ('notxcredits', 0.0, None, None, None, None)
                    ]
                )
            ]
        ),
        (
            '46 ISL port46', {
                'assumed_speed': 2.0,
                'phystate': [6],
                'notxcredits': (3.0, 20.0),
                'opstate': [1],
                'c3discards': (3.0, 20.0),
                'admstate': [1],
                'rxencinframes': (3.0, 20.0),
                'rxcrcs': (3.0, 20.0),
                'rxencoutframes': (3.0, 20.0)
            }, [
                (
                    0,
                    'ISL speed: 16 Gbit/s, In: 0.00 B/s, Out: 0.00 B/s, Physical: in sync, Operational: online, Administrative: online',
                    [
                        ('in', 0.0, None, None, 0, 1600000000.0),
                        ('out', 0.0, None, None, 0, 1600000000.0),
                        ('rxframes', 0.0, None, None, None, None),
                        ('txframes', 0.0, None, None, None, None),
                        ('rxcrcs', 0.0, None, None, None, None),
                        ('rxencoutframes', 0.0, None, None, None, None),
                        ('rxencinframes', 0.0, None, None, None, None),
                        ('c3discards', 0.0, None, None, None, None),
                        ('notxcredits', 0.0, None, None, None, None)
                    ]
                )
            ]
        ),
        (
            '47 ISL port47', {
                'assumed_speed': 2.0,
                'phystate': [6],
                'notxcredits': (3.0, 20.0),
                'opstate': [1],
                'c3discards': (3.0, 20.0),
                'admstate': [1],
                'rxencinframes': (3.0, 20.0),
                'rxcrcs': (3.0, 20.0),
                'rxencoutframes': (3.0, 20.0)
            }, [
                (
                    0,
                    'ISL speed: 16 Gbit/s, In: 0.00 B/s, Out: 0.00 B/s, Physical: in sync, Operational: online, Administrative: online',
                    [
                        ('in', 0.0, None, None, 0, 1600000000.0),
                        ('out', 0.0, None, None, 0, 1600000000.0),
                        ('rxframes', 0.0, None, None, None, None),
                        ('txframes', 0.0, None, None, None, None),
                        ('rxcrcs', 0.0, None, None, None, None),
                        ('rxencoutframes', 0.0, None, None, None, None),
                        ('rxencinframes', 0.0, None, None, None, None),
                        ('c3discards', 0.0, None, None, None, None),
                        ('notxcredits', 0.0, None, None, None, None)
                    ]
                )
            ]
        )
    ]
}
