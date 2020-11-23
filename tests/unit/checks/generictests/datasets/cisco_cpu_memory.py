#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# yapf: disable
# type: ignore

checkname = 'cisco_cpu_memory'

info = [
    [['11000', '3343553', '565879', '284872']],
    [
        ['1', 'Virtual Stack'],
        ['25', 'Switch1 Container of Power Supply Bay'],
        ['11000', 'Switch2 Supervisor 1 (virtual slot 11)']
    ]
]

discovery = {'': [('Switch2 Supervisor 1 (virtual slot 11)', {})]}

checks = {
    '': [
        (
            'Switch2 Supervisor 1 (virtual slot 11)', {}, [
                (
                    0, 'Usage: 92.81% - 3.46 GB of 3.73 GB',
                    [('mem_used_percent', 92.81207602536634, None, None, 0.0, None)]
                )
            ]
        ),
        (
            'Switch2 Supervisor 1 (virtual slot 11)', {
                'levels': (-2000, -1000)
            }, [
                (
                    2,
                    'Usage: 92.81% - 3.46 GB of 3.73 GB (warn/crit below 1.95 GiB/1000 MiB free)',
                    [
                        (
                            'mem_used_percent', 92.81207602536634, 47.61387331970475,
                            73.80693665985237, 0.0, None
                        )
                    ]
                )
            ]
        ),
        (
            'Switch2 Supervisor 1 (virtual slot 11)', {
                'levels': (50.0, 90.0)
            }, [
                (
                    2,
                    'Usage: 92.81% - 3.46 GB of 3.73 GB (warn/crit at 50.0%/90.0% used)',
                    [('mem_used_percent', 92.81207602536634, 50.0, 90.0, 0.0, None)]
                )
            ]
        ),
        (
            'Switch2 Supervisor 1 (virtual slot 11)', {
                'levels': (-20.0, -10.0)
            }, [
                (
                    2,
                    'Usage: 92.81% - 3.46 GB of 3.73 GB (warn/crit below 20.0%/10.0% free)',
                    [('mem_used_percent', 92.81207602536634, 80.0, 89.99999999999999, 0.0, None)]
                )
            ]
        )
    ]
}
