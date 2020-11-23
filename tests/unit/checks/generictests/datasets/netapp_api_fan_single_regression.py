#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# yapf: disable
# type: ignore



checkname = 'netapp_api_fan'


info = [['cooling-element-list 0',
         'cooling-element-number 1',
         'rpm 3000',
         'cooling-element-is-error false'],
        ['cooling-element-list 0',
         'cooling-element-number 2',
         'rpm 3000',
         'cooling-element-is-error true'],
        ['cooling-element-list 0',
         'cooling-element-number 3',
         'rpm 3000',
         'cooling-element-is-error false'],
        ['cooling-element-list 0',
         'cooling-element-number 4',
         'rpm 3020',
         'cooling-element-is-error false']]


discovery = {'': [('0/1', None), ('0/2', None), ('0/3', None), ('0/4', None)],
             'summary': []}


checks = {'': [('0/1', {}, [(0, 'Operational state OK', [])]),
               ('0/2', {}, [(2, 'Error in Fan 2', [])]),
               ('0/3', {}, [(0, 'Operational state OK', [])]),
               ('0/4', {}, [(0, 'Operational state OK', [])])]}


mock_host_conf_merged = {'': {'mode': 'single'}, 'summary': {'mode': 'single'}}
