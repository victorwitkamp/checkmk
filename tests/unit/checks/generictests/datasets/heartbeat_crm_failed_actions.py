#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# yapf: disable
# type: ignore



checkname = 'heartbeat_crm'


freeze_time = '2019-04-11 12:38:36'


info = [['Stack:', 'corosync'],
        ['Current',
         'DC:',
         'cluster',
         '(version',
         '1.1.16-12.el7_4.8-94ff4df)',
         '-',
         'partition',
         'with',
         'quorum'],
        ['Last', 'updated:', 'Tue', 'Oct', '26', '13:58:47', '2019'],
        ['Last',
         'change:',
         'Sat',
         'Oct',
         '24',
         '10:54:28',
         '2019',
         'by',
         'root',
         'via',
         'cibadmin',
         'on',
         'cluster'],
        ['2', 'nodes', 'configured'],
        ['6', 'resources', 'configured'],
        ['Online:', '[', 'cluster1', 'cluster2', ']'],
        ['Full', 'list', 'of', 'resources:'],
        ['Resource', 'Group:', 'mysqldb1'],
        ['_', 'mysqldb1_lvm', '(ocf::heartbeat:LVM):Started', 'cluster1'],
        ['_', 'mysqldb1_fs', '(ocf::heartbeat:Filesystem):Started', 'cluster1'],
        ['_', 'mysqldb1_ip', '(ocf::heartbeat:IPaddr2):Started', 'cluster1'],
        ['_', 'mysqldb1_mysql', '(service:mysqldb1):Started', 'cluster1'],
        ['cluster1_fence(stonith:fence_ipmilan):', 'Started', 'cluster2'],
        ['cluster2_fence(stonith:fence_ipmilan):', 'Started', 'cluster1'],
        ['Failed', 'Actions:'],
        ['*',
         'mysqldb1_lvm_monitor_10000',
         'on',
         'cluster1',
         "'unknown",
         "error'",
         '(1):',
         'call=158,',
         'status=Timed',
         'Out,',
         "exitreason='none',"],
        ['_',
         "last-rc-change='Fri",
         'Feb',
         '22',
         '22:54:52',
         "2019',",
         'queued=0ms,',
         'exec=0ms']]


discovery = {'': [(None, {'num_nodes': 2, 'num_resources': 6})],
             'resources': [('cluster1_fence(stonith:fence_ipmilan):', None),
                           ('cluster2_fence(stonith:fence_ipmilan):', None),
                           ('mysqldb1', None)]}


checks = {
    '': [
        (None,
         {'max_age': 60, 'num_nodes': 2, 'num_resources': 6},
         [(0, 'DC: cluster', []),
          (0, 'Nodes: 2', []),
          (0, 'Resources: 6', [])]),
        (None,
         {'max_age': 60, 'num_nodes': 2, 'num_resources': 6, 'show_failed_actions': True},
         [(0, 'DC: cluster', []),
          (0, 'Nodes: 2', []),
          (0, 'Resources: 6', []),
          (1, "Failed: mysqldb1_lvm_monitor_10000 on cluster1 'unknown error' (1): call=158, "
              "status=Timed Out, exitreason='none', last-rc-change='Fri Feb 22 22:54:52 2019', "
              "queued=0ms, exec=0ms", [])]),
    ],
    'resources': [
        ('cluster1_fence(stonith:fence_ipmilan):',
         {},
         [(0,
           'cluster1_fence(stonith:fence_ipmilan): Started cluster2',
           []),
          (2, 'Resource is in state "cluster2"', [])]),
        ('cluster2_fence(stonith:fence_ipmilan):',
         {},
         [(0,
           'cluster2_fence(stonith:fence_ipmilan): Started cluster1',
           []),
          (2, 'Resource is in state "cluster1"', [])]),
        ('mysqldb1',
         {},
         [(0,
           'mysqldb1_lvm (ocf::heartbeat:LVM):Started cluster1',
           []),
          (2, 'Resource is in state "cluster1"', []),
          (0,
           'mysqldb1_fs (ocf::heartbeat:Filesystem):Started cluster1',
           []),
          (2, 'Resource is in state "cluster1"', []),
          (0,
           'mysqldb1_ip (ocf::heartbeat:IPaddr2):Started cluster1',
           []),
          (2, 'Resource is in state "cluster1"', []),
          (0,
           'mysqldb1_mysql (service:mysqldb1):Started cluster1',
           []),
          (2, 'Resource is in state "cluster1"', [])])
    ],
}
