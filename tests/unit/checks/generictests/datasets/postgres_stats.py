#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# yapf: disable
# type: ignore



checkname = 'postgres_stats'


mock_item_state = {
    '': 1547250000.0,
}


freeze_time = '2019-01-12 00:00:00'


info = [['[databases_start]'],
        ['postgres'],
        ['adwebconnect'],
        ['[databases_end]'],
        ['datname', 'sname', 'tname', 'vtime', 'atime'],
        ['postgres', 'pg_catalog', 'pg_statistic', '-1', '-1'],
        ['adwebconnect', 'public', 'serveraktion', '1488881726', '1488881726'],
        ['adwebconnect', 'pg_catalog', 'pg_statistic', '1488882719', '-1'],
        ['adwebconnect', 'public', 'auftrag', '1489001316', '1489001316'],
        ['adwebconnect', 'public', 'anrede', '-1', '-1'],
        ['adwebconnect', 'public', 'auftrag_mediadaten', '-1', '']]


discovery = {'': [('ANALYZE adwebconnect', {}),
                  ('ANALYZE postgres', {}),
                  ('VACUUM adwebconnect', {}),
                  ('VACUUM postgres', {})]}


checks = {
    '': [
        ('ANALYZE adwebconnect', {'never_analyze_vacuum': (1000, 1100)}, [
            (0, 'Table: serveraktion', []),
            (0, 'Time since last analyse: 676 d', []),
            (0, '2 tables were never analyzed: anrede/auftrag_mediadaten', []),
            (2, 'Unhandled tables for: 20 m (warn/crit at 16 m/18 m)', []),
        ]),
        ('ANALYZE adwebconnect', {'never_analyze_vacuum': (0, 1000 * 365 * 24 * 3600)}, [
            (0, 'Table: serveraktion', []),
            (0, 'Time since last analyse: 676 d', []),
            (0, '2 tables were never analyzed: anrede/auftrag_mediadaten', []),
            (1, 'Unhandled tables for: 20 m (warn/crit at 0.00 s/1000 y)', []),
        ]),
        ('ANALYZE adwebconnect', {'never_analyze_vacuum': None}, [
            (0, 'Table: serveraktion', []),
            (0, 'Time since last analyse: 676 d', []),
            (0, '2 tables were never analyzed: anrede/auftrag_mediadaten', []),
            (0, 'Unhandled tables for: 20 m', []),
        ]),
        ('ANALYZE postgres', {}, [
            (0, 'No never checked tables', []),
        ]),
        ('VACUUM adwebconnect', {}, [
            (0, 'Table: serveraktion', []),
            (0, 'Time since last vacuum: 676 d', []),
            (0, '2 tables were never vacuumed: anrede/auftrag_mediadaten', []),
            (0, 'Unhandled tables for: 20 m', []),
        ]),
        ('VACUUM postgres', {}, [
            (0, 'No never checked tables', []),
        ]),
]}
