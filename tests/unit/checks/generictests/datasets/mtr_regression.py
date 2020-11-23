#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# yapf: disable
# type: ignore

checkname = 'mtr'

info = [
    [
        'foo.bar.1', '1578427995', '2', 'baz-1', '0.0%', '10', '0.3',
        '0.2', '0.2', '0.3', '0.0', '???', '100.0', '10', '0.0',
        '0.0', '0.0', '0.0', '0.0'
    ],
    [
        'foo.bar.2', '1578427995', '2', 'baz-2', '0.0%', '10', '0.3',
        '0.2', '0.2', '0.3', '0.0', '???', '0.0', '10', '0.0', '0.0',
        '0.0', '0.0', '0.0'
    ]
]

discovery = {'': [('foo.bar.1', {}), ('foo.bar.2', {})]}

checks = {
    '': [
        (
            'foo.bar.1', {
                'rtstddev': (150, 250),
                'rta': (150, 250),
                'pl': (10, 25)
            }, [
                (
                    0, 'Number of Hops: 2', [
                        ('hops', 2, None, None, None, None),
                        ('hop_1_rta', 0.0002, None, None, None, None),
                        ('hop_1_rtmin', 0.0002, None, None, None, None),
                        ('hop_1_rtmax', 0.0003, None, None, None, None),
                        ('hop_1_rtstddev', 0.0, None, None, None, None),
                        (
                            'hop_1_response_time', 0.0003, None, None, None,
                            None
                        ), ('hop_1_pl', 0.0, None, None, None, None)
                    ]
                ),
                (
                    2,
                    'Packet loss 100.0%(!!) (warn/crit at 10%/25%), Round trip average 0.0ms, Standard deviation 0.0ms\r\nHops in last check:\nHop 1: baz-1\nHop 2: ???\n',
                    [
                        ('hop_1_rta', 0.0002, None, None, None, None),
                        ('hop_1_rtmin', 0.0002, None, None, None, None),
                        ('hop_1_rtmax', 0.0003, None, None, None, None),
                        ('hop_1_rtstddev', 0.0, None, None, None, None),
                        (
                            'hop_1_response_time', 0.0003, None, None, None,
                            None
                        ), ('hop_1_pl', 0.0, None, None, None, None),
                        ('hop_2_rta', 0.0, 0.15, 0.25, None, None),
                        ('hop_2_rtmin', 0.0, None, None, None, None),
                        ('hop_2_rtmax', 0.0, None, None, None, None),
                        ('hop_2_rtstddev', 0.0, 0.15, 0.25, None, None),
                        ('hop_2_response_time', 0.0, None, None, None, None),
                        ('hop_2_pl', 100.0, 10, 25, None, None)
                    ]
                )
            ]
        ),
        (
            'foo.bar.2', {
                'rtstddev': (150, 250),
                'rta': (150, 250),
                'pl': (10, 25)
            }, [
                (
                    0, 'Number of Hops: 2', [
                        ('hops', 2, None, None, None, None),
                        ('hop_1_rta', 0.0002, None, None, None, None),
                        ('hop_1_rtmin', 0.0002, None, None, None, None),
                        ('hop_1_rtmax', 0.0003, None, None, None, None),
                        ('hop_1_rtstddev', 0.0, None, None, None, None),
                        (
                            'hop_1_response_time', 0.0003, None, None, None,
                            None
                        ), ('hop_1_pl', 0.0, None, None, None, None)
                    ]
                ),
                (
                    0,
                    'Packet loss 0.0%, Round trip average 0.0ms, Standard deviation 0.0ms\r\nHops in last check:\nHop 1: baz-2\nHop 2: ???\n',
                    [
                        ('hop_1_rta', 0.0002, None, None, None, None),
                        ('hop_1_rtmin', 0.0002, None, None, None, None),
                        ('hop_1_rtmax', 0.0003, None, None, None, None),
                        ('hop_1_rtstddev', 0.0, None, None, None, None),
                        (
                            'hop_1_response_time', 0.0003, None, None, None,
                            None
                        ), ('hop_1_pl', 0.0, None, None, None, None),
                        ('hop_2_rta', 0.0, 0.15, 0.25, None, None),
                        ('hop_2_rtmin', 0.0, None, None, None, None),
                        ('hop_2_rtmax', 0.0, None, None, None, None),
                        ('hop_2_rtstddev', 0.0, 0.15, 0.25, None, None),
                        ('hop_2_response_time', 0.0, None, None, None, None),
                        ('hop_2_pl', 0.0, 10, 25, None, None)
                    ]
                )
            ]
        )
    ]
}
