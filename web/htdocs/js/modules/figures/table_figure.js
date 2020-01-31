/* eslint-disable indent */

import * as d3 from "d3";
import * as dc from "dc";
import * as cmk_figures from "cmk_figures";

class TableFigure extends cmk_figures.FigureBase {
    static ident() {
        return "table";
    }

    initialize(debug) {
        this._table = this._div_selection.append("table");

        if (debug)
            this._add_scheduler_debugging();
    }

    // Data format
    // data = {
    //   title: "My title",              // Optional
    //   headers: []
    //   rows: [
    //      [ {                 // Dict, representing a row
    //          "cells": [ {    // Dict, representing a cell
    //            content: "Text to display",
    //            classes: ["styles", "to", "apply"],
    //            colspan: 3,
    //          } ]
    //      ], ...
    //   ]
    // }

    update_data(data) { // eslint-disable-line no-unused-vars
    }

    update_gui(data) {
        cmk_figures.set_classes(this._table.node(), data.classes);

        let rows = this._table.selectAll("tr").data(data.rows);

        rows.exit()
            .transition()
            .duration(1000)
            .style("opacity", 0)
            .remove();

        rows = rows.enter().append("tr").merge(rows);
        rows.each(function(d) {
                cmk_figures.set_classes(this, d.classes);
            });

        let tds = rows.selectAll("td").data(d=>d.cells);
        let new_tds = tds.enter().append("td")
            .each((d, idx, nodes) => {
                let td = d3.select(nodes[idx]);
                if (d.colspan)
                    td.attr("colspan", d.colspan);
                if (d.rowspan)
                    td.attr("rowspan", d.rowspan);

            });

        new_tds.style("opacity", 0).transition().style("opacity", 1);

        new_tds.merge(tds)
            .each(function(d) { // Update classes
                cmk_figures.set_classes(this, d.classes);
                let td = d3.select(this);
                if (d.id)
                    td.attr("id", d.id);
                if (d.content != null)
                    td.text(d.content);
                if (d.html != null)
                    td.html(d.html);
            });

        _update_dc_graphs_in_selection(this._div_selection);
    }
}

cmk_figures.figure_registry.register(TableFigure);

// Debugging stuff

function _update_dc_graphs_in_selection(selection, graph_group) {
    selection.selectAll(".dc_graph_element").each((d, idx, nodes) => {
        // TODO: implement better intialization solution, works for now
        let node = d3.select(nodes[idx]);
        let svg = node.select("svg");
        if (svg.empty()) {
            let new_crossfilter = new crossfilter(d.dc_graph_config.elements);
            let label_dimension = new_crossfilter.dimension(d=>d.label);
            let label_group = label_dimension.group().reduceSum(d=>d.value);
            let pie_chart = dc.pieChart("#" + d.dc_graph_config.id, graph_group);
            pie_chart
                .width(400)
                .height(200)
                .dimension(label_dimension)
                .radius(90)
                .innerRadius(30)
                .drawPaths(true)
                .minAngleForLabel(0)
                .externalLabels(25)
                .externalRadiusPadding(30)
                .title(d=>d.value)
                .group(label_group)
                .on("postRedraw", (chart)=>{_pie_chart_custom_renderlet(chart);});

            pie_chart.filter = function() {};
            pie_chart.render();
            nodes[idx].__crossfilter__ = new_crossfilter;
        } else {
            // Update
            nodes[idx].__crossfilter__.remove(()=>true);
            nodes[idx].__crossfilter__.add(d.dc_graph_config.elements);
        }
    });
}

function _pie_chart_custom_renderlet(chart) {
    let labels_data = [];
    chart.selectAll("text.pie-label").each((d, idx, nodes)=>{
        labels_data.push(d3.select(nodes[idx]));
    });

    let labels_key = chart.select("g.pie-label-group").selectAll("text.pie-label-key").data(labels_data, d=>d.datum().data.key);
    labels_key.exit().remove();

    labels_key = labels_key.enter().append("text")
        .classed("pie-label-key", true);

    labels_key.exit().remove();
    labels_key.attr("transform", d=>{
            let coords = _get_translation(d.attr("transform"));
            return "translate(" + coords[0] + "," + (coords[1] + 10) + ")";
        }).text(d=>{
            let data = d.datum();
            return Math.round((data.endAngle - data.startAngle) / Math.PI * 50) + "%";}
        );
}

function _get_translation(transform) {
  // Create a dummy g for calculation purposes only. This will never
  // be appended to the DOM and will be discarded once this function
  // returns.
  var g = document.createElementNS("http://www.w3.org/2000/svg", "g");

  // Set the transform attribute to the provided string value.
  g.setAttributeNS(null, "transform", transform);

  // consolidate the SVGTransformList containing all transformations
  // to a single SVGTransform of type SVG_TRANSFORM_MATRIX and get
  // its SVGMatrix.
  var matrix = g.transform.baseVal.consolidate().matrix;

  // As per definition values e and f are the ones for the translation.
  return [matrix.e, matrix.f];
}
