#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# yapf: disable
# type: ignore


checkname = 'timesyncd'

info = [['Server:', '(null)', '(ntp.ubuntu.com)'],
        [
            'Poll', 'interval:', '0', '(min:', '32s;', 'max', '34min',
            '8s)'
        ], ['Packet', 'count:', '0'], ['[[[1569922392.37]]]']]

discovery = {'': [(None, {})]}

checks = {
    '': [(None, {
        'alert_delay': (300, 3600),
        'last_synchronized': (3600, 7200),
        'quality_levels': (200, 500),
        'stratum_level': 9
    }, [
        (0, 'Time since last sync: N/A (started monitoring)', []),
        (0, 'Found no time server', []),
    ])]
}
