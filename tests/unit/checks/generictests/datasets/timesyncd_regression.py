#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# yapf: disable
# type: ignore


checkname = 'timesyncd'

freeze_time = '2019-10-02 07:34:59'

info = [['Server:', '91.189.91.157', '(ntp.ubuntu.com)'],
        [
            'Poll', 'interval:', '32s', '(min:', '32s;', 'max', '34min',
            '8s)'
        ], ['Leap:', 'normal'], ['Version:', '4'], ['Stratum:', '2'],
        ['Reference:', 'C0248F97'], ['Precision:', '1us', '(-24)'],
        ['Root', 'distance:', '87.096ms', '(max:', '5s)'],
        ['Offset:', '-53.991ms'], ['Delay:', '208.839ms'],
        ['Jitter:', '0'], ['Packet', 'count:', '1'],
        ['Frequency:', '-500,000ppm'], ['[[[1569922392.37]]]']]

discovery = {'': [(None, {})]}

checks = {
    '': [
        (None, {
            'alert_delay': (300, 3600),
            'last_synchronized': (3600, 7200),
            'quality_levels': (200.0, 500.0),
            'stratum_level': 10
         }, [
             (0, 'Offset: 54 microseconds', [('time_offset', 5.3991e-05, 0.2, 0.5)]),
             (2, ('Time since last sync: 22 hours 1 minute '
                 '(warn/crit at 1 hour 0 minutes/2 hours 0 minutes)'), []),
             (0, 'Stratum: 2.00', []),
             (0, 'Jitter: 0.00 s', [('jitter', 0.0, 0.2, 0.5)]),
             (0, 'synchronized on 91.189.91.157', []),
        ]),
    ],
}


# this should be set by the check itself, but that won't work in tests.
mock_item_state = {'': {'time_server': 1569922392.37}}
