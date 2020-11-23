#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# yapf: disable
# type: ignore



checkname = 'mssql_instance'


info = [['MSSQL_MSSQLSERVER', 'config', '10.50.6000.34', 'Standard Edition', ''],
        ['MSSQL_ABC', 'config', '10.50.6000.34', 'Standard Edition', ''],
        ['MSSQL_ABCDEV', 'config', '10.50.6000.34', 'Standard Edition', ''],
        ['MSSQL_MSSQLSERVER', 'state', '1', ''],
        ['MSSQL_ABC', 'state', '1', ''],
        ['MSSQL_ABCDEV',
         'state',
         '0',
         '[DBNETLIB][ConnectionOpen (Connect()).]SQL Server existiert nicht oder Zugriff verweigert.'],
        ['Hier kommt eine laaaangre Fehlermeldung'],
        ['die sich ueber                mehrere             Zeilen ersteckt']]


discovery = {'': [('ABC', {}), ('ABCDEV', {}), ('MSSQLSERVER', {})]}


checks = {'': [('ABC', {}, [(0, 'Version: 10.50.6000.34 - Standard Edition', [])]),
               ('ABCDEV',
                {},
                [(2,
                  'Failed to connect to database ([DBNETLIB][ConnectionOpen (Connect()).]SQL Server existiert nicht oder Zugriff verweigert.)',
                  []),
                 (0, 'Version: 10.50.6000.34 - Standard Edition', [])]),
               ('MSSQLSERVER',
                {},
                [(0, 'Version: 10.50.6000.34 - Standard Edition', [])])]}
