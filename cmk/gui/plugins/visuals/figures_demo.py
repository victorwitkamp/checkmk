import os
import random
from cmk.gui.pages import page_registry, Page, AjaxPage
from cmk.gui.globals import html


def create_response(data, context=None):
    response = {"data": data}
    if context:
        response["context"] = context
    return response


@page_registry.register_page("full_demo")
class FullDemo(Page):
    def page(self):
        html.header("Full demo")

        BarChartDemo.render()
        PieChartDemo.render()
        HeatMapDemo.render()
        HeatBucketDemo.render()
        SankeyDiagramDemo.render()


################################ Bar chart
@page_registry.register_page("bar_chart")
class BarChartDemo(Page):
    def page(self):
        html.header("Bar chart")
        BarChartDemo.render()

    @staticmethod
    def render():
        html.javascript(
            """let bar_chart_class = cmk.figures.figure_registry.get_figure("bar_chart")""")

        figures = 1
        height = 150
        for index in range(figures):
            instance_div = "main_div_%d" % index
            html.div("", id_=instance_div)
            html.javascript("""
                let bar_chart = new bar_chart_class("%s",600, %d)
                bar_chart.set_post_url_and_body("bar_chart_data.py", "")
                bar_chart.initialize();
                bar_chart.scheduler.force_update();
            """ % (instance_div, height))


@page_registry.register_page("bar_chart_data")
class BarDataPage(AjaxPage):
    def page(self):
        response = {}
        response["elements"] = []
        response["title"] = "Test title"
        response["ylabel"] = "Test Y"
        if random.random() > 1:
            raise Exception("BOOM - Fetch data error")
        for i in range(25):
            response["elements"].append({
                "label": "Day %s" % i,
                "value": random.randint(0, 100),
                "tooltip": "SOSO %.3f" % random.random(),
                "classes": ["csstest", "csstestneu"]
            })
        return create_response(response)


################################ Pie chart
@page_registry.register_page("pie_chart")
class PieChartDemo(Page):
    def page(self):
        html.header("Pie chart")
        PieChartDemo.render()

    @staticmethod
    def render():
        html.javascript(
            """let pie_chart_class = cmk.figures.figure_registry.get_figure("pie_chart")""")

        figures = 1
        height = 200
        for index in range(figures):
            instance_div = "main_div_%d" % index
            html.span("", id_=instance_div)
            html.javascript("""
                let pie_chart = new pie_chart_class("%s", 400, %d);
                pie_chart.set_post_url_and_body("random_data.py", "")
                pie_chart.initialize();
                pie_chart.scheduler.force_update();
            """ % (instance_div, height))


################################ Heat map
@page_registry.register_page("heat_map")
class HeatMapDemo(Page):
    def page(self):
        html.header("Heat map")
        HeatMapDemo.render()

    @staticmethod
    def render():
        html.javascript(
            """let heat_map_class = cmk.figures.figure_registry.get_figure("heat_map")""")

        figures = 1
        height = 400
        for index in range(figures):
            instance_div = "main_div_%d" % index
            html.span("", id_=instance_div)
            html.javascript("""
                let heat_map = new heat_map_class("%s", 400, %d)
                heat_map.set_post_url_and_body("heat_map_data.py", "")
                heat_map.initialize();
                heat_map.scheduler.force_update();
            """ % (instance_div, height))


@page_registry.register_page("heat_map_data")
class HeatMapDataPage(AjaxPage):
    def page(self):
        # data format
        # {
        #    "elements": [{"x": "a", "y": "T2", "label": "Element A", "value": 23}, ..]
        #    "x_axis": ["a","b", "c", "d"],
        #    "y_axis": ["T1","T2", "T3", "T4"],
        # }

        response = {"elements": []}
        response["x_axis"] = ["X%d" % x for x in range(0, 3)]
        response["y_axis"] = ["F%d" % x for x in range(0, 3)]
        response["x_axis"] = ["X%d" % x for x in range(0, 16)]
        response["y_axis"] = ["F%d" % x for x in range(0, 16)]
        elements = ["Ele %d" % x for x in range(0, 1000)]
        random_factor = max(0.3, random.random())
        for idx_i, i in enumerate(response["x_axis"]):
            for idx_j, j in enumerate(response["y_axis"]):
                if random.random() > random_factor:
                    continue
                response["elements"].append({
                    "label": "Element %d" % (idx_i * 10 + idx_j),
                    "tooltip": "Tooltip of Element %d" % (idx_i * 10 + idx_j),
                    "name": elements.pop(),
                    "value": random.randint(0, 100),
                    "x": i,
                    "y": j
                })
        return create_response(response)


################################ Heat bucket
@page_registry.register_page("heat_bucket")
class HeatBucketDemo(Page):
    def page(self):
        html.header("Heat bucket")
        HeatBucketDemo.render()

    @staticmethod
    def render():
        html.javascript(
            """let heat_bucket_class = cmk.figures.figure_registry.get_figure("heat_bucket")""")

        figures = 1
        height = 400
        for index in range(figures):
            instance_div = "main_div_%d" % index
            html.span("", id_=instance_div)
            html.javascript("""
                let heat_bucket = new heat_bucket_class("%s", 400, %d);
                heat_bucket.set_post_url_and_body("heat_map_data.py", "")
                heat_bucket.initialize();
                heat_bucket.scheduler.force_update();
            """ % (instance_div, height))


################################ Sankey
@page_registry.register_page("sankey_diagram")
class SankeyDiagramDemo(Page):
    def page(self):
        html.header("Sankey diagram")
        SankeyDiagramDemo.render()

    @staticmethod
    def render():
        html.javascript(
            """let sankey_diagram_class = cmk.figures.figure_registry.get_figure("sankey_diagram")"""
        )

        figures = 1
        height = 400
        for index in range(figures):
            instance_div = "main_div_%d" % index
            html.span("", id_=instance_div)
            html.javascript("""
                let sankey_diagram = new sankey_diagram_class("%s", 700, %d)
                sankey_diagram.initialize();
                sankey_diagram.scheduler.force_update();
            """ % (instance_div, height))


################################ Sankey


@page_registry.register_page("random_data")
class RandomDataPage(AjaxPage):
    def page(self):
        response = {"elements": []}
        #        if random.random() > 0.8:
        #            raise Exception("BOOM - Fetch data error")
        for i in range(5):
            response["elements"].append({
                "label": "Name %s" % i,
                "tooltip": "Tooltip of %d" % i,
                "value": random.randint(0, 40)
            })
        return create_response(response)
