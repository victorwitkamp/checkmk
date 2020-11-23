#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from collections import namedtuple
from testlib import Check  # type: ignore[import]
import pytest  #type: ignore[import]
from checktestlib import (
    BasicCheckResult,
    CheckResult,
    DiscoveryResult,
    PerfValue,
    assertCheckResultsEqual,
    assertDiscoveryResultsEqual,
)

# since both nfsmounts and cifsmounts use the parse, inventory
# and check functions from network_fs.include unchanged we test
# both checks here.

pytestmark = pytest.mark.checks

Size = namedtuple('Size', 'info,total,used,text')

size1 = Size(
    ['491520', '460182', '460182', '65536'],
    491520 * 65536,
    491520 * 65536 - 460182 * 65536,
    "6.38% used (1.91 of 30.00 GB)",
)

size2 = Size(
    ['201326592', '170803720', '170803720', '32768'],
    None,  # not in use
    None,  # not in use
    "15.16% used (931.48 GB of 6.00 TB)",
)


@pytest.mark.parametrize(
    "info,discovery_expected,check_expected",
    [
        (  # no info
            [], [], ()),
        (  # single mountpoint with data
            [['/ABCshare', 'ok'] + size1.info], [('/ABCshare', {})], [
                ('/ABCshare', {}, BasicCheckResult(0, size1.text, None)),
            ]),
        (  # two mountpoints with empty data
            [['/AB', 'ok', '-', '-', '-', '-'], ['/ABC', 'ok', '-', '-', '-', '-']], [
                ('/AB', {}), ('/ABC', {})
            ], [('/AB', {}, BasicCheckResult(0, "Mount seems OK", None)),
                ('/ABC', {}, BasicCheckResult(0, "Mount seems OK", None))]),
        (  # Mountpoint with spaces and permission denied
            [['/var/dba', 'export', 'Permission',
              'denied'], ['/var/dbaexport', 'ok'] + size2.info], [
                  ('/var/dbaexport', {}), ('/var/dba export', {})
              ], [('/var/dba export', {}, BasicCheckResult(2, 'Permission denied', None)),
                  ('/var/dbaexport', {}, BasicCheckResult(0, size2.text, None))]),
        (  # with perfdata
            [['/PERFshare', 'ok'] + size1.info], [('/PERFshare', {})], [
                ('/PERFshare', {
                    'has_perfdata': True
                },
                 BasicCheckResult(0, size1.text, [
                     PerfValue('fs_used', size1.used, 0.8 * size1.total, 0.9 * size1.total, 0,
                               size1.total),
                     PerfValue('fs_size', size1.total),
                 ]))
            ]),
        (  # state == 'hanging'
            [['/test', 'hanging', 'hanging', '0', '0', '0', '0']
            ], [('/test hanging', {})], [('/test hanging', {
                'has_perfdata': True
            }, BasicCheckResult(2, "Server not responding", None))]),
        (  # unknown state
            [['/test', 'unknown', 'unknown', '1', '1', '1', '1']], [('/test unknown', {})], [
                ('/test unknown', {}, BasicCheckResult(2, "Unknown state: unknown", None))
            ]),
        (  # zero block size
            [['/test', 'perfdata', 'ok', '0', '460182', '460182', '0']],
            [('/test perfdata', {})],
            [(
                '/test perfdata',
                {
                    'has_perfdata': True
                },
                # TODO: display a better error message
                #BasicCheckResult(0, "server is responding", [PerfValue('fs_size', 0), PerfValue('fs_used', 0)]))]
                BasicCheckResult(2, "Stale fs handle", None))]),
    ])
@pytest.mark.usefixtures("config_load_all_checks")
def test_nfsmounts(info, discovery_expected, check_expected):
    check_nfs = Check("nfsmounts")
    check_cifs = Check("cifsmounts")

    # assure that the code of both checks is identical
    assert (check_nfs.info['parse_function'].__code__.co_code ==
            check_cifs.info['parse_function'].__code__.co_code)
    assert (check_nfs.info['inventory_function'].__code__.co_code ==
            check_cifs.info['inventory_function'].__code__.co_code)
    assert (check_nfs.info['check_function'].__code__.co_code ==
            check_cifs.info['check_function'].__code__.co_code)

    parsed = check_nfs.run_parse(info)

    assertDiscoveryResultsEqual(
        check_nfs,
        DiscoveryResult(check_nfs.run_discovery(parsed)),  #
        DiscoveryResult(discovery_expected))

    for item, params, result_expected in check_expected:
        result = CheckResult(check_nfs.run_check(item, params, parsed))
        assertCheckResultsEqual(result, CheckResult([result_expected]))
