#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from typing import List, Optional, Tuple as _Tuple

from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    CascadingDropdown,
    Dictionary,
    DictionaryElements,
    DropdownChoice,
    GraphColor,
    Timerange,
)

from cmk.gui.pages import page_registry, AjaxPage
from cmk.gui.plugins.dashboard import dashlet_registry, ABCFigureDashlet, ABCDataGenerator
from cmk.gui.plugins.dashboard.utils import site_query, create_data_for_single_metric
from cmk.gui.plugins.metrics.valuespecs import ValuesWithUnits
from cmk.gui.plugins.metrics.utils import MetricName, reverse_translate_metric_name
from cmk.gui.plugins.metrics.html_render import title_info_elements
from cmk.gui.plugins.metrics.rrd_fetch import rrd_columns
from cmk.gui.plugins.views.painters import paint_service_state_short


class SingleMetricDataGenerator(ABCDataGenerator):
    def __init__(self, exclude_properties: Optional[List[str]] = None):
        self._exclude_properties = exclude_properties

    def vs_parameters(self):
        return Dictionary(title=_("Properties"),
                          render="form",
                          optional_keys=False,
                          elements=self._vs_elements())

    @staticmethod
    def _time_range_historic_dict_elements() -> DictionaryElements:
        return [
            (
                'window',
                Timerange(
                    title=_("Time range to consider"),
                    default_value="d0",
                    allow_empty=True,
                ),
            ),
            (
                "rrd_consolidation",
                DropdownChoice(
                    choices=[
                        ("average", _("Average")),
                        ("min", _("Minimum")),
                        ("max", _("Maximum")),
                    ],
                    default_value="max",
                    title="RRD consolidation",
                    help=_("Consolidation function for the [cms_graphing#rrds|RRD] data column"),
                ),
            ),
        ]

    def _vs_elements(self):
        elements = [
            ("metric", MetricName()),  # MetricChoice would be nicer, but we use the context filters
            (
                "time_range",
                CascadingDropdown(
                    title=_("Timerange"),
                    orientation="horizontal",
                    choices=[
                        (
                            "current",
                            _("Only show current value"),
                        ),
                        (
                            "range",
                            _("Show historic values"),
                            Dictionary(
                                optional_keys=False,
                                elements=self._time_range_historic_dict_elements(),
                            ),
                        ),
                    ],
                    default_value="current",
                ),
            ),
            ("display_range",
             CascadingDropdown(title=_("Display range"),
                               choices=[
                                   ("infer", _("Automatic")),
                                   ("fixed", _("Fixed range"),
                                    ValuesWithUnits(
                                        vs_name="display_range",
                                        metric_vs_name="metric",
                                        help=_("Set the range in which data is displayed. "
                                               "Having selected a metric before auto selects "
                                               "here the matching unit of the metric."),
                                        elements=[_("Minimum"), _("Maximum")])),
                               ])),
            ("status_border",
             DropdownChoice(title=_("Status border"),
                            choices=[
                                (False, _("Do not show any service status border")),
                                ("not_ok", _("Draw a status border when service is not OK")),
                                ("always", _("Always draw the service status on the border")),
                            ],
                            default_value="not_ok")),
        ]

        if self._exclude_properties:
            elements = [x for x in elements if x[0] not in self._exclude_properties]

        return elements

    @classmethod
    @site_query
    def _get_data(cls, properties, context):
        cmc_cols = [
            "host_name", "service_check_command", "service_description", "service_perf_data",
            "service_state", "service_has_been_checked"
        ]
        metric_columns = []
        if properties["time_range"] != "current":
            params = properties["time_range"][1]

            from_time, until_time = map(int, Timerange().compute_range(params['window'])[0])
            data_range = "%s:%s:%s" % (from_time, until_time, 60)
            _metrics: List[_Tuple[str, Optional[str], float]] = [
                (name, None, scale)
                for name, scale in reverse_translate_metric_name(properties["metric"])
            ]
            metric_columns = list(rrd_columns(_metrics, params["rrd_consolidation"], data_range))

        return cmc_cols + metric_columns

    @classmethod
    def generate_response_data(cls, properties, context, settings):
        data, metrics = create_data_for_single_metric(cls, properties, context)
        return cls._create_single_metric_config(data, metrics, properties, context, settings)

    @classmethod
    def _create_single_metric_config(cls, data, metrics, properties, context, settings):
        plot_definitions = []

        def svc_map(row):
            css_classes, status_name = paint_service_state_short(row)
            draw_status = properties.get("status_border", "not_ok")
            if draw_status == "not_ok" and css_classes.endswith("state0"):
                draw_status = False

            return {"style": css_classes, "msg": _("Status: ") + status_name, "draw": draw_status}

        # Historic values are always added as plot_type area
        if properties["time_range"] != "current":
            time_range_params = properties["time_range"][1]
            for row_id, metric, row in metrics:
                chosen_color = time_range_params["color"]
                color = metric.get(
                    'color',
                    "#008EFF",
                ) if chosen_color == "default" else chosen_color
                plot_definition = {
                    "label": row['host_name'],
                    "id": row_id,
                    "plot_type": "area",
                    "use_tags": [row_id],
                    "color": color,
                    "fill": time_range_params["fill"],
                    "opacity": 0.1 if time_range_params["fill"] else 0
                }
                plot_definitions.append(plot_definition)

        # The current/last value definition also gets the metric levels
        for row_id, metric, row in metrics:
            plot_definition = {
                "label": row['host_name'],
                "id": "%s_single" % row_id,
                "plot_type": "single_value",
                "use_tags": [row_id],
                "svc_state": svc_map(row),
                "js_render": metric['unit'].get("js_render"),
                "metrics": {
                    "warn": metric["scalar"].get("warn"),
                    "crit": metric["scalar"].get("crit"),
                    "min": metric["scalar"].get("min"),
                    "max": metric["scalar"].get("max"),
                }
            }
            if "color" in metric:
                plot_definition["color"] = metric["color"]

            plot_definitions.append(plot_definition)

        response = {
            "plot_definitions": plot_definitions,
            "data": data,
        }
        title: List[_Tuple[str, Optional[str]]] = []
        title_format = settings.get("title_format", ["plain"])

        if settings.get("show_title", True) and metrics:
            if settings.get("title") and "plain" in title_format:
                title.append((settings.get("title"), ""))
            title.extend(
                title_info_elements(metrics[0][2], [f for f in title_format if f != "plain"]))

        response["title"] = " / ".join(txt for txt, _ in title)

        return response


@page_registry.register_page("single_metric_data")
class SingleMetricPage(AjaxPage):
    def page(self):
        return SingleMetricStyledDataGenerator().generate_response_from_request()


#   .--Gauge---------------------------------------------------------------.
#   |                     ____                                             |
#   |                    / ___| __ _ _   _  __ _  ___                      |
#   |                   | |  _ / _` | | | |/ _` |/ _ \                     |
#   |                   | |_| | (_| | |_| | (_| |  __/                     |
#   |                    \____|\__,_|\__,_|\__, |\___|                     |
#   |                                      |___/                           |
#   +----------------------------------------------------------------------+


@dashlet_registry.register
class GaugeDashlet(ABCFigureDashlet):
    """Dashlet that displays a scatterplot and average lines for a selected type of service"""
    @classmethod
    def type_name(cls):
        return "gauge"

    @classmethod
    def title(cls):
        return _("Gauge")

    @classmethod
    def description(cls):
        return _("Displays Gauge")

    @classmethod
    def data_generator(cls):
        return SingleMetricDataGenerator()

    @classmethod
    def single_infos(cls):
        return ["service", "host"]

    def show(self):
        self.js_dashlet("single_metric_data.py")


#   .--Bar Plot------------------------------------------------------------.
#   |                ____               ____  _       _                    |
#   |               | __ )  __ _ _ __  |  _ \| | ___ | |_                  |
#   |               |  _ \ / _` | '__| | |_) | |/ _ \| __|                 |
#   |               | |_) | (_| | |    |  __/| | (_) | |_                  |
#   |               |____/ \__,_|_|    |_|   |_|\___/ \__|                 |
#   |                                                                      |
#   +----------------------------------------------------------------------+


@dashlet_registry.register
class BarplotDashlet(ABCFigureDashlet):
    @classmethod
    def type_name(cls):
        return "barplot"

    @classmethod
    def title(cls):
        return _("Barplot")

    @classmethod
    def data_generator(cls):
        return SingleMetricDataGenerator()

    @classmethod
    def description(cls):
        return _("Barplot")

    @classmethod
    def single_infos(cls):
        return ["service"]

    def show(self):
        self.js_dashlet("single_metric_data.py")


#   .--Single Graph--------------------------------------------------------.
#   |      ____  _             _         ____                 _            |
#   |     / ___|(_)_ __   __ _| | ___   / ___|_ __ __ _ _ __ | |__         |
#   |     \___ \| | '_ \ / _` | |/ _ \ | |  _| '__/ _` | '_ \| '_ \        |
#   |      ___) | | | | | (_| | |  __/ | |_| | | | (_| | |_) | | | |       |
#   |     |____/|_|_| |_|\__, |_|\___|  \____|_|  \__,_| .__/|_| |_|       |
#   |                    |___/                         |_|                 |
#   +----------------------------------------------------------------------+


class SingleMetricStyledDataGenerator(SingleMetricDataGenerator):
    @staticmethod
    def _time_range_historic_dict_elements() -> DictionaryElements:
        yield from super(
            SingleMetricStyledDataGenerator,
            SingleMetricStyledDataGenerator,
        )._time_range_historic_dict_elements()
        yield from (
            (
                "fill",
                DropdownChoice(
                    choices=[
                        (False, _("Line")),
                        (True, _("Area")),
                    ],
                    default_value=True,
                    title=_("Style"),
                ),
            ),
            (
                "color",
                GraphColor(
                    title=_("Color"),
                    default_value="default",
                ),
            ),
        )


@dashlet_registry.register
class SingleMetricDashlet(ABCFigureDashlet):
    """Dashlet that displays a single metric"""
    def __init__(self, dashboard_name, dashboard, dashlet_id, dashlet):
        super(SingleMetricDashlet, self).__init__(dashboard_name, dashboard, dashlet_id, dashlet)
        self._perf_data = []
        self._check_command = ""

    @classmethod
    def type_name(cls):
        return "single_metric"

    @classmethod
    def title(cls):
        return _("Single metric")

    @classmethod
    def data_generator(cls):
        return SingleMetricStyledDataGenerator(exclude_properties=["display_range"])

    @classmethod
    def description(cls):
        return _("Displays a single metric of a specific host and service.")

    @classmethod
    def single_infos(cls):
        return ["service", "host"]

    def show(self):
        self.js_dashlet("single_metric_data.py")
