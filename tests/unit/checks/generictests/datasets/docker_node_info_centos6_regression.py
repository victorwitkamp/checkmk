#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# yapf: disable
# type: ignore

from cmk.base.plugins.agent_based.docker_node_info import parse_docker_node_info


DEPRECATION_WARNING = (1, (
    "Deprecated plugin/agent (see long output)(!)\nYou are using legacy code, which may lead to "
    "crashes and/or incomplete information. Please upgrade the monitored host to use the plugin "
    "'mk_docker.py'."
), [])

checkname = 'docker_node_info'

parsed = parse_docker_node_info([
    ['|Containers', ' 42'],
    ['|Images', ' 23'],
    ['|Storage Driver', ' devicemapper'],
    ['| Pool Name', ' docker-9', '232-23232323-pool'],
    ['| Pool Blocksize', ' 23.23 kB'],
    ['| Backing Filesystem', ' extfs'],
    ['| Data file', ' /dev/loop23'],
    ['| Metadata file', ' /dev/loop24'],
    ['| Data Space Used', ' 42.42 GB'],
    ['| Data Space Total', ' 142.42 GB'],
    ['| Data Space Available', ' 42.42 GB'],
    ['| Metadata Space Used', ' 42.42 MB'],
    ['| Metadata Space Total', ' 23.23 GB'],
    ['| Metadata Space Available', ' 3.141 GB'],
    ['| Udev Sync Supported', ' true'],
    ['| Deferred Removal Enabled', ' false'],
    ['| Data loop file', ' /data/docker/devicemapper/devicemapper/data'],
    ['| Metadata loop file', ' /data/docker/devicemapper/devicemapper/metadata'],
    ['| Library Version', ' 1.02.117-Koechelverzeichnis/ (2024-12-12)'],
    ['|Execution Driver', ' killmenow-0.23'],
    ['|Logging Driver', ' json-file'],
    ['|Kernel Version', ' 3.14.15-926.5.3.el5.x86_64'],
    ['|Operating System', ' <unknown>'],
    ['|CPUs', ' 1024'],
    ['|Total Memory', ' -23 GiB'],
    ['|Name', ' voms01'],
    [
        '|ID', ' XXXX', 'XXXX', 'XXXX', 'XXXX', 'XXXX', 'XXXX', 'BLOB', 'BOBO', '0COV',
        'FEFE', 'WHOO', '0TEH'
    ],
])

discovery = {
    '': [(None, {})],
    'containers': [(None, {})],
}

checks = {
    '': [
        (None, {}, [
            (0, 'Daemon running on host voms01', []),
            DEPRECATION_WARNING,
        ]),
    ],
    'containers': [
        (None, {}, [
            (0, 'Containers: 42', [('containers', 42, None, None, None, None)]),
            (3, 'Running: count not present in agent output', []),
            (3, 'Paused: count not present in agent output', []),
            (3, 'Stopped: count not present in agent output', []),
            DEPRECATION_WARNING,
        ]),
    ],
}
