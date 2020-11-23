#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# yapf: disable
# type: ignore



checkname = 'solaris_services'


info = [['STATE', 'STIME', 'FMRI'],
        ['online', 'Jan_1', 'svc1:/cat1/name1:inst1'],
        ['online', 'Jan_1', '0:00:00', 'svc2:/cat2/name2:inst2']]


discovery = {'': [], 'summary': [(None, {})]}


checks = {'summary': [(None, {}, [(0, '2 services', []), (0, '2 online', [])])]}
