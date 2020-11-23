#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# yapf: disable
# type: ignore

checkname = 'ucd_diskio'

freeze_time = '1970-01-01 00:00:01'

info = [
    ['1', 'sdk', '208537088', '1368398848', '3924134', '704587945'],
    ['2', 'dm-0', '2438861824', '1343166464', '4027162', '440261948'],
    ['3', 'dm-1', '85700608', '0', '20026', '0']
]

discovery = {'': [('dm-0', {}), ('dm-1', {}), ('sdk', {})]}

checks = {
    '': [
        (
            'dm-0', {}, [
                (0, '[2]', []),
                (
                    0, 'Read: 2.27 GB/s', [
                        (
                            'disk_read_throughput', 2438861824.0, None, None,
                            None, None
                        )
                    ]
                ),
                (
                    0, 'Write: 1.25 GB/s', [
                        (
                            'disk_write_throughput', 1343166464.0, None, None,
                            None, None
                        )
                    ]
                ),
                (
                    0, 'Read operations: 4027162.00 1/s', [
                        ('disk_read_ios', 4027162.0, None, None, None, None)
                    ]
                ),
                (
                    0, 'Write operations: 440261948.00 1/s',
                    [('disk_write_ios', 440261948.0, None, None, None, None)]
                )
            ]
        ),
        (
            'dm-1', {}, [
                (0, '[3]', []),
                (
                    0, 'Read: 81.73 MB/s', [
                        (
                            'disk_read_throughput', 85700608.0, None, None,
                            None, None
                        )
                    ]
                ),
                (
                    0, 'Write: 0.00 B/s', [
                        ('disk_write_throughput', 0.0, None, None, None, None)
                    ]
                ),
                (
                    0, 'Read operations: 20026.00 1/s', [
                        ('disk_read_ios', 20026.0, None, None, None, None)
                    ]
                ),
                (
                    0, 'Write operations: 0.00 1/s', [
                        ('disk_write_ios', 0.0, None, None, None, None)
                    ]
                )
            ]
        ),
        (
            'sdk', {'read': (50.0, 100.0), 'write': (1000.0, 5000.0)}, [
                (0, '[1]', []),
                (
                    2, 'Read: 198.88 MB/s (warn/crit at 50.00 MB/s/100.00 MB/s)', [
                        (
                            'disk_read_throughput', 208537089.0, 52428800.0, 104857600.0,
                            None, None
                        )
                    ]
                ),
                (
                    1, 'Write: 1.27 GB/s (warn/crit at 1000.00 MB/s/4.88 GB/s)', [
                        (
                            'disk_write_throughput', 1368398849.0, 1048576000.0, 5242880000.0,
                            None, None
                        )
                    ]
                ),
                (
                    0, 'Read operations: 3924134.00 1/s', [
                        ('disk_read_ios', 3924134.0, None, None, None, None)
                    ]
                ),
                (
                    0, 'Write operations: 704587945.00 1/s',
                    [('disk_write_ios', 704587945.0, None, None, None, None)]
                )
            ]
        )
    ]
}

mock_item_state = {'': (0, 0)}
