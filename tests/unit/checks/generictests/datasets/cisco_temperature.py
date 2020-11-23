#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# yapf: disable
# type: ignore


checkname = 'cisco_temperature'

info = [
    [
        ['1176', 'Filtered sensor'],
        ['1177', 'Sensor with large precision'],
        ['2008', 'Switch 1 - WS-C2960X-24PD-L - Sensor 0'],
        ['4950', 'Linecard-1 Port-1'],
        ['21590', 'module-1 Crossbar1(s1)'],
        ['21591', 'module-1 Crossbar2(s2)'],
        ['21592', 'module-1 Arb-mux (s3)'],
        ['31958', 'Transceiver(slot:1-port:1)'],
        ['300000003', 'Ethernet1/1 Lane 1 Transceiver Voltage Sensor'],
        ['300000004', 'Ethernet1/1 Lane 1 Transceiver Bias Current Sensor'],
        ['300000007', 'Ethernet1/1 Lane 1 Transceiver Temperature Sensor'],
        ['300000013', 'Ethernet1/1 Lane 1 Transceiver Receive Power Sensor'],
        ['300000014', 'Ethernet1/1 Lane 1 Transceiver Transmit Power Sensor'],
    ],
    [
        ['1176', '1', '9', '1613258611', '0', '1'],
        ['1177', '8', '9', '1613258611', '0', '1'],
        ['21590', '8', '9', '0', '62', '1'],
        ['21591', '8', '9', '0', '58', '1'],
        ['21592', '8', '9', '0', '49', '1'],
        ['300000003', '4', '8', '0', '3333', '1'],
        ['300000004', '5', '7', '0', '6002', '1'],
        ['300000007', '8', '8', '0', '24492', '1'],
        ['300000013', '14', '8', '0', '-3271', '1'],
        ['300000014', '14', '8', '0', '1000', '1'],
    ],
    [
        ['21590.1', '115'],
        ['21590.2', '125'],
        ['21591.1', '115'],
        ['21591.2', '125'],
        ['21592.1', '115'],
        ['21592.2', '125'],
        ['300000003.1', '3630'],
        ['300000003.2', '3465'],
        ['300000003.3', '2970'],
        ['300000003.4', '3135'],
        ['300000004.1', '10500'],
        ['300000004.2', '10500'],
        ['300000004.3', '2500'],
        ['300000004.4', '2500'],
        ['300000007.1', '75000'],
        ['300000007.2', '70000'],
        ['300000007.3', '-5000'],
        ['300000007.4', '0'],
        ['300000013.1', '2000'],
        ['300000013.2', '-1000'],
        ['300000013.3', '-13904'],
        ['300000013.4', '-9901'],
        ['300000014.1', '1699'],
        ['300000014.2', '-1300'],
        ['300000014.3', '-11301'],
        ['300000014.4', '-7300'],
    ],
    [
        ['2008', 'SW#1, Sensor#1, GREEN', '36', '68', '1'],
        ['3008', 'SW#2, Sensor#1, GREEN', '37', '68', '1'],
    ],
    [],
]

discovery = {
    '': [
        ('Sensor with large precision', {}),
        ('Ethernet1/1 Lane 1 Transceiver Temperature Sensor', {}),
        ('SW 1 Sensor 1', {}),
        ('SW 2 Sensor 1', {}),
        ('module-1 Arb-mux (s3)', {}),
        ('module-1 Crossbar1(s1)', {}),
        ('module-1 Crossbar2(s2)', {}),
    ],
    'dom': [
        ('Ethernet1/1 Lane 1 Transceiver Receive Power Sensor', {}),
        ('Ethernet1/1 Lane 1 Transceiver Transmit Power Sensor', {}),
    ]
}

checks = {
    '': [
        (
            'Sensor with large precision',
            {},
            [(
                0,
                '0.0 \xb0C',
                [('temp', 0.0, None, None, None, None)],
            )],
        ),
        (
            'Ethernet1/1 Lane 1 Transceiver Temperature Sensor',
            {},
            [(
                0,
                '24.5 \xb0C',
                [('temp', 24.492, 70.0, 75.0, None, None)],
            )],
        ),
        (
            'SW 1 Sensor 1',
            {},
            [(
                0,
                '36 \xb0C',
                [('temp', 36, 68, 68, None, None)],
            )],
        ),
        (
            'SW 2 Sensor 1',
            {},
            [(
                0,
                '37 \xb0C',
                [('temp', 37, 68, 68, None, None)],
            )],
        ),
        (
            'module-1 Arb-mux (s3)',
            {},
            [(
                0,
                '49.0 \xb0C',
                [('temp', 49.0, None, None, None, None)],
            )],
        ),
        ('module-1 Crossbar1(s1)', {}, [
            (0, '62.0 \xb0C', [('temp', 62.0, None, None, None, None)]),
        ]),
        (
            'module-1 Crossbar2(s2)',
            {},
            [
                (0, '58.0 \xb0C', [('temp', 58.0, None, None, None, None)]),
            ],
        ),
    ],
    'dom': [
        (
            'Ethernet1/1 Lane 1 Transceiver Receive Power Sensor',
            {},
            [(
                0,
                'Status: OK',
                [],
            ),
             (
                 0,
                 'Signal power: -3.27 dBm',
                 [('input_signal_power_dbm', -3.271, -1.0, 2.0, None, None)],
             )],
        ),
        (
            'Ethernet1/1 Lane 1 Transceiver Transmit Power Sensor',
            {},
            [(
                0,
                'Status: OK',
                [],
            ),
             (
                 1,
                 'Signal power: 1.00 dBm (warn/crit at -1.30 dBm/1.70 dBm)',
                 [('output_signal_power_dbm', 1.0, -1.3, 1.699, None, None)],
             )],
        ),
    ],
}
