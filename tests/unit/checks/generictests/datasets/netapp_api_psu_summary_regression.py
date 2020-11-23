#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# yapf: disable
# type: ignore



checkname = 'netapp_api_psu'


info = [['power-supply-list 0',
         'is-auto-power-reset-enabled false',
         'power-supply-part-no 114-00065+A2',
         'power-supply-serial-no XXT133880145',
         'power-supply-is-error false',
         'power-supply-firmware-revision 020F',
         'power-supply-type 9C',
         'power-supply-swap-count 0',
         'power-supply-element-number 1'],
        ['power-supply-list 0',
         'is-auto-power-reset-enabled false',
         'power-supply-part-no 114-00065+A2',
         'power-supply-serial-no XXT133880140',
         'power-supply-is-error true',
         'power-supply-firmware-revision 020F',
         'power-supply-type 9C',
         'power-supply-swap-count 0',
         'power-supply-element-number 2']]


discovery = {'': [], 'summary': [('Summary', {})]}


checks = {'summary': [('Summary',
                       {},
                       [(0, '2 power supply units in total', []),
                        (2, '1 power supply unit in error state (0/2)', [])])]}


mock_host_conf_merged = {'': {'mode': 'summary'}, 'summary': {'mode': 'summary'}}
