#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# yapf: disable
# type: ignore



checkname = 'cisco_temperature'


info = [[['300000013', 'Ethernet1/1 Lane 1 Transceiver Receive Power Sensor'],
         ['300000014', 'Ethernet1/1 Lane 1 Transceiver Transmit Power Sensor'],
         ['300003533', 'Ethernet1/3 Lane 1 Transceiver Receive Power Sensor'],
         ['300003534', 'Ethernet1/3 Lane 1 Transceiver Transmit Power Sensor'],
         ['300005293', 'Ethernet1/4 Lane 1 Transceiver Receive Power Sensor'],
         ['300005294', 'Ethernet1/4 Lane 1 Transceiver Transmit Power Sensor']],
        [['300000013', '14', '8', '0', '-3271', '1'],
         ['300000014', '14', '8', '0', '1000', '1'],
         ['300003533', '14', '8', '0', '-2823', '1'],
         ['300003534', '14', '8', '0', '-1000', '1'],
         ['300005293', '14', '8', '0', '-40000', '1'],
         ['300005294', '14', '8', '0', '0', '1']],
        [['300000013.1', '2000'],
         ['300000013.2', '-1000'],
         ['300000013.3', '-13904'],
         ['300000013.4', '-9901'],
         ['300000014.1', '1699'],
         ['300000014.2', '-1300'],
         ['300000014.3', '-11301'],
         ['300000014.4', '-7300'],
         ['300003533.1', '2000'],
         ['300003533.2', '-1000'],
         ['300003533.3', '-13904'],
         ['300003533.4', '-9901'],
         ['300003534.1', '1699'],
         ['300003534.2', '-1300'],
         ['300003534.3', '-11301'],
         ['300003534.4', '-7300'],
         ['300005293.1', '2000'],
         ['300005293.2', '-1000'],
         ['300005293.3', '-13904'],
         ['300005293.4', '-9901'],
         ['300005294.1', '1699'],
         ['300005294.2', '-1300'],
         ['300005294.3', '-11301'],
         ['300005294.4', '-7300']],
        [],
        [['Ethernet1/1 Lane 1 Transceiver Receive Power Sensor', '1'],
         ['Ethernet1/1 Lane 1 Transceiver Transmit Power Sensor', '1'],
         ['Ethernet1/3 Lane 1 Transceiver Receive Power Sensor', '2'],
         ['Ethernet1/3 Lane 1 Transceiver Transmit Power Sensor', '2'],
         ['Ethernet1/4 Lane 1 Transceiver Receive Power Sensor', '3'],
         ['Ethernet1/4 Lane 1 Transceiver Transmit Power Sensor', '3']]]


discovery = {'': [],
             'dom': [('Ethernet1/1 Lane 1 Transceiver Receive Power Sensor', {}),
                     ('Ethernet1/1 Lane 1 Transceiver Transmit Power Sensor', {}),
                     ('Ethernet1/4 Lane 1 Transceiver Receive Power Sensor', {}),
                     ('Ethernet1/4 Lane 1 Transceiver Transmit Power Sensor', {})]}


checks = {'dom': [('Ethernet1/1 Lane 1 Transceiver Receive Power Sensor',
                   {},
                   [(0, 'Status: OK', []),
                    (0,
                     'Signal power: -3.27 dBm',
                     [('input_signal_power_dbm', -3.271, -1.0, 2.0, None, None)])]),
                  ('Ethernet1/1 Lane 1 Transceiver Transmit Power Sensor',
                   {},
                   [(0, 'Status: OK', []),
                    (1,
                     'Signal power: 1.00 dBm (warn/crit at -1.30 dBm/1.70 dBm)',
                     [('output_signal_power_dbm', 1.0, -1.3, 1.699, None, None)])]),
                  ('Ethernet1/4 Lane 1 Transceiver Receive Power Sensor',
                   {},
                   [(0, 'Status: OK', []),
                    (2,
                     'Signal power: -40.00 dBm (warn/crit below -9.90 dBm/-13.90 dBm)',
                     [('input_signal_power_dbm', -40.0, -1.0, 2.0, None, None)])]),
                  ('Ethernet1/4 Lane 1 Transceiver Transmit Power Sensor',
                   {},
                   [(0, 'Status: OK', []),
                    (1,
                     'Signal power: 0.00 dBm (warn/crit at -1.30 dBm/1.70 dBm)',
                     [('output_signal_power_dbm', 0.0, -1.3, 1.699, None, None)])])]}


mock_host_conf_merged = {'dom': {'admin_states': ['1', '3']}}
