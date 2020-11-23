#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# yapf: disable
# type: ignore



checkname = 'netapp_api_ports'


info = [['port cl01-02.e0c-614',
         'is-administrative-auto-negotiate true',
         'operational-speed 10000',
         'is-administrative-up true',
         'vlan-port e0c',
         'operational-flowcontrol none',
         'vlan-id 614',
         'port e0c-614',
         'role data',
         'ignore-health-status false',
         'mac-address 00:a0:98:f2:39:8d',
         'is-operational-auto-negotiate true',
         'node cl01-02',
         'ipspace Default',
         'vlan-node cl01-02',
         'mtu-admin 9000',
         'operational-duplex full',
         'administrative-speed auto',
         'broadcast-domain vlan-614-p',
         'administrative-duplex auto',
         'health-status healthy',
         'mtu 9000',
         'link-status up',
         'administrative-flowcontrol none',
         'port-type vlan'],
        ['port cl01-02.e0d',
         'administrative-speed auto',
         'node cl01-02',
         'operational-speed 10000',
         'port-type physical',
         'remote-device-id LAB01_SAP_HANA5(FDO231719MB)',
         'administrative-duplex auto',
         'health-status healthy',
         'is-administrative-auto-negotiate true',
         'operational-flowcontrol none',
         'ipspace Default',
         'port e0d',
         'is-administrative-up true',
         'link-status up',
         'role data',
         'ignore-health-status false',
         'mtu-admin 9000',
         'administrative-flowcontrol none',
         'mtu 9000',
         'mac-address 00:a0:98:f2:39:8e',
         'operational-duplex full',
         'is-operational-auto-negotiate true']]


discovery = {'': [('Physical port cl01-02.e0d', {})]}


checks = {'': [('Physical port cl01-02.e0d',
                {},
                [(0, 'Health status: healthy, Operational speed: 10000', [])])]}


mock_host_conf_merged = {'': {'ignored_ports': ['vlan']}}
