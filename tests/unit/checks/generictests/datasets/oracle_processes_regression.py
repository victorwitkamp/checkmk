#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# yapf: disable
# type: ignore



checkname = 'oracle_processes'


info = [['FDMTST', '50', '300'],
        ['METWFPRD', '46', '150'],
        ['METRODEV', '138', '1000'],
        ['TLDTST', '122', '500'],
        ['FDMPRD', '125', '300'],
        ['FARMPRD', '54', '300'],
        ['DB1DEV2', '1152', '1500']]


discovery = {'': [('DB1DEV2', {}),
                  ('FARMPRD', {}),
                  ('FDMPRD', {}),
                  ('FDMTST', {}),
                  ('METRODEV', {}),
                  ('METWFPRD', {}),
                  ('TLDTST', {})]}


checks = {'': [('DB1DEV2',
                {'levels': (70.0, 90.0)},
                [(1,
                  '1152 of 1500 processes are used (76%, warn/crit at 70%/90%)',
                  [('processes', 1152, 1050.0, 1350.0, None, None)])]),
               ('FARMPRD',
                {'levels': (70.0, 90.0)},
                [(0,
                  '54 of 300 processes are used (18%, warn/crit at 70%/90%)',
                  [('processes', 54, 210.0, 270.0, None, None)])]),
               ('FDMPRD',
                {'levels': (70.0, 90.0)},
                [(0,
                  '125 of 300 processes are used (41%, warn/crit at 70%/90%)',
                  [('processes', 125, 210.0, 270.0, None, None)])]),
               ('FDMTST',
                {'levels': (70.0, 90.0)},
                [(0,
                  '50 of 300 processes are used (16%, warn/crit at 70%/90%)',
                  [('processes', 50, 210.0, 270.0, None, None)])]),
               ('METRODEV',
                {'levels': (70.0, 90.0)},
                [(0,
                  '138 of 1000 processes are used (13%, warn/crit at 70%/90%)',
                  [('processes', 138, 700.0, 900.0, None, None)])]),
               ('METWFPRD',
                {'levels': (70.0, 90.0)},
                [(0,
                  '46 of 150 processes are used (30%, warn/crit at 70%/90%)',
                  [('processes', 46, 105.0, 135.0, None, None)])]),
               ('TLDTST',
                {'levels': (70.0, 90.0)},
                [(0,
                  '122 of 500 processes are used (24%, warn/crit at 70%/90%)',
                  [('processes', 122, 350.0, 450.0, None, None)])])]}
