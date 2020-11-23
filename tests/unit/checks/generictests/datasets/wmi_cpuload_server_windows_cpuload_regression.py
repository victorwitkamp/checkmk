#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# yapf: disable
# type: ignore

checkname = 'wmi_cpuload'

info = [['[system_perf]'],
        [
            'AlignmentFixupsPersec', 'Caption', 'ContextSwitchesPersec', 'Description',
            'ExceptionDispatchesPersec', 'FileControlBytesPersec', 'FileControlOperationsPersec',
            'FileDataOperationsPersec', 'FileReadBytesPersec', 'FileReadOperationsPersec',
            'FileWriteBytesPersec', 'FileWriteOperationsPersec', 'FloatingEmulationsPersec',
            'Frequency_Object', 'Frequency_PerfTime', 'Frequency_Sys100NS', 'Name',
            'PercentRegistryQuotaInUse', 'PercentRegistryQuotaInUse_Base', 'Processes',
            'ProcessorQueueLength', 'SystemCallsPersec', 'SystemUpTime', 'Threads',
            'Timestamp_Object', 'Timestamp_PerfTime', 'Timestamp_Sys100NS'
        ],
        [
            '0', '', '515871527', '', '80813', '1740164809', '35749693', '19282359',
            '71868764935', '17418626', '10976290970', '1863733', '0', '10000000', '1757890',
            '10000000', '', '50230448', '714429781', '59', '0', '-1438646331',
            '131087385121255994', '762', '131090689667831652', '580911371748',
            '131090761667830000'
        ]]

discovery = {'': []}
