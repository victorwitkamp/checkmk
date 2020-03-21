#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

import re
import json
from datetime import datetime
import cmk.gui.sites as sites
from cmk.gui.exceptions import MKTimeout, MKGeneralException, MKUserError
from cmk.gui.i18n import _
from cmk.gui.globals import html
from cmk.gui.valuespec import (
    Dictionary,
    DropdownChoice,
    Timerange,
)
from cmk.gui.plugins.dashboard import (
    Dashlet,
    dashlet_registry,
)
from cmk.gui.pages import page_registry, AjaxPage
from cmk.utils.render import date_and_time
from cmk.gui.visuals import get_filter_headers
from cmk.gui.log import logger


def _query_for_alerts(time_range, context, dashlet_infos, return_column_headers=True):
    c_headers = "ColumnHeaders: on\n" if return_column_headers else ""
    filter_headers, only_sites = get_filter_headers("log", dashlet_infos, context)
    query = ("GET log\n"
             "Columns: log_state host_name service_description log_type log_time\n"
             "%s"
             "Filter: class = 1\n"
             "Filter: log_time >= %f\n"
             "Filter: log_time <= %f\n"
             "%s" % (c_headers, time_range[0], time_range[1], filter_headers))
    try:
        if only_sites:
            sites.live().set_only_sites(only_sites)
        rows = sites.live().query(query)
    except MKTimeout:
        raise
    except Exception as _e:
        raise MKGeneralException(
            _("The query for the given metric, service and host names returned no data."))
    finally:
        sites.live().set_only_sites(None)

    c_headers = ""
    if return_column_headers:
        c_headers = rows.pop(0)
    return rows, c_headers


def _forge_tooltip_and_url(start_time, value, context, timestep, end_time, log_type):
    # TODO: move this to context dict
    type_params = {
        "host": "logst_h0=on&logst_h1=on&logst_h2=on",
        "service": "logst_s0=on&logst_s1=on&logst_s2=on&logst_s3=on",
    }
    context_filters = "&"
    for fil in context.values():
        for k, f in fil.iteritems():
            context_filters += "%s=%s&" % (k, f)
    context_filters = context_filters.rstrip("&")
    if start_time + timestep < end_time:
        end_time = start_time + timestep - 1
    '''
    dt_start = datetime.fromtimestamp(start_time)
    dt_end = datetime.fromtimestamp(end_time)
    time_pattern = "%m-%d, %H:%M"
    if dt_end.strftime("%Y") != dt_start.strftime("%Y"):
        time_pattern = "%Y-%m-%d, %H:%M"
    from_time_str = dt_start.strftime(time_pattern)
    to_time_str = dt_end.strftime(time_pattern)
    '''
    from_time_str = date_and_time(start_time)
    to_time_str = date_and_time(end_time)

    tooltip = html.render_table(
        html.render_tr(html.render_td(_("From:")) + html.render_td(from_time_str)) +
        html.render_tr(html.render_td(_("To:")) + html.render_td(to_time_str)) +
        html.render_tr(html.render_td("Alerts:") + html.render_td(value)),
        class_="alert_info_table",
    )
    url = "view.py?filled_in=filter&view_name=events&logtime_from=%(from)d&logtime_from_range=unix&logtime_until=%(until)d&logtime_until_range=unix&logclass1=on&%(type)s%(context)s" % {
        "from": start_time,
        "until": end_time,
        "type": type_params[log_type],
        "context": context_filters,
    }
    return tooltip, url


def _forge_timestamps_and_timestep(time_range, resolution):
    """Round down the starting timestamp to the beginning of the respective hour
    or day and return the adjusted time range with the time step"""
    timestep = 60 * 60
    if resolution == "d":
        timestep *= 24
    timestamps = [time_range[0]]
    if time_range[0] + timestep >= time_range[1]:
        return timestamps, timestep

    if time_range[0] % 3600 != 0:
        # Adding 3600 (1h) because timestamp 0 corresponds to
        # 1970-01-01 01:00 (not 00:00)
        timestamps.append(time_range[0] + timestep - (time_range[0] + 3600) % timestep)
    timestamps = timestamps[:-1] + range(timestamps[-1], time_range[1], timestep)
    if timestamps[-1] != time_range[1]:
        timestamps.append(time_range[1])
    return timestamps, timestep


def _parse_alerts_list(rows, time_range, resolution, context):
    """Returns a dict with keys "host" and "service" for respective lists
    of the number of host/service alerts as well as optional detail per
    day/hour and information about the specified time settings:
    alerts_list = [{
        "host": { "value": 15, "tooltip": blabla, "url": https://blabla.bla, <optional_detail> },
        "service": { "value": 17, "tooltip": blabli, "url": https://blabli.blu, <optional_detail> },
        "timestamp": 1234567,
        "timestep": 84600,
        "label": 23.03.2020,
    }, ... ]
    """
    timestamps, basic_timestep = _forge_timestamps_and_timestep(time_range, resolution)
    alerts_list = []
    for timestamp in timestamps:
        # Adding 3600 (1h) because timestamp 0 corresponds to
        # 1970-01-01 01:00 (not 00:00)
        timestep = basic_timestep - (timestamp + 3600) % basic_timestep
        if timestamp + basic_timestep > time_range[1]:
            timestep = time_range[1] - timestamp
        alerts_list.append({
            "timestamp": timestamp,
            "timestep": timestep,
            "label": date_and_time(timestamp),
            "host": {
                "value": 0,
                "tooltip": "",
                "url": "",
                "css": []
            },
            "service": {
                "value": 0,
                "tooltip": "",
                "url": "",
                "css": []
            }
        })

    rows.sort(key=lambda x: x[4])
    row_offset = 0
    for time_frame in alerts_list:
        end_time = time_frame["timestamp"] + time_frame["timestep"] - 1
        for row in rows[row_offset:]:
            if row[4] >= end_time:
                break
            row_offset += 1
            log_type = row[3]
            if re.match("HOST *", log_type):
                time_frame["host"]["value"] += 1
            else:
                time_frame["service"]["value"] += 1

    for time_frame in alerts_list:
        for key in ["host", "service"]:
            tooltip, url = _forge_tooltip_and_url(time_frame["timestamp"], time_frame[key]["value"],
                                                  context, time_frame["timestep"], time_range[1],
                                                  key)
            time_frame[key]["tooltip"] = tooltip
            time_frame[key]["url"] = url
    return alerts_list


def _alert_data_to_bar_chart_structure(alerts_list, log_type, title=None):
    if not log_type in ["service", "host"]:
        raise MKUserError("log_type", _("Invalid log type given: %s" % log_type))
    if not title:
        title = "%s alerts" % log_type.capitalize()

    for time_frame in alerts_list:
        time_frame.update(time_frame[log_type])
    return {"title": title, "elements": alerts_list}


def _fetch_alert_data(properties, context, dashlet_infos):
    rangespec = properties["time_range"]
    resolution = properties["time_resolution"]
    time_range, _range_title = Timerange().compute_range(rangespec)
    time_range = [int(t) for t in time_range]
    alerts, _column_headers = _query_for_alerts(time_range, context, dashlet_infos)
    alerts_list = _parse_alerts_list(alerts, time_range, resolution, context)
    return alerts_list


def _group_data_elements(data,
                         properties,
                         context,
                         log_type,
                         grouping_indices=None,
                         group_size=None):
    rangespec = properties["time_range"]
    time_range, _range_title = Timerange().compute_range(rangespec)
    if group_size:
        grouping_indices = [[k, k + group_size - 1] for k in range(0, len(data), group_size)]
        grouping_indices[-1][1] = len(data) - 1
    if not grouping_indices:
        raise MKUserError("alert_grouping", _("No group size or grouping indices given"))
    grouped_data = []
    for start, end in grouping_indices:
        grouped_data.append({
            "value": sum([e["value"] for e in data[start:end + 1]]),
            "element_range": [start, end],
            "timestamp": data[start]["timestamp"],
            "timestep": data[end]["timestamp"] + data[end]["timestep"] - data[start]["timestamp"],
            "url": "",
            "tooltip": "",
            "css": "",
        })
    if properties["time_resolution"] == "h":
        timestep = 3600 * group_size
    else:
        timestep = 86400 * group_size
    for time_frame in grouped_data:
        tooltip, url = _forge_tooltip_and_url(time_frame["timestamp"], time_frame["value"], context,
                                              timestep, time_range[1], log_type)
        time_frame["tooltip"] = tooltip
        time_frame["url"] = url
    return grouped_data


@dashlet_registry.register
class AlertBarChartDashlet(Dashlet):
    """Dashlet that displays a bar chart for host and service alerts"""
    @classmethod
    def type_name(cls):
        return "alert_bar_chart_metric"

    @classmethod
    def title(cls):
        return _("Host and service alerts")

    @classmethod
    def description(cls):
        return _("Displays a bar chart for host and service alerts.")

    @classmethod
    def sort_index(cls):
        return 95

    @classmethod
    def initial_refresh_interval(cls):
        return False

    @classmethod
    def initial_size(cls):
        return (62, 48)

    @classmethod
    def default_settings(cls):
        return {}

    @classmethod
    def infos(cls):
        return ["host", "service"]

    @classmethod
    def single_infos(cls):
        return []

    @classmethod
    def has_context(cls):
        # type: () -> bool
        """Whether or not this dashlet is context sensitive."""
        return True

    @classmethod
    def vs_parameters(cls):
        return Dictionary(title=_("Properties"),
                          render="form",
                          optional_keys=[],
                          elements=[
                              ("time_range", Timerange(
                                  title=_("Time range"),
                                  default_value='d0',
                              )),
                              ("time_resolution",
                               DropdownChoice(title=_("Time resolution"),
                                              choices=[("h", _("Show alerts per hour")),
                                                       ("d", _("Show alerts per day"))],
                                              default_value="d")),
                          ])

    def show(self):
        #TODO: get rid of this debugging line
        html.header("HUHU")
        real_valuespec = self.vs_parameters()
        json_value = real_valuespec.value_to_json(self._dashlet_spec)
        context = self._dashlet_spec["context"]
        html.debug(context)
        html.debug(json_value)

        post_params = "context=%s&properties=%s" % (json.dumps(context), json.dumps(json_value))
        fetch_url = "alert_test.py"
        div_id = "alert_dashlet_%d" % self._dashlet_id
        html.open_div(id_=div_id)
        html.close_div()
        html.javascript(
            """
            let bar_chart_class_%(dashlet_id)d = cmk.figures.figure_registry.get_figure("barbar_chart");
            let bar_chart_%(dashlet_id)d = new bar_chart_class_%(dashlet_id)d("#%(div_id)s", 600, 400);
            bar_chart_%(dashlet_id)d.initialize();
            bar_chart_%(dashlet_id)d.set_post_url_and_body("%(url)s", '%(post_params)s');
            bar_chart_%(dashlet_id)d.scheduler.enable();
            """ % {
                "dashlet_id": self._dashlet_id,
                "div_id": div_id,
                "url": fetch_url,
                "post_params": post_params
            })


@page_registry.register_page("alert_test")
class AlertTestDataPage(AjaxPage):
    def page(self):
        dashlet_vs = AlertBarChartDashlet.vs_parameters()
        dashlet_infos = AlertBarChartDashlet.infos()
        properties = dashlet_vs.value_from_json(json.loads(html.request.var("properties")))
        context = json.loads(html.request.var("context"))
        data = _fetch_alert_data(properties, context, dashlet_infos)
        _host_data = _alert_data_to_bar_chart_structure(data, "host")
        service_data = _alert_data_to_bar_chart_structure(data, "service")
        service_data["grouped_elements"] = _group_data_elements(service_data["elements"],
                                                                properties,
                                                                context,
                                                                "service",
                                                                group_size=12)

        return create_response(service_data)


def create_response(data, context=None):
    response = {"data": data}
    if context:
        response["context"] = context
    return response
