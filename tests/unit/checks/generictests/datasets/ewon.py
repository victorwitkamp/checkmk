#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# yapf: disable
# type: ignore

checkname = 'ewon'

info = [
    ['1', '0', 'System'], ['2', '0', 'System'], ['3', '0', 'System'],
    ['4', '8192', 'System'], ['5', '1', 'N2-Versorgung'],
    ['6', '0', 'Betriebsraum'], ['7', '0', 'Betriebsraum'],
    ['8', '0', 'Flur_Nebenraum'], ['9', '0', 'Flur_Nebenraum'],
    ['10', '1527', 'Schutzbereich01'], ['11', '1550', 'Schutzbereich01'],
    ['12', '1550', 'Schutzbereich01'], ['13', '1520', 'Schutzbereich01'],
    ['14', '0', 'Schutzbereich01'], ['15', '1029', 'Schutzbereich01'],
    ['16', '512', 'Schutzbereich01'], ['17', '513', 'Schutzbereich01'],
    ['18', '1539', 'Schutzbereich02'], ['19', '1550', 'Schutzbereich02'],
    ['20', '1550', 'Schutzbereich02'], ['21', '1520', 'Schutzbereich02'],
    ['22', '0', 'Schutzbereich02'], ['23', '1029', 'Schutzbereich02'],
    ['24', '512', 'Schutzbereich02'], ['25', '513', 'Schutzbereich02'],
    ['26', '1533', 'Schutzbereich03'], ['27', '1550', 'Schutzbereich03'],
    ['28', '1550', 'Schutzbereich03'], ['29', '1520', 'Schutzbereich03'],
    ['30', '0', 'Schutzbereich03'], ['31', '1029', 'Schutzbereich03'],
    ['32', '512', 'Schutzbereich03'], ['33', '513', 'Schutzbereich03'],
    ['34', '0', 'Schutzbereich04'], ['35', '0', 'Schutzbereich04'],
    ['36', '0', 'Schutzbereich04'], ['37', '0', 'Schutzbereich04'],
    ['38', '0', 'Schutzbereich04'], ['39', '0', 'Schutzbereich04'],
    ['40', '0', 'Schutzbereich04'], ['41', '0', 'Schutzbereich04']
]


mock_host_conf = {'': ['oxyreduct']}


discovery = {
    '': [
        ('eWON Status', {'device': 'oxyreduct'}),
        ('Betriebsraum', {'device': 'oxyreduct'}),
        ('Flur_Nebenraum', {'device': 'oxyreduct'}),
        ('N2-Versorgung', {'device': 'oxyreduct'}),
        ('Schutzbereich01', {'device': 'oxyreduct'}),
        ('Schutzbereich02', {'device': 'oxyreduct'}),
        ('Schutzbereich03', {'device': 'oxyreduct'}),
        ('System', {'device': 'oxyreduct'}),
    ]
}


checks = {
    '': [
        ('eWON Status', {'device': 'oxyreduct'}, [
            (0, 'Configured for oxyreduct', []),
        ]),
        ('Betriebsraum', {'device': 'oxyreduct'}, [
            (0, 'O2 Sensor inactive', []),
        ]),
        ('Flur_Nebenraum', {'device': 'oxyreduct'}, [
            (0, 'O2 Sensor inactive', []),
        ]),
        ('N2-Versorgung', {'device': 'oxyreduct'}, [
            (0, 'N2 to safe area inactive', []),
            (0, 'N2 request from safe area inactive', []),
            (2, 'N2 via compressor inactive', []),
        ]),
        ('Schutzbereich01', {'device': 'oxyreduct'}, [
            (0, 'O2 average: 15.27 %', [
                ('o2_percentage', 15.27, 16, 17, None, None),
            ]),
            (0, 'O2 target: 15.50 %', []),
            (0, 'O2 for N2-in: 15.50 %', []),
            (0, 'O2 for N2-out: 15.20 %', []),
            (0, 'CO2 maximum: 0.00 ppm', []),
            (0, 'air control closed', []),
            (0, 'valve closed', []),
            (0, 'valve active', []),
            (0, 'access open', []),
            (0, 'mode BK1', []),
        ]),
        ('System', {'device': 'oxyreduct'}, [
            (0, 'alarms: 0.00', []),
            (0, 'incidents: 0.00', []),
            (0, 'shutdown messages: 0.00', []),
            (2, 'luminous field active', []),
        ]),
    ],
}
