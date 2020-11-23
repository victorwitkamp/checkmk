#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# yapf: disable
# type: ignore

checkname = 'elasticsearch_indices'

info = [
    ['.monitoring-kibana-6', '971.0', '765236.0'],
    ['filebeat', '28298.0', '21524354.0'],
    ['.monitoring-es-6', '11986.0', '15581765.0']
]

discovery = {
    '': [
        ('.monitoring-es-6', {}), ('.monitoring-kibana-6', {}),
        ('filebeat', {})
    ]
}

checks = {
    '': [
        (
            '.monitoring-es-6', {}, [
                (
                    0, 'Total count: 11986 docs',
                    [('elasticsearch_count', 11986.0, None, None, None, None)]
                ),
                (
                    0, 'Average count: 0 docs per Minute', [
                        (
                            'elasticsearch_count_rate', 0.0, None, None, None,
                            None
                        )
                    ]
                ),
                (
                    0, 'Total size: 14.86 MB', [
                        (
                            'elasticsearch_size', 15581765.0, None, None, None,
                            None
                        )
                    ]
                ),
                (
                    0, 'Average size: 0.00 B  per Minute',
                    [('elasticsearch_size_rate', 0.0, None, None, None, None)]
                )
            ]
        ),
        (
            '.monitoring-kibana-6', {}, [
                (
                    0, 'Total count: 971 docs', [
                        ('elasticsearch_count', 971.0, None, None, None, None)
                    ]
                ),
                (
                    0, 'Average count: 0 docs per Minute', [
                        (
                            'elasticsearch_count_rate', 0.0, None, None, None,
                            None
                        )
                    ]
                ),
                (
                    0, 'Total size: 747.30 kB',
                    [('elasticsearch_size', 765236.0, None, None, None, None)]
                ),
                (
                    0, 'Average size: 0.00 B  per Minute',
                    [('elasticsearch_size_rate', 0.0, None, None, None, None)]
                )
            ]
        ),
        (
            'filebeat', {}, [
                (
                    0, 'Total count: 28298 docs',
                    [('elasticsearch_count', 28298.0, None, None, None, None)]
                ),
                (
                    0, 'Average count: 0 docs per Minute', [
                        (
                            'elasticsearch_count_rate', 0.0, None, None, None,
                            None
                        )
                    ]
                ),
                (
                    0, 'Total size: 20.53 MB', [
                        (
                            'elasticsearch_size', 21524354.0, None, None, None,
                            None
                        )
                    ]
                ),
                (
                    0, 'Average size: 0.00 B  per Minute',
                    [('elasticsearch_size_rate', 0.0, None, None, None, None)]
                )
            ]
        )
    ]
}
