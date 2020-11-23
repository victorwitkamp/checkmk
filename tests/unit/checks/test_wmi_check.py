#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

import pytest  # type: ignore[import]
from testlib import Check  # type: ignore[import]

from checktestlib import (
    DiscoveryResult,
    CheckResult,
    assertDiscoveryResultsEqual,
)

from cmk.base.check_api import MKCounterWrapped

pytestmark = pytest.mark.checks

#   .--infos---------------------------------------------------------------.
#   |                        _        __                                   |
#   |                       (_)_ __  / _| ___  ___                         |
#   |                       | | '_ \| |_ / _ \/ __|                        |
#   |                       | | | | |  _| (_) \__ \                        |
#   |                       |_|_| |_|_|  \___/|___/                        |
#   |                                                                      |
#   '----------------------------------------------------------------------'

info_wmi_timeout = [['WMItimeout']]

info_subsection_wmi_timeout = [
    ['[system_perf]'],
    ['WMItimeout'],
    ['[computer_system]'],
    ['name', 'unimportant', 'data'],
]

info_wmi_cpuload_1 = [
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
        '0', '', '469922985', '', '222849', '6503221217', '72494625', '75272330',
        '111617810637', '68676492', '34750951332', '6595838', '0', '10000000', '2156247',
        '10000000', '', '250803278', '-1', '384', '0', '2144858950', '131983188065000000',
        '5534', '131983336220258827', '31947393930', '131983372220250000'
    ], ['[computer_system]'],
    [
        'AdminPasswordStatus', 'AutomaticManagedPagefile', 'AutomaticResetBootOption',
        'AutomaticResetCapability', 'BootOptionOnLimit', 'BootOptionOnWatchDog',
        'BootROMSupported', 'BootStatus', 'BootupState', 'Caption', 'ChassisBootupState',
        'ChassisSKUNumber', 'CreationClassName', 'CurrentTimeZone', 'DaylightInEffect',
        'Description', 'DNSHostName', 'Domain', 'DomainRole', 'EnableDaylightSavingsTime',
        'FrontPanelResetStatus', 'HypervisorPresent', 'InfraredSupported', 'InitialLoadInfo',
        'InstallDate', 'KeyboardPasswordStatus', 'LastLoadInfo', 'Manufacturer', 'Model',
        'Name', 'NameFormat', 'NetworkServerModeEnabled', 'NumberOfLogicalProcessors',
        'NumberOfProcessors', 'OEMLogoBitmap', 'OEMStringArray', 'PartOfDomain',
        'PauseAfterReset', 'PCSystemType', 'PCSystemTypeEx', 'PowerManagementCapabilities',
        'PowerManagementSupported', 'PowerOnPasswordStatus', 'PowerState', 'PowerSupplyState',
        'PrimaryOwnerContact', 'PrimaryOwnerName', 'ResetCapability', 'ResetCount',
        'ResetLimit', 'Roles', 'Status', 'SupportContactDescription', 'SystemFamily',
        'SystemSKUNumber', 'SystemStartupDelay', 'SystemStartupOptions', 'SystemStartupSetting',
        'SystemType', 'ThermalState', 'TotalPhysicalMemory', 'UserName', 'WakeUpType',
        'Workgroup'
    ],
    [
        '3', '1', '1', '1', '', '', '1', '<array>', 'Normal boot', 'SERG-DELL', '3',
        'Notebook', 'Win32_ComputerSystem', '60', '0', 'AT/AT COMPATIBLE', 'SERG-DELL',
        'WORKGROUP', '0', '1', '3', '0', '0', '', '', '3', '', 'Dell Inc.',
        'XPS 15 9570', 'SERG-DELL', '', '1', '12', '1', '', '<array>', '0', '-1', '2',
        '2', '', '', '3', '0', '3', '', 'sk', '1', '-1', '-1', '<array>', 'OK', '',
        'XPS', '087C', '', '', '', 'x64-based PC', '3', '34077048832', 'SERG-DELL\\sk',
        '6', 'WORKGROUP'
    ]
]

info_wmi_cpuload_2 = [
    ['[system_perf]'], ['WMItimeout'], ['[computer_system]'],
    [
        'AdminPasswordStatus', 'AutomaticManagedPagefile', 'AutomaticResetBootOption',
        'AutomaticResetCapability', 'BootOptionOnLimit', 'BootOptionOnWatchDog',
        'BootROMSupported', 'BootStatus', 'BootupState', 'Caption', 'ChassisBootupState',
        'ChassisSKUNumber', 'CreationClassName', 'CurrentTimeZone', 'DaylightInEffect',
        'Description', 'DNSHostName', 'Domain', 'DomainRole', 'EnableDaylightSavingsTime',
        'FrontPanelResetStatus', 'HypervisorPresent', 'InfraredSupported', 'InitialLoadInfo',
        'InstallDate', 'KeyboardPasswordStatus', 'LastLoadInfo', 'Manufacturer', 'Model',
        'Name', 'NameFormat', 'NetworkServerModeEnabled', 'NumberOfLogicalProcessors',
        'NumberOfProcessors', 'OEMLogoBitmap', 'OEMStringArray', 'PartOfDomain',
        'PauseAfterReset', 'PCSystemType', 'PCSystemTypeEx', 'PowerManagementCapabilities',
        'PowerManagementSupported', 'PowerOnPasswordStatus', 'PowerState', 'PowerSupplyState',
        'PrimaryOwnerContact', 'PrimaryOwnerName', 'ResetCapability', 'ResetCount',
        'ResetLimit', 'Roles', 'Status', 'SupportContactDescription', 'SystemFamily',
        'SystemSKUNumber', 'SystemStartupDelay', 'SystemStartupOptions', 'SystemStartupSetting',
        'SystemType', 'ThermalState', 'TotalPhysicalMemory', 'UserName', 'WakeUpType',
        'Workgroup'
    ],
    [
        '3', '1', '1', '1', '', '', '1', '<array>', 'Normal boot', 'SERG-DELL', '3',
        'Notebook', 'Win32_ComputerSystem', '60', '0', 'AT/AT COMPATIBLE', 'SERG-DELL',
        'WORKGROUP', '0', '1', '3', '0', '0', '', '', '3', '', 'Dell Inc.',
        'XPS 15 9570', 'SERG-DELL', '', '1', '12', '1', '', '<array>', '0', '-1', '2',
        '2', '', '', '3', '0', '3', '', 'sk', '1', '-1', '-1', '<array>', 'OK', '',
        'XPS', '087C', '', '', '', 'x64-based PC', '3', '34077048832', 'SERG-DELL\\sk',
        '6', 'WORKGROUP'
    ]
]

info_wmi_cpuload_3 = [
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
        '0', '', '469922985', '', '222849', '6503221217', '72494625', '75272330',
        '111617810637', '68676492', '34750951332', '6595838', '0', '10000000', '2156247',
        '10000000', '', '250803278', '-1', '384', '0', '2144858950', '131983188065000000',
        '5534', '131983336220258827', '31947393930', '131983372220250000'
    ], ['[computer_system]'], ['WMItimeout']
]

info_wmi_cpuload_4 = [['[system_perf]'], ['WMItimeout'], ['[computer_system]'], ['WMItimeout']]

info_wmi_cpuload_5 = [
    ['[system_perf]'],
    [
        'AlignmentFixupsPersec', 'Caption', 'ContextSwitchesPersec', 'Description',
        'ExceptionDispatchesPersec', 'FileControlBytesPersec', 'FileControlOperationsPersec',
        'FileDataOperationsPersec', 'FileReadBytesPersec', 'FileReadOperationsPersec',
        'FileWriteBytesPersec', 'FileWriteOperationsPersec', 'FloatingEmulationsPersec',
        'Frequency_Object', 'Frequency_PerfTime', 'Frequency_Sys100NS', 'Name',
        'PercentRegistryQuotaInUse', 'PercentRegistryQuotaInUse_Base', 'Processes',
        'ProcessorQueueLength', 'SystemCallsPersec', 'SystemUpTime', 'Threads',
        'Timestamp_Object', 'Timestamp_PerfTime', 'Timestamp_Sys100NS', 'WMIStatus'
    ],
    [
        '0', '', '469922985', '', '222849', '6503221217', '72494625', '75272330',
        '111617810637', '68676492', '34750951332', '6595838', '0', '10000000', '2156247',
        '10000000', '', '250803278', '-1', '384', '0', '2144858950', '131983188065000000',
        '5534', '131983336220258827', '31947393930', '131983372220250000', 'OK'
    ], ['[computer_system]'],
    [
        'AdminPasswordStatus', 'AutomaticManagedPagefile', 'AutomaticResetBootOption',
        'AutomaticResetCapability', 'BootOptionOnLimit', 'BootOptionOnWatchDog',
        'BootROMSupported', 'BootStatus', 'BootupState', 'Caption', 'ChassisBootupState',
        'ChassisSKUNumber', 'CreationClassName', 'CurrentTimeZone', 'DaylightInEffect',
        'Description', 'DNSHostName', 'Domain', 'DomainRole', 'EnableDaylightSavingsTime',
        'FrontPanelResetStatus', 'HypervisorPresent', 'InfraredSupported', 'InitialLoadInfo',
        'InstallDate', 'KeyboardPasswordStatus', 'LastLoadInfo', 'Manufacturer', 'Model',
        'Name', 'NameFormat', 'NetworkServerModeEnabled', 'NumberOfLogicalProcessors',
        'NumberOfProcessors', 'OEMLogoBitmap', 'OEMStringArray', 'PartOfDomain',
        'PauseAfterReset', 'PCSystemType', 'PCSystemTypeEx', 'PowerManagementCapabilities',
        'PowerManagementSupported', 'PowerOnPasswordStatus', 'PowerState', 'PowerSupplyState',
        'PrimaryOwnerContact', 'PrimaryOwnerName', 'ResetCapability', 'ResetCount',
        'ResetLimit', 'Roles', 'Status', 'SupportContactDescription', 'SystemFamily',
        'SystemSKUNumber', 'SystemStartupDelay', 'SystemStartupOptions', 'SystemStartupSetting',
        'SystemType', 'ThermalState', 'TotalPhysicalMemory', 'UserName', 'WakeUpType',
        'Workgroup', 'WMIStatus'
    ],
    [
        '3', '1', '1', '1', '', '', '1', '<array>', 'Normal boot', 'SERG-DELL', '3',
        'Notebook', 'Win32_ComputerSystem', '60', '0', 'AT/AT COMPATIBLE', 'SERG-DELL',
        'WORKGROUP', '0', '1', '3', '0', '0', '', '', '3', '', 'Dell Inc.',
        'XPS 15 9570', 'SERG-DELL', '', '1', '12', '1', '', '<array>', '0', '-1', '2',
        '2', '', '', '3', '0', '3', '', 'sk', '1', '-1', '-1', '<array>', 'OK', '',
        'XPS', '087C', '', '', '', 'x64-based PC', '3', '34077048832', 'SERG-DELL\\sk',
        '6', 'WORKGROUP', 'OK'
    ]
]

info_wmi_cpuload_6 = [
    ['[system_perf]'],
    [
        'AlignmentFixupsPersec', 'Caption', 'ContextSwitchesPersec', 'Description',
        'ExceptionDispatchesPersec', 'FileControlBytesPersec', 'FileControlOperationsPersec',
        'FileDataOperationsPersec', 'FileReadBytesPersec', 'FileReadOperationsPersec',
        'FileWriteBytesPersec', 'FileWriteOperationsPersec', 'FloatingEmulationsPersec',
        'Frequency_Object', 'Frequency_PerfTime', 'Frequency_Sys100NS', 'Name',
        'PercentRegistryQuotaInUse', 'PercentRegistryQuotaInUse_Base', 'Processes',
        'ProcessorQueueLength', 'SystemCallsPersec', 'SystemUpTime', 'Threads',
        'Timestamp_Object', 'Timestamp_PerfTime', 'Timestamp_Sys100NS', 'WMIStatus'
    ],
    [
        '0', '', '469922985', '', '222849', '6503221217', '72494625', '75272330',
        '111617810637', '68676492', '34750951332', '6595838', '0', '10000000', '2156247',
        '10000000', '', '250803278', '-1', '384', '0', '2144858950', '131983188065000000',
        '5534', '131983336220258827', '31947393930', '131983372220250000', 'Timeout'
    ], ['[computer_system]'],
    [
        'AdminPasswordStatus', 'AutomaticManagedPagefile', 'AutomaticResetBootOption',
        'AutomaticResetCapability', 'BootOptionOnLimit', 'BootOptionOnWatchDog',
        'BootROMSupported', 'BootStatus', 'BootupState', 'Caption', 'ChassisBootupState',
        'ChassisSKUNumber', 'CreationClassName', 'CurrentTimeZone', 'DaylightInEffect',
        'Description', 'DNSHostName', 'Domain', 'DomainRole', 'EnableDaylightSavingsTime',
        'FrontPanelResetStatus', 'HypervisorPresent', 'InfraredSupported', 'InitialLoadInfo',
        'InstallDate', 'KeyboardPasswordStatus', 'LastLoadInfo', 'Manufacturer', 'Model',
        'Name', 'NameFormat', 'NetworkServerModeEnabled', 'NumberOfLogicalProcessors',
        'NumberOfProcessors', 'OEMLogoBitmap', 'OEMStringArray', 'PartOfDomain',
        'PauseAfterReset', 'PCSystemType', 'PCSystemTypeEx', 'PowerManagementCapabilities',
        'PowerManagementSupported', 'PowerOnPasswordStatus', 'PowerState', 'PowerSupplyState',
        'PrimaryOwnerContact', 'PrimaryOwnerName', 'ResetCapability', 'ResetCount',
        'ResetLimit', 'Roles', 'Status', 'SupportContactDescription', 'SystemFamily',
        'SystemSKUNumber', 'SystemStartupDelay', 'SystemStartupOptions', 'SystemStartupSetting',
        'SystemType', 'ThermalState', 'TotalPhysicalMemory', 'UserName', 'WakeUpType',
        'Workgroup', 'WMIStatus'
    ],
    [
        '3', '1', '1', '1', '', '', '1', '<array>', 'Normal boot', 'SERG-DELL', '3',
        'Notebook', 'Win32_ComputerSystem', '60', '0', 'AT/AT COMPATIBLE', 'SERG-DELL',
        'WORKGROUP', '0', '1', '3', '0', '0', '', '', '3', '', 'Dell Inc.',
        'XPS 15 9570', 'SERG-DELL', '', '1', '12', '1', '', '<array>', '0', '-1', '2',
        '2', '', '', '3', '0', '3', '', 'sk', '1', '-1', '-1', '<array>', 'OK', '',
        'XPS', '087C', '', '', '', 'x64-based PC', '3', '34077048832', 'SERG-DELL\\sk',
        '6', 'WORKGROUP', 'OK'
    ]
]

info_wmi_cpuload_7 = [
    ['[system_perf]'],
    [
        'AlignmentFixupsPersec', 'Caption', 'ContextSwitchesPersec', 'Description',
        'ExceptionDispatchesPersec', 'FileControlBytesPersec', 'FileControlOperationsPersec',
        'FileDataOperationsPersec', 'FileReadBytesPersec', 'FileReadOperationsPersec',
        'FileWriteBytesPersec', 'FileWriteOperationsPersec', 'FloatingEmulationsPersec',
        'Frequency_Object', 'Frequency_PerfTime', 'Frequency_Sys100NS', 'Name',
        'PercentRegistryQuotaInUse', 'PercentRegistryQuotaInUse_Base', 'Processes',
        'ProcessorQueueLength', 'SystemCallsPersec', 'SystemUpTime', 'Threads',
        'Timestamp_Object', 'Timestamp_PerfTime', 'Timestamp_Sys100NS', 'WMIStatus'
    ],
    [
        '0', '', '469922985', '', '222849', '6503221217', '72494625', '75272330',
        '111617810637', '68676492', '34750951332', '6595838', '0', '10000000', '2156247',
        '10000000', '', '250803278', '-1', '384', '0', '2144858950', '131983188065000000',
        '5534', '131983336220258827', '31947393930', '131983372220250000', 'OK'
    ], ['[computer_system]'],
    [
        'AdminPasswordStatus', 'AutomaticManagedPagefile', 'AutomaticResetBootOption',
        'AutomaticResetCapability', 'BootOptionOnLimit', 'BootOptionOnWatchDog',
        'BootROMSupported', 'BootStatus', 'BootupState', 'Caption', 'ChassisBootupState',
        'ChassisSKUNumber', 'CreationClassName', 'CurrentTimeZone', 'DaylightInEffect',
        'Description', 'DNSHostName', 'Domain', 'DomainRole', 'EnableDaylightSavingsTime',
        'FrontPanelResetStatus', 'HypervisorPresent', 'InfraredSupported', 'InitialLoadInfo',
        'InstallDate', 'KeyboardPasswordStatus', 'LastLoadInfo', 'Manufacturer', 'Model',
        'Name', 'NameFormat', 'NetworkServerModeEnabled', 'NumberOfLogicalProcessors',
        'NumberOfProcessors', 'OEMLogoBitmap', 'OEMStringArray', 'PartOfDomain',
        'PauseAfterReset', 'PCSystemType', 'PCSystemTypeEx', 'PowerManagementCapabilities',
        'PowerManagementSupported', 'PowerOnPasswordStatus', 'PowerState', 'PowerSupplyState',
        'PrimaryOwnerContact', 'PrimaryOwnerName', 'ResetCapability', 'ResetCount',
        'ResetLimit', 'Roles', 'Status', 'SupportContactDescription', 'SystemFamily',
        'SystemSKUNumber', 'SystemStartupDelay', 'SystemStartupOptions', 'SystemStartupSetting',
        'SystemType', 'ThermalState', 'TotalPhysicalMemory', 'UserName', 'WakeUpType',
        'Workgroup', 'WMIStatus'
    ],
    [
        '3', '1', '1', '1', '', '', '1', '<array>', 'Normal boot', 'SERG-DELL', '3',
        'Notebook', 'Win32_ComputerSystem', '60', '0', 'AT/AT COMPATIBLE', 'SERG-DELL',
        'WORKGROUP', '0', '1', '3', '0', '0', '', '', '3', '', 'Dell Inc.',
        'XPS 15 9570', 'SERG-DELL', '', '1', '12', '1', '', '<array>', '0', '-1', '2',
        '2', '', '', '3', '0', '3', '', 'sk', '1', '-1', '-1', '<array>', 'OK', '',
        'XPS', '087C', '', '', '', 'x64-based PC', '3', '34077048832', 'SERG-DELL\\sk',
        '6', 'WORKGROUP', 'Timeout'
    ]
]

info_wmi_cpuload_8 = [
    ['[system_perf]'],
    [
        'AlignmentFixupsPersec', 'Caption', 'ContextSwitchesPersec', 'Description',
        'ExceptionDispatchesPersec', 'FileControlBytesPersec', 'FileControlOperationsPersec',
        'FileDataOperationsPersec', 'FileReadBytesPersec', 'FileReadOperationsPersec',
        'FileWriteBytesPersec', 'FileWriteOperationsPersec', 'FloatingEmulationsPersec',
        'Frequency_Object', 'Frequency_PerfTime', 'Frequency_Sys100NS', 'Name',
        'PercentRegistryQuotaInUse', 'PercentRegistryQuotaInUse_Base', 'Processes',
        'ProcessorQueueLength', 'SystemCallsPersec', 'SystemUpTime', 'Threads',
        'Timestamp_Object', 'Timestamp_PerfTime', 'Timestamp_Sys100NS', 'WMIStatus'
    ],
    [
        '0', '', '469922985', '', '222849', '6503221217', '72494625', '75272330',
        '111617810637', '68676492', '34750951332', '6595838', '0', '10000000', '2156247',
        '10000000', '', '250803278', '-1', '384', '0', '2144858950', '131983188065000000',
        '5534', '131983336220258827', '31947393930', '131983372220250000', 'Timeout'
    ], ['[computer_system]'],
    [
        'AdminPasswordStatus', 'AutomaticManagedPagefile', 'AutomaticResetBootOption',
        'AutomaticResetCapability', 'BootOptionOnLimit', 'BootOptionOnWatchDog',
        'BootROMSupported', 'BootStatus', 'BootupState', 'Caption', 'ChassisBootupState',
        'ChassisSKUNumber', 'CreationClassName', 'CurrentTimeZone', 'DaylightInEffect',
        'Description', 'DNSHostName', 'Domain', 'DomainRole', 'EnableDaylightSavingsTime',
        'FrontPanelResetStatus', 'HypervisorPresent', 'InfraredSupported', 'InitialLoadInfo',
        'InstallDate', 'KeyboardPasswordStatus', 'LastLoadInfo', 'Manufacturer', 'Model',
        'Name', 'NameFormat', 'NetworkServerModeEnabled', 'NumberOfLogicalProcessors',
        'NumberOfProcessors', 'OEMLogoBitmap', 'OEMStringArray', 'PartOfDomain',
        'PauseAfterReset', 'PCSystemType', 'PCSystemTypeEx', 'PowerManagementCapabilities',
        'PowerManagementSupported', 'PowerOnPasswordStatus', 'PowerState', 'PowerSupplyState',
        'PrimaryOwnerContact', 'PrimaryOwnerName', 'ResetCapability', 'ResetCount',
        'ResetLimit', 'Roles', 'Status', 'SupportContactDescription', 'SystemFamily',
        'SystemSKUNumber', 'SystemStartupDelay', 'SystemStartupOptions', 'SystemStartupSetting',
        'SystemType', 'ThermalState', 'TotalPhysicalMemory', 'UserName', 'WakeUpType',
        'Workgroup', 'WMIStatus'
    ],
    [
        '3', '1', '1', '1', '', '', '1', '<array>', 'Normal boot', 'SERG-DELL', '3',
        'Notebook', 'Win32_ComputerSystem', '60', '0', 'AT/AT COMPATIBLE', 'SERG-DELL',
        'WORKGROUP', '0', '1', '3', '0', '0', '', '', '3', '', 'Dell Inc.',
        'XPS 15 9570', 'SERG-DELL', '', '1', '12', '1', '', '<array>', '0', '-1', '2',
        '2', '', '', '3', '0', '3', '', 'sk', '1', '-1', '-1', '<array>', 'OK', '',
        'XPS', '087C', '', '', '', 'x64-based PC', '3', '34077048832', 'SERG-DELL\\sk',
        '6', 'WORKGROUP', 'Timeout'
    ]
]

#.

discovered_wmi_cpuload_result = [(None, None)]


@pytest.mark.parametrize("check_name,info,expected", [
    ('wmi_webservices', info_wmi_timeout, []),
    ('wmi_cpuload', info_wmi_cpuload_1, discovered_wmi_cpuload_result),
    ('wmi_cpuload', info_wmi_cpuload_2, discovered_wmi_cpuload_result),
    ('wmi_cpuload', info_wmi_cpuload_3, discovered_wmi_cpuload_result),
    ('wmi_cpuload', info_wmi_cpuload_4, discovered_wmi_cpuload_result),
    ('wmi_cpuload', info_wmi_cpuload_5, discovered_wmi_cpuload_result),
    ('wmi_cpuload', info_wmi_cpuload_6, discovered_wmi_cpuload_result),
    ('wmi_cpuload', info_wmi_cpuload_7, discovered_wmi_cpuload_result),
    ('wmi_cpuload', info_wmi_cpuload_8, discovered_wmi_cpuload_result),
    ('dotnet_clrmemory', [['WMItimeout']], []),
])
@pytest.mark.usefixtures("config_load_all_checks")
def test_wmi_cpu_load_discovery(check_name, info, expected):
    check = Check(check_name)
    discovery_result = DiscoveryResult(check.run_discovery(check.run_parse(info)))
    discovery_expected = DiscoveryResult(expected)
    assertDiscoveryResultsEqual(check, discovery_result, discovery_expected)


@pytest.mark.parametrize("check_name,info,expected", [
    ('wmi_webservices', info_wmi_timeout, None),
    ('wmi_cpuload', info_subsection_wmi_timeout, None),
])
@pytest.mark.usefixtures("config_load_all_checks")
def test_wmi_cpuload_timeout_exceptions(check_name, info, expected):
    check = Check(check_name)
    with pytest.raises(MKCounterWrapped):
        CheckResult(check.run_check(None, {}, check.run_parse(info)))
