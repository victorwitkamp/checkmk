#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# yapf: disable
# type: ignore



checkname = 'splunk_system_msg'


info = [['manifest_error',
         'warn',
         'klappclub',
         '2019-05-16T08:32:33+02:00',
         'File',
         'Integrity',
         'checks',
         'found',
         '1',
         'files',
         'that',
         'did',
         'not',
         'match',
         'the',
         'system-provided',
         'manifest.',
         'Review',
         'the',
         'list',
         'of',
         'problems',
         'reported',
         'by',
         'the',
         'InstalledFileHashChecker',
         'in',
         'splunkd.log',
         '[[/app/search/integrity_check_of_installed_files?form.splunk_server=klappclub|File',
         'Integrity',
         'Check',
         'View]]',
         ';',
         'potentially',
         'restore',
         'files',
         'from',
         'installation',
         'media,',
         'change',
         'practices',
         'to',
         'avoid',
         'changing',
         'files,',
         'or',
         'work',
         'with',
         'support',
         'to',
         'identify',
         'the',
         'problem.']]


discovery = {'': [(None, {})]}


checks = {'': [(None,
                {},
                [(1,
                  'Worst severity: warn, Last message from server: klappclub, Creation time: 2019-05-16T08:32:33+02:00\n2019-05-16T08:32:33+02:00 - klappclub - Integrity checks found 1 files that did not match the system-provided manifest. Review the list of problems reported by the InstalledFileHashChecker in splunkd.log [[/app/search/integrity_check_of_installed_files?form.splunk_server=klappclub|File Integrity Check View]] ; potentially restore files from installation media, change practices to avoid changing files, or work with support to identify the problem.\n',
                  [])])]}
