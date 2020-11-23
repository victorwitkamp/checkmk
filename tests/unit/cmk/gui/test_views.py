#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# yapf: disable

import copy
from typing import Any, Dict

import pytest  # type: ignore[import]

import cmk.gui.config as config
import cmk.utils.version as cmk_version

pytestmark = pytest.mark.usefixtures("load_plugins")

from cmk.gui.globals import html
from cmk.gui.valuespec import ValueSpec
import cmk.gui.plugins.views
from cmk.gui.plugins.views.utils import transform_painter_spec
from cmk.gui.type_defs import PainterSpec
import cmk.gui.views


@pytest.fixture(name="view")
def view_fixture(register_builtin_html):
    view_name = "allhosts"
    view_spec = transform_painter_spec(cmk.gui.views.multisite_builtin_views[view_name])
    return cmk.gui.views.View(view_name, view_spec, view_spec.get("context", {}))


def test_registered_painter_options():
    expected = [
        'aggr_expand',
        'aggr_onlyproblems',
        'aggr_treetype',
        'aggr_wrap',
        'matrix_omit_uniform',
        'pnp_timerange',
        'show_internal_tree_paths',
        'ts_date',
        'ts_format',
        'graph_render_options',
        "refresh",
        "num_columns",
    ]

    names = cmk.gui.plugins.views.painter_option_registry.keys()
    assert sorted(expected) == sorted(names)

    for cls in cmk.gui.plugins.views.painter_option_registry.values():
        vs = cls().valuespec
        assert isinstance(vs, ValueSpec)


def test_registered_layouts():
    expected = [
        'boxed',
        'boxed_graph',
        'dataset',
        'matrix',
        'mobiledataset',
        'mobilelist',
        'mobiletable',
        'table',
        'tiled',
    ]

    names = cmk.gui.plugins.views.layout_registry.keys()
    assert sorted(expected) == sorted(names)


def test_layout_properties():
    expected = {
        'boxed': {
            'checkboxes': True,
            'title': 'Balanced boxes'
        },
        'boxed_graph': {
            'checkboxes': True,
            'title': 'Balanced graph boxes'
        },
        'dataset': {
            'checkboxes': False,
            'title': 'Single dataset'
        },
        'matrix': {
            'checkboxes': False,
            'has_csv_export': True,
            'options': ['matrix_omit_uniform'],
            'title': 'Matrix'
        },
        'mobiledataset': {
            'checkboxes': False,
            'title': 'Mobile: Dataset'
        },
        'mobilelist': {
            'checkboxes': False,
            'title': 'Mobile: List'
        },
        'mobiletable': {
            'checkboxes': False,
            'title': 'Mobile: Table'
        },
        'table': {
            'checkboxes': True,
            'title': 'Table'
        },
        'tiled': {
            'checkboxes': True,
            'title': 'Tiles'
        },
    }

    for ident, spec in expected.items():
        plugin = cmk.gui.plugins.views.layout_registry[ident]()
        assert isinstance(plugin.title, str)
        assert spec["title"] == plugin.title
        assert spec["checkboxes"] == plugin.can_display_checkboxes
        assert spec.get("has_csv_export", False) == plugin.has_individual_csv_export


def test_get_layout_choices():
    choices = cmk.gui.plugins.views.layout_registry.get_choices()
    assert sorted(choices) == sorted([
        ('matrix', 'Matrix'),
        ('boxed_graph', 'Balanced graph boxes'),
        ('dataset', 'Single dataset'),
        ('tiled', 'Tiles'),
        ('table', 'Table'),
        ('boxed', 'Balanced boxes'),
        ('mobiledataset', 'Mobile: Dataset'),
        ('mobiletable', 'Mobile: Table'),
        ('mobilelist', 'Mobile: List'),
    ])


def test_registered_exporters():
    expected = [
        'csv',
        'csv_export',
        'json',
        'json_export',
        'jsonp',
        'python',
        'python-raw',
    ]
    names = cmk.gui.plugins.views.exporter_registry.keys()
    assert sorted(expected) == sorted(names)


def test_registered_command_groups():
    expected = [
        'acknowledge',
        'downtimes',
        'fake_check',
        'various',
    ]

    names = cmk.gui.plugins.views.utils.command_group_registry.keys()
    assert sorted(expected) == sorted(names)


def test_legacy_register_command_group(monkeypatch):
    monkeypatch.setattr(cmk.gui.plugins.views.utils, "command_group_registry",
                        cmk.gui.plugins.views.utils.CommandGroupRegistry())
    cmk.gui.plugins.views.utils.register_command_group("abc", "A B C", 123)

    group = cmk.gui.plugins.views.utils.command_group_registry["abc"]()
    assert isinstance(group, cmk.gui.plugins.views.utils.CommandGroup)
    assert group.ident == "abc"
    assert group.title == "A B C"
    assert group.sort_index == 123


def test_registered_commands():
    expected: Dict[str, Dict[str, Any]] = {
        'acknowledge': {
            'group': 'acknowledge',
            'permission': 'action.acknowledge',
            'tables': ['host', 'service', 'aggr'],
            'title': 'Acknowledge problems'
        },
        'ec_custom_actions': {
            'permission': 'mkeventd.actions',
            'tables': ['event'],
            'title': 'Custom Action'
        },
        'remove_comments': {
            'permission': 'action.addcomment',
            'tables': ['comment'],
            'title': 'Remove comments'
        },
        'remove_downtimes': {
            'permission': 'action.downtimes',
            'tables': ['downtime'],
            'title': 'Remove downtimes'
        },
        'schedule_downtimes': {
            'permission': 'action.downtimes',
            'tables': ['host', 'service', 'aggr'],
            'title': 'Schedule downtimes'
        },
        'ec_archive_events_of_host': {
            'permission': 'mkeventd.archive_events_of_hosts',
            'tables': ['host', 'service'],
            'title': 'Archive events of hosts'
        },
        'ec_change_state': {
            'permission': 'mkeventd.changestate',
            'tables': ['event'],
            'title': 'Change State'
        },
        'clear_modified_attributes': {
            'permission': 'action.clearmodattr',
            'tables': ['host', 'service'],
            'title': 'Modified attributes'
        },
        'send_custom_notification': {
            'permission': 'action.customnotification',
            'tables': ['host', 'service'],
            'title': 'Custom notification'
        },
        'ec_archive_event': {
            'permission': 'mkeventd.delete',
            'tables': ['event'],
            'title': 'Archive Event'
        },
        'add_comment': {
            'permission': 'action.addcomment',
            'tables': ['host', 'service'],
            'title': 'Add comment'
        },
        'toggle_passive_checks': {
            'permission': 'action.enablechecks',
            'tables': ['host', 'service'],
            'title': 'Passive checks'
        },
        'toggle_active_checks': {
            'permission': 'action.enablechecks',
            'tables': ['host', 'service'],
            'title': 'Active checks'
        },
        'fake_check_result': {
            'group': 'fake_check',
            'permission': 'action.fakechecks',
            'tables': ['host', 'service'],
            'title': 'Fake check results'
        },
        'notifications': {
            'permission': 'action.notifications',
            'tables': ['host', 'service'],
            'title': 'Notifications'
        },
        'reschedule': {
            'permission': 'action.reschedule',
            'row_stats': True,
            'tables': ['host', 'service'],
            'title': 'Reschedule active checks'
        },
        'favorites': {
            'permission': 'action.star',
            'tables': ['host', 'service'],
            'title': 'Favorites'
        },
        'ec_update_event': {
            'permission': 'mkeventd.update',
            'tables': ['event'],
            'title': 'Update & Acknowledge'
        },
        'delete_crash_reports': {
            'permission': 'action.delete_crash_report',
            'tables': ['crash'],
            'title': 'Delete crash reports',
        },
    }

    if not cmk_version.is_raw_edition():
        expected.update({'edit_downtimes': {
            'permission': 'action.downtimes',
            'tables': ['downtime'],
            'title': 'Edit Downtimes'
        },
        })

    names = cmk.gui.plugins.views.command_registry.keys()
    assert sorted(expected.keys()) == sorted(names)

    for cmd_class in cmk.gui.plugins.views.utils.command_registry.values():
        cmd = cmd_class()
        cmd_spec = expected[cmd.ident]
        assert cmd.title == cmd_spec["title"]
        assert cmd.tables == cmd_spec["tables"], cmd.ident
        assert cmd.permission.name == cmd_spec["permission"]


def test_legacy_register_command(monkeypatch):
    monkeypatch.setattr(cmk.gui.plugins.views.utils, "command_registry",
                        cmk.gui.plugins.views.utils.CommandRegistry())

    def render():
        pass

    def action():
        pass

    cmk.gui.plugins.views.utils.register_legacy_command({
        "tables": ["tabl"],
        "permission": "general.use",
        "title": "Bla Bla",
        "render": render,
        "action": action,
    })

    cmd = cmk.gui.plugins.views.utils.command_registry["blabla"]()
    assert isinstance(cmd, cmk.gui.plugins.views.utils.Command)
    assert cmd.ident == "blabla"
    assert cmd.title == "Bla Bla"
    assert cmd.permission == cmk.gui.default_permissions.PermissionGeneralUse


# These tests make adding new elements needlessly painful.
# Skip pending discussion with development team.
@pytest.mark.skip
def test_registered_datasources():
    expected: Dict[str, Dict[str, Any]] = {
        'alert_stats': {
            'add_columns': [
                'log_alerts_ok', 'log_alerts_warn', 'log_alerts_crit', 'log_alerts_unknown',
                'log_alerts_problem'
            ],
            'add_headers': 'Filter: class = 1\nStats: state = 0\nStats: state = 1\nStats: state = 2\nStats: state = 3\nStats: state != 0\n',
            'idkeys': ['host_name', 'service_description'],
            'ignore_limit': True,
            'infos': ['log', 'host', 'service', 'contact', 'command'],
            'keys': [],
            'table': 'log',
            'time_filters': ['logtime'],
            'title': 'Alert Statistics'
        },
        'bi_aggregations': {
            'idkeys': ['aggr_name'],
            'infos': ['aggr', 'aggr_group'],
            'keys': [],
            'table': ('func', 'table'),
            'title': 'BI Aggregations'
        },
        'bi_host_aggregations': {
            'idkeys': ['aggr_name'],
            'infos': ['aggr', 'host', 'aggr_group'],
            'keys': [],
            'table': ('func', 'host_table'),
            'title': 'BI Aggregations affected by one host'
        },
        'bi_hostname_aggregations': {
            'idkeys': ['aggr_name'],
            'infos': ['aggr', 'host', 'aggr_group'],
            'keys': [],
            'table': ('func', 'hostname_table'),
            'title': 'BI Hostname Aggregations'
        },
        'bi_hostnamebygroup_aggregations': {
            'idkeys': ['aggr_name'],
            'infos': ['aggr', 'host', 'hostgroup', 'aggr_group'],
            'keys': [],
            'table': ('func', 'hostname_by_group_table'),
            'title': 'BI Aggregations for Hosts by Hostgroups'
        },
        'comments': {
            'idkeys': ['comment_id'],
            'infos': ['comment', 'host', 'service'],
            'keys': ['comment_id', 'comment_type', 'host_name', 'service_description'],
            'table': 'comments',
            'title': 'Host- and Servicecomments'
        },
        'downtimes': {
            'idkeys': ['downtime_id'],
            'infos': ['downtime', 'host', 'service'],
            'keys': ['downtime_id', 'service_description'],
            'table': 'downtimes',
            'title': 'Scheduled Downtimes'
        },
        'hostgroups': {
            'idkeys': ['site', 'hostgroup_name'],
            'infos': ['hostgroup'],
            'keys': ['hostgroup_name'],
            'table': 'hostgroups',
            'title': 'Hostgroups'
        },
        'hosts': {
            'description': 'Displays a list of hosts.',
            'idkeys': ['site', 'host_name'],
            'infos': ['host'],
            'join': ('services', 'host_name'),
            'keys': ['host_name', 'host_downtimes'],
            'link_filters': {
                'hostgroup': 'opthostgroup'
            },
            'table': 'hosts',
            'title': 'All hosts'
        },
        'hostsbygroup': {
            'description': 'This datasource has a separate row for each group membership that a host has.',
            'idkeys': ['site', 'hostgroup_name', 'host_name'],
            'infos': ['host', 'hostgroup'],
            'join': ('services', 'host_name'),
            'keys': ['host_name', 'host_downtimes'],
            'table': 'hostsbygroup',
            'title': 'Hosts grouped by host groups'
        },
        'invbackplane': {
            'idkeys': [],
            'infos': ['host', 'invbackplane'],
            'keys': [],
            'table': ('func', 'inv_table'),
            'title': 'Inventory: Backplanes'
        },
        'invchassis': {
            'idkeys': [],
            'infos': ['host', 'invchassis'],
            'keys': [],
            'table': ('func', 'inv_table'),
            'title': 'Inventory: Chassis'
        },
        'invcontainer': {
            'idkeys': [],
            'infos': ['host', 'invcontainer'],
            'keys': [],
            'table': ('func', 'inv_table'),
            'title': 'Inventory: HW containers'
        },
        'invdockercontainers': {
            'idkeys': [],
            'infos': ['host', 'invdockercontainers'],
            'keys': [],
            'table': ('func', 'inv_table'),
            'title': 'Inventory: Docker containers'
        },
        'invdockerimages': {
            'idkeys': [],
            'infos': ['host', 'invdockerimages'],
            'keys': [],
            'table': ('func', 'inv_table'),
            'title': 'Inventory: Docker images'
        },
        'invfan': {
            'idkeys': [],
            'infos': ['host', 'invfan'],
            'keys': [],
            'table': ('func', 'inv_table'),
            'title': 'Inventory: Fans'
        },
        'invhist': {
            'idkeys': ['host_name', 'invhist_time'],
            'infos': ['host', 'invhist'],
            'keys': [],
            'table': ('func', 'inv_history_table'),
            'title': 'Inventory: History'
        },
        'invinterface': {
            'idkeys': [],
            'infos': ['host', 'invinterface'],
            'keys': [],
            'table': ('func', 'inv_table'),
            'title': 'Inventory: Network interfaces'
        },
        'invmodule': {
            'idkeys': [],
            'infos': ['host', 'invmodule'],
            'keys': [],
            'table': ('func', 'inv_table'),
            'title': 'Inventory: Modules'
        },
        'invoradataguardstats': {
            'idkeys': [],
            'infos': ['host', 'invoradataguardstats'],
            'keys': [],
            'table': ('func', 'inv_table'),
            'title': 'Inventory: Oracle dataguard statistics'
        },
        'invorainstance': {
            'idkeys': [],
            'infos': ['host', 'invorainstance'],
            'keys': [],
            'table': ('func', 'inv_table'),
            'title': 'Inventory: Oracle instances'
        },
        'invorarecoveryarea': {
            'idkeys': [],
            'infos': ['host', 'invorarecoveryarea'],
            'keys': [],
            'table': ('func', 'inv_table'),
            'title': 'Inventory: Oracle recovery areas'
        },
        'invorasga': {
            'idkeys': [],
            'infos': ['host', 'invorasga'],
            'keys': [],
            'table': ('func', 'inv_table'),
            'title': 'Inventory: Oracle performance'
        },
        'invoratablespace': {
            'idkeys': [],
            'infos': ['host', 'invoratablespace'],
            'keys': [],
            'table': ('func', 'inv_table'),
            'title': 'Inventory: Oracle tablespaces'
        },
        'invother': {
            'idkeys': [],
            'infos': ['host', 'invother'],
            'keys': [],
            'table': ('func', 'inv_table'),
            'title': 'Inventory: Other entities'
        },
        'invpsu': {
            'idkeys': [],
            'infos': ['host', 'invpsu'],
            'keys': [],
            'table': ('func', 'inv_table'),
            'title': 'Inventory: Power supplies'
        },
        'invsensor': {
            'idkeys': [],
            'infos': ['host', 'invsensor'],
            'keys': [],
            'table': ('func', 'inv_table'),
            'title': 'Inventory: Sensors'
        },
        'invstack': {
            'idkeys': [],
            'infos': ['host', 'invstack'],
            'keys': [],
            'table': ('func', 'inv_table'),
            'title': 'Inventory: Stacks'
        },
        'invswpac': {
            'idkeys': [],
            'infos': ['host', 'invswpac'],
            'keys': [],
            'table': ('func', 'inv_table'),
            'title': 'Inventory: Software packages'
        },
        'invunknown': {
            'idkeys': [],
            'infos': ['host', 'invunknown'],
            'keys': [],
            'table': ('func', 'inv_table'),
            'title': 'Inventory: Unknown entities'
        },
        'log': {
            'idkeys': ['log_lineno'],
            'infos': ['log', 'host', 'service', 'contact', 'command'],
            'keys': [],
            'table': 'log',
            'time_filters': ['logtime'],
            'title': 'The Logfile'
        },
        'log_events': {
            'add_headers': 'Filter: class = 1\nFilter: class = 3\nFilter: class = 8\nOr: 3\n',
            'idkeys': ['log_lineno'],
            'infos': ['log', 'host', 'service'],
            'keys': [],
            'table': 'log',
            'time_filters': ['logtime'],
            'title': 'Host and Service Events'
        },
        'log_host_events': {
            'add_headers': 'Filter: class = 1\nFilter: class = 3\nFilter: class = 8\nOr: 3\nFilter: service_description = \n',
            'idkeys': ['log_lineno'],
            'infos': ['log', 'host'],
            'keys': [],
            'table': 'log',
            'time_filters': ['logtime'],
            'title': 'Host Events'
        },
        'merged_hostgroups': {
            'idkeys': ['hostgroup_name'],
            'infos': ['hostgroup'],
            'keys': ['hostgroup_name'],
            'merge_by': 'hostgroup_name',
            'table': 'hostgroups',
            'title': 'Hostgroups, merged'
        },
        'merged_servicegroups': {
            'idkeys': ['servicegroup_name'],
            'infos': ['servicegroup'],
            'keys': ['servicegroup_name'],
            'merge_by': 'servicegroup_name',
            'table': 'servicegroups',
            'title': 'Servicegroups, merged'
        },
        'mkeventd_events': {
            'auth_domain': 'ec',
            'idkeys': ['site', 'host_name', 'event_id'],
            'infos': ['event', 'host'],
            'keys': [],
            'table': ('tuple', ('query_ec_table', ['eventconsoleevents'])),
            'time_filters': ['event_first'],
            'title': 'Event Console: Current Events'
        },
        'mkeventd_history': {
            'auth_domain': 'ec',
            'idkeys': ['site', 'host_name', 'event_id', 'history_line'],
            'infos': ['history', 'event', 'host'],
            'keys': [],
            'table': ('tuple', ('query_ec_table', ['eventconsolehistory'])),
            'time_filters': ['history_time'],
            'title': 'Event Console: Event History'
        },
        'service_discovery': {
            'add_columns': ['discovery_state', 'discovery_check', 'discovery_service'],
            'idkeys': ['host_name'],
            'infos': ['host', 'discovery'],
            'keys': [],
            'table': ('func', 'query_service_discovery'),
            'title': 'Service discovery'
        },
        'servicegroups': {
            'idkeys': ['site', 'servicegroup_name'],
            'infos': ['servicegroup'],
            'keys': ['servicegroup_name'],
            'table': 'servicegroups',
            'title': 'Servicegroups'
        },
        'services': {
            'idkeys': ['site', 'host_name', 'service_description'],
            'infos': ['service', 'host'],
            'joinkey': 'service_description',
            'keys': ['host_name', 'service_description', 'service_downtimes'],
            'link_filters': {
                'hostgroup': 'opthostgroup',
                'servicegroup': 'optservicegroup'
            },
            'table': 'services',
            'title': 'All services'
        },
        'servicesbygroup': {
            'idkeys': ['site', 'servicegroup_name', 'host_name', 'service_description'],
            'infos': ['service', 'host', 'servicegroup'],
            'keys': ['host_name', 'service_description', 'service_downtimes'],
            'table': 'servicesbygroup',
            'title': 'Services grouped by service groups'
        },
        'servicesbyhostgroup': {
            'idkeys': ['site', 'hostgroup_name', 'host_name', 'service_description'],
            'infos': ['service', 'host', 'hostgroup'],
            'keys': ['host_name', 'service_description', 'service_downtimes'],
            'table': 'servicesbyhostgroup',
            'title': 'Services grouped by host groups'
        },
    }

    names = cmk.gui.plugins.views.data_source_registry.keys()
    assert sorted(expected.keys()) == sorted(names)

    for ds_class in cmk.gui.plugins.views.utils.data_source_registry.values():
        ds = ds_class()
        spec = expected[ds.ident]
        assert ds.title == spec["title"]
        if hasattr(ds.table, '__call__'):
            # FIXME: ugly getattr so that mypy doesn't complain about missing attribute __name__
            name = getattr(ds.table, '__name__')
            assert ("func", name) == spec["table"]
        elif isinstance(ds.table, tuple):
            assert spec["table"][0] == "tuple"
            assert spec["table"][1][0] == ds.table[0].__name__
        else:
            assert ds.table == spec["table"]
        assert ds.keys == spec["keys"]
        assert ds.id_keys == spec["idkeys"]
        assert ds.infos == spec["infos"]


# These tests make adding new elements needlessly painful.
# Skip pending discussion with development team.
@pytest.mark.skip
def test_registered_painters():
    expected: Dict[str, Dict[str, Any]] = {
        'aggr_acknowledged': {
            'columns': ['aggr_effective_state'],
            'title': 'Acknowledged'
        },
        'aggr_assumed_state': {
            'columns': ['aggr_assumed_state'],
            'short': 'Assumed',
            'title': 'Aggregated assumed state'
        },
        'aggr_group': {
            'columns': ['aggr_group'],
            'short': 'Group',
            'title': 'Aggregation group'
        },
        'aggr_hosts': {
            'columns': ['aggr_hosts'],
            'short': 'Hosts',
            'title': 'Aggregation: affected hosts'
        },
        'aggr_hosts_services': {
            'columns': ['aggr_hosts'],
            'short': 'Hosts',
            'title': 'Aggregation: affected hosts (link to host page)'
        },
        'aggr_icons': {
            'columns': ['aggr_group', 'aggr_name', 'aggr_effective_state'],
            'printable': False,
            'title': 'Links'
        },
        'aggr_in_downtime': {
            'columns': ['aggr_effective_state'],
            'title': 'In Downtime'
        },
        'aggr_name': {
            'columns': ['aggr_name'],
            'short': 'Aggregation',
            'title': 'Aggregation name'
        },
        'aggr_output': {
            'columns': ['aggr_output'],
            'short': 'Output',
            'title': 'Aggregation status output'
        },
        'aggr_real_state': {
            'columns': ['aggr_state'],
            'short': 'R.State',
            'title': 'Aggregated real state (never assumed)'
        },
        'aggr_state': {
            'columns': ['aggr_effective_state'],
            'short': 'State',
            'title': 'Aggregated state'
        },
        'aggr_state_num': {
            'columns': ['aggr_effective_state'],
            'short': 'State',
            'title': 'Aggregated state (number)'
        },
        'aggr_treestate': {
            'columns': ['aggr_treestate', 'aggr_hosts'],
            'options': ['aggr_expand', 'aggr_onlyproblems', 'aggr_treetype', 'aggr_wrap'],
            'short': 'Tree',
            'title': 'Aggregation: complete tree'
        },
        'aggr_treestate_boxed': {
            'columns': ['aggr_treestate', 'aggr_hosts'],
            'short': 'Tree',
            'title': 'Aggregation: simplistic boxed layout'
        },
        'alert_stats_crit': {
            'columns': ['log_alerts_crit'],
            'short': 'CRIT',
            'title': 'Alert Statistics: Number of critical alerts'
        },
        'alert_stats_ok': {
            'columns': ['log_alerts_ok'],
            'short': 'OK',
            'title': 'Alert Statistics: Number of recoveries'
        },
        'alert_stats_problem': {
            'columns': ['log_alerts_problem'],
            'short': 'PROB',
            'title': 'Alert Statistics: Number of problem alerts'
        },
        'alert_stats_unknown': {
            'columns': ['log_alerts_unknown'],
            'short': 'UNKN',
            'title': 'Alert Statistics: Number of unknown alerts'
        },
        'alert_stats_warn': {
            'columns': ['log_alerts_warn'],
            'short': 'WARN',
            'title': 'Alert Statistics: Number of warnings'
        },
        'alias': {
            'columns': ['host_alias'],
            'short': 'Alias',
            'title': 'Host alias'
        },
        'check_manpage': {
            'columns': ['service_check_command'],
            'short': 'Manual',
            'title': 'Check manual (for Check_MK based checks)'
        },
        'comment_author': {
            'columns': ['comment_author'],
            'short': 'Author',
            'title': 'Comment author'
        },
        'comment_comment': {
            'columns': ['comment_comment'],
            'title': 'Comment text'
        },
        'comment_entry_type': {
            'columns': ['comment_entry_type', 'host_name', 'service_description'],
            'short': 'E.Type',
            'title': 'Comment entry type (user/downtime/flapping/ack)'
        },
        'comment_expires': {
            'columns': ['comment_expire_time'],
            'options': ['ts_format', 'ts_date'],
            'short': 'Expires',
            'title': 'Comment expiry time'
        },
        'comment_id': {
            'columns': ['comment_id'],
            'short': 'ID',
            'title': 'Comment id'
        },
        'comment_time': {
            'columns': ['comment_entry_time'],
            'options': ['ts_format', 'ts_date'],
            'short': 'Time',
            'title': 'Comment entry time'
        },
        'comment_what': {
            'columns': ['comment_type'],
            'short': 'Type',
            'title': 'Comment type (host/service)'
        },
        'deployment_downloaded_hash': {
            'columns': ['host_name'],
            'short': 'Downloaded Agent',
            'title': 'Agent Deployment: Downloaded Agent Hash'
        },
        'deployment_icons': {
            'columns': ['host_name'],
            'short': '',
            'title': 'Agent Deployment: Icons'
        },
        'deployment_installed_hash': {
            'columns': ['host_name'],
            'short': 'Installed Agent',
            'title': 'Agent Deployment: Installed Agent Hash'
        },
        'deployment_last_contact': {
            'columns': ['host_name'],
            'options': ['ts_format', 'ts_date'],
            'short': 'Last Contact',
            'title': 'Agent Deployment: Last Contact'
        },
        'deployment_last_download': {
            'columns': ['host_name'],
            'options': ['ts_format', 'ts_date'],
            'short': 'Last Download',
            'title': 'Agent Deployment: Last Download'
        },
        'deployment_last_error': {
            'columns': ['host_name'],
            'short': 'Last Error',
            'title': 'Agent Deployment: Last Error'
        },
        'deployment_target_hash': {
            'columns': ['host_name'],
            'short': 'Target Agent',
            'title': 'Agent Deployment: Target Agent Hash'
        },
        'downtime_author': {
            'columns': ['downtime_author'],
            'short': 'Author',
            'title': 'Downtime author'
        },
        'downtime_comment': {
            'columns': ['downtime_comment'],
            'short': 'Comment',
            'title': 'Downtime comment'
        },
        'downtime_duration': {
            'columns': ['downtime_duration', 'downtime_fixed'],
            'short': 'Flex. Duration',
            'title': 'Downtime duration (if flexible)'
        },
        'downtime_end_time': {
            'columns': ['downtime_end_time'],
            'options': ['ts_format', 'ts_date'],
            'short': 'End',
            'title': 'Downtime end time'
        },
        'downtime_entry_time': {
            'columns': ['downtime_entry_time'],
            'options': ['ts_format', 'ts_date'],
            'short': 'Entry',
            'title': 'Downtime entry time'
        },
        'downtime_fixed': {
            'columns': ['downtime_fixed'],
            'short': 'Mode',
            'title': 'Downtime start mode'
        },
        'downtime_id': {
            'columns': ['downtime_id'],
            'short': 'ID',
            'title': 'Downtime id'
        },
        'downtime_origin': {
            'columns': ['downtime_origin'],
            'short': 'Origin',
            'title': 'Downtime origin'
        },
        'downtime_recurring': {
            'columns': ['downtime_recurring'],
            'short': 'Recurring',
            'title': 'Downtime recurring interval'
        },
        'downtime_start_time': {
            'columns': ['downtime_start_time'],
            'options': ['ts_format', 'ts_date'],
            'short': 'Start',
            'title': 'Downtime start time'
        },
        'downtime_type': {
            'columns': ['downtime_type'],
            'short': 'act/pend',
            'title': 'Downtime active or pending'
        },
        'downtime_what': {
            'columns': ['downtime_is_service'],
            'short': 'for',
            'title': 'Downtime for host/service'
        },
        'event_application': {
            'columns': ['event_application'],
            'short': 'Application',
            'title': 'Application / Syslog-Tag'
        },
        'event_comment': {
            'columns': ['event_comment'],
            'short': 'Comment',
            'title': 'Comment to the event'
        },
        'event_contact': {
            'columns': ['event_contact'],
            'short': 'Contact',
            'title': 'Contact Person'
        },
        'event_contact_groups': {
            'columns': ['event_contact_groups'],
            'short': 'Rule contact groups',
            'title': 'Contact groups defined in rule'
        },
        'event_count': {
            'columns': ['event_count'],
            'short': 'Cnt.',
            'title': 'Count (number of recent occurrances)'
        },
        'event_effective_contact_groups': {
            'columns': [
                'event_contact_groups', 'event_contact_groups_precedence', 'host_contact_groups'
            ],
            'short': 'Contact groups',
            'title': 'Contact groups effective (Host or rule contact groups)'
        },
        'event_facility': {
            'columns': ['event_facility'],
            'short': 'Facility',
            'title': 'Syslog-Facility'
        },
        'event_first': {
            'columns': ['event_first'],
            'options': ['ts_format', 'ts_date'],
            'short': 'First',
            'title': 'Time of first occurrence of this serial'
        },
        'event_history_icons': {
            'columns': ['event_phase', 'event_host_in_downtime'],
            'printable': False,
            'short': 'Icons',
            'title': 'Event Icons'
        },
        'event_host': {
            'columns': ['event_host', 'host_name'],
            'short': 'Host',
            'title': 'Hostname'
        },
        'event_host_in_downtime': {
            'columns': ['event_host_in_downtime'],
            'short': 'Dt.',
            'title': 'Host in downtime during event creation'
        },
        'event_icons': {
            'columns': ['event_phase', 'event_host_in_downtime'],
            'printable': False,
            'short': 'Icons',
            'title': 'Event Icons'
        },
        'event_id': {
            'columns': ['event_id'],
            'short': 'ID',
            'title': 'ID of the event'
        },
        'event_ipaddress': {
            'columns': ['event_ipaddress'],
            'short': 'Orig. IP',
            'title': 'Original IP-Address'
        },
        'event_last': {
            'columns': ['event_last'],
            'options': ['ts_format', 'ts_date'],
            'short': 'Last',
            'title': 'Time of last occurrance'
        },
        'event_match_groups': {
            'columns': ['event_match_groups'],
            'short': 'Match',
            'title': 'Match Groups'
        },
        'event_owner': {
            'columns': ['event_owner'],
            'short': 'owner',
            'title': 'Owner of event'
        },
        'event_phase': {
            'columns': ['event_phase'],
            'short': 'Phase',
            'title': 'Phase of event (open, counting, etc.)'
        },
        'event_pid': {
            'columns': ['event_pid'],
            'short': 'PID',
            'title': 'Process ID'
        },
        'event_priority': {
            'columns': ['event_priority'],
            'short': 'Prio',
            'title': 'Syslog-Priority'
        },
        'event_rule_id': {
            'columns': ['event_rule_id'],
            'short': 'Rule',
            'title': 'Rule-ID'
        },
        'event_sl': {
            'columns': ['event_sl'],
            'short': 'Level',
            'title': 'Service-Level'
        },
        'event_state': {
            'columns': ['event_state'],
            'short': 'State',
            'title': 'State (severity) of event'
        },
        'event_text': {
            'columns': ['event_text'],
            'short': 'Message',
            'title': 'Text/Message of the event'
        },
        'hg_alias': {
            'columns': ['hostgroup_alias'],
            'short': 'Alias',
            'title': 'Hostgroup alias'
        },
        'hg_name': {
            'columns': ['hostgroup_name'],
            'short': 'Name',
            'title': 'Hostgroup name'
        },
        'hg_num_hosts_down': {
            'columns': ['hostgroup_num_hosts_down'],
            'short': 'Dw',
            'title': 'Number of hosts in state DOWN (Host Group)'
        },
        'hg_num_hosts_pending': {
            'columns': ['hostgroup_num_hosts_pending'],
            'short': 'Pd',
            'title': 'Number of hosts in state PENDING (Host Group)'
        },
        'hg_num_hosts_unreach': {
            'columns': ['hostgroup_num_hosts_unreach'],
            'short': 'Un',
            'title': 'Number of hosts in state UNREACH (Host Group)'
        },
        'hg_num_hosts_up': {
            'columns': ['hostgroup_num_hosts_up'],
            'short': 'Up',
            'title': 'Number of hosts in state UP (Host Group)'
        },
        'hg_num_services': {
            'columns': ['hostgroup_num_services'],
            'short': '',
            'title': 'Number of services (Host Group)'
        },
        'hg_num_services_crit': {
            'columns': ['hostgroup_num_services_crit'],
            'short': 'C',
            'title': 'Number of services in state CRIT (Host Group)'
        },
        'hg_num_services_ok': {
            'columns': ['hostgroup_num_services_ok'],
            'short': 'O',
            'title': 'Number of services in state OK (Host Group)'
        },
        'hg_num_services_pending': {
            'columns': ['hostgroup_num_services_pending'],
            'short': 'P',
            'title': 'Number of services in state PENDING (Host Group)'
        },
        'hg_num_services_unknown': {
            'columns': ['hostgroup_num_services_unknown'],
            'short': 'U',
            'title': 'Number of services in state UNKNOWN (Host Group)'
        },
        'hg_num_services_warn': {
            'columns': ['hostgroup_num_services_warn'],
            'short': 'W',
            'title': 'Number of services in state WARN (Host Group)'
        },
        'history_addinfo': {
            'columns': ['history_addinfo'],
            'short': 'Info',
            'title': 'Additional Information'
        },
        'history_line': {
            'columns': ['history_line'],
            'short': 'Line',
            'title': 'Line number in log file'
        },
        'history_time': {
            'columns': ['history_time'],
            'options': ['ts_format', 'ts_date'],
            'short': 'Time',
            'title': 'Time of entry in logfile'
        },
        'history_what': {
            'columns': ['history_what'],
            'short': 'Action',
            'title': 'Type of event action'
        },
        'history_what_explained': {
            'columns': ['history_what'],
            'title': 'Explanation for event action'
        },
        'history_who': {
            'columns': ['history_who'],
            'short': 'Who',
            'title': 'User who performed action'
        },
        'host': {
            'columns': [
                'host_name', 'host_state', 'host_has_been_checked', 'host_scheduled_downtime_depth'
            ],
            'short': 'Host',
            'sorter': 'site_host',
            'title': 'Hostname, with configurable colors'
        },
        'host_acknowledged': {
            'columns': ['host_acknowledged'],
            'short': 'Ack',
            'title': 'Host problem acknowledged'
        },
        'host_address': {
            'columns': ['host_address'],
            'short': 'IP address',
            'title': 'Host address (Primary)'
        },
        'host_address_families': {
            'columns': ['host_custom_variable_names', 'host_custom_variable_values'],
            'short': 'Address families',
            'title': 'Host address families'
        },
        'host_address_family': {
            'columns': ['host_custom_variable_names', 'host_custom_variable_values'],
            'short': 'Address family',
            'title': 'Host address family (Primary)'
        },
        'host_addresses': {
            'columns': [
                'host_address', 'host_custom_variable_names', 'host_custom_variable_values'
            ],
            'short': 'IP addresses',
            'title': 'Host addresses'
        },
        'host_attempt': {
            'columns': ['host_current_attempt', 'host_max_check_attempts'],
            'short': 'Att.',
            'title': 'Current host check attempt'
        },
        'host_black': {
            'columns': ['site', 'host_name', 'host_state'],
            'short': 'Host',
            'sorter': 'site_host',
            'title': 'Hostname, red background if down or unreachable (Deprecated)'
        },
        'host_black_nagios': {
            'columns': ['site', 'host_name', 'host_state'],
            'short': 'Host',
            'sorter': 'site_host',
            'title': 'Hostname, red background if down, link to Nagios services'
        },
        'host_check_age': {
            'columns': ['host_has_been_checked', 'host_last_check'],
            'options': ['ts_format', 'ts_date'],
            'short': 'Checked',
            'title': 'The time since the last check of the host'
        },
        'host_check_command': {
            'columns': ['host_check_command'],
            'short': 'Check command',
            'title': 'Host check command'
        },
        'host_check_command_expanded': {
            'columns': ['host_check_command_expanded'],
            'short': 'Check command expanded',
            'title': 'Host check command expanded'
        },
        'host_check_duration': {
            'columns': ['host_execution_time'],
            'short': 'Duration',
            'title': 'Host check duration'
        },
        'host_check_interval': {
            'columns': ['host_check_interval', 'host_retry_interval'],
            'short': 'Interval',
            'title': 'Normal/retry check interval'
        },
        'host_check_latency': {
            'columns': ['host_latency'],
            'short': 'Latency',
            'title': 'Host check latency'
        },
        'host_check_type': {
            'columns': ['host_check_type'],
            'short': 'Type',
            'title': 'Host check type'
        },
        'host_childs': {
            'columns': ['host_childs'],
            'short': 'children',
            'title': "Host's children"
        },
        'host_comments': {
            'columns': ['host_comments_with_info'],
            'short': 'Comments',
            'title': 'Host comments'
        },
        'host_contact_groups': {
            'columns': ['host_contact_groups'],
            'short': 'Contact groups',
            'title': 'Host contact groups'
        },
        'host_contacts': {
            'columns': ['host_contacts'],
            'short': 'Contacts',
            'title': 'Host contacts'
        },
        'host_custom_notes': {
            'columns': ['host_name', 'host_address', 'host_plugin_output'],
            'short': 'Notes',
            'title': 'Custom host notes'
        },
        'host_custom_vars': {
            'columns': ['host_custom_variables'],
            'title': 'Host custom variables'
        },
        'host_filename': {
            'columns': ['host_filename'],
            'short': 'Filename',
            'title': 'Check_MK config filename'
        },
        'host_flapping': {
            'columns': ['host_is_flapping'],
            'short': 'Flap',
            'title': 'Host is flapping'
        },
        'host_graphs': {
            'columns': ['host_name', 'host_perf_data', 'host_metrics', 'host_check_command'],
            'options': ['pnp_timerange', 'graph_render_options'],
            'printable': 'time_graph',
            'title': 'Host Graphs with Timerange Previews'
        },
        'host_group_memberlist': {
            'columns': ['host_groups'],
            'short': 'Groups',
            'title': 'Host groups the host is member of'
        },
        'host_icons': {
            'columns': {
                'host_scheduled_downtime_depth',
                'host_in_check_period',
                'host_downtimes_with_extra_info',
                'site',
                'host_pnpgraph_present',
                'host_check_type',
                'host_accept_passive_checks',
                'host_icon_image',
                'host_is_flapping',
                'host_in_notification_period',
                'host_custom_variable_values',
                'host_modified_attributes_list',
                'host_filename',
                'host_acknowledged',
                'host_custom_variable_names',
                'host_action_url_expanded',
                'host_comments_with_extra_info',
                'host_in_service_period',
                'host_address',
                'host_staleness',
                'host_notifications_enabled',
                'host_active_checks_enabled',
                'host_perf_data',
                'host_check_command',
                'host_name',
                'host_notes_url_expanded',
            },
            'printable': False,
            'short': 'Icons',
            'title': 'Host icons'
        },
        'host_in_downtime': {
            'columns': ['host_scheduled_downtime_depth'],
            'short': 'Downtime',
            'title': 'Host in downtime'
        },
        'host_in_notifper': {
            'columns': ['host_in_notification_period'],
            'short': 'in notif. p.',
            'title': 'Host in notif. period'
        },
        'host_ipv4_address': {
            'columns': ['host_custom_variable_names', 'host_custom_variable_values'],
            'short': 'IPv4 address',
            'title': 'Host address (IPv4)'
        },
        'host_ipv6_address': {
            'columns': ['host_custom_variable_names', 'host_custom_variable_values'],
            'short': 'IPv6 address',
            'title': 'Host address (IPv6)'
        },
        'host_is_active': {
            'columns': ['host_active_checks_enabled'],
            'short': 'Active',
            'title': 'Host is active'
        },
        'host_is_stale': {
            'columns': ['host_staleness'],
            'short': 'Stale',
            'sorter': 'svc_staleness',
            'title': 'Host is stale'
        },
        'host_last_notification': {
            'columns': ['host_last_notification'],
            'options': ['ts_format', 'ts_date'],
            'short': 'last notification',
            'title': 'The time of the last host notification'
        },
        'host_nagios_link': {
            'columns': ['site', 'host_name'],
            'short': '',
            'title': 'Icon with link to host to Nagios GUI'
        },
        'host_next_check': {
            'columns': ['host_next_check'],
            'short': 'Next check',
            'title': 'The time of the next scheduled host check'
        },
        'host_next_notification': {
            'columns': ['host_next_notification'],
            'short': 'Next notification',
            'title': 'The time of the next host notification'
        },
        'host_normal_interval': {
            'columns': ['host_check_interval'],
            'short': 'Check int.',
            'title': 'Normal check interval'
        },
        'host_notification_number': {
            'columns': ['host_current_notification_number'],
            'short': 'N#',
            'title': 'Host notification number'
        },
        'host_notification_postponement_reason': {
            'columns': ['host_notification_postponement_reason'],
            'short': 'Notif. postponed',
            'title': 'Notification postponement reason'
        },
        'host_notifications_enabled': {
            'columns': ['host_notifications_enabled'],
            'short': 'Notif.',
            'title': 'Host notifications enabled'
        },
        'host_notifper': {
            'columns': ['host_notification_period'],
            'short': 'notif.',
            'title': 'Host notification period'
        },
        'host_parents': {
            'columns': ['host_parents'],
            'short': 'Parents',
            'title': "Host's parents"
        },
        'host_perf_data': {
            'columns': ['host_perf_data'],
            'short': 'Performance data',
            'title': 'Host performance data'
        },
        'host_plugin_output': {
            'columns': ['host_plugin_output', 'host_custom_variables'],
            'short': 'Summary',
            'title': 'Summary'
        },
        'host_pnpgraph': {
            'columns': ['host_name', 'host_perf_data', 'host_metrics', 'host_check_command'],
            'options': ['pnp_timerange'],
            'printable': 'time_graph',
            'short': 'Graph',
            'title': 'Host graph'
        },
        'host_retry_interval': {
            'columns': ['host_retry_interval'],
            'short': 'Retry',
            'title': 'Retry check interval'
        },
        'host_servicelevel': {
            'columns': ['host_custom_variable_names', 'host_custom_variable_values'],
            'short': 'Service Level',
            'sorter': 'servicelevel',
            'title': 'Host service level'
        },
        'host_services': {
            'columns': ['host_name', 'host_services_with_state'],
            'short': 'Services',
            'title': 'Services colored according to state'
        },
        'host_staleness': {
            'columns': ['host_staleness'],
            'short': 'Staleness',
            'title': 'Host staleness value'
        },
        'host_state': {
            'columns': ['host_has_been_checked', 'host_state'],
            'short': 'state',
            'sorter': 'hoststate',
            'title': 'Host state'
        },
        'host_state_age': {
            'columns': ['host_has_been_checked', 'host_last_state_change'],
            'options': ['ts_format', 'ts_date'],
            'short': 'Age',
            'title': 'The age of the current host state'
        },
        'host_state_onechar': {
            'columns': ['host_has_been_checked', 'host_state'],
            'short': 'S.',
            'sorter': 'hoststate',
            'title': 'Host state (first character)'
        },
        'host_tag_address_family': {
            "title": "Host tag: Address / IP Address Family ",
            "short": "IP Address Family ",
            "columns": ["host_custom_variables"],
        },
        'host_tag_agent': {
            "title": "Host tag: Data sources / Check_MK Agent",
            "short": "Check_MK Agent",
            "columns": ["host_custom_variables"],
        },
        'host_tag_snmp': {
            "title": "Host tag: Data sources / SNMP",
            "short": "SNMP",
            "columns": ["host_custom_variables"],
        },
        'host_tags': {
            'columns': ['host_custom_variable_names', 'host_custom_variable_values'],
            'short': 'Tags',
            'sorter': 'host',
            'title': 'Host tags (raw)'
        },
        'host_tags_with_titles': {
            'columns': ['host_custom_variable_names', 'host_custom_variable_values'],
            'short': 'Tags',
            'sorter': 'host',
            'title': 'Host tags (with titles)'
        },
        'host_with_state': {
            'columns': ['site', 'host_name', 'host_state', 'host_has_been_checked'],
            'short': 'Host',
            'sorter': 'site_host',
            'title': 'Hostname, marked red if down (Deprecated)'
        },
        'hostgroup_hosts': {
            'columns': ['hostgroup_members_with_state'],
            'short': 'Hosts',
            'title': 'Hosts colored according to state (Host Group)'
        },
        'invbackplane_description': {
            'columns': ['invbackplane_description'],
            'short': 'Description',
            'sorter': 'invbackplane_description',
            'title': 'Backplane: Description'
        },
        'invbackplane_index': {
            'columns': ['invbackplane_index'],
            'short': 'Index',
            'sorter': 'invbackplane_index',
            'title': 'Backplane: Index'
        },
        'invbackplane_location': {
            'columns': ['invbackplane_location'],
            'short': 'Location',
            'sorter': 'invbackplane_location',
            'title': 'Backplane: Location'
        },
        'invbackplane_manufacturer': {
            'columns': ['invbackplane_manufacturer'],
            'short': 'Manufacturer',
            'sorter': 'invbackplane_manufacturer',
            'title': 'Backplane: Manufacturer'
        },
        'invbackplane_model': {
            'columns': ['invbackplane_model'],
            'short': 'Model Name',
            'sorter': 'invbackplane_model',
            'title': 'Backplane: Model Name'
        },
        'invbackplane_name': {
            'columns': ['invbackplane_name'],
            'short': 'Name',
            'sorter': 'invbackplane_name',
            'title': 'Backplane: Name'
        },
        'invbackplane_serial': {
            'columns': ['invbackplane_serial'],
            'short': 'Serial Number',
            'sorter': 'invbackplane_serial',
            'title': 'Backplane: Serial Number'
        },
        'invbackplane_software': {
            'columns': ['invbackplane_software'],
            'short': 'Software',
            'sorter': 'invbackplane_software',
            'title': 'Backplane: Software'
        },
        'invchassis_description': {
            'columns': ['invchassis_description'],
            'short': 'Description',
            'sorter': 'invchassis_description',
            'title': 'Chassis: Description'
        },
        'invchassis_index': {
            'columns': ['invchassis_index'],
            'short': 'Index',
            'sorter': 'invchassis_index',
            'title': 'Chassis: Index'
        },
        'invchassis_location': {
            'columns': ['invchassis_location'],
            'short': 'Location',
            'sorter': 'invchassis_location',
            'title': 'Chassis: Location'
        },
        'invchassis_manufacturer': {
            'columns': ['invchassis_manufacturer'],
            'short': 'Manufacturer',
            'sorter': 'invchassis_manufacturer',
            'title': 'Chassis: Manufacturer'
        },
        'invchassis_model': {
            'columns': ['invchassis_model'],
            'short': 'Model Name',
            'sorter': 'invchassis_model',
            'title': 'Chassis: Model Name'
        },
        'invchassis_name': {
            'columns': ['invchassis_name'],
            'short': 'Name',
            'sorter': 'invchassis_name',
            'title': 'Chassis: Name'
        },
        'invchassis_serial': {
            'columns': ['invchassis_serial'],
            'short': 'Serial Number',
            'sorter': 'invchassis_serial',
            'title': 'Chassis: Serial Number'
        },
        'invchassis_software': {
            'columns': ['invchassis_software'],
            'short': 'Software',
            'sorter': 'invchassis_software',
            'title': 'Chassis: Software'
        },
        'invcontainer_description': {
            'columns': ['invcontainer_description'],
            'short': 'Description',
            'sorter': 'invcontainer_description',
            'title': 'HW container: Description'
        },
        'invcontainer_index': {
            'columns': ['invcontainer_index'],
            'short': 'Index',
            'sorter': 'invcontainer_index',
            'title': 'HW container: Index'
        },
        'invcontainer_location': {
            'columns': ['invcontainer_location'],
            'short': 'Location',
            'sorter': 'invcontainer_location',
            'title': 'HW container: Location'
        },
        'invcontainer_manufacturer': {
            'columns': ['invcontainer_manufacturer'],
            'short': 'Manufacturer',
            'sorter': 'invcontainer_manufacturer',
            'title': 'HW container: Manufacturer'
        },
        'invcontainer_model': {
            'columns': ['invcontainer_model'],
            'short': 'Model Name',
            'sorter': 'invcontainer_model',
            'title': 'HW container: Model Name'
        },
        'invcontainer_name': {
            'columns': ['invcontainer_name'],
            'short': 'Name',
            'sorter': 'invcontainer_name',
            'title': 'HW container: Name'
        },
        'invcontainer_serial': {
            'columns': ['invcontainer_serial'],
            'short': 'Serial Number',
            'sorter': 'invcontainer_serial',
            'title': 'HW container: Serial Number'
        },
        'invcontainer_software': {
            'columns': ['invcontainer_software'],
            'short': 'Software',
            'sorter': 'invcontainer_software',
            'title': 'HW container: Software'
        },
        'invdockercontainers_creation': {
            'columns': ['invdockercontainers_creation'],
            'short': 'Creation',
            'sorter': 'invdockercontainers_creation',
            'title': 'Docker containers: Creation'
        },
        'invdockercontainers_id': {
            'columns': ['invdockercontainers_id'],
            'short': 'ID',
            'sorter': 'invdockercontainers_id',
            'title': 'Docker containers: ID'
        },
        'invdockercontainers_labels': {
            'columns': ['invdockercontainers_labels'],
            'short': 'Labels',
            'sorter': 'invdockercontainers_labels',
            'title': 'Docker containers: Labels'
        },
        'invdockercontainers_name': {
            'columns': ['invdockercontainers_name'],
            'short': 'Name',
            'sorter': 'invdockercontainers_name',
            'title': 'Docker containers: Name'
        },
        'invdockercontainers_repository': {
            'columns': ['invdockercontainers_repository'],
            'short': 'Repository',
            'sorter': 'invdockercontainers_repository',
            'title': 'Docker containers: Repository'
        },
        'invdockercontainers_status': {
            'columns': ['invdockercontainers_status'],
            'short': 'Status',
            'sorter': 'invdockercontainers_status',
            'title': 'Docker containers: Status'
        },
        'invdockercontainers_tag': {
            'columns': ['invdockercontainers_tag'],
            'short': 'Tag',
            'sorter': 'invdockercontainers_tag',
            'title': 'Docker containers: Tag'
        },
        'invdockerimages_amount_containers': {
            'columns': ['invdockerimages_amount_containers'],
            'short': '# Containers',
            'sorter': 'invdockerimages_amount_containers',
            'title': 'Docker images: # Containers'
        },
        'invdockerimages_creation': {
            'columns': ['invdockerimages_creation'],
            'short': 'Creation',
            'sorter': 'invdockerimages_creation',
            'title': 'Docker images: Creation'
        },
        'invdockerimages_id': {
            'columns': ['invdockerimages_id'],
            'short': 'ID',
            'sorter': 'invdockerimages_id',
            'title': 'Docker images: ID'
        },
        'invdockerimages_labels': {
            'columns': ['invdockerimages_labels'],
            'short': 'Labels',
            'sorter': 'invdockerimages_labels',
            'title': 'Docker images: Labels'
        },
        'invdockerimages_repository': {
            'columns': ['invdockerimages_repository'],
            'short': 'Repository',
            'sorter': 'invdockerimages_repository',
            'title': 'Docker images: Repository'
        },
        'invdockerimages_size': {
            'columns': ['invdockerimages_size'],
            'short': 'Size',
            'sorter': 'invdockerimages_size',
            'title': 'Docker images: Size'
        },
        'invdockerimages_tag': {
            'columns': ['invdockerimages_tag'],
            'short': 'Tag',
            'sorter': 'invdockerimages_tag',
            'title': 'Docker images: Tag'
        },
        'inventory_tree': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'title': 'Hardware & Software Tree'
        },
        'invfan_description': {
            'columns': ['invfan_description'],
            'short': 'Description',
            'sorter': 'invfan_description',
            'title': 'Fan: Description'
        },
        'invfan_index': {
            'columns': ['invfan_index'],
            'short': 'Index',
            'sorter': 'invfan_index',
            'title': 'Fan: Index'
        },
        'invfan_location': {
            'columns': ['invfan_location'],
            'short': 'Location',
            'sorter': 'invfan_location',
            'title': 'Fan: Location'
        },
        'invfan_manufacturer': {
            'columns': ['invfan_manufacturer'],
            'short': 'Manufacturer',
            'sorter': 'invfan_manufacturer',
            'title': 'Fan: Manufacturer'
        },
        'invfan_model': {
            'columns': ['invfan_model'],
            'short': 'Model Name',
            'sorter': 'invfan_model',
            'title': 'Fan: Model Name'
        },
        'invfan_name': {
            'columns': ['invfan_name'],
            'short': 'Name',
            'sorter': 'invfan_name',
            'title': 'Fan: Name'
        },
        'invfan_serial': {
            'columns': ['invfan_serial'],
            'short': 'Serial Number',
            'sorter': 'invfan_serial',
            'title': 'Fan: Serial Number'
        },
        'invfan_software': {
            'columns': ['invfan_software'],
            'short': 'Software',
            'sorter': 'invfan_software',
            'title': 'Fan: Software'
        },
        'invhist_changed': {
            'columns': ['invhist_changed'],
            'short': 'changed',
            'title': 'changed entries'
        },
        'invhist_delta': {
            'columns': ['invhist_deltainvhist_time'],
            'title': 'Inventory changes'
        },
        'invhist_new': {
            'columns': ['invhist_new'],
            'short': 'new',
            'title': 'new entries'
        },
        'invhist_removed': {
            'columns': ['invhist_removed'],
            'short': 'Removed',
            'title': 'Removed entries'
        },
        'invhist_time': {
            'columns': ['invhist_time'],
            'options': ['ts_format', 'ts_date'],
            'short': 'Date/Time',
            'title': 'Inventory Date/Time'
        },
        'invinterface_admin_status': {
            'columns': ['invinterface_admin_status'],
            'short': 'Admin',
            'sorter': 'invinterface_admin_status',
            'title': 'Network interface: Administrative Status'
        },
        'invinterface_alias': {
            'columns': ['invinterface_alias'],
            'short': 'Alias',
            'sorter': 'invinterface_alias',
            'title': 'Network interface: Alias'
        },
        'invinterface_available': {
            'columns': ['invinterface_available'],
            'short': 'Used',
            'sorter': 'invinterface_available',
            'title': 'Network interface: Port Usage'
        },
        'invinterface_description': {
            'columns': ['invinterface_description'],
            'short': 'Description',
            'sorter': 'invinterface_description',
            'title': 'Network interface: Description'
        },
        'invinterface_index': {
            'columns': ['invinterface_index'],
            'short': 'Index',
            'sorter': 'invinterface_index',
            'title': 'Network interface: Index'
        },
        'invinterface_last_change': {
            'columns': ['invinterface_last_change'],
            'short': 'Last Change',
            'sorter': 'invinterface_last_change',
            'title': 'Network interface: Last Change'
        },
        'invinterface_oper_status': {
            'columns': ['invinterface_oper_status'],
            'short': 'Status',
            'sorter': 'invinterface_oper_status',
            'title': 'Network interface: Operational Status'
        },
        'invinterface_phys_address': {
            'columns': ['invinterface_phys_address'],
            'short': 'Physical Address (MAC)',
            'sorter': 'invinterface_phys_address',
            'title': 'Network interface: Physical Address (MAC)'
        },
        'invinterface_port_type': {
            'columns': ['invinterface_port_type'],
            'short': 'Type',
            'sorter': 'invinterface_port_type',
            'title': 'Network interface: Type'
        },
        'invinterface_speed': {
            'columns': ['invinterface_speed'],
            'short': 'Speed',
            'sorter': 'invinterface_speed',
            'title': 'Network interface: Speed'
        },
        'invinterface_vlans': {
            'columns': ['invinterface_vlans'],
            'short': 'VLANs',
            'sorter': 'invinterface_vlans',
            'title': 'Network interface: VLANs'
        },
        'invinterface_vlantype': {
            'columns': ['invinterface_vlantype'],
            'short': 'VLAN type',
            'sorter': 'invinterface_vlantype',
            'title': 'Network interface: VLAN type'
        },
        'invmodule_bootloader': {
            'columns': ['invmodule_bootloader'],
            'short': 'Bootloader',
            'sorter': 'invmodule_bootloader',
            'title': 'Module: Bootloader'
        },
        'invmodule_description': {
            'columns': ['invmodule_description'],
            'short': 'Description',
            'sorter': 'invmodule_description',
            'title': 'Module: Description'
        },
        'invmodule_firmware': {
            'columns': ['invmodule_firmware'],
            'short': 'Firmware',
            'sorter': 'invmodule_firmware',
            'title': 'Module: Firmware'
        },
        'invmodule_index': {
            'columns': ['invmodule_index'],
            'short': 'Index',
            'sorter': 'invmodule_index',
            'title': 'Module: Index'
        },
        'invmodule_location': {
            'columns': ['invmodule_location'],
            'short': 'Location',
            'sorter': 'invmodule_location',
            'title': 'Module: Location'
        },
        'invmodule_manufacturer': {
            'columns': ['invmodule_manufacturer'],
            'short': 'Manufacturer',
            'sorter': 'invmodule_manufacturer',
            'title': 'Module: Manufacturer'
        },
        'invmodule_model': {
            'columns': ['invmodule_model'],
            'short': 'Model Name',
            'sorter': 'invmodule_model',
            'title': 'Module: Model Name'
        },
        'invmodule_name': {
            'columns': ['invmodule_name'],
            'short': 'Name',
            'sorter': 'invmodule_name',
            'title': 'Module: Name'
        },
        'invmodule_serial': {
            'columns': ['invmodule_serial'],
            'short': 'Serial Number',
            'sorter': 'invmodule_serial',
            'title': 'Module: Serial Number'
        },
        'invmodule_software': {
            'columns': ['invmodule_software'],
            'short': 'Software',
            'sorter': 'invmodule_software',
            'title': 'Module: Software'
        },
        'invmodule_type': {
            'columns': ['invmodule_type'],
            'short': 'Type',
            'sorter': 'invmodule_type',
            'title': 'Module: Type'
        },
        'invoradataguardstats_db_unique': {
            'columns': ['invoradataguardstats_db_unique'],
            'short': 'Name',
            'sorter': 'invoradataguardstats_db_unique',
            'title': 'Oracle dataguard statistic: Name'
        },
        'invoradataguardstats_role': {
            'columns': ['invoradataguardstats_role'],
            'short': 'Role',
            'sorter': 'invoradataguardstats_role',
            'title': 'Oracle dataguard statistic: Role'
        },
        'invoradataguardstats_sid': {
            'columns': ['invoradataguardstats_sid'],
            'short': 'SID',
            'sorter': 'invoradataguardstats_sid',
            'title': 'Oracle dataguard statistic: SID'
        },
        'invoradataguardstats_switchover': {
            'columns': ['invoradataguardstats_switchover'],
            'short': 'Switchover',
            'sorter': 'invoradataguardstats_switchover',
            'title': 'Oracle dataguard statistic: Switchover'
        },
        'invorainstance_db_creation_time': {
            'columns': ['invorainstance_db_creation_time'],
            'short': 'Creation time',
            'sorter': 'invorainstance_db_creation_time',
            'title': 'Oracle instance: Creation time'
        },
        'invorainstance_db_uptime': {
            'columns': ['invorainstance_db_uptime'],
            'short': 'Uptime',
            'sorter': 'invorainstance_db_uptime',
            'title': 'Oracle instance: Uptime'
        },
        'invorainstance_logins': {
            'columns': ['invorainstance_logins'],
            'short': 'Logins',
            'sorter': 'invorainstance_logins',
            'title': 'Oracle instance: Logins'
        },
        'invorainstance_logmode': {
            'columns': ['invorainstance_logmode'],
            'short': 'Log mode',
            'sorter': 'invorainstance_logmode',
            'title': 'Oracle instance: Log mode'
        },
        'invorainstance_openmode': {
            'columns': ['invorainstance_openmode'],
            'short': 'Open mode',
            'sorter': 'invorainstance_openmode',
            'title': 'Oracle instance: Open mode'
        },
        'invorainstance_sid': {
            'columns': ['invorainstance_sid'],
            'short': 'SID',
            'sorter': 'invorainstance_sid',
            'title': 'Oracle instance: SID'
        },
        'invorainstance_version': {
            'columns': ['invorainstance_version'],
            'short': 'Version',
            'sorter': 'invorainstance_version',
            'title': 'Oracle instance: Version'
        },
        'invorarecoveryarea_flashback': {
            'columns': ['invorarecoveryarea_flashback'],
            'short': 'Flashback',
            'sorter': 'invorarecoveryarea_flashback',
            'title': 'Oracle recovery area: Flashback'
        },
        'invorarecoveryarea_sid': {
            'columns': ['invorarecoveryarea_sid'],
            'short': 'SID',
            'sorter': 'invorarecoveryarea_sid',
            'title': 'Oracle recovery area: SID'
        },
        'invorasga_buf_cache_size': {
            'columns': ['invorasga_buf_cache_size'],
            'short': 'Buffer cache size',
            'sorter': 'invorasga_buf_cache_size',
            'title': 'Oracle performance: Buffer cache size'
        },
        'invorasga_data_trans_cache_size': {
            'columns': ['invorasga_data_trans_cache_size'],
            'short': 'Data transfer cache size',
            'sorter': 'invorasga_data_trans_cache_size',
            'title': 'Oracle performance: Data transfer cache size'
        },
        'invorasga_fixed_size': {
            'columns': ['invorasga_fixed_size'],
            'short': 'Fixed size',
            'sorter': 'invorasga_fixed_size',
            'title': 'Oracle performance: Fixed size'
        },
        'invorasga_free_mem_avail': {
            'columns': ['invorasga_free_mem_avail'],
            'short': 'Free SGA memory available',
            'sorter': 'invorasga_free_mem_avail',
            'title': 'Oracle performance: Free SGA memory available'
        },
        'invorasga_granule_size': {
            'columns': ['invorasga_granule_size'],
            'short': 'Granule size',
            'sorter': 'invorasga_granule_size',
            'title': 'Oracle performance: Granule size'
        },
        'invorasga_in_mem_area_size': {
            'columns': ['invorasga_in_mem_area_size'],
            'short': 'In-memory area',
            'sorter': 'invorasga_in_mem_area_size',
            'title': 'Oracle performance: In-memory area'
        },
        'invorasga_java_pool_size': {
            'columns': ['invorasga_java_pool_size'],
            'short': 'Java pool size',
            'sorter': 'invorasga_java_pool_size',
            'title': 'Oracle performance: Java pool size'
        },
        'invorasga_large_pool_size': {
            'columns': ['invorasga_large_pool_size'],
            'short': 'Large pool size',
            'sorter': 'invorasga_large_pool_size',
            'title': 'Oracle performance: Large pool size'
        },
        'invorasga_max_size': {
            'columns': ['invorasga_max_size'],
            'short': 'Maximum size',
            'sorter': 'invorasga_max_size',
            'title': 'Oracle performance: Maximum size'
        },
        'invorasga_redo_buffer': {
            'columns': ['invorasga_redo_buffer'],
            'short': 'Redo buffers',
            'sorter': 'invorasga_redo_buffer',
            'title': 'Oracle performance: Redo buffers'
        },
        'invorasga_shared_io_pool_size': {
            'columns': ['invorasga_shared_io_pool_size'],
            'short': 'Shared pool size',
            'sorter': 'invorasga_shared_io_pool_size',
            'title': 'Oracle performance: Shared pool size'
        },
        'invorasga_shared_pool_size': {
            'columns': ['invorasga_shared_pool_size'],
            'short': 'Shared pool size',
            'sorter': 'invorasga_shared_pool_size',
            'title': 'Oracle performance: Shared pool size'
        },
        'invorasga_sid': {
            'columns': ['invorasga_sid'],
            'short': 'SID',
            'sorter': 'invorasga_sid',
            'title': 'Oracle performance: SID'
        },
        'invorasga_start_oh_shared_pool': {
            'columns': ['invorasga_start_oh_shared_pool'],
            'short': 'Startup overhead in shared pool',
            'sorter': 'invorasga_start_oh_shared_pool',
            'title': 'Oracle performance: Startup overhead in shared pool'
        },
        'invorasga_streams_pool_size': {
            'columns': ['invorasga_streams_pool_size'],
            'short': 'Streams pool size',
            'sorter': 'invorasga_streams_pool_size',
            'title': 'Oracle performance: Streams pool size'
        },
        'invoratablespace_autoextensible': {
            'columns': ['invoratablespace_autoextensible'],
            'short': 'Autoextensible',
            'sorter': 'invoratablespace_autoextensible',
            'title': 'Oracle tablespace: Autoextensible'
        },
        'invoratablespace_current_size': {
            'columns': ['invoratablespace_current_size'],
            'short': 'Current size',
            'sorter': 'invoratablespace_current_size',
            'title': 'Oracle tablespace: Current size'
        },
        'invoratablespace_free_space': {
            'columns': ['invoratablespace_free_space'],
            'short': 'Free space',
            'sorter': 'invoratablespace_free_space',
            'title': 'Oracle tablespace: Free space'
        },
        'invoratablespace_increment_size': {
            'columns': ['invoratablespace_increment_size'],
            'short': 'Increment size',
            'sorter': 'invoratablespace_increment_size',
            'title': 'Oracle tablespace: Increment size'
        },
        'invoratablespace_max_size': {
            'columns': ['invoratablespace_max_size'],
            'short': 'Max. size',
            'sorter': 'invoratablespace_max_size',
            'title': 'Oracle tablespace: Max. size'
        },
        'invoratablespace_name': {
            'columns': ['invoratablespace_name'],
            'short': 'Name',
            'sorter': 'invoratablespace_name',
            'title': 'Oracle tablespace: Name'
        },
        'invoratablespace_num_increments': {
            'columns': ['invoratablespace_num_increments'],
            'short': 'Number of increments',
            'sorter': 'invoratablespace_num_increments',
            'title': 'Oracle tablespace: Number of increments'
        },
        'invoratablespace_sid': {
            'columns': ['invoratablespace_sid'],
            'short': 'SID',
            'sorter': 'invoratablespace_sid',
            'title': 'Oracle tablespace: SID'
        },
        'invoratablespace_type': {
            'columns': ['invoratablespace_type'],
            'short': 'Type',
            'sorter': 'invoratablespace_type',
            'title': 'Oracle tablespace: Type'
        },
        'invoratablespace_used_size': {
            'columns': ['invoratablespace_used_size'],
            'short': 'Used size',
            'sorter': 'invoratablespace_used_size',
            'title': 'Oracle tablespace: Used size'
        },
        'invoratablespace_version': {
            'columns': ['invoratablespace_version'],
            'short': 'Version',
            'sorter': 'invoratablespace_version',
            'title': 'Oracle tablespace: Version'
        },
        'invother_description': {
            'columns': ['invother_description'],
            'short': 'Description',
            'sorter': 'invother_description',
            'title': 'Other entity: Description'
        },
        'invother_index': {
            'columns': ['invother_index'],
            'short': 'Index',
            'sorter': 'invother_index',
            'title': 'Other entity: Index'
        },
        'invother_location': {
            'columns': ['invother_location'],
            'short': 'Location',
            'sorter': 'invother_location',
            'title': 'Other entity: Location'
        },
        'invother_manufacturer': {
            'columns': ['invother_manufacturer'],
            'short': 'Manufacturer',
            'sorter': 'invother_manufacturer',
            'title': 'Other entity: Manufacturer'
        },
        'invother_model': {
            'columns': ['invother_model'],
            'short': 'Model Name',
            'sorter': 'invother_model',
            'title': 'Other entity: Model Name'
        },
        'invother_name': {
            'columns': ['invother_name'],
            'short': 'Name',
            'sorter': 'invother_name',
            'title': 'Other entity: Name'
        },
        'invother_serial': {
            'columns': ['invother_serial'],
            'short': 'Serial Number',
            'sorter': 'invother_serial',
            'title': 'Other entity: Serial Number'
        },
        'invother_software': {
            'columns': ['invother_software'],
            'short': 'Software',
            'sorter': 'invother_software',
            'title': 'Other entity: Software'
        },
        'invpsu_description': {
            'columns': ['invpsu_description'],
            'short': 'Description',
            'sorter': 'invpsu_description',
            'title': 'Power supply: Description'
        },
        'invpsu_index': {
            'columns': ['invpsu_index'],
            'short': 'Index',
            'sorter': 'invpsu_index',
            'title': 'Power supply: Index'
        },
        'invpsu_location': {
            'columns': ['invpsu_location'],
            'short': 'Location',
            'sorter': 'invpsu_location',
            'title': 'Power supply: Location'
        },
        'invpsu_manufacturer': {
            'columns': ['invpsu_manufacturer'],
            'short': 'Manufacturer',
            'sorter': 'invpsu_manufacturer',
            'title': 'Power supply: Manufacturer'
        },
        'invpsu_model': {
            'columns': ['invpsu_model'],
            'short': 'Model Name',
            'sorter': 'invpsu_model',
            'title': 'Power supply: Model Name'
        },
        'invpsu_name': {
            'columns': ['invpsu_name'],
            'short': 'Name',
            'sorter': 'invpsu_name',
            'title': 'Power supply: Name'
        },
        'invpsu_serial': {
            'columns': ['invpsu_serial'],
            'short': 'Serial Number',
            'sorter': 'invpsu_serial',
            'title': 'Power supply: Serial Number'
        },
        'invpsu_software': {
            'columns': ['invpsu_software'],
            'short': 'Software',
            'sorter': 'invpsu_software',
            'title': 'Power supply: Software'
        },
        'invsensor_description': {
            'columns': ['invsensor_description'],
            'short': 'Description',
            'sorter': 'invsensor_description',
            'title': 'Sensor: Description'
        },
        'invsensor_index': {
            'columns': ['invsensor_index'],
            'short': 'Index',
            'sorter': 'invsensor_index',
            'title': 'Sensor: Index'
        },
        'invsensor_location': {
            'columns': ['invsensor_location'],
            'short': 'Location',
            'sorter': 'invsensor_location',
            'title': 'Sensor: Location'
        },
        'invsensor_manufacturer': {
            'columns': ['invsensor_manufacturer'],
            'short': 'Manufacturer',
            'sorter': 'invsensor_manufacturer',
            'title': 'Sensor: Manufacturer'
        },
        'invsensor_model': {
            'columns': ['invsensor_model'],
            'short': 'Model Name',
            'sorter': 'invsensor_model',
            'title': 'Sensor: Model Name'
        },
        'invsensor_name': {
            'columns': ['invsensor_name'],
            'short': 'Name',
            'sorter': 'invsensor_name',
            'title': 'Sensor: Name'
        },
        'invsensor_serial': {
            'columns': ['invsensor_serial'],
            'short': 'Serial Number',
            'sorter': 'invsensor_serial',
            'title': 'Sensor: Serial Number'
        },
        'invsensor_software': {
            'columns': ['invsensor_software'],
            'short': 'Software',
            'sorter': 'invsensor_software',
            'title': 'Sensor: Software'
        },
        'invstack_description': {
            'columns': ['invstack_description'],
            'short': 'Description',
            'sorter': 'invstack_description',
            'title': 'Stack: Description'
        },
        'invstack_index': {
            'columns': ['invstack_index'],
            'short': 'Index',
            'sorter': 'invstack_index',
            'title': 'Stack: Index'
        },
        'invstack_location': {
            'columns': ['invstack_location'],
            'short': 'Location',
            'sorter': 'invstack_location',
            'title': 'Stack: Location'
        },
        'invstack_manufacturer': {
            'columns': ['invstack_manufacturer'],
            'short': 'Manufacturer',
            'sorter': 'invstack_manufacturer',
            'title': 'Stack: Manufacturer'
        },
        'invstack_model': {
            'columns': ['invstack_model'],
            'short': 'Model Name',
            'sorter': 'invstack_model',
            'title': 'Stack: Model Name'
        },
        'invstack_name': {
            'columns': ['invstack_name'],
            'short': 'Name',
            'sorter': 'invstack_name',
            'title': 'Stack: Name'
        },
        'invstack_serial': {
            'columns': ['invstack_serial'],
            'short': 'Serial Number',
            'sorter': 'invstack_serial',
            'title': 'Stack: Serial Number'
        },
        'invstack_software': {
            'columns': ['invstack_software'],
            'short': 'Software',
            'sorter': 'invstack_software',
            'title': 'Stack: Software'
        },
        'invswpac_arch': {
            'columns': ['invswpac_arch'],
            'short': 'Architecture',
            'sorter': 'invswpac_arch',
            'title': 'Software package: Architecture'
        },
        'invswpac_install_date': {
            'columns': ['invswpac_install_date'],
            'short': 'Install Date',
            'sorter': 'invswpac_install_date',
            'title': 'Software package: Install Date'
        },
        'invswpac_name': {
            'columns': ['invswpac_name'],
            'short': 'Name',
            'sorter': 'invswpac_name',
            'title': 'Software package: Name'
        },
        'invswpac_package_type': {
            'columns': ['invswpac_package_type'],
            'short': 'Type',
            'sorter': 'invswpac_package_type',
            'title': 'Software package: Type'
        },
        'invswpac_package_version': {
            'columns': ['invswpac_package_version'],
            'short': 'Package Version',
            'sorter': 'invswpac_package_version',
            'title': 'Software package: Package Version'
        },
        'invswpac_path': {
            'columns': ['invswpac_path'],
            'short': 'Path',
            'sorter': 'invswpac_path',
            'title': 'Software package: Path'
        },
        'invswpac_size': {
            'columns': ['invswpac_size'],
            'short': 'Size',
            'sorter': 'invswpac_size',
            'title': 'Software package: Size'
        },
        'invswpac_summary': {
            'columns': ['invswpac_summary'],
            'short': 'Description',
            'sorter': 'invswpac_summary',
            'title': 'Software package: Description'
        },
        'invswpac_vendor': {
            'columns': ['invswpac_vendor'],
            'short': 'Publisher',
            'sorter': 'invswpac_vendor',
            'title': 'Software package: Publisher'
        },
        'invswpac_version': {
            'columns': ['invswpac_version'],
            'short': 'Version',
            'sorter': 'invswpac_version',
            'title': 'Software package: Version'
        },
        'invunknown_description': {
            'columns': ['invunknown_description'],
            'short': 'Description',
            'sorter': 'invunknown_description',
            'title': 'Unknown entity: Description'
        },
        'invunknown_index': {
            'columns': ['invunknown_index'],
            'short': 'Index',
            'sorter': 'invunknown_index',
            'title': 'Unknown entity: Index'
        },
        'invunknown_location': {
            'columns': ['invunknown_location'],
            'short': 'Location',
            'sorter': 'invunknown_location',
            'title': 'Unknown entity: Location'
        },
        'invunknown_manufacturer': {
            'columns': ['invunknown_manufacturer'],
            'short': 'Manufacturer',
            'sorter': 'invunknown_manufacturer',
            'title': 'Unknown entity: Manufacturer'
        },
        'invunknown_model': {
            'columns': ['invunknown_model'],
            'short': 'Model Name',
            'sorter': 'invunknown_model',
            'title': 'Unknown entity: Model Name'
        },
        'invunknown_name': {
            'columns': ['invunknown_name'],
            'short': 'Name',
            'sorter': 'invunknown_name',
            'title': 'Unknown entity: Name'
        },
        'invunknown_serial': {
            'columns': ['invunknown_serial'],
            'short': 'Serial Number',
            'sorter': 'invunknown_serial',
            'title': 'Unknown entity: Serial Number'
        },
        'invunknown_software': {
            'columns': ['invunknown_software'],
            'short': 'Software',
            'sorter': 'invunknown_software',
            'title': 'Unknown entity: Software'
        },
        'log_attempt': {
            'columns': ['log_attempt'],
            'short': 'Att.',
            'title': 'Log: number of check attempt'
        },
        'log_command': {
            'columns': ['log_command_name'],
            'short': 'Command',
            'title': 'Log: command/plugin'
        },
        'log_comment': {
            'columns': ['log_options'],
            'short': 'Comment',
            'title': 'Log: comment'
        },
        'log_contact_name': {
            'columns': ['log_contact_name'],
            'short': 'Contact',
            'title': 'Log: contact name'
        },
        'log_date': {
            'columns': ['log_time'],
            'short': 'Date',
            'title': 'Log: day of entry'
        },
        'log_icon': {
            'columns': ['log_type', 'log_state', 'log_state_type', 'log_command_name'],
            'short': '',
            'title': 'Log: event icon'
        },
        'log_lineno': {
            'columns': ['log_lineno'],
            'short': 'Line',
            'title': 'Log: line number in log file'
        },
        'log_message': {
            'columns': ['log_message'],
            'short': 'Message',
            'title': 'Log: complete message'
        },
        'log_options': {
            'columns': ['log_options'],
            'short': 'Info',
            'title': 'Log: informational part of message'
        },
        'log_plugin_output': {
            'columns': [
                'log_plugin_output', 'log_type', 'log_state_type', 'log_comment', 'custom_variables'
            ],
            'short': 'Output',
            'title': 'Log: Output'
        },
        'log_state': {
            'columns': ['log_state', 'log_state_type', 'log_service_description', 'log_type'],
            'short': 'State',
            'title': 'Log: state of host/service at log time'
        },
        'log_state_type': {
            'columns': ['log_state_type'],
            'short': 'Type',
            'title': 'Log: type of state (hard/soft/stopped/started)'
        },
        'log_time': {
            'columns': ['log_time'],
            'options': ['ts_format', 'ts_date'],
            'short': 'Time',
            'title': 'Log: entry time'
        },
        'log_type': {
            'columns': ['log_type'],
            'short': 'Event',
            'title': 'Log: event'
        },
        'log_what': {
            'columns': ['log_type'],
            'short': 'Host/Service',
            'title': 'Log: host or service'
        },
        'num_problems': {
            'columns': ['host_num_services', 'host_num_services_ok', 'host_num_services_pending'],
            'short': 'Pro.',
            'title': 'Number of problems'
        },
        'num_services': {
            'columns': ['host_num_services'],
            'short': '',
            'title': 'Number of services'
        },
        'num_services_crit': {
            'columns': ['host_num_services_crit'],
            'short': 'Cr',
            'title': 'Number of services in state CRIT'
        },
        'num_services_ok': {
            'columns': ['host_num_services_ok'],
            'short': 'OK',
            'title': 'Number of services in state OK'
        },
        'num_services_pending': {
            'columns': ['host_num_services_pending'],
            'short': 'Pd',
            'title': 'Number of services in state PENDING'
        },
        'num_services_unknown': {
            'columns': ['host_num_services_unknown'],
            'short': 'Un',
            'title': 'Number of services in state UNKNOWN'
        },
        'num_services_warn': {
            'columns': ['host_num_services_warn'],
            'short': 'Wa',
            'title': 'Number of services in state WARN'
        },
        'perfometer': {
            'columns': [
                'service_staleness', 'service_perf_data', 'service_state', 'service_check_command',
                'service_pnpgraph_present', 'service_plugin_output'
            ],
            'printable': 'perfometer',
            'short': 'Perf-O-Meter',
            'title': 'Service Perf-O-Meter'
        },
        'service_description': {
            'columns': ['service_description'],
            'short': 'Service',
            'sorter': 'svcdescr',
            'title': 'Service description'
        },
        'service_discovery_check': {
            'columns': ['discovery_state', 'discovery_check', 'discovery_service'],
            'short': 'Check type',
            'title': 'Service discovery: Check type'
        },
        'service_discovery_service': {
            'columns': ['discovery_state', 'discovery_check', 'discovery_service'],
            'short': 'Service description',
            'title': 'Service discovery: Service description'
        },
        'service_discovery_state': {
            'columns': ['discovery_state'],
            'short': 'State',
            'title': 'Service discovery: State'
        },
        'service_display_name': {
            'columns': ['service_display_name'],
            'short': 'Display name',
            'sorter': 'svcdispname',
            'title': 'Service alternative display name'
        },
        'service_graphs': {
            'columns': [
                'host_name', 'service_description', 'service_perf_data', 'service_metrics',
                'service_check_command'
            ],
            'options': ['pnp_timerange', 'graph_render_options'],
            'printable': 'time_graph',
            'title': 'Service Graphs with Timerange Previews'
        },
        'service_icons': {
            'columns': {
                'host_scheduled_downtime_depth',
                'service_check_command',
                'host_downtimes_with_extra_info',
                'site',
                'service_cached_at',
                'service_notifications_enabled',
                'service_downtimes_with_extra_info',
                'host_check_type',
                'service_active_passive_checks',
                'service_in_passive_check_period',
                'service_comments_with_extra_info',
                'service_host_name',
                'service_cache_interval',
                'service_action_url_expanded',
                'service_custom_variable_names',
                'service_perf_data',
                'service_in_service_period',
                'host_check_command',
                'host_filename',
                'service_scheduled_downtime_depth',
                'host_custom_variable_names',
                'service_icon_image',
                'service_notes_url_expanded',
                'service_modified_attributes_list',
                'service_custom_variable_values',
                'service_acknowledged',
                'service_plugin_output',
                'service_staleness',
                'service_description',
                'host_address',
                'service_in_notification_period',
                'service_service_description',
                'service_active_checks_enabled',
                'service_check_type',
                'service_pnpgraph_present',
                'service_in_check_period',
                'host_custom_variable_values',
                'host_name',
                'service_is_flapping',
                'service_state',
            },
            'printable': False,
            'short': 'Icons',
            'title': 'Service icons'
        },
        'service_nagios_link': {
            'columns': ['site', 'host_name', 'service_description'],
            'short': '',
            'title': 'Icon with link to service in Nagios GUI'
        },
        'service_state': {
            'columns': ['service_has_been_checked', 'service_state'],
            'short': 'State',
            'sorter': 'svcstate',
            'title': 'Service state'
        },
        'sg_alias': {
            'columns': ['servicegroup_alias'],
            'short': 'Alias',
            'title': 'Servicegroup alias'
        },
        'sg_name': {
            'columns': ['servicegroup_name'],
            'short': 'Name',
            'title': 'Servicegroup name'
        },
        'sg_num_services': {
            'columns': ['servicegroup_num_services'],
            'short': '',
            'title': 'Number of services (Service Group)'
        },
        'sg_num_services_crit': {
            'columns': ['servicegroup_num_services_crit'],
            'short': 'C',
            'title': 'Number of services in state CRIT (Service Group)'
        },
        'sg_num_services_ok': {
            'columns': ['servicegroup_num_services_ok'],
            'short': 'O',
            'title': 'Number of services in state OK (Service Group)'
        },
        'sg_num_services_pending': {
            'columns': ['servicegroup_num_services_pending'],
            'short': 'P',
            'title': 'Number of services in state PENDING (Service Group)'
        },
        'sg_num_services_unknown': {
            'columns': ['servicegroup_num_services_unknown'],
            'short': 'U',
            'title': 'Number of services in state UNKNOWN (Service Group)'
        },
        'sg_num_services_warn': {
            'columns': ['servicegroup_num_services_warn'],
            'short': 'W',
            'title': 'Number of services in state WARN (Service Group)'
        },
        'sg_services': {
            'columns': ['servicegroup_members_with_state'],
            'short': 'Services',
            'title': 'Services colored according to state (Service Group)'
        },
        'site_icon': {
            'columns': ['site'],
            'short': '',
            'sorter': 'site',
            'title': 'Site icon'
        },
        'sitealias': {
            'columns': ['site'],
            'title': 'Site alias'
        },
        'sitename_plain': {
            'columns': ['site'],
            'short': 'Site',
            'sorter': 'site',
            'title': 'Site ID'
        },
        'sla_fixed': {
            'columns': [
                'host_name', 'host_perf_data', 'host_metrics', 'host_check_command',
                'service_custom_variables'
            ],
            'printable': 'sla_printer',
            'short': ("func", None),
            'title': ("func", None)
        },
        'sla_specific': {
            'columns': [
                'host_name', 'host_perf_data', 'host_metrics', 'host_check_command',
                'service_custom_variables'
            ],
            'printable': 'sla_printer',
            'short': ("func", None),
            'title': ("func", None)
        },
        'svc_acknowledged': {
            'columns': ['service_acknowledged'],
            'short': 'Ack',
            'title': 'Service problem acknowledged'
        },
        'svc_attempt': {
            'columns': ['service_current_attempt', 'service_max_check_attempts'],
            'short': 'Att.',
            'title': 'Current check attempt'
        },
        'svc_check_age': {
            'columns': ['service_has_been_checked', 'service_last_check', 'service_cached_at'],
            'options': ['ts_format', 'ts_date'],
            'short': 'Checked',
            'title': 'The time since the last check of the service'
        },
        'svc_check_cache_info': {
            'columns': ['service_last_check', 'service_cached_at', 'service_cache_interval'],
            'options': ['ts_format', 'ts_date'],
            'short': 'Cached',
            'title': 'Cached agent data'
        },
        'svc_check_command': {
            'columns': ['service_check_command'],
            'short': 'Check command',
            'title': 'Service check command'
        },
        'svc_check_command_expanded': {
            'columns': ['service_check_command_expanded'],
            'short': 'Check command expanded',
            'title': 'Service check command expanded'
        },
        'svc_check_duration': {
            'columns': ['service_execution_time'],
            'short': 'Duration',
            'title': 'Service check duration'
        },
        'svc_check_interval': {
            'columns': ['service_check_interval', 'service_retry_interval'],
            'short': 'Interval',
            'title': 'Service normal/retry check interval'
        },
        'svc_check_latency': {
            'columns': ['service_latency'],
            'short': 'Latency',
            'title': 'Service check latency'
        },
        'svc_check_period': {
            'columns': ['service_check_period'],
            'short': 'check.',
            'title': 'Service check period'
        },
        'svc_check_type': {
            'columns': ['service_check_type'],
            'short': 'Type',
            'title': 'Service check type'
        },
        'svc_comments': {
            'columns': ['service_comments_with_info'],
            'short': 'Comments',
            'title': 'Service Comments'
        },
        'svc_contact_groups': {
            'columns': ['service_contact_groups'],
            'short': 'Contact groups',
            'title': 'Service contact groups'
        },
        'svc_contacts': {
            'columns': ['service_contacts'],
            'short': 'Contacts',
            'title': 'Service contacts'
        },
        'svc_custom_notes': {
            'columns': [
                'host_name', 'host_address', 'service_description', 'service_plugin_output'
            ],
            'short': 'Notes',
            'title': 'Custom services notes'
        },
        'svc_custom_vars': {
            'columns': ['service_custom_variables'],
            'title': 'Service custom variables'
        },
        'svc_flapping': {
            'columns': ['service_is_flapping'],
            'short': 'Flap',
            'title': 'Service is flapping'
        },
        'svc_group_memberlist': {
            'columns': ['service_groups'],
            'short': 'Groups',
            'title': 'Service groups the service is member of'
        },
        'svc_in_downtime': {
            'columns': ['service_scheduled_downtime_depth'],
            'short': 'Dt.',
            'title': 'Currently in downtime'
        },
        'svc_in_notifper': {
            'columns': ['service_in_notification_period'],
            'short': 'in notif. p.',
            'title': 'In notification period'
        },
        'svc_is_active': {
            'columns': ['service_active_checks_enabled'],
            'short': 'Active',
            'title': 'Service is active'
        },
        'svc_is_stale': {
            'columns': ['service_staleness'],
            'short': 'Stale',
            'sorter': 'svc_staleness',
            'title': 'Service is stale'
        },
        'svc_last_notification': {
            'columns': ['service_last_notification'],
            'options': ['ts_format', 'ts_date'],
            'short': 'last notification',
            'title': 'The time of the last service notification'
        },
        'svc_last_time_ok': {
            'columns': ['service_last_time_ok', 'service_has_been_checked'],
            'short': 'Last OK',
            'title': 'The last time the service was OK'
        },
        'svc_long_plugin_output': {
            'columns': ['service_long_plugin_output', 'service_custom_variables'],
            'short': 'Details',
            'title': 'Details',
        },
        'svc_metrics': {
            'columns': ['service_check_command', 'service_perf_data'],
            'printable': False,
            'short': 'Metrics',
            'title': 'Service Metrics'
        },
        'svc_next_check': {
            'columns': ['service_next_check'],
            'short': 'Next check',
            'title': 'The time of the next scheduled service check'
        },
        'svc_next_notification': {
            'columns': ['service_next_notification'],
            'short': 'Next notification',
            'title': 'The time of the next service notification'
        },
        'svc_normal_interval': {
            'columns': ['service_check_interval'],
            'short': 'Check int.',
            'title': 'Service normal check interval'
        },
        'svc_notification_number': {
            'columns': ['service_current_notification_number'],
            'short': 'N#',
            'title': 'Service notification number'
        },
        'svc_notification_postponement_reason': {
            'columns': ['service_notification_postponement_reason'],
            'short': 'Notif. postponed',
            'title': 'Notification postponement reason'
        },
        'svc_notifications_enabled': {
            'columns': ['service_notifications_enabled'],
            'short': 'Notif.',
            'title': 'Service notifications enabled'
        },
        'svc_notifper': {
            'columns': ['service_notification_period'],
            'short': 'notif.',
            'title': 'Service notification period'
        },
        'svc_perf_data': {
            'columns': ['service_perf_data'],
            'short': 'Perfdata',
            'title': 'Service performance data (source code)'
        },
        'svc_perf_val01': {
            'columns': ['service_perf_data'],
            'short': 'Val. 1',
            'title': 'Service performance data - value number  1'
        },
        'svc_perf_val02': {
            'columns': ['service_perf_data'],
            'short': 'Val. 2',
            'title': 'Service performance data - value number  2'
        },
        'svc_perf_val03': {
            'columns': ['service_perf_data'],
            'short': 'Val. 3',
            'title': 'Service performance data - value number  3'
        },
        'svc_perf_val04': {
            'columns': ['service_perf_data'],
            'short': 'Val. 4',
            'title': 'Service performance data - value number  4'
        },
        'svc_perf_val05': {
            'columns': ['service_perf_data'],
            'short': 'Val. 5',
            'title': 'Service performance data - value number  5'
        },
        'svc_perf_val06': {
            'columns': ['service_perf_data'],
            'short': 'Val. 6',
            'title': 'Service performance data - value number  6'
        },
        'svc_perf_val07': {
            'columns': ['service_perf_data'],
            'short': 'Val. 7',
            'title': 'Service performance data - value number  7'
        },
        'svc_perf_val08': {
            'columns': ['service_perf_data'],
            'short': 'Val. 8',
            'title': 'Service performance data - value number  8'
        },
        'svc_perf_val09': {
            'columns': ['service_perf_data'],
            'short': 'Val. 9',
            'title': 'Service performance data - value number  9'
        },
        'svc_perf_val10': {
            'columns': ['service_perf_data'],
            'short': 'Val. 10',
            'title': 'Service performance data - value number 10'
        },
        'svc_plugin_output': {
            'columns': ['service_plugin_output', 'service_custom_variables'],
            'short': 'Summary',
            'sorter': 'svcoutput',
            'title': 'Summary'
        },
        'svc_pnpgraph': {
            'columns': [
                'host_name', 'service_description', 'service_perf_data', 'service_metrics',
                'service_check_command'
            ],
            'options': ['pnp_timerange'],
            'printable': 'time_graph',
            'title': 'Service Graphs'
        },
        'svc_retry_interval': {
            'columns': ['service_retry_interval'],
            'short': 'Retry',
            'title': 'Service retry check interval'
        },
        'svc_servicelevel': {
            'columns': ['service_custom_variable_names', 'service_custom_variable_values'],
            'short': 'Service Level',
            'sorter': 'servicelevel',
            'title': 'Service service level'
        },
        'svc_staleness': {
            'columns': ['service_staleness'],
            'short': 'Staleness',
            'title': 'Service staleness value'
        },
        'svc_state_age': {
            'columns': ['service_has_been_checked', 'service_last_state_change'],
            'options': ['ts_format', 'ts_date'],
            'short': 'Age',
            'sorter': 'stateage',
            'title': 'The age of the current service state'
        },
        'wato_folder_abs': {
            'columns': ['host_filename'],
            'short': 'WATO folder',
            'sorter': 'wato_folder_abs',
            'title': 'WATO folder - complete path'
        },
        'wato_folder_plain': {
            'columns': ['host_filename'],
            'short': 'WATO folder',
            'sorter': 'wato_folder_plain',
            'title': 'WATO folder - just folder name'
        },
        'wato_folder_rel': {
            'columns': ['host_filename'],
            'short': 'WATO folder',
            'sorter': 'wato_folder_rel',
            'title': 'WATO folder - relative path'
        },
        'inv': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Inventory',
            'sorter': 'inv',
            'title': 'Inventory Tree'
        },
        'inv_hardware': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Hardware',
            'sorter': 'inv_hardware',
            'title': 'Inventory: Inventory \u27a4 Hardware'
        },
        'inv_hardware_chassis': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Chassis',
            'sorter': 'inv_hardware_chassis',
            'title': 'Inventory: Hardware \u27a4 Chassis'
        },
        'inv_hardware_components': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Physical Components',
            'sorter': 'inv_hardware_components',
            'title': 'Inventory: Hardware \u27a4 Physical Components'
        },
        'inv_hardware_components_backplanes': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Backplanes',
            'sorter': 'inv_hardware_components_backplanes',
            'title': 'Inventory: Physical Components \u27a4 Backplanes'
        },
        'inv_hardware_components_chassis': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Chassis',
            'sorter': 'inv_hardware_components_chassis',
            'title': 'Inventory: Physical Components \u27a4 Chassis'
        },
        'inv_hardware_components_containers': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Containers',
            'sorter': 'inv_hardware_components_containers',
            'title': 'Inventory: Physical Components \u27a4 Containers'
        },
        'inv_hardware_components_fans': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Fans',
            'sorter': 'inv_hardware_components_fans',
            'title': 'Inventory: Physical Components \u27a4 Fans'
        },
        'inv_hardware_components_modules': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Modules',
            'sorter': 'inv_hardware_components_modules',
            'title': 'Inventory: Physical Components \u27a4 Modules'
        },
        'inv_hardware_components_others': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Other entities',
            'sorter': 'inv_hardware_components_others',
            'title': 'Inventory: Physical Components \u27a4 Other entities'
        },
        'inv_hardware_components_psus': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Power Supplies',
            'sorter': 'inv_hardware_components_psus',
            'title': 'Inventory: Physical Components \u27a4 Power Supplies'
        },
        'inv_hardware_components_sensors': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Sensors',
            'sorter': 'inv_hardware_components_sensors',
            'title': 'Inventory: Physical Components \u27a4 Sensors'
        },
        'inv_hardware_components_stacks': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Stacks',
            'sorter': 'inv_hardware_components_stacks',
            'title': 'Inventory: Physical Components \u27a4 Stacks'
        },
        'inv_hardware_components_unknowns': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Unknown entities',
            'sorter': 'inv_hardware_components_unknowns',
            'title': 'Inventory: Physical Components \u27a4 Unknown entities'
        },
        'inv_hardware_cpu': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Processor',
            'sorter': 'inv_hardware_cpu',
            'title': 'Inventory: Hardware \u27a4 Processor'
        },
        'inv_hardware_cpu_arch': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'CPU Arch',
            'sorter': 'inv_hardware_cpu_arch',
            'title': 'Inventory: Processor \u27a4 CPU Architecture'
        },
        'inv_hardware_cpu_bus_speed': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Bus Speed',
            'sorter': 'inv_hardware_cpu_bus_speed',
            'title': 'Inventory: Processor \u27a4 Bus Speed'
        },
        'inv_hardware_cpu_cache_size': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Cache Size',
            'sorter': 'inv_hardware_cpu_cache_size',
            'title': 'Inventory: Processor \u27a4 Cache Size'
        },
        'inv_hardware_cpu_cores': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Cores',
            'sorter': 'inv_hardware_cpu_cores',
            'title': 'Inventory: Processor \u27a4 Total Number of Cores'
        },
        'inv_hardware_cpu_cores_per_cpu': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Cores per CPU',
            'sorter': 'inv_hardware_cpu_cores_per_cpu',
            'title': 'Inventory: Processor \u27a4 Cores per CPU'
        },
        'inv_hardware_cpu_cpus': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'CPUs',
            'sorter': 'inv_hardware_cpu_cpus',
            'title': 'Inventory: Processor \u27a4 Number of physical CPUs'
        },
        'inv_hardware_cpu_entitlement': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'CPU Entitlement',
            'sorter': 'inv_hardware_cpu_entitlement',
            'title': 'Inventory: Processor \u27a4 CPU Entitlement'
        },
        'inv_hardware_cpu_logical_cpus': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Logical CPUs',
            'sorter': 'inv_hardware_cpu_logical_cpus',
            'title': 'Inventory: Processor \u27a4 Number of logical CPUs'
        },
        'inv_hardware_cpu_max_speed': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Maximum Speed',
            'sorter': 'inv_hardware_cpu_max_speed',
            'title': 'Inventory: Processor \u27a4 Maximum Speed'
        },
        'inv_hardware_cpu_model': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'CPU Model',
            'sorter': 'inv_hardware_cpu_model',
            'title': 'Inventory: Processor \u27a4 Model'
        },
        'inv_hardware_cpu_sharing_mode': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'CPU sharing mode',
            'sorter': 'inv_hardware_cpu_sharing_mode',
            'title': 'Inventory: Processor \u27a4 CPU sharing mode'
        },
        'inv_hardware_cpu_smt_threads': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Simultaneous multithreading',
            'sorter': 'inv_hardware_cpu_smt_threads',
            'title': 'Inventory: Processor \u27a4 Simultaneous multithreading'
        },
        'inv_hardware_cpu_threads': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Total Number of Hyperthreads',
            'sorter': 'inv_hardware_cpu_threads',
            'title': 'Inventory: Processor \u27a4 Total Number of Hyperthreads'
        },
        'inv_hardware_cpu_threads_per_cpu': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Hyperthreads per CPU',
            'sorter': 'inv_hardware_cpu_threads_per_cpu',
            'title': 'Inventory: Processor \u27a4 Hyperthreads per CPU'
        },
        'inv_hardware_cpu_voltage': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Voltage',
            'sorter': 'inv_hardware_cpu_voltage',
            'title': 'Inventory: Processor \u27a4 Voltage'
        },
        'inv_hardware_memory': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Memory (RAM)',
            'sorter': 'inv_hardware_memory',
            'title': 'Inventory: Hardware \u27a4 Memory (RAM)'
        },
        'inv_hardware_memory_arrays': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Arrays (Controllers)',
            'sorter': 'inv_hardware_memory_arrays',
            'title': 'Inventory: Memory (RAM) \u27a4 Arrays (Controllers)'
        },
        'inv_hardware_memory_total_ram_usable': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Total usable RAM',
            'sorter': 'inv_hardware_memory_total_ram_usable',
            'title': 'Inventory: Memory (RAM) \u27a4 Total usable RAM'
        },
        'inv_hardware_memory_total_swap': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Total swap space',
            'sorter': 'inv_hardware_memory_total_swap',
            'title': 'Inventory: Memory (RAM) \u27a4 Total swap space'
        },
        'inv_hardware_memory_total_vmalloc': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Virtual addresses for mapping',
            'sorter': 'inv_hardware_memory_total_vmalloc',
            'title': 'Inventory: Memory (RAM) \u27a4 Virtual addresses for mapping'
        },
        'inv_hardware_nwadapter': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Network Adapters',
            'sorter': 'inv_hardware_nwadapter',
            'title': 'Inventory: Hardware \u27a4 Network Adapters'
        },
        'inv_hardware_storage': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Storage',
            'sorter': 'inv_hardware_storage',
            'title': 'Inventory: Hardware \u27a4 Storage'
        },
        'inv_hardware_storage_controller': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Controller',
            'sorter': 'inv_hardware_storage_controller',
            'title': 'Inventory: Storage \u27a4 Controller'
        },
        'inv_hardware_storage_controller_version': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Version',
            'sorter': 'inv_hardware_storage_controller_version',
            'title': 'Inventory: Controller \u27a4 Version'
        },
        'inv_hardware_storage_disks': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Block Devices',
            'sorter': 'inv_hardware_storage_disks',
            'title': 'Inventory: Storage \u27a4 Block Devices'
        },
        'inv_hardware_system': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'System',
            'sorter': 'inv_hardware_system',
            'title': 'Inventory: Hardware \u27a4 System'
        },
        'inv_hardware_system_expresscode': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Express Servicecode',
            'sorter': 'inv_hardware_system_expresscode',
            'title': 'Inventory: System \u27a4 Express Servicecode'
        },
        'inv_hardware_system_manufacturer': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Manufacturer',
            'sorter': 'inv_hardware_system_manufacturer',
            'title': 'Inventory: System \u27a4 Manufacturer'
        },
        'inv_hardware_system_model': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Model Name',
            'sorter': 'inv_hardware_system_model',
            'title': 'Inventory: System \u27a4 Model Name'
        },
        'inv_hardware_system_model_name': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': "Model Name - LEGACY, don't use",
            'sorter': 'inv_hardware_system_model_name',
            'title': "Inventory: System \u27a4 Model Name - LEGACY, don't use"
        },
        'inv_hardware_system_product': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Product',
            'sorter': 'inv_hardware_system_product',
            'title': 'Inventory: System \u27a4 Product'
        },
        'inv_hardware_system_serial': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Serial Number',
            'sorter': 'inv_hardware_system_serial',
            'title': 'Inventory: System \u27a4 Serial Number'
        },
        'inv_hardware_system_serial_number': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': "Serial Number - LEGACY, don't use",
            'sorter': 'inv_hardware_system_serial_number',
            'title': "Inventory: System \u27a4 Serial Number - LEGACY, don't use"
        },
        'inv_hardware_video': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Graphic Cards',
            'sorter': 'inv_hardware_video',
            'title': 'Inventory: Hardware \u27a4 Graphic Cards'
        },
        'inv_networking': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Networking',
            'sorter': 'inv_networking',
            'title': 'Inventory: Inventory \u27a4 Networking'
        },
        'inv_networking_addresses': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'IP Addresses',
            'sorter': 'inv_networking_addresses',
            'title': 'Inventory: Networking \u27a4 IP Addresses'
        },
        'inv_networking_available_ethernet_ports': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Ports available',
            'sorter': 'inv_networking_available_ethernet_ports',
            'title': 'Inventory: Networking \u27a4 Ports available'
        },
        'inv_networking_interfaces': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Interfaces',
            'sorter': 'inv_networking_interfaces',
            'title': 'Inventory: Networking \u27a4 Interfaces'
        },
        'inv_networking_routes': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Routes',
            'sorter': 'inv_networking_routes',
            'title': 'Inventory: Networking \u27a4 Routes'
        },
        'inv_networking_total_ethernet_ports': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Ports',
            'sorter': 'inv_networking_total_ethernet_ports',
            'title': 'Inventory: Networking \u27a4 Ports'
        },
        'inv_networking_total_interfaces': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Interfaces',
            'sorter': 'inv_networking_total_interfaces',
            'title': 'Inventory: Networking \u27a4 Interfaces'
        },
        'inv_networking_wlan': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'WLAN',
            'sorter': 'inv_networking_wlan',
            'title': 'Inventory: Networking \u27a4 WLAN'
        },
        'inv_networking_wlan_controller': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Controller',
            'sorter': 'inv_networking_wlan_controller',
            'title': 'Inventory: WLAN \u27a4 Controller'
        },
        'inv_networking_wlan_controller_accesspoints': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Access Points',
            'sorter': 'inv_networking_wlan_controller_accesspoints',
            'title': 'Inventory: Controller \u27a4 Access Points'
        },
        'inv_software': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Software',
            'sorter': 'inv_software',
            'title': 'Inventory: Inventory \u27a4 Software'
        },
        'inv_software_applications': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Applications',
            'sorter': 'inv_software_applications',
            'title': 'Inventory: Software \u27a4 Applications'
        },
        'inv_software_applications_check_mk': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Check_MK',
            'sorter': 'inv_software_applications_check_mk',
            'title': 'Inventory: Applications \u27a4 Check_MK'
        },
        'inv_software_applications_check_mk_cluster_is_cluster': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Cluster',
            'sorter': 'inv_software_applications_check_mk_cluster_is_cluster',
            'title': 'Inventory: Cluster \u27a4 Cluster host'
        },
        'inv_software_applications_check_mk_cluster_nodes': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Nodes',
            'sorter': 'inv_software_applications_check_mk_cluster_nodes',
            'title': 'Inventory: Cluster \u27a4 Nodes'
        },
        'inv_software_applications_citrix': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Citrix',
            'sorter': 'inv_software_applications_citrix',
            'title': 'Inventory: Applications \u27a4 Citrix'
        },
        'inv_software_applications_citrix_controller': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Controller',
            'sorter': 'inv_software_applications_citrix_controller',
            'title': 'Inventory: Citrix \u27a4 Controller'
        },
        'inv_software_applications_citrix_controller_controller_version': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Controller Version',
            'sorter': 'inv_software_applications_citrix_controller_controller_version',
            'title': 'Inventory: Controller \u27a4 Controller Version'
        },
        'inv_software_applications_citrix_vm': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Virtual Machine',
            'sorter': 'inv_software_applications_citrix_vm',
            'title': 'Inventory: Citrix \u27a4 Virtual Machine'
        },
        'inv_software_applications_citrix_vm_agent_version': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Agent Version',
            'sorter': 'inv_software_applications_citrix_vm_agent_version',
            'title': 'Inventory: Virtual Machine \u27a4 Agent Version'
        },
        'inv_software_applications_citrix_vm_catalog': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Catalog',
            'sorter': 'inv_software_applications_citrix_vm_catalog',
            'title': 'Inventory: Virtual Machine \u27a4 Catalog'
        },
        'inv_software_applications_citrix_vm_desktop_group_name': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Desktop Group Name',
            'sorter': 'inv_software_applications_citrix_vm_desktop_group_name',
            'title': 'Inventory: Virtual Machine \u27a4 Desktop Group Name'
        },
        'inv_software_applications_docker': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Docker',
            'sorter': 'inv_software_applications_docker',
            'title': 'Inventory: Applications \u27a4 Docker'
        },
        'inv_software_applications_docker_container': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Container',
            'sorter': 'inv_software_applications_docker_container',
            'title': 'Inventory: Docker \u27a4 Container'
        },
        'inv_software_applications_docker_container_networks': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Networks',
            'sorter': 'inv_software_applications_docker_container_networks',
            'title': 'Inventory: Container \u27a4 Networks'
        },
        'inv_software_applications_docker_container_node_name': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Node name',
            'sorter': 'inv_software_applications_docker_container_node_name',
            'title': 'Inventory: Container \u27a4 Node name'
        },
        'inv_software_applications_docker_container_ports': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Ports',
            'sorter': 'inv_software_applications_docker_container_ports',
            'title': 'Inventory: Container \u27a4 Ports'
        },
        'inv_software_applications_docker_containers': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Containers',
            'sorter': 'inv_software_applications_docker_containers',
            'title': 'Inventory: Docker \u27a4 Containers'
        },
        'inv_software_applications_docker_images': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Images',
            'sorter': 'inv_software_applications_docker_images',
            'title': 'Inventory: Docker \u27a4 Images'
        },
        'inv_software_applications_docker_num_containers_paused': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': '# Containers paused',
            'sorter': 'inv_software_applications_docker_num_containers_paused',
            'title': 'Inventory: Docker \u27a4 # Containers paused'
        },
        'inv_software_applications_docker_num_containers_running': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': '# Containers running',
            'sorter': 'inv_software_applications_docker_num_containers_running',
            'title': 'Inventory: Docker \u27a4 # Containers running'
        },
        'inv_software_applications_docker_num_containers_stopped': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': '# Containers stopped',
            'sorter': 'inv_software_applications_docker_num_containers_stopped',
            'title': 'Inventory: Docker \u27a4 # Containers stopped'
        },
        'inv_software_applications_docker_num_containers_total': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': '# Containers',
            'sorter': 'inv_software_applications_docker_num_containers_total',
            'title': 'Inventory: Docker \u27a4 # Containers'
        },
        'inv_software_applications_docker_num_images': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': '# Images',
            'sorter': 'inv_software_applications_docker_num_images',
            'title': 'Inventory: Docker \u27a4 # Images'
        },
        'inv_software_applications_kubernetes_nodes': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Nodes',
            'sorter': 'inv_software_applications_kubernetes_nodes',
            'title': 'Inventory: Kubernetes \u27a4 Nodes',
        },
        'inv_software_applications_kubernetes_roles': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Roles',
            'sorter': 'inv_software_applications_kubernetes_roles',
            'title': 'Inventory: Kubernetes \u27a4 Roles',
        },
        'inv_software_applications_mssql': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'MSSQL',
            'sorter': 'inv_software_applications_mssql',
            'title': 'Inventory: Applications \u27a4 MSSQL'
        },
        'inv_software_applications_mssql_instances': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Instances',
            'sorter': 'inv_software_applications_mssql_instances',
            'title': 'Inventory: MSSQL \u27a4 Instances'
        },
        'inv_software_applications_oracle': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Oracle DB',
            'sorter': 'inv_software_applications_oracle',
            'title': 'Inventory: Applications \u27a4 Oracle DB'
        },
        'inv_software_applications_oracle_dataguard_stats': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Dataguard statistics',
            'sorter': 'inv_software_applications_oracle_dataguard_stats',
            'title': 'Inventory: Oracle DB \u27a4 Dataguard statistics'
        },
        'inv_software_applications_oracle_instance': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Instances',
            'sorter': 'inv_software_applications_oracle_instance',
            'title': 'Inventory: Oracle DB \u27a4 Instances'
        },
        'inv_software_applications_oracle_recovery_area': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Recovery area',
            'sorter': 'inv_software_applications_oracle_recovery_area',
            'title': 'Inventory: Oracle DB \u27a4 Recovery area'
        },
        'inv_software_applications_oracle_sga': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'SGA Info',
            'sorter': 'inv_software_applications_oracle_sga',
            'title': 'Inventory: Oracle DB \u27a4 SGA Info'
        },
        'inv_software_applications_oracle_tablespaces': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Tablespaces',
            'sorter': 'inv_software_applications_oracle_tablespaces',
            'title': 'Inventory: Oracle DB \u27a4 Tablespaces'
        },
        'inv_software_bios': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'BIOS',
            'sorter': 'inv_software_bios',
            'title': 'Inventory: Software \u27a4 BIOS'
        },
        'inv_software_bios_date': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Date',
            'sorter': 'inv_software_bios_date',
            'title': 'Inventory: BIOS \u27a4 Date'
        },
        'inv_software_bios_vendor': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Vendor',
            'sorter': 'inv_software_bios_vendor',
            'title': 'Inventory: BIOS \u27a4 Vendor'
        },
        'inv_software_bios_version': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Version',
            'sorter': 'inv_software_bios_version',
            'title': 'Inventory: BIOS \u27a4 Version'
        },
        'inv_software_configuration': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Configuration',
            'sorter': 'inv_software_configuration',
            'title': 'Inventory: Software \u27a4 Configuration'
        },
        'inv_software_configuration_snmp_info': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'SNMP Information',
            'sorter': 'inv_software_configuration_snmp_info',
            'title': 'Inventory: Configuration \u27a4 SNMP Information'
        },
        'inv_software_configuration_snmp_info_contact': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Contact',
            'sorter': 'inv_software_configuration_snmp_info_contact',
            'title': 'Inventory: SNMP Information \u27a4 Contact'
        },
        'inv_software_configuration_snmp_info_location': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Location',
            'sorter': 'inv_software_configuration_snmp_info_location',
            'title': 'Inventory: SNMP Information \u27a4 Location'
        },
        'inv_software_configuration_snmp_info_name': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'System name',
            'sorter': 'inv_software_configuration_snmp_info_name',
            'title': 'Inventory: SNMP Information \u27a4 System name'
        },
        'inv_software_firmware_platform_level': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Platform Firmware level',
            'sorter': 'inv_software_firmware_platform_level',
            'title': 'Inventory: Firmware \u27a4 Platform Firmware level'
        },
        'inv_software_firmware_vendor': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Vendor',
            'sorter': 'inv_software_firmware_vendor',
            'title': 'Inventory: Firmware \u27a4 Vendor'
        },
        'inv_software_firmware_version': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Version',
            'sorter': 'inv_software_firmware_version',
            'title': 'Inventory: Firmware \u27a4 Version'
        },
        'inv_software_os': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Operating System',
            'sorter': 'inv_software_os',
            'title': 'Inventory: Software \u27a4 Operating System'
        },
        'inv_software_os_arch': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Architecture',
            'sorter': 'inv_software_os_arch',
            'title': 'Inventory: Operating System \u27a4 Kernel Architecture'
        },
        'inv_software_os_install_date': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Install Date',
            'sorter': 'inv_software_os_install_date',
            'title': 'Inventory: Operating System \u27a4 Install Date'
        },
        'inv_software_os_kernel_version': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Kernel',
            'sorter': 'inv_software_os_kernel_version',
            'title': 'Inventory: Operating System \u27a4 Kernel Version'
        },
        'inv_software_os_name': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Operating System',
            'sorter': 'inv_software_os_name',
            'title': 'Inventory: Operating System \u27a4 Name'
        },
        'inv_software_os_service_pack': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Service Pack',
            'sorter': 'inv_software_os_service_pack',
            'title': 'Inventory: Operating System \u27a4 Latest Service Pack'
        },
        'inv_software_os_service_packs': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Service Packs',
            'sorter': 'inv_software_os_service_packs',
            'title': 'Inventory: Operating System \u27a4 Service Packs'
        },
        'inv_software_os_type': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Type',
            'sorter': 'inv_software_os_type',
            'title': 'Inventory: Operating System \u27a4 Type'
        },
        'inv_software_os_vendor': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Vendor',
            'sorter': 'inv_software_os_vendor',
            'title': 'Inventory: Operating System \u27a4 Vendor'
        },
        'inv_software_os_version': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Version',
            'sorter': 'inv_software_os_version',
            'title': 'Inventory: Operating System \u27a4 Version'
        },
        'inv_software_packages': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'options': ['show_internal_tree_paths'],
            'short': 'Packages',
            'sorter': 'inv_software_packages',
            'title': 'Inventory: Software \u27a4 Packages'
        },
    }

    #xx = {}
    #for ident, p in cmk.gui.plugins.views.multisite_painters.items():
    #    if ident == "inv" or ident.startswith("inv_"):
    #        del p["paint"]
    #        try:
    #            del p["groupby"]
    #        except KeyError:
    #            pass
    #        try:
    #            del p["params"]
    #        except KeyError:
    #            pass
    #        xx[ident] = p

    #import pprint
    #x = pprint.pformat(xx)
    #open("/tmp/x", "w").write(x)

    names = cmk.gui.plugins.views.painter_registry.keys()
    assert sorted(expected.keys()) == sorted(names)

    known_keys = {
        "title",
        "columns",
        "short",
        "sorter",
        "options",
        "printable",
        "load_inv",
    }
    for spec in expected.values():
        this_keys = set(spec.keys())
        assert not this_keys.difference(known_keys)

    for painter_class in cmk.gui.plugins.views.painter_registry.values():
        painter = painter_class()
        spec = expected[painter.ident]

        assert painter.title == spec["title"]

        if isinstance(spec["columns"], tuple) and spec["columns"][0] == "func":
            assert hasattr(painter.columns, '__call__')
        else:
            assert painter.columns == spec["columns"]

        assert painter.short_title == spec.get("short", spec["title"])

        assert painter.sorter == spec.get("sorter")
        assert painter.painter_options == spec.get("options", [])
        assert painter.printable == spec.get("printable", True)
        assert painter.load_inv == spec.get("load_inv", False)


def test_legacy_register_painter(monkeypatch):
    monkeypatch.setattr(cmk.gui.plugins.views.utils, "painter_registry",
                        cmk.gui.plugins.views.utils.PainterRegistry())

    def rendr(row):
        return ("abc", "xyz")

    cmk.gui.plugins.views.utils.register_painter(
        "abc", {
            "title": "A B C",
            "short": "ABC",
            "columns": ["x"],
            "sorter": "aaaa",
            "options": ["opt1"],
            "printable": False,
            "paint": rendr,
            "groupby": "xyz",
        })

    painter = cmk.gui.plugins.views.utils.painter_registry["abc"]()
    dummy_cell = cmk.gui.plugins.views.utils.Cell(cmk.gui.views.View("", {}, {}), PainterSpec(painter.ident))
    assert isinstance(painter, cmk.gui.plugins.views.utils.Painter)
    assert painter.ident == "abc"
    assert painter.title(dummy_cell) == "A B C"
    assert painter.short_title(dummy_cell) == "ABC"
    assert painter.columns == ["x"]
    assert painter.sorter == "aaaa"
    assert painter.painter_options == ["opt1"]
    assert painter.printable is False
    assert painter.render(row={}, cell=dummy_cell) == ("abc", "xyz")
    assert painter.group_by(row={}) == "xyz"


# These tests make adding new elements needlessly painful.
# Skip pending discussion with development team.
@pytest.mark.skip
def test_registered_sorters():
    expected: Dict[str, Dict[str, Any]] = {
        'aggr_group': {
            'columns': ['aggr_group'],
            'title': 'Aggregation group'
        },
        'aggr_name': {
            'columns': ['aggr_name'],
            'title': 'Aggregation name'
        },
        'alerts_crit': {
            'columns': ['log_alerts_crit'],
            'title': 'Number of critical alerts'
        },
        'alerts_ok': {
            'columns': ['log_alerts_ok'],
            'title': 'Number of recoveries'
        },
        'alerts_problem': {
            'columns': ['log_alerts_problem'],
            'title': 'Number of problem alerts'
        },
        'alerts_unknown': {
            'columns': ['log_alerts_unknown'],
            'title': 'Number of unknown alerts'
        },
        'alerts_warn': {
            'columns': ['log_alerts_warn'],
            'title': 'Number of warnings'
        },
        'alias': {
            'columns': ['host_alias'],
            'title': 'Host alias'
        },
        'comment_author': {
            'columns': ['comment_author'],
            'title': 'Comment author'
        },
        'comment_comment': {
            'columns': ['comment_comment'],
            'title': 'Comment text'
        },
        'comment_expires': {
            'columns': ['comment_expire_time'],
            'title': 'Comment expiry time'
        },
        'comment_id': {
            'columns': ['comment_id'],
            'title': 'Comment id'
        },
        'comment_time': {
            'columns': ['comment_entry_time'],
            'title': 'Comment entry time'
        },
        'comment_type': {
            'columns': ['comment_type'],
            'title': 'Comment type'
        },
        'comment_what': {
            'columns': ['comment_type'],
            'title': 'Comment type (host/service)'
        },
        'downtime_author': {
            'columns': ['downtime_author'],
            'title': 'Downtime author'
        },
        'downtime_comment': {
            'columns': ['downtime_comment'],
            'title': 'Downtime comment'
        },
        'downtime_end_time': {
            'columns': ['downtime_end_time'],
            'title': 'Downtime end'
        },
        'downtime_entry_time': {
            'columns': ['downtime_entry_time'],
            'title': 'Downtime entry time'
        },
        'downtime_fixed': {
            'columns': ['downtime_fixed'],
            'title': 'Downtime start mode'
        },
        'downtime_id': {
            'columns': ['downtime_id'],
            'title': 'Downtime id'
        },
        'downtime_start_time': {
            'columns': ['downtime_start_time'],
            'title': 'Downtime start'
        },
        'downtime_type': {
            'columns': ['downtime_type'],
            'title': 'Downtime active or pending'
        },
        'downtime_what': {
            'columns': ['downtime_is_service'],
            'title': 'Downtime for host/service'
        },
        'event_application': {
            'columns': ['event_application'],
            'title': 'Application / Syslog-Tag'
        },
        'event_comment': {
            'columns': ['event_comment'],
            'title': 'Comment to the event'
        },
        'event_contact': {
            'columns': ['event_contact'],
            'title': 'Contact Person'
        },
        'event_count': {
            'columns': ['event_count'],
            'title': 'Count (number of recent occurrances)'
        },
        'event_facility': {
            'columns': ['event_facility'],
            'title': 'Syslog-Facility'
        },
        'event_first': {
            'columns': ['event_first'],
            'title': 'Time of first occurrence of this serial'
        },
        'event_host': {
            'columns': ['event_host', 'host_name'],
            'title': 'Hostname'
        },
        'event_id': {
            'columns': ['event_id'],
            'title': 'ID of the event'
        },
        'event_ipaddress': {
            'columns': ['event_ipaddress'],
            'title': 'Original IP-Address'
        },
        'event_last': {
            'columns': ['event_last'],
            'title': 'Time of last occurrance'
        },
        'event_owner': {
            'columns': ['event_owner'],
            'title': 'Owner of event'
        },
        'event_phase': {
            'columns': ['event_phase'],
            'title': 'Phase of event (open, counting, etc.)'
        },
        'event_pid': {
            'columns': ['event_pid'],
            'title': 'Process ID'
        },
        'event_priority': {
            'columns': ['event_priority'],
            'title': 'Syslog-Priority'
        },
        'event_rule_id': {
            'columns': ['event_rule_id'],
            'title': 'Rule-ID'
        },
        'event_sl': {
            'columns': ['event_sl'],
            'title': 'Service-Level'
        },
        'event_state': {
            'columns': ['event_state'],
            'title': 'State (severity) of event'
        },
        'event_text': {
            'columns': ['event_text'],
            'title': 'Text/Message of the event'
        },
        'hg_alias': {
            'columns': ['hostgroup_alias'],
            'title': 'Hostgroup alias'
        },
        'hg_name': {
            'columns': ['hostgroup_name'],
            'title': 'Hostgroup name'
        },
        'hg_num_hosts_down': {
            'columns': ['hostgroup_num_hosts_down'],
            'title': 'Number of hosts in state DOWN (Host Group)'
        },
        'hg_num_hosts_pending': {
            'columns': ['hostgroup_num_hosts_pending'],
            'title': 'Number of hosts in state PENDING (Host Group)'
        },
        'hg_num_hosts_unreach': {
            'columns': ['hostgroup_num_hosts_unreach'],
            'title': 'Number of hosts in state UNREACH (Host Group)'
        },
        'hg_num_hosts_up': {
            'columns': ['hostgroup_num_hosts_up'],
            'title': 'Number of hosts in state UP (Host Group)'
        },
        'hg_num_services': {
            'columns': ['hostgroup_num_services'],
            'title': 'Number of services (Host Group)'
        },
        'hg_num_services_crit': {
            'columns': ['hostgroup_num_services_crit'],
            'title': 'Number of services in state CRIT (Host Group)'
        },
        'hg_num_services_ok': {
            'columns': ['hostgroup_num_services_ok'],
            'title': 'Number of services in state OK (Host Group)'
        },
        'hg_num_services_pending': {
            'columns': ['hostgroup_num_services_pending'],
            'title': 'Number of services in state PENDING (Host Group)'
        },
        'hg_num_services_unknown': {
            'columns': ['hostgroup_num_services_unknown'],
            'title': 'Number of services in state UNKNOWN (Host Group)'
        },
        'hg_num_services_warn': {
            'columns': ['hostgroup_num_services_warn'],
            'title': 'Number of services in state WARN (Host Group)'
        },
        'history_addinfo': {
            'columns': ['history_addinfo'],
            'title': 'Additional Information'
        },
        'history_line': {
            'columns': ['history_line'],
            'title': 'Line number in log file'
        },
        'history_time': {
            'columns': ['history_time'],
            'title': 'Time of entry in logfile'
        },
        'history_what': {
            'columns': ['history_what'],
            'title': 'Type of event action'
        },
        'history_who': {
            'columns': ['history_who'],
            'title': 'User who performed action'
        },
        'host': {
            'columns': ['host_custom_variable_names', 'host_custom_variable_values'],
            'title': 'Host Tags (raw)'
        },
        'host_acknowledged': {
            'columns': ['host_acknowledged'],
            'title': 'Host problem acknowledged'
        },
        'host_address': {
            'columns': ['host_address'],
            'title': 'Host address (Primary)'
        },
        'host_address_family': {
            'columns': ['host_custom_variable_names', 'host_custom_variable_values'],
            'title': 'Host address family (Primary)'
        },
        'host_attempt': {
            'columns': ['host_current_attempt', 'host_max_check_attempts'],
            'title': 'Current host check attempt'
        },
        'host_check_age': {
            'columns': ['host_has_been_checked', 'host_last_check'],
            'title': 'The time since the last check of the host'
        },
        'host_check_command': {
            'columns': ['host_check_command'],
            'title': 'Host check command'
        },
        'host_check_duration': {
            'columns': ['host_execution_time'],
            'title': 'Host check duration'
        },
        'host_check_latency': {
            'columns': ['host_latency'],
            'title': 'Host check latency'
        },
        'host_check_type': {
            'columns': ['host_check_type'],
            'title': 'Host check type'
        },
        'host_childs': {
            'columns': ['host_childs'],
            'title': "Host's children"
        },
        'host_contact_groups': {
            'columns': ['host_contact_groups'],
            'title': 'Host contact groups'
        },
        'host_contacts': {
            'columns': ['host_contacts'],
            'title': 'Host contacts'
        },
        'host_flapping': {
            'columns': ['host_is_flapping'],
            'title': 'Host is flapping'
        },
        'host_group_memberlist': {
            'columns': ['host_groups'],
            'title': 'Host groups the host is member of'
        },
        'host_in_downtime': {
            'columns': ['host_scheduled_downtime_depth'],
            'title': 'Host in downtime'
        },
        'host_in_notifper': {
            'columns': ['host_in_notification_period'],
            'title': 'Host in notif. period'
        },
        'host_ipv4_address': {
            'columns': ['host_custom_variable_names', 'host_custom_variable_values'],
            'title': 'Host IPv4 address'
        },
        'host_is_active': {
            'columns': ['host_active_checks_enabled'],
            'title': 'Host is active'
        },
        'host_last_notification': {
            'columns': ['host_last_notification'],
            'title': 'The time of the last host notification'
        },
        'host_name': {
            'columns': ['host_name'],
            'title': 'Host name'
        },
        'host_next_check': {
            'columns': ['host_next_check'],
            'title': 'The time of the next scheduled host check'
        },
        'host_next_notification': {
            'columns': ['host_next_notification'],
            'title': 'The time of the next host notification'
        },
        'host_notifper': {
            'columns': ['host_notification_period'],
            'title': 'Host notification period'
        },
        'host_parents': {
            'columns': ['host_parents'],
            'title': "Host's parents"
        },
        'host_perf_data': {
            'columns': ['host_perf_data'],
            'title': 'Host performance data'
        },
        'host_plugin_output': {
            'columns': ['host_plugin_output', 'host_custom_variables'],
            'title': 'Output of host check plugin'
        },
        'host_servicelevel': {
            'columns': ['host_custom_variable_names', 'host_custom_variable_values'],
            'title': 'Host service level'
        },
        'host_state_age': {
            'columns': ['host_has_been_checked', 'host_last_state_change'],
            'title': 'The age of the current host state'
        },
        'host_tag_address_family': {
            'columns': ['host_custom_variable_names', 'host_custom_variable_values'],
            'title': 'Host tag: Address/IP Address Family '
        },
        'host_tag_agent': {
            'columns': ['host_custom_variable_names', 'host_custom_variable_values'],
            'title': 'Host tag: Data sources/Check_MK Agent'
        },
        'host_tag_snmp': {
            'columns': ['host_custom_variable_names', 'host_custom_variable_values'],
            'title': 'Host tag: Data sources/SNMP'
        },
        'hostgroup': {
            'columns': ['hostgroup_alias'],
            'title': 'Hostgroup'
        },
        'hoststate': {
            'columns': ['host_state', 'host_has_been_checked'],
            'title': 'Host state'
        },
        'inv_hardware_cpu_arch': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: Processor \u27a4 CPU Architecture'
        },
        'inv_hardware_cpu_bus_speed': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: Processor \u27a4 Bus Speed'
        },
        'inv_hardware_cpu_cache_size': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: Processor \u27a4 Cache Size'
        },
        'inv_hardware_cpu_cores': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: Processor \u27a4 Total Number of Cores'
        },
        'inv_hardware_cpu_cores_per_cpu': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: Processor \u27a4 Cores per CPU'
        },
        'inv_hardware_cpu_cpus': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: Processor \u27a4 Number of physical CPUs'
        },
        'inv_hardware_cpu_entitlement': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: Processor \u27a4 CPU Entitlement'
        },
        'inv_hardware_cpu_logical_cpus': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: Processor \u27a4 Number of logical CPUs'
        },
        'inv_hardware_cpu_max_speed': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: Processor \u27a4 Maximum Speed'
        },
        'inv_hardware_cpu_model': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: Processor \u27a4 Model'
        },
        'inv_hardware_cpu_sharing_mode': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: Processor \u27a4 CPU sharing mode'
        },
        'inv_hardware_cpu_smt_threads': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: Processor \u27a4 Simultaneous multithreading'
        },
        'inv_hardware_cpu_threads': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: Processor \u27a4 Total Number of Hyperthreads'
        },
        'inv_hardware_cpu_threads_per_cpu': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: Processor \u27a4 Hyperthreads per CPU'
        },
        'inv_hardware_cpu_voltage': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: Processor \u27a4 Voltage'
        },
        'inv_hardware_memory_total_ram_usable': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: Memory (RAM) \u27a4 Total usable RAM'
        },
        'inv_hardware_memory_total_swap': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: Memory (RAM) \u27a4 Total swap space'
        },
        'inv_hardware_memory_total_vmalloc': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: Memory (RAM) \u27a4 Virtual addresses for mapping'
        },
        'inv_hardware_storage_controller_version': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: Controller \u27a4 Version'
        },
        'inv_hardware_system_expresscode': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: System \u27a4 Express Servicecode'
        },
        'inv_hardware_system_manufacturer': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: System \u27a4 Manufacturer'
        },
        'inv_hardware_system_model': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: System \u27a4 Model Name'
        },
        'inv_hardware_system_model_name': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': "Inventory: System \u27a4 Model Name - LEGACY, don't use"
        },
        'inv_hardware_system_product': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: System \u27a4 Product'
        },
        'inv_hardware_system_serial': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: System \u27a4 Serial Number'
        },
        'inv_hardware_system_serial_number': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': "Inventory: System \u27a4 Serial Number - LEGACY, don't use"
        },
        'inv_networking_available_ethernet_ports': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: Networking \u27a4 Ports available'
        },
        'inv_networking_total_ethernet_ports': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: Networking \u27a4 Ports'
        },
        'inv_networking_total_interfaces': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: Networking \u27a4 Interfaces'
        },
        'inv_networking_wlan': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: Networking \u27a4 WLAN'
        },
        'inv_networking_wlan_controller': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: WLAN \u27a4 Controller'
        },
        'inv_software_applications_check_mk_cluster_is_cluster': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: Cluster \u27a4 Cluster host'
        },
        'inv_software_applications_citrix_controller_controller_version': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: Controller \u27a4 Controller Version'
        },
        'inv_software_applications_citrix_vm_agent_version': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: Virtual Machine \u27a4 Agent Version'
        },
        'inv_software_applications_citrix_vm_catalog': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: Virtual Machine \u27a4 Catalog'
        },
        'inv_software_applications_citrix_vm_desktop_group_name': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: Virtual Machine \u27a4 Desktop Group Name'
        },
        'inv_software_applications_docker_container_node_name': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: Container \u27a4 Node name'
        },
        'inv_software_applications_docker_num_containers_paused': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: Docker \u27a4 # Containers paused'
        },
        'inv_software_applications_docker_num_containers_running': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: Docker \u27a4 # Containers running'
        },
        'inv_software_applications_docker_num_containers_stopped': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: Docker \u27a4 # Containers stopped'
        },
        'inv_software_applications_docker_num_containers_total': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: Docker \u27a4 # Containers'
        },
        'inv_software_applications_docker_num_images': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: Docker \u27a4 # Images'
        },
        'inv_software_bios_date': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: BIOS \u27a4 Date'
        },
        'inv_software_bios_vendor': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: BIOS \u27a4 Vendor'
        },
        'inv_software_bios_version': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: BIOS \u27a4 Version'
        },
        'inv_software_configuration_snmp_info_contact': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: SNMP Information \u27a4 Contact'
        },
        'inv_software_configuration_snmp_info_location': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: SNMP Information \u27a4 Location'
        },
        'inv_software_configuration_snmp_info_name': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: SNMP Information \u27a4 System name'
        },
        'inv_software_firmware_platform_level': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: Firmware \u27a4 Platform Firmware level'
        },
        'inv_software_firmware_vendor': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: Firmware \u27a4 Vendor'
        },
        'inv_software_firmware_version': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: Firmware \u27a4 Version'
        },
        'inv_software_os_arch': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: Operating System \u27a4 Kernel Architecture'
        },
        'inv_software_os_install_date': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: Operating System \u27a4 Install Date'
        },
        'inv_software_os_kernel_version': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: Operating System \u27a4 Kernel Version'
        },
        'inv_software_os_name': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: Operating System \u27a4 Name'
        },
        'inv_software_os_service_pack': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: Operating System \u27a4 Latest Service Pack'
        },
        'inv_software_os_type': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: Operating System \u27a4 Type'
        },
        'inv_software_os_vendor': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: Operating System \u27a4 Vendor'
        },
        'inv_software_os_version': {
            'columns': ['host_inventory', 'host_structured_status'],
            'load_inv': True,
            'title': 'Inventory: Operating System \u27a4 Version'
        },
        'invbackplane_description': {
            'columns': ['invbackplane_description'],
            'title': 'Inventory: Description'
        },
        'invbackplane_index': {
            'columns': ['invbackplane_index'],
            'title': 'Inventory: Index'
        },
        'invbackplane_location': {
            'columns': ['invbackplane_location'],
            'title': 'Inventory: Location'
        },
        'invbackplane_manufacturer': {
            'columns': ['invbackplane_manufacturer'],
            'title': 'Inventory: Manufacturer'
        },
        'invbackplane_model': {
            'columns': ['invbackplane_model'],
            'title': 'Inventory: Model Name'
        },
        'invbackplane_name': {
            'columns': ['invbackplane_name'],
            'title': 'Inventory: Name'
        },
        'invbackplane_serial': {
            'columns': ['invbackplane_serial'],
            'title': 'Inventory: Serial Number'
        },
        'invbackplane_software': {
            'columns': ['invbackplane_software'],
            'title': 'Inventory: Software'
        },
        'invchassis_description': {
            'columns': ['invchassis_description'],
            'title': 'Inventory: Description'
        },
        'invchassis_index': {
            'columns': ['invchassis_index'],
            'title': 'Inventory: Index'
        },
        'invchassis_location': {
            'columns': ['invchassis_location'],
            'title': 'Inventory: Location'
        },
        'invchassis_manufacturer': {
            'columns': ['invchassis_manufacturer'],
            'title': 'Inventory: Manufacturer'
        },
        'invchassis_model': {
            'columns': ['invchassis_model'],
            'title': 'Inventory: Model Name'
        },
        'invchassis_name': {
            'columns': ['invchassis_name'],
            'title': 'Inventory: Name'
        },
        'invchassis_serial': {
            'columns': ['invchassis_serial'],
            'title': 'Inventory: Serial Number'
        },
        'invchassis_software': {
            'columns': ['invchassis_software'],
            'title': 'Inventory: Software'
        },
        'invcontainer_description': {
            'columns': ['invcontainer_description'],
            'title': 'Inventory: Description'
        },
        'invcontainer_index': {
            'columns': ['invcontainer_index'],
            'title': 'Inventory: Index'
        },
        'invcontainer_location': {
            'columns': ['invcontainer_location'],
            'title': 'Inventory: Location'
        },
        'invcontainer_manufacturer': {
            'columns': ['invcontainer_manufacturer'],
            'title': 'Inventory: Manufacturer'
        },
        'invcontainer_model': {
            'columns': ['invcontainer_model'],
            'title': 'Inventory: Model Name'
        },
        'invcontainer_name': {
            'columns': ['invcontainer_name'],
            'title': 'Inventory: Name'
        },
        'invcontainer_serial': {
            'columns': ['invcontainer_serial'],
            'title': 'Inventory: Serial Number'
        },
        'invcontainer_software': {
            'columns': ['invcontainer_software'],
            'title': 'Inventory: Software'
        },
        'invdockercontainers_creation': {
            'columns': ['invdockercontainers_creation'],
            'title': 'Inventory: Creation'
        },
        'invdockercontainers_id': {
            'columns': ['invdockercontainers_id'],
            'title': 'Inventory: ID'
        },
        'invdockercontainers_labels': {
            'columns': ['invdockercontainers_labels'],
            'title': 'Inventory: Labels'
        },
        'invdockercontainers_name': {
            'columns': ['invdockercontainers_name'],
            'title': 'Inventory: Name'
        },
        'invdockercontainers_repository': {
            'columns': ['invdockercontainers_repository'],
            'title': 'Inventory: Repository'
        },
        'invdockercontainers_status': {
            'columns': ['invdockercontainers_status'],
            'title': 'Inventory: Status'
        },
        'invdockercontainers_tag': {
            'columns': ['invdockercontainers_tag'],
            'title': 'Inventory: Tag'
        },
        'invdockerimages_amount_containers': {
            'columns': ['invdockerimages_amount_containers'],
            'title': 'Inventory: # Containers'
        },
        'invdockerimages_creation': {
            'columns': ['invdockerimages_creation'],
            'title': 'Inventory: Creation'
        },
        'invdockerimages_id': {
            'columns': ['invdockerimages_id'],
            'title': 'Inventory: ID'
        },
        'invdockerimages_labels': {
            'columns': ['invdockerimages_labels'],
            'title': 'Inventory: Labels'
        },
        'invdockerimages_repository': {
            'columns': ['invdockerimages_repository'],
            'title': 'Inventory: Repository'
        },
        'invdockerimages_size': {
            'columns': ['invdockerimages_size'],
            'title': 'Inventory: Size'
        },
        'invdockerimages_tag': {
            'columns': ['invdockerimages_tag'],
            'title': 'Inventory: Tag'
        },
        'invfan_description': {
            'columns': ['invfan_description'],
            'title': 'Inventory: Description'
        },
        'invfan_index': {
            'columns': ['invfan_index'],
            'title': 'Inventory: Index'
        },
        'invfan_location': {
            'columns': ['invfan_location'],
            'title': 'Inventory: Location'
        },
        'invfan_manufacturer': {
            'columns': ['invfan_manufacturer'],
            'title': 'Inventory: Manufacturer'
        },
        'invfan_model': {
            'columns': ['invfan_model'],
            'title': 'Inventory: Model Name'
        },
        'invfan_name': {
            'columns': ['invfan_name'],
            'title': 'Inventory: Name'
        },
        'invfan_serial': {
            'columns': ['invfan_serial'],
            'title': 'Inventory: Serial Number'
        },
        'invfan_software': {
            'columns': ['invfan_software'],
            'title': 'Inventory: Software'
        },
        'invhist_changed': {
            'columns': ['invhist_changed'],
            'title': 'changed entries'
        },
        'invhist_new': {
            'columns': ['invhist_new'],
            'title': 'new entries'
        },
        'invhist_removed': {
            'columns': ['invhist_removed'],
            'title': 'Removed entries'
        },
        'invhist_time': {
            'columns': ['invhist_time'],
            'title': 'Inventory Date/Time'
        },
        'invinterface_admin_status': {
            'columns': ['invinterface_admin_status'],
            'title': 'Inventory: Administrative Status'
        },
        'invinterface_alias': {
            'columns': ['invinterface_alias'],
            'title': 'Inventory: Alias'
        },
        'invinterface_available': {
            'columns': ['invinterface_available'],
            'title': 'Inventory: Port Usage'
        },
        'invinterface_description': {
            'columns': ['invinterface_description'],
            'title': 'Inventory: Description'
        },
        'invinterface_index': {
            'columns': ['invinterface_index'],
            'title': 'Inventory: Index'
        },
        'invinterface_last_change': {
            'columns': ['invinterface_last_change'],
            'title': 'Inventory: Last Change'
        },
        'invinterface_oper_status': {
            'columns': ['invinterface_oper_status'],
            'title': 'Inventory: Operational Status'
        },
        'invinterface_phys_address': {
            'columns': ['invinterface_phys_address'],
            'title': 'Inventory: Physical Address (MAC)'
        },
        'invinterface_port_type': {
            'columns': ['invinterface_port_type'],
            'title': 'Inventory: Type'
        },
        'invinterface_speed': {
            'columns': ['invinterface_speed'],
            'title': 'Inventory: Speed'
        },
        'invinterface_vlans': {
            'columns': ['invinterface_vlans'],
            'title': 'Inventory: VLANs'
        },
        'invinterface_vlantype': {
            'columns': ['invinterface_vlantype'],
            'title': 'Inventory: VLAN type'
        },
        'invmodule_bootloader': {
            'columns': ['invmodule_bootloader'],
            'title': 'Inventory: Bootloader'
        },
        'invmodule_description': {
            'columns': ['invmodule_description'],
            'title': 'Inventory: Description'
        },
        'invmodule_firmware': {
            'columns': ['invmodule_firmware'],
            'title': 'Inventory: Firmware'
        },
        'invmodule_index': {
            'columns': ['invmodule_index'],
            'title': 'Inventory: Index'
        },
        'invmodule_location': {
            'columns': ['invmodule_location'],
            'title': 'Inventory: Location'
        },
        'invmodule_manufacturer': {
            'columns': ['invmodule_manufacturer'],
            'title': 'Inventory: Manufacturer'
        },
        'invmodule_model': {
            'columns': ['invmodule_model'],
            'title': 'Inventory: Model Name'
        },
        'invmodule_name': {
            'columns': ['invmodule_name'],
            'title': 'Inventory: Name'
        },
        'invmodule_serial': {
            'columns': ['invmodule_serial'],
            'title': 'Inventory: Serial Number'
        },
        'invmodule_software': {
            'columns': ['invmodule_software'],
            'title': 'Inventory: Software'
        },
        'invmodule_type': {
            'columns': ['invmodule_type'],
            'title': 'Inventory: Type'
        },
        'invoradataguardstats_db_unique': {
            'columns': ['invoradataguardstats_db_unique'],
            'title': 'Inventory: Name'
        },
        'invoradataguardstats_role': {
            'columns': ['invoradataguardstats_role'],
            'title': 'Inventory: Role'
        },
        'invoradataguardstats_sid': {
            'columns': ['invoradataguardstats_sid'],
            'title': 'Inventory: SID'
        },
        'invoradataguardstats_switchover': {
            'columns': ['invoradataguardstats_switchover'],
            'title': 'Inventory: Switchover'
        },
        'invorainstance_db_creation_time': {
            'columns': ['invorainstance_db_creation_time'],
            'title': 'Inventory: Creation time'
        },
        'invorainstance_db_uptime': {
            'columns': ['invorainstance_db_uptime'],
            'title': 'Inventory: Uptime'
        },
        'invorainstance_logins': {
            'columns': ['invorainstance_logins'],
            'title': 'Inventory: Logins'
        },
        'invorainstance_logmode': {
            'columns': ['invorainstance_logmode'],
            'title': 'Inventory: Log mode'
        },
        'invorainstance_openmode': {
            'columns': ['invorainstance_openmode'],
            'title': 'Inventory: Open mode'
        },
        'invorainstance_sid': {
            'columns': ['invorainstance_sid'],
            'title': 'Inventory: SID'
        },
        'invorainstance_version': {
            'columns': ['invorainstance_version'],
            'title': 'Inventory: Version'
        },
        'invorarecoveryarea_flashback': {
            'columns': ['invorarecoveryarea_flashback'],
            'title': 'Inventory: Flashback'
        },
        'invorarecoveryarea_sid': {
            'columns': ['invorarecoveryarea_sid'],
            'title': 'Inventory: SID'
        },
        'invorasga_buf_cache_size': {
            'columns': ['invorasga_buf_cache_size'],
            'title': 'Inventory: Buffer cache size'
        },
        'invorasga_data_trans_cache_size': {
            'columns': ['invorasga_data_trans_cache_size'],
            'title': 'Inventory: Data transfer cache size'
        },
        'invorasga_fixed_size': {
            'columns': ['invorasga_fixed_size'],
            'title': 'Inventory: Fixed size'
        },
        'invorasga_free_mem_avail': {
            'columns': ['invorasga_free_mem_avail'],
            'title': 'Inventory: Free SGA memory available'
        },
        'invorasga_granule_size': {
            'columns': ['invorasga_granule_size'],
            'title': 'Inventory: Granule size'
        },
        'invorasga_in_mem_area_size': {
            'columns': ['invorasga_in_mem_area_size'],
            'title': 'Inventory: In-memory area'
        },
        'invorasga_java_pool_size': {
            'columns': ['invorasga_java_pool_size'],
            'title': 'Inventory: Java pool size'
        },
        'invorasga_large_pool_size': {
            'columns': ['invorasga_large_pool_size'],
            'title': 'Inventory: Large pool size'
        },
        'invorasga_max_size': {
            'columns': ['invorasga_max_size'],
            'title': 'Inventory: Maximum size'
        },
        'invorasga_redo_buffer': {
            'columns': ['invorasga_redo_buffer'],
            'title': 'Inventory: Redo buffers'
        },
        'invorasga_shared_io_pool_size': {
            'columns': ['invorasga_shared_io_pool_size'],
            'title': 'Inventory: Shared pool size'
        },
        'invorasga_shared_pool_size': {
            'columns': ['invorasga_shared_pool_size'],
            'title': 'Inventory: Shared pool size'
        },
        'invorasga_sid': {
            'columns': ['invorasga_sid'],
            'title': 'Inventory: SID'
        },
        'invorasga_start_oh_shared_pool': {
            'columns': ['invorasga_start_oh_shared_pool'],
            'title': 'Inventory: Startup overhead in shared pool'
        },
        'invorasga_streams_pool_size': {
            'columns': ['invorasga_streams_pool_size'],
            'title': 'Inventory: Streams pool size'
        },
        'invoratablespace_autoextensible': {
            'columns': ['invoratablespace_autoextensible'],
            'title': 'Inventory: Autoextensible'
        },
        'invoratablespace_current_size': {
            'columns': ['invoratablespace_current_size'],
            'title': 'Inventory: Current size'
        },
        'invoratablespace_free_space': {
            'columns': ['invoratablespace_free_space'],
            'title': 'Inventory: Free space'
        },
        'invoratablespace_increment_size': {
            'columns': ['invoratablespace_increment_size'],
            'title': 'Inventory: Increment size'
        },
        'invoratablespace_max_size': {
            'columns': ['invoratablespace_max_size'],
            'title': 'Inventory: Max. size'
        },
        'invoratablespace_name': {
            'columns': ['invoratablespace_name'],
            'title': 'Inventory: Name'
        },
        'invoratablespace_num_increments': {
            'columns': ['invoratablespace_num_increments'],
            'title': 'Inventory: Number of increments'
        },
        'invoratablespace_sid': {
            'columns': ['invoratablespace_sid'],
            'title': 'Inventory: SID'
        },
        'invoratablespace_type': {
            'columns': ['invoratablespace_type'],
            'title': 'Inventory: Type'
        },
        'invoratablespace_used_size': {
            'columns': ['invoratablespace_used_size'],
            'title': 'Inventory: Used size'
        },
        'invoratablespace_version': {
            'columns': ['invoratablespace_version'],
            'title': 'Inventory: Version'
        },
        'invother_description': {
            'columns': ['invother_description'],
            'title': 'Inventory: Description'
        },
        'invother_index': {
            'columns': ['invother_index'],
            'title': 'Inventory: Index'
        },
        'invother_location': {
            'columns': ['invother_location'],
            'title': 'Inventory: Location'
        },
        'invother_manufacturer': {
            'columns': ['invother_manufacturer'],
            'title': 'Inventory: Manufacturer'
        },
        'invother_model': {
            'columns': ['invother_model'],
            'title': 'Inventory: Model Name'
        },
        'invother_name': {
            'columns': ['invother_name'],
            'title': 'Inventory: Name'
        },
        'invother_serial': {
            'columns': ['invother_serial'],
            'title': 'Inventory: Serial Number'
        },
        'invother_software': {
            'columns': ['invother_software'],
            'title': 'Inventory: Software'
        },
        'invpsu_description': {
            'columns': ['invpsu_description'],
            'title': 'Inventory: Description'
        },
        'invpsu_index': {
            'columns': ['invpsu_index'],
            'title': 'Inventory: Index'
        },
        'invpsu_location': {
            'columns': ['invpsu_location'],
            'title': 'Inventory: Location'
        },
        'invpsu_manufacturer': {
            'columns': ['invpsu_manufacturer'],
            'title': 'Inventory: Manufacturer'
        },
        'invpsu_model': {
            'columns': ['invpsu_model'],
            'title': 'Inventory: Model Name'
        },
        'invpsu_name': {
            'columns': ['invpsu_name'],
            'title': 'Inventory: Name'
        },
        'invpsu_serial': {
            'columns': ['invpsu_serial'],
            'title': 'Inventory: Serial Number'
        },
        'invpsu_software': {
            'columns': ['invpsu_software'],
            'title': 'Inventory: Software'
        },
        'invsensor_description': {
            'columns': ['invsensor_description'],
            'title': 'Inventory: Description'
        },
        'invsensor_index': {
            'columns': ['invsensor_index'],
            'title': 'Inventory: Index'
        },
        'invsensor_location': {
            'columns': ['invsensor_location'],
            'title': 'Inventory: Location'
        },
        'invsensor_manufacturer': {
            'columns': ['invsensor_manufacturer'],
            'title': 'Inventory: Manufacturer'
        },
        'invsensor_model': {
            'columns': ['invsensor_model'],
            'title': 'Inventory: Model Name'
        },
        'invsensor_name': {
            'columns': ['invsensor_name'],
            'title': 'Inventory: Name'
        },
        'invsensor_serial': {
            'columns': ['invsensor_serial'],
            'title': 'Inventory: Serial Number'
        },
        'invsensor_software': {
            'columns': ['invsensor_software'],
            'title': 'Inventory: Software'
        },
        'invstack_description': {
            'columns': ['invstack_description'],
            'title': 'Inventory: Description'
        },
        'invstack_index': {
            'columns': ['invstack_index'],
            'title': 'Inventory: Index'
        },
        'invstack_location': {
            'columns': ['invstack_location'],
            'title': 'Inventory: Location'
        },
        'invstack_manufacturer': {
            'columns': ['invstack_manufacturer'],
            'title': 'Inventory: Manufacturer'
        },
        'invstack_model': {
            'columns': ['invstack_model'],
            'title': 'Inventory: Model Name'
        },
        'invstack_name': {
            'columns': ['invstack_name'],
            'title': 'Inventory: Name'
        },
        'invstack_serial': {
            'columns': ['invstack_serial'],
            'title': 'Inventory: Serial Number'
        },
        'invstack_software': {
            'columns': ['invstack_software'],
            'title': 'Inventory: Software'
        },
        'invswpac_arch': {
            'columns': ['invswpac_arch'],
            'title': 'Inventory: Architecture'
        },
        'invswpac_install_date': {
            'columns': ['invswpac_install_date'],
            'title': 'Inventory: Install Date'
        },
        'invswpac_name': {
            'columns': ['invswpac_name'],
            'title': 'Inventory: Name'
        },
        'invswpac_package_type': {
            'columns': ['invswpac_package_type'],
            'title': 'Inventory: Type'
        },
        'invswpac_package_version': {
            'columns': ['invswpac_package_version'],
            'title': 'Inventory: Package Version'
        },
        'invswpac_path': {
            'columns': ['invswpac_path'],
            'title': 'Inventory: Path'
        },
        'invswpac_size': {
            'columns': ['invswpac_size'],
            'title': 'Inventory: Size'
        },
        'invswpac_summary': {
            'columns': ['invswpac_summary'],
            'title': 'Inventory: Description'
        },
        'invswpac_vendor': {
            'columns': ['invswpac_vendor'],
            'title': 'Inventory: Publisher'
        },
        'invswpac_version': {
            'columns': ['invswpac_version'],
            'title': 'Inventory: Version'
        },
        'invunknown_description': {
            'columns': ['invunknown_description'],
            'title': 'Inventory: Description'
        },
        'invunknown_index': {
            'columns': ['invunknown_index'],
            'title': 'Inventory: Index'
        },
        'invunknown_location': {
            'columns': ['invunknown_location'],
            'title': 'Inventory: Location'
        },
        'invunknown_manufacturer': {
            'columns': ['invunknown_manufacturer'],
            'title': 'Inventory: Manufacturer'
        },
        'invunknown_model': {
            'columns': ['invunknown_model'],
            'title': 'Inventory: Model Name'
        },
        'invunknown_name': {
            'columns': ['invunknown_name'],
            'title': 'Inventory: Name'
        },
        'invunknown_serial': {
            'columns': ['invunknown_serial'],
            'title': 'Inventory: Serial Number'
        },
        'invunknown_software': {
            'columns': ['invunknown_software'],
            'title': 'Inventory: Software'
        },
        'log_attempt': {
            'columns': ['log_attempt'],
            'title': 'Log: number of check attempt'
        },
        'log_contact_name': {
            'columns': ['log_contact_name'],
            'title': 'Log: contact name'
        },
        'log_date': {
            'columns': ['log_time'],
            'title': 'Log: day of entry'
        },
        'log_lineno': {
            'columns': ['log_lineno'],
            'title': 'Log: line number in log file'
        },
        'log_plugin_output': {
            'columns': [
                'log_plugin_output', 'log_type', 'log_state_type', 'log_comment', 'custom_variables'
            ],
            'title': 'Log: Output'
        },
        'log_state_type': {
            'columns': ['log_state_type'],
            'title': 'Log: type of state (hard/soft/stopped/started)'
        },
        'log_time': {
            'columns': ['log_time'],
            'title': 'Log: entry time'
        },
        'log_type': {
            'columns': ['log_type'],
            'title': 'Log: event'
        },
        'log_what': {
            'columns': ['log_type'],
            'title': 'Log: host or service'
        },
        'num_problems': {
            'columns': ['host_num_services', 'host_num_services_ok', 'host_num_services_pending'],
            'title': 'Number of problems'
        },
        'num_services': {
            'columns': ['host_num_services'],
            'title': 'Number of services'
        },
        'num_services_crit': {
            'columns': ['host_num_services_crit'],
            'title': 'Number of services in state CRIT'
        },
        'num_services_ok': {
            'columns': ['host_num_services_ok'],
            'title': 'Number of services in state OK'
        },
        'num_services_pending': {
            'columns': ['host_num_services_pending'],
            'title': 'Number of services in state PENDING'
        },
        'num_services_unknown': {
            'columns': ['host_num_services_unknown'],
            'title': 'Number of services in state UNKNOWN'
        },
        'num_services_warn': {
            'columns': ['host_num_services_warn'],
            'title': 'Number of services in state WARN'
        },
        'perfometer': {
            'columns': [
                'service_perf_data', 'service_state', 'service_check_command',
                'service_pnpgraph_present', 'service_plugin_output'
            ],
            'title': 'Perf-O-Meter'
        },
        'servicegroup': {
            'columns': ['servicegroup_alias'],
            'title': 'Servicegroup'
        },
        'servicelevel': {
            'columns': ['custom_variable_names', 'custom_variable_values'],
            'title': 'Servicelevel'
        },
        'sg_alias': {
            'columns': ['servicegroup_alias'],
            'title': 'Servicegroup alias'
        },
        'sg_name': {
            'columns': ['servicegroup_name'],
            'title': 'Servicegroup name'
        },
        'sg_num_services': {
            'columns': ['servicegroup_num_services'],
            'title': 'Number of services (Service Group)'
        },
        'sg_num_services_crit': {
            'columns': ['servicegroup_num_services_crit'],
            'title': 'Number of services in state CRIT (Service Group)'
        },
        'sg_num_services_ok': {
            'columns': ['servicegroup_num_services_ok'],
            'title': 'Number of services in state OK (Service Group)'
        },
        'sg_num_services_pending': {
            'columns': ['servicegroup_num_services_pending'],
            'title': 'Number of services in state PENDING (Service Group)'
        },
        'sg_num_services_unknown': {
            'columns': ['servicegroup_num_services_unknown'],
            'title': 'Number of services in state UNKNOWN (Service Group)'
        },
        'sg_num_services_warn': {
            'columns': ['servicegroup_num_services_warn'],
            'title': 'Number of services in state WARN (Service Group)'
        },
        'site': {
            'columns': ['site'],
            'title': 'Site'
        },
        'site_host': {
            'columns': ['site', 'host_name'],
            'title': 'Host site and name'
        },
        'sitealias': {
            'columns': ['site'],
            'title': 'Site Alias'
        },
        'stateage': {
            'columns': ['service_last_state_change'],
            'title': 'Service state age'
        },
        'svc_acknowledged': {
            'columns': ['service_acknowledged'],
            'title': 'Service problem acknowledged'
        },
        'svc_attempt': {
            'columns': ['service_current_attempt', 'service_max_check_attempts'],
            'title': 'Current check attempt'
        },
        'svc_check_age': {
            'columns': ['service_has_been_checked', 'service_last_check', 'service_cached_at'],
            'title': 'The time since the last check of the service'
        },
        'svc_check_command': {
            'columns': ['service_check_command'],
            'title': 'Service check command'
        },
        'svc_check_duration': {
            'columns': ['service_execution_time'],
            'title': 'Service check duration'
        },
        'svc_check_latency': {
            'columns': ['service_latency'],
            'title': 'Service check latency'
        },
        'svc_check_type': {
            'columns': ['service_check_type'],
            'title': 'Service check type'
        },
        'svc_contact_groups': {
            'columns': ['service_contact_groups'],
            'title': 'Service contact groups'
        },
        'svc_contacts': {
            'columns': ['service_contacts'],
            'title': 'Service contacts'
        },
        'svc_flapping': {
            'columns': ['service_is_flapping'],
            'title': 'Service is flapping'
        },
        'svc_group_memberlist': {
            'columns': ['service_groups'],
            'title': 'Service groups the service is member of'
        },
        'svc_in_downtime': {
            'columns': ['service_scheduled_downtime_depth'],
            'title': 'Currently in downtime'
        },
        'svc_in_notifper': {
            'columns': ['service_in_notification_period'],
            'title': 'In notification period'
        },
        'svc_is_active': {
            'columns': ['service_active_checks_enabled'],
            'title': 'Service is active'
        },
        'svc_last_notification': {
            'columns': ['service_last_notification'],
            'title': 'The time of the last service notification'
        },
        'svc_long_plugin_output': {
            'columns': ['service_long_plugin_output'],
            'title': 'Long output of check plugin'
        },
        'svc_next_check': {
            'columns': ['service_next_check'],
            'title': 'The time of the next scheduled service check'
        },
        'svc_next_notification': {
            'columns': ['service_next_notification'],
            'title': 'The time of the next service notification'
        },
        'svc_notifications_enabled': {
            'columns': ['service_notifications_enabled'],
            'title': 'Service notifications enabled'
        },
        'svc_notifper': {
            'columns': ['service_notification_period'],
            'title': 'Service notification period'
        },
        'svc_perf_val01': {
            'columns': ['service_perf_data'],
            'title': 'Service performance data - value number 01'
        },
        'svc_perf_val02': {
            'columns': ['service_perf_data'],
            'title': 'Service performance data - value number 02'
        },
        'svc_perf_val03': {
            'columns': ['service_perf_data'],
            'title': 'Service performance data - value number 03'
        },
        'svc_perf_val04': {
            'columns': ['service_perf_data'],
            'title': 'Service performance data - value number 04'
        },
        'svc_perf_val05': {
            'columns': ['service_perf_data'],
            'title': 'Service performance data - value number 05'
        },
        'svc_perf_val06': {
            'columns': ['service_perf_data'],
            'title': 'Service performance data - value number 06'
        },
        'svc_perf_val07': {
            'columns': ['service_perf_data'],
            'title': 'Service performance data - value number 07'
        },
        'svc_perf_val08': {
            'columns': ['service_perf_data'],
            'title': 'Service performance data - value number 08'
        },
        'svc_perf_val09': {
            'columns': ['service_perf_data'],
            'title': 'Service performance data - value number 09'
        },
        'svc_perf_val10': {
            'columns': ['service_perf_data'],
            'title': 'Service performance data - value number 10'
        },
        'svc_servicelevel': {
            'columns': ['service_custom_variable_names', 'service_custom_variable_values'],
            'title': 'Service service level'
        },
        'svc_staleness': {
            'columns': ['service_staleness'],
            'title': 'Service staleness value'
        },
        'svcdescr': {
            'columns': ['service_description'],
            'title': 'Service description'
        },
        'svcdispname': {
            'columns': ['service_display_name'],
            'title': 'Service alternative display name'
        },
        'svcoutput': {
            'columns': ['service_plugin_output'],
            'title': 'Service plugin output'
        },
        'svcstate': {
            'columns': ['service_state', 'service_has_been_checked'],
            'title': 'Service state'
        },
        'wato_folder_abs': {
            'columns': ['host_filename'],
            'title': 'WATO folder - complete path'
        },
        'wato_folder_plain': {
            'columns': ['host_filename'],
            'title': 'WATO folder - just folder name'
        },
        'wato_folder_rel': {
            'columns': ['host_filename'],
            'title': 'WATO folder - relative path'
        },
    }

    for sorter_class in cmk.gui.plugins.views.sorter_registry.values():
        sorter = sorter_class()
        spec = expected[sorter.ident]

        if isinstance(spec["title"], tuple) and spec["title"][0] == "func":
            assert hasattr(sorter.title, '__call__')
        else:
            assert sorter.title == spec["title"]

        if isinstance(spec["columns"], tuple) and spec["columns"][0] == "func":
            assert hasattr(sorter.columns, '__call__')
        else:
            assert sorter.columns == spec["columns"]

        assert sorter.load_inv == spec.get("load_inv", False)


def test_register_sorter(monkeypatch):
    monkeypatch.setattr(cmk.gui.plugins.views.utils, "sorter_registry",
                        cmk.gui.plugins.views.utils.SorterRegistry())

    def cmpfunc():
        pass

    cmk.gui.plugins.views.utils.register_sorter("abc", {
        "title": "A B C",
        "columns": ["x"],
        "cmp": cmpfunc,
    })

    sorter = cmk.gui.plugins.views.utils.sorter_registry["abc"]()
    assert isinstance(sorter, cmk.gui.plugins.views.utils.Sorter)
    assert sorter.ident == "abc"
    assert sorter.title == "A B C"
    assert sorter.columns == ["x"]
    assert sorter.cmp.__name__ == cmpfunc.__name__


def test_get_needed_regular_columns(view):

    columns = cmk.gui.views._get_needed_regular_columns(view.group_cells + view.row_cells, view.sorters, view.datasource)
    assert sorted(columns) == sorted([
        'host_scheduled_downtime_depth',
        'host_in_check_period',
        'host_num_services_pending',
        'host_downtimes_with_extra_info',
        'host_pnpgraph_present',
        'host_check_type',
        'host_accept_passive_checks',
        'host_num_services_crit',
        'host_icon_image',
        'host_is_flapping',
        'host_in_notification_period',
        'host_check_command',
        'host_modified_attributes_list',
        'host_downtimes',
        'host_filename',
        'host_acknowledged',
        'host_custom_variable_names',
        'host_state',
        'host_action_url_expanded',
        'host_comments_with_extra_info',
        'host_in_service_period',
        'host_num_services_ok',
        'host_has_been_checked',
        'host_address',
        'host_staleness',
        'host_num_services_unknown',
        'host_notifications_enabled',
        'host_active_checks_enabled',
        'host_perf_data',
        'host_custom_variable_values',
        'host_name',
        'host_num_services_warn',
        'host_notes_url_expanded',
    ])


def test_get_needed_join_columns(view):
    view_spec = copy.deepcopy(view.spec)
    view_spec["painters"].append(PainterSpec('service_description', None, None, 'CPU load'))
    view = cmk.gui.views.View(view.name, view_spec, view_spec.get("context", {}))

    columns = cmk.gui.views._get_needed_join_columns(view.join_cells, view.sorters)

    expected_columns = [
        'host_name',
        'service_description',
    ]

    if cmk_version.is_managed_edition():
        expected_columns += [
            "host_custom_variable_names",
            "host_custom_variable_values",
        ]

    assert sorted(columns) == sorted(expected_columns)


def test_create_view_basics():
    view_name = "allhosts"
    view_spec = cmk.gui.views.multisite_builtin_views[view_name]
    view = cmk.gui.views.View(view_name, view_spec, view_spec.get("context", {}))

    assert view.name == view_name
    assert view.spec == view_spec
    assert isinstance(view.datasource, cmk.gui.plugins.views.utils.ABCDataSource)
    assert isinstance(view.datasource.table, cmk.gui.plugins.views.utils.RowTable)
    assert view.row_limit is None
    assert view.user_sorters is None
    assert view.want_checkboxes is False
    assert view.only_sites is None


def test_view_row_limit(view):
    assert view.row_limit is None
    view.row_limit = 101
    assert view.row_limit == 101


@pytest.mark.parametrize("limit,permissions,result", [
    (None, [], 1000),

    ("soft", {}, 1000),
    ("hard", {}, 1000),
    ("none", {}, 1000),

    ("soft", {"general.ignore_soft_limit": True}, 1000),
    ("hard", {"general.ignore_soft_limit": True}, 5000),
    # Strange. Shouldn't this stick to the hard limit?
    ("none", {"general.ignore_soft_limit": True}, 1000),

    ("soft", {"general.ignore_soft_limit": True, "general.ignore_hard_limit": True}, 1000),
    ("hard", {"general.ignore_soft_limit": True, "general.ignore_hard_limit": True}, 5000),
    ("none", {"general.ignore_soft_limit": True, "general.ignore_hard_limit": True}, None),
])
def test_gui_view_row_limit(register_builtin_html, monkeypatch, mocker, limit, permissions, result):
    if limit is not None:
        monkeypatch.setitem(html.request._vars, "limit", limit)

    mocker.patch.object(config, "roles", {"nobody": {"permissions": permissions}})
    mocker.patch.object(config.user, "role_ids", ["nobody"])
    assert cmk.gui.views.get_limit() == result


def test_view_only_sites(view):
    assert view.only_sites is None
    view.only_sites = ["unit"]
    assert view.only_sites == ["unit"]


def test_view_user_sorters(view):
    assert view.user_sorters is None
    view.user_sorters = [("abc", True)]
    assert view.user_sorters == [("abc", True)]


def test_view_want_checkboxes(view):
    assert view.want_checkboxes is False
    view.want_checkboxes = True
    assert view.want_checkboxes is True


def test_registered_display_hints():
    expected = ['.',
    '.hardware.',
    '.hardware.chassis.',
    '.hardware.components.',
    '.hardware.components.backplanes:',
    '.hardware.components.backplanes:*.description',
    '.hardware.components.backplanes:*.index',
    '.hardware.components.backplanes:*.location',
    '.hardware.components.backplanes:*.manufacturer',
    '.hardware.components.backplanes:*.model',
    '.hardware.components.backplanes:*.name',
    '.hardware.components.backplanes:*.serial',
    '.hardware.components.backplanes:*.software',
    '.hardware.components.chassis:',
    '.hardware.components.chassis:*.description',
    '.hardware.components.chassis:*.index',
    '.hardware.components.chassis:*.location',
    '.hardware.components.chassis:*.manufacturer',
    '.hardware.components.chassis:*.model',
    '.hardware.components.chassis:*.name',
    '.hardware.components.chassis:*.serial',
    '.hardware.components.chassis:*.software',
    '.hardware.components.containers:',
    '.hardware.components.containers:*.description',
    '.hardware.components.containers:*.index',
    '.hardware.components.containers:*.location',
    '.hardware.components.containers:*.manufacturer',
    '.hardware.components.containers:*.model',
    '.hardware.components.containers:*.name',
    '.hardware.components.containers:*.serial',
    '.hardware.components.containers:*.software',
    '.hardware.components.fans:',
    '.hardware.components.fans:*.description',
    '.hardware.components.fans:*.index',
    '.hardware.components.fans:*.location',
    '.hardware.components.fans:*.manufacturer',
    '.hardware.components.fans:*.model',
    '.hardware.components.fans:*.name',
    '.hardware.components.fans:*.serial',
    '.hardware.components.fans:*.software',
    '.hardware.components.modules:',
    '.hardware.components.modules:*.bootloader',
    '.hardware.components.modules:*.description',
    '.hardware.components.modules:*.firmware',
    '.hardware.components.modules:*.index',
    '.hardware.components.modules:*.location',
    '.hardware.components.modules:*.manufacturer',
    '.hardware.components.modules:*.model',
    '.hardware.components.modules:*.name',
    '.hardware.components.modules:*.serial',
    '.hardware.components.modules:*.software',
    '.hardware.components.modules:*.type',
    '.hardware.components.others:',
    '.hardware.components.others:*.description',
    '.hardware.components.others:*.index',
    '.hardware.components.others:*.location',
    '.hardware.components.others:*.manufacturer',
    '.hardware.components.others:*.model',
    '.hardware.components.others:*.name',
    '.hardware.components.others:*.serial',
    '.hardware.components.others:*.software',
    '.hardware.components.psus:',
    '.hardware.components.psus:*.description',
    '.hardware.components.psus:*.index',
    '.hardware.components.psus:*.location',
    '.hardware.components.psus:*.manufacturer',
    '.hardware.components.psus:*.model',
    '.hardware.components.psus:*.name',
    '.hardware.components.psus:*.serial',
    '.hardware.components.psus:*.software',
    '.hardware.components.sensors:',
    '.hardware.components.sensors:*.description',
    '.hardware.components.sensors:*.index',
    '.hardware.components.sensors:*.location',
    '.hardware.components.sensors:*.manufacturer',
    '.hardware.components.sensors:*.model',
    '.hardware.components.sensors:*.name',
    '.hardware.components.sensors:*.serial',
    '.hardware.components.sensors:*.software',
    '.hardware.components.stacks:',
    '.hardware.components.stacks:*.description',
    '.hardware.components.stacks:*.index',
    '.hardware.components.stacks:*.location',
    '.hardware.components.stacks:*.manufacturer',
    '.hardware.components.stacks:*.model',
    '.hardware.components.stacks:*.name',
    '.hardware.components.stacks:*.serial',
    '.hardware.components.stacks:*.software',
    '.hardware.components.unknowns:',
    '.hardware.components.unknowns:*.description',
    '.hardware.components.unknowns:*.index',
    '.hardware.components.unknowns:*.location',
    '.hardware.components.unknowns:*.manufacturer',
    '.hardware.components.unknowns:*.model',
    '.hardware.components.unknowns:*.name',
    '.hardware.components.unknowns:*.serial',
    '.hardware.components.unknowns:*.software',
    '.hardware.cpu.',
    '.hardware.cpu.arch',
    '.hardware.cpu.bus_speed',
    '.hardware.cpu.cache_size',
    '.hardware.cpu.cores',
    '.hardware.cpu.cores_per_cpu',
    '.hardware.cpu.cpu_max_capa',
    '.hardware.cpu.cpus',
    '.hardware.cpu.entitlement',
    '.hardware.cpu.implementation_mode',
    '.hardware.cpu.logical_cpus',
    '.hardware.cpu.max_speed',
    '.hardware.cpu.model',
    '.hardware.cpu.sharing_mode',
    '.hardware.cpu.smt_threads',
    '.hardware.cpu.threads',
    '.hardware.cpu.threads_per_cpu',
    '.hardware.cpu.voltage',
    '.hardware.memory.',
    '.hardware.memory.arrays:',
    '.hardware.memory.arrays:*.',
    '.hardware.memory.arrays:*.devices:',
    '.hardware.memory.arrays:*.devices:*.',
    '.hardware.memory.arrays:*.devices:*.size',
    '.hardware.memory.arrays:*.devices:*.speed',
    '.hardware.memory.arrays:*.maximum_capacity',
    '.hardware.memory.total_ram_usable',
    '.hardware.memory.total_swap',
    '.hardware.memory.total_vmalloc',
    '.hardware.nwadapter:',
    '.hardware.nwadapter:*.',
    '.hardware.nwadapter:*.gateway',
    '.hardware.nwadapter:*.ipv4_address',
    '.hardware.nwadapter:*.ipv4_subnet',
    '.hardware.nwadapter:*.ipv6_address',
    '.hardware.nwadapter:*.ipv6_subnet',
    '.hardware.nwadapter:*.macaddress',
    '.hardware.nwadapter:*.name',
    '.hardware.nwadapter:*.speed',
    '.hardware.nwadapter:*.type',
    '.hardware.storage.',
    '.hardware.storage.controller.',
    '.hardware.storage.controller.version',
    '.hardware.storage.disks:',
    '.hardware.storage.disks:*.',
    '.hardware.storage.disks:*.bus',
    '.hardware.storage.disks:*.fsnode',
    '.hardware.storage.disks:*.local',
    '.hardware.storage.disks:*.product',
    '.hardware.storage.disks:*.serial',
    '.hardware.storage.disks:*.signature',
    '.hardware.storage.disks:*.size',
    '.hardware.storage.disks:*.type',
    '.hardware.storage.disks:*.vendor',
    '.hardware.system.',
    '.hardware.system.expresscode',
    '.hardware.system.manufacturer',
    '.hardware.system.model',
    '.hardware.system.model_name',
    '.hardware.system.product',
    '.hardware.system.serial',
    '.hardware.system.serial_number',
    '.hardware.video:',
    '.hardware.video:*.',
    '.hardware.video:*.driver',
    '.hardware.video:*.driver_date',
    '.hardware.video:*.driver_version',
    '.hardware.video:*.graphic_memory',
    '.hardware.video:*.name',
    '.hardware.video:*.subsystem',
    '.hardware.volumes.physical_volumes.*:',
    '.hardware.volumes.physical_volumes:*.volume_group_name',
    '.hardware.volumes.physical_volumes:*.physical_volume_name',
    '.hardware.volumes.physical_volumes:*.physical_volume_status',
    '.hardware.volumes.physical_volumes:*.physical_volume_total_partitions',
    '.hardware.volumes.physical_volumes:*.physical_volume_free_partitions',
    '.networking.',
    '.networking.addresses:',
    '.networking.addresses:*.address',
    '.networking.addresses:*.device',
    '.networking.addresses:*.type',
    '.networking.available_ethernet_ports',
    '.networking.interfaces:',
    '.networking.interfaces:*.admin_status',
    '.networking.interfaces:*.alias',
    '.networking.interfaces:*.available',
    '.networking.interfaces:*.description',
    '.networking.interfaces:*.index',
    '.networking.interfaces:*.last_change',
    '.networking.interfaces:*.oper_status',
    '.networking.interfaces:*.phys_address',
    '.networking.interfaces:*.port_type',
    '.networking.interfaces:*.speed',
    '.networking.interfaces:*.vlans',
    '.networking.interfaces:*.vlantype',
    '.networking.routes:',
    '.networking.routes:*.device',
    '.networking.routes:*.gateway',
    '.networking.routes:*.target',
    '.networking.routes:*.type',
    '.networking.total_ethernet_ports',
    '.networking.total_interfaces',
    '.networking.tunnels:',
    '.networking.tunnels:*.index',
    '.networking.tunnels:*.link_priority',
    '.networking.tunnels:*.peerip',
    '.networking.tunnels:*.peername',
    '.networking.tunnels:*.sourceip',
    '.networking.tunnels:*.tunnel_interface',
    '.networking.wlan',
    '.networking.wlan.controller',
    '.networking.wlan.controller.accesspoints:',
    '.networking.wlan.controller.accesspoints:*.group',
    '.networking.wlan.controller.accesspoints:*.ip_addr',
    '.networking.wlan.controller.accesspoints:*.model',
    '.networking.wlan.controller.accesspoints:*.name',
    '.networking.wlan.controller.accesspoints:*.serial',
    '.networking.wlan.controller.accesspoints:*.sys_location',
    '.software.',
    '.software.applications.',
    '.software.applications.check_mk.',
    '.software.applications.check_mk.agent_version',
    '.software.applications.check_mk.cluster.is_cluster',
    '.software.applications.check_mk.cluster.nodes:',
    '.software.applications.check_mk.num_hosts',
    '.software.applications.check_mk.num_services',
    '.software.applications.check_mk.host_labels:',
    '.software.applications.check_mk.host_labels:*.plugin_name',
    '.software.applications.check_mk.host_labels:*.label',
    '.software.applications.check_mk.versions:',
    '.software.applications.check_mk.versions:*.demo',
    '.software.applications.check_mk.sites:',
    '.software.applications.check_mk.sites:*.autostart',
    '.software.applications.check_mk.sites:*.apache',
    '.software.applications.check_mk.sites:*.cmc',
    '.software.applications.check_mk.sites:*.crontab',
    '.software.applications.check_mk.sites:*.dcd',
    '.software.applications.check_mk.sites:*.liveproxyd',
    '.software.applications.check_mk.sites:*.mkeventd',
    '.software.applications.check_mk.sites:*.mknotifyd',
    '.software.applications.check_mk.sites:*.rrdcached',
    '.software.applications.check_mk.sites:*.stunnel',
    '.software.applications.check_mk.sites:*.xinetd',
    '.software.applications.check_mk.sites:*.nagios',
    '.software.applications.check_mk.sites:*.npcd',
    '.software.applications.check_mk.sites:*.check_helper_usage',
    '.software.applications.check_mk.sites:*.check_mk_helper_usage',
    '.software.applications.check_mk.sites:*.fetcher_helper_usage',
    '.software.applications.check_mk.sites:*.checker_helper_usage',
    '.software.applications.check_mk.sites:*.livestatus_usage',
    '.software.applications.check_mk.sites:*.num_hosts',
    '.software.applications.check_mk.sites:*.num_services',
    '.software.applications.check_mk.sites:*.used_version',
    '.software.applications.citrix.',
    '.software.applications.citrix.controller.',
    '.software.applications.citrix.controller.controller_version',
    '.software.applications.citrix.vm.',
    '.software.applications.citrix.vm.agent_version',
    '.software.applications.citrix.vm.catalog',
    '.software.applications.citrix.vm.desktop_group_name',
    '.software.applications.docker.',
    '.software.applications.docker.container.',
    '.software.applications.docker.container.networks:',
    '.software.applications.docker.container.networks:*.ip_address',
    '.software.applications.docker.container.networks:*.ip_prefixlen',
    '.software.applications.docker.container.networks:*.mac_address',
    '.software.applications.docker.container.networks:*.network_id',
    '.software.applications.docker.container.node_name',
    '.software.applications.docker.container.ports:',
    '.software.applications.docker.containers:',
    '.software.applications.docker.containers:*.id',
    '.software.applications.docker.containers:*.labels',
    '.software.applications.docker.images:',
    '.software.applications.docker.images:*.size',
    '.software.applications.docker.images:*.amount_containers',
    '.software.applications.docker.images:*.id',
    '.software.applications.docker.images:*.labels',
    '.software.applications.docker.images:*.repodigests',
    '.software.applications.docker.images:*.repotags',
    '.software.applications.docker.networks.*.',
    '.software.applications.docker.networks.*.containers:',
    '.software.applications.docker.networks.*.containers:*.id',
    '.software.applications.docker.networks.*.containers:*.ipv4_address',
    '.software.applications.docker.networks.*.containers:*.ipv6_address',
    '.software.applications.docker.networks.*.containers:*.mac_address',
    '.software.applications.docker.networks.*.network_id',
    '.software.applications.docker.num_containers_paused',
    '.software.applications.docker.num_containers_running',
    '.software.applications.docker.num_containers_stopped',
    '.software.applications.docker.num_containers_total',
    '.software.applications.docker.num_images',
    '.software.applications.docker.version',
    '.software.applications.ibm_mq.',
    '.software.applications.ibm_mq.channels:',
    '.software.applications.ibm_mq.channels:*.name',
    '.software.applications.ibm_mq.channels:*.qmgr',
    '.software.applications.ibm_mq.channels:*.status',
    '.software.applications.ibm_mq.channels:*.type',
    '.software.applications.ibm_mq.managers:',
    '.software.applications.ibm_mq.managers:*.instname',
    '.software.applications.ibm_mq.managers:*.instver',
    '.software.applications.ibm_mq.managers:*.name',
    '.software.applications.ibm_mq.managers:*.standby',
    '.software.applications.ibm_mq.managers:*.status',
    '.software.applications.ibm_mq.queues:',
    '.software.applications.ibm_mq.queues:*.maxdepth',
    '.software.applications.ibm_mq.queues:*.maxmsgl',
    '.software.applications.ibm_mq.queues:*.name',
    '.software.applications.ibm_mq.queues:*.qmgr',
    '.software.applications.kubernetes.assigned_pods:',
    '.software.applications.kubernetes.assigned_pods:*.name',
    '.software.applications.kubernetes.nodes:',
    '.software.applications.kubernetes.nodes:*.name',
    '.software.applications.kubernetes.ingresses:',
    '.software.applications.kubernetes.pod_container:',
    '.software.applications.kubernetes.pod_container:*.container_id',
    '.software.applications.kubernetes.pod_container:*.image',
    '.software.applications.kubernetes.pod_container:*.image_id',
    '.software.applications.kubernetes.pod_container:*.image_pull_policy',
    '.software.applications.kubernetes.pod_container:*.name',
    '.software.applications.kubernetes.pod_container:*.ready',
    '.software.applications.kubernetes.pod_container:*.restart_count',
    '.software.applications.kubernetes.job_container:',
    '.software.applications.kubernetes.job_container:*.name',
    '.software.applications.kubernetes.job_container:*.image',
    '.software.applications.kubernetes.job_container:*.image_pull_policy',
    '.software.applications.kubernetes.daemon_pod_containers:*.name',
    '.software.applications.kubernetes.daemon_pod_containers:*.image',
    '.software.applications.kubernetes.daemon_pod_containers:*.image_pull_policy',
    '.software.applications.kubernetes.pod_info.',
    '.software.applications.kubernetes.pod_info.dns_policy',
    '.software.applications.kubernetes.pod_info.host_ip',
    '.software.applications.kubernetes.pod_info.host_network',
    '.software.applications.kubernetes.pod_info.node',
    '.software.applications.kubernetes.pod_info.pod_ip',
    '.software.applications.kubernetes.pod_info.qos_class',
    '.software.applications.kubernetes.roles:',
    '.software.applications.kubernetes.roles:*.namespace',
    '.software.applications.kubernetes.roles:*.role',
    '.software.applications.kubernetes.selector.',
    '.software.applications.kubernetes.service_info.',
    '.software.applications.kubernetes.service_info.cluster_ip',
    '.software.applications.kubernetes.service_info.load_balancer_ip',
    '.software.applications.kubernetes.service_info.type',
    '.software.applications.mssql.',
    '.software.applications.mssql.instances:',
    '.software.applications.mssql.instances:*.clustered',
    '.software.applications.oracle.',
    '.software.applications.oracle.dataguard_stats:',
    '.software.applications.oracle.dataguard_stats:*.db_unique',
    '.software.applications.oracle.dataguard_stats:*.role',
    '.software.applications.oracle.dataguard_stats:*.sid',
    '.software.applications.oracle.dataguard_stats:*.switchover',
    '.software.applications.oracle.systemparameter:',
    '.software.applications.oracle.systemparameter:*.sid',
    '.software.applications.oracle.systemparameter:*.name',
    '.software.applications.oracle.systemparameter:*.value',
    '.software.applications.oracle.systemparameter:*.isdefault',
    '.software.applications.oracle.instance:',
    '.software.applications.oracle.instance:*.db_creation_time',
    '.software.applications.oracle.instance:*.db_uptime',
    '.software.applications.oracle.instance:*.logins',
    '.software.applications.oracle.instance:*.logmode',
    '.software.applications.oracle.instance:*.openmode',
    '.software.applications.oracle.instance:*.pname',
    '.software.applications.oracle.instance:*.sid',
    '.software.applications.oracle.instance:*.version',
    '.software.applications.oracle.recovery_area:',
    '.software.applications.oracle.recovery_area:*.flashback',
    '.software.applications.oracle.recovery_area:*.sid',
    ".software.applications.oracle.pga:",
    ".software.applications.oracle.pga:*.aggregate_pga_auto_target",
    ".software.applications.oracle.pga:*.aggregate_pga_target_parameter",
    ".software.applications.oracle.pga:*.bytes_processed",
    ".software.applications.oracle.pga:*.extra_bytes_read_written",
    ".software.applications.oracle.pga:*.global_memory_bound",
    ".software.applications.oracle.pga:*.maximum_pga_allocated",
    ".software.applications.oracle.pga:*.maximum_pga_used_for_auto_workareas",
    ".software.applications.oracle.pga:*.maximum_pga_used_for_manual_workareas",
    ".software.applications.oracle.pga:*.sid",
    ".software.applications.oracle.pga:*.total_freeable_pga_memory",
    ".software.applications.oracle.pga:*.total_pga_allocated",
    ".software.applications.oracle.pga:*.total_pga_inuse",
    ".software.applications.oracle.pga:*.total_pga_used_for_auto_workareas",
    ".software.applications.oracle.pga:*.total_pga_used_for_manual_workareas",
    '.software.applications.oracle.sga:',
    '.software.applications.oracle.sga:*.buf_cache_size',
    '.software.applications.oracle.sga:*.data_trans_cache_size',
    '.software.applications.oracle.sga:*.fixed_size',
    '.software.applications.oracle.sga:*.free_mem_avail',
    '.software.applications.oracle.sga:*.granule_size',
    '.software.applications.oracle.sga:*.in_mem_area_size',
    '.software.applications.oracle.sga:*.java_pool_size',
    '.software.applications.oracle.sga:*.large_pool_size',
    '.software.applications.oracle.sga:*.max_size',
    '.software.applications.oracle.sga:*.redo_buffer',
    '.software.applications.oracle.sga:*.shared_io_pool_size',
    '.software.applications.oracle.sga:*.shared_pool_size',
    '.software.applications.oracle.sga:*.sid',
    '.software.applications.oracle.sga:*.start_oh_shared_pool',
    '.software.applications.oracle.sga:*.streams_pool_size',
    '.software.applications.oracle.tablespaces:',
    '.software.applications.oracle.tablespaces:*.autoextensible',
    '.software.applications.oracle.tablespaces:*.current_size',
    '.software.applications.oracle.tablespaces:*.free_space',
    '.software.applications.oracle.tablespaces:*.increment_size',
    '.software.applications.oracle.tablespaces:*.max_size',
    '.software.applications.oracle.tablespaces:*.name',
    '.software.applications.oracle.tablespaces:*.num_increments',
    '.software.applications.oracle.tablespaces:*.sid',
    '.software.applications.oracle.tablespaces:*.type',
    '.software.applications.oracle.tablespaces:*.used_size',
    '.software.applications.oracle.tablespaces:*.version',
    '.software.applications.vmwareesx:*.',
    '.software.applications.vmwareesx:*.clusters:*.',
    '.software.bios.',
    '.software.bios.date',
    '.software.bios.vendor',
    '.software.bios.version',
    '.software.configuration.',
    '.software.configuration.snmp_info.',
    '.software.configuration.snmp_info.contact',
    '.software.configuration.snmp_info.location',
    '.software.configuration.snmp_info.name',
    '.software.firmware',
    '.software.firmware.platform_level',
    '.software.firmware.vendor',
    '.software.firmware.version',
    '.software.kernel_config:',
    '.software.kernel_config:*.parameter',
    '.software.kernel_config:*.value',
    '.software.os.',
    '.software.os.arch',
    '.software.os.install_date',
    '.software.os.kernel_version',
    '.software.os.name',
    '.software.os.service_pack',
    '.software.os.service_packs:',
    '.software.os.type',
    '.software.os.vendor',
    '.software.os.version',
    '.software.packages:',
    '.software.packages:*.arch',
    '.software.packages:*.install_date',
    '.software.packages:*.name',
    '.software.packages:*.package_type',
    '.software.packages:*.package_version',
    '.software.packages:*.path',
    '.software.packages:*.size',
    '.software.packages:*.summary',
    '.software.packages:*.vendor',
    '.software.packages:*.version',]

    assert sorted(expected) == sorted(cmk.gui.plugins.views.inventory_displayhints.keys())


def test_get_inventory_display_hint():
    hint = cmk.gui.plugins.views.inventory_displayhints.get(".software.packages:*.summary")
    assert isinstance(hint, dict)
