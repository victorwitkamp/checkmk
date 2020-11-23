#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

import collections
from testlib import Check  # type: ignore[import]
import pytest  # type: ignore[import]

pytestmark = pytest.mark.checks

UnitEntry = collections.namedtuple(
    "UnitEntry", ['name', 'type', 'load', 'active', 'sub', 'description', 'state'])


@pytest.mark.parametrize('services, blacklist, expected', [
    ([
        UnitEntry(name='gpu-manager',
                  type='service',
                  load='loaded',
                  active='inactive',
                  sub='dead',
                  description='Detect the available GPUs and deal with any system changes',
                  state='unknown'),
        UnitEntry(name='rsyslog',
                  type='service',
                  load='loaded',
                  active='active',
                  sub='running',
                  description='System Logging Service',
                  state='enabled'),
        UnitEntry(name='alsa-state',
                  type='service',
                  load='loaded',
                  active='inactive',
                  sub='dead',
                  description='Manage Sound Card State (restore and store)',
                  state='disabled'),
    ], [], {
        "included": [
            UnitEntry(name='gpu-manager',
                      type='service',
                      load='loaded',
                      active='inactive',
                      sub='dead',
                      description='Detect the available GPUs and deal with any system changes',
                      state='unknown'),
            UnitEntry(name='rsyslog',
                      type='service',
                      load='loaded',
                      active='active',
                      sub='running',
                      description='System Logging Service',
                      state='enabled')
        ],
        "excluded": [],
        "disabled": [
            UnitEntry(name='alsa-state',
                      type='service',
                      load='loaded',
                      active='inactive',
                      sub='dead',
                      description='Manage Sound Card State (restore and store)',
                      state='disabled')
        ],
        "static": [],
        "activating": [],
        "reloading": [],
    }),
    (
        [
            UnitEntry(name='gpu-manager',
                      type='service',
                      load='loaded',
                      active='inactive',
                      sub='dead',
                      description='Detect the available GPUs and deal with any system changes',
                      state='unknown'),
            UnitEntry(name='rsyslog',
                      type='service',
                      load='loaded',
                      active='active',
                      sub='running',
                      description='System Logging Service',
                      state='enabled'),
            UnitEntry(name='alsa-state',
                      type='service',
                      load='loaded',
                      active='inactive',
                      sub='dead',
                      description='Manage Sound Card State (restore and store)',
                      state='indirect')
        ],
        ['gpu'],
        {
            "included": [
                UnitEntry(name='rsyslog',
                          type='service',
                          load='loaded',
                          active='active',
                          sub='running',
                          description='System Logging Service',
                          state='enabled'),
            ],
            "excluded": [
                UnitEntry(name='gpu-manager',
                          type='service',
                          load='loaded',
                          active='inactive',
                          sub='dead',
                          description='Detect the available GPUs and deal with any system changes',
                          state='unknown'),
            ],
            "disabled": [
                UnitEntry(name='alsa-state',
                          type='service',
                          load='loaded',
                          active='inactive',
                          sub='dead',
                          description='Manage Sound Card State (restore and store)',
                          state='indirect')
            ],
            "static": [],
            "activating": [],
            "reloading": [],
        },
    ),
])
@pytest.mark.usefixtures("config_load_all_checks")
def test_services_split(services, blacklist, expected):
    check = Check('systemd_units')
    services_split = check.context['_services_split']
    actual = services_split(services, blacklist)
    assert actual == expected
