#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# yapf: disable
# type: ignore



checkname = 'oracle_crs_res'


info = [['NAME=ora.ARCH.dg'],
        ['TYPE=ora.diskgroup.type'],
        ['STATE=ONLINE'],
        ['TARGET=ONLINE'],
        ['ENABLED=1'],
        ['NAME=ora.DATA.dg'],
        ['TYPE=ora.diskgroup.type'],
        ['STATE=ONLINE'],
        ['TARGET=ONLINE'],
        ['ENABLED=1']]


discovery = {'': [('ora.ARCH.dg', None), ('ora.DATA.dg', None)]}


checks = {'': [('ora.ARCH.dg', {}, [(0, 'online', [])]),
               ('ora.DATA.dg', {}, [(0, 'online', [])])]}
