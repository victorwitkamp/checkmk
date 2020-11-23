#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# yapf: disable
# type: ignore

checkname = 'wmi_cpuload'

info = [
    ['[system_perf]'],
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
        '0', '', '-69479562', '', '14178685', '804099358366', '-783070306', '1533491993',
        '154737860718293', '422989950', '3094169943814', '1110502043', '0', '10000000',
        '2734511', '10000000', '', '152069756', '2147483647', '132', '0', '-655373265',
        '131051948225967966', '2964', '131096941722079880', '12303331974804',
        '131097013722070000'
    ], ['[computer_system]'],
    [
        'AdminPasswordStatus', 'AutomaticManagedPagefile', 'AutomaticResetBootOption',
        'AutomaticResetCapability', 'BootOptionOnLimit', 'BootOptionOnWatchDog',
        'BootROMSupported', 'BootupState', 'Caption', 'ChassisBootupState',
        'CreationClassName', 'CurrentTimeZone', 'DaylightInEffect', 'Description',
        'DNSHostName', 'Domain', 'DomainRole', 'EnableDaylightSavingsTime',
        'FrontPanelResetStatus', 'InfraredSupported', 'InitialLoadInfo', 'InstallDate',
        'KeyboardPasswordStatus', 'LastLoadInfo', 'Manufacturer', 'Model', 'Name',
        'NameFormat', 'NetworkServerModeEnabled', 'NumberOfLogicalProcessors',
        'NumberOfProcessors', 'OEMLogoBitmap', 'OEMStringArray', 'PartOfDomain',
        'PauseAfterReset', 'PCSystemType', 'PowerManagementCapabilities',
        'PowerManagementSupported', 'PowerOnPasswordStatus', 'PowerState', 'PowerSupplyState',
        'PrimaryOwnerContact', 'PrimaryOwnerName', 'ResetCapability', 'ResetCount',
        'ResetLimit', 'Roles', 'Status', 'SupportContactDescription', 'SystemStartupDelay',
        'SystemStartupOptions', 'SystemStartupSetting', 'SystemType', 'ThermalState',
        'TotalPhysicalMemory', 'UserName', 'WakeUpType', 'Workgroup'
    ],
    [
        '3', '0', '1', '1', '', '', '1', 'Normal boot', 'ROZRHPDB09', '3',
        'Win32_ComputerSystem', '120', '1', 'AT/AT COMPATIBLE', 'ROZRHPDB09',
        'testch.testint.net', '3', '1', '3', '0', '', '', '3', '', 'HP',
        'ProLiant DL380 G6', 'ROZRHPDB09', '', '1', '16', '2', '', '<array>', '1', '-1',
        '0', '', '', '3', '0', '3', '', 'test International', '1', '-1', '-1',
        '<array>', 'OK', '', '', '', '', 'x64-based PC', '3', '77298651136', '', '6', ''
    ]
]

discovery = {'': [(None, None)]}

checks = {
    '': [(
        None,
        {},
        [(
            0,
            "15 min load: 0.00 at 16 logical cores (0.00 per core)",
            [('load1', 0, None, None, 0, 16), ('load5', 0, None, None, 0, 16),
             ('load15', 0, None, None, 0, 16)],
        )],
    ),],
}
