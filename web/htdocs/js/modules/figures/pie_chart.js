import * as d3 from "d3";
import * as cmk_figures from "cmk_figures";

function add_styles() {
    let styles = `
path.slice{
    stroke-width:2px;
}

polyline{
    opacity: .3;
    stroke: black;
    stroke-width: 2px;
    fill: none;
}
`;
    var styleSheet = document.createElement("style");
    styleSheet.type = "text/css";
    styleSheet.innerText = styles;
    document.head.appendChild(styleSheet);
}


class PieChart extends cmk_figures.FigureBase {
    static ident() {
        return "pie_chart";
    }

    initialize() {
        add_styles();
        this._scope.svg = this._div_selection.append("svg")
            .attr("width", this._size.width)
            .attr("height", this._size.height)
            .append("g");

        this._scope.svg.append("g").classed("slices", true);
        this._scope.svg.append("g").classed("labels", true);
        this._scope.svg.append("g").classed("lines", true);

        this._scope.radius = Math.min(this._size.width, this._size.height) / 2;
        this._scope.arc = d3.arc()
            .outerRadius(this._scope.radius * 0.8)
            .innerRadius(this._scope.radius * 0.4);

        this._scope.outerArc = d3.arc()
            .innerRadius(this._scope.radius * 0.9)
            .outerRadius(this._scope.radius * 0.9);

        this._scope.svg.attr("transform", "translate(" + (this._size.width/2) + "," + (this._size.height/2) + ")");

        this._scope.color = d3.scaleOrdinal()
            .domain(["Lorem ipsum", "dolor sit", "amet", "consectetur", "adipisicing", "elit", "sed", "do", "eiusmod", "tempor", "incididunt"])
            .range(["#98abc5", "#8a89a6", "#7b6888", "#6b486b", "#a05d56", "#d0743c", "#ff8c00"]);

        this._add_scheduler_debugging();

        this._tooltip = new cmk_figures.FigureTooltip(this._div_selection);
    }

    get_data_key(item) {
        return item.data.label;
    }

    mid_angle(arc) {
        return arc.startAngle + (arc.endAngle - arc.startAngle)/2;
    }

    // Data format
    // data = {
    //   title: "My title",
    //   display_options: {"show_percent": true},
    //   elements: [{
    //          "label": "Element A",
    //          "tooltip": "Tooltip for this element",
    //          "value": 100,
    //          "css": ["host_bar"],    // assign the following css style(s) to this bar
    //          "url": "target.py,      // url on click
    //      },
    //      {
    //          "label": "Element B",
    //          "value": 200,
    //      }
    //  ]
    // }

    update_gui(data) {
        let elements = data.elements;
        this._pie_data = d3.pie().sort(null).value(d=>d.value)(elements);
        this._update_tooltip(this._pie_data);

        this._update_arcs();
        this._update_texts(data);
        this._update_lines();
    }

    _update_tooltip(pie_data) {
        // The pie data tooltip is nested in a data
        //   {
        //      data: Object { value: 37, tooltip: "Tooltip of 3", label: "Name 3" }
        //      endAngle: 5.1481582839471445
        //      index: 3
        //      padAngle: 0
        //      startAngle: 3.6483011461042754
        //      value: 37
        //   }
        pie_data.forEach(pie=>{
            pie.tooltip = pie.data.tooltip;
        });
    }

    _update_arcs() {
        let scope = this._scope;

        var slice = this._scope.svg.select(".slices").selectAll("path.slice")
            .data(this._pie_data, this.get_data_key);

        slice.exit().remove();

        slice = slice.enter()
            .insert("path")
            .each((d, idx, nodes)=>{this._tooltip.add_support(nodes[idx]);})
            .style("fill", d=>this._scope.color(d.data.label))
            .attr("class", "slice")
            .merge(slice);


        slice.on("click", d=>{
            if (d.data.onclick)
                d.data.onclick();
            })
            .each((d, idx, nodes)=>{
                if (d.data.classes)
                    cmk_figures.set_classes(nodes[idx], d.data.classes.concat("slice"));
            })
            .transition()
            .duration(1000)
            .attrTween("d", function(d) {
                this._current = this._current || d;
                var interpolate = d3.interpolate(this._current, d);
                this._current = interpolate(0);
                return function(t) {
                    return scope.arc(interpolate(t));
                };
            });

    }

    _update_texts(data) {
        let total_value = 0;
        data.elements.forEach(element=>{total_value+=element.value;});
        let scope = this._scope;
        let mid_angle = this.mid_angle;

        var text = this._scope.svg.select(".labels").selectAll("text").data(this._pie_data, this.get_data_key);

        text.exit()
            .remove();

        let percentage_formatter = d3.format(".2f");
        text = text.enter()
            .append("text")
            .attr("dy", ".35em")
            .text(d=>{
                let label = d.data.label;
                if (data.display_options && data.display_options.show_percentage)
                    label = label + " ("+percentage_formatter(100.0 * d.data.value/total_value) + " %)"
                return label;}
            ).merge(text);

        text.transition().duration(1000)
            .attrTween("transform", function(d) {
                this._current = this._current || d;
                var interpolate = d3.interpolate(this._current, d);
                this._current = interpolate(0);
                return function(t) {
                    var d2 = interpolate(t);
                    var pos = scope.outerArc.centroid(d2);
                    pos[0] = scope.radius * (mid_angle(d2) < Math.PI ? 1 : -1);
                    return "translate("+ pos +")";
                };
            })
            .styleTween("text-anchor", function(d){
                this._current = this._current || d;
                var interpolate = d3.interpolate(this._current, d);
                this._current = interpolate(0);
                return function(t) {
                    var d2 = interpolate(t);
                    return mid_angle(d2) < Math.PI ? "start":"end";
                };
            });
    }

    _update_lines() {
        let scope = this._scope;
        let mid_angle = this.mid_angle;

        var polyline = this._scope.svg.select(".lines").selectAll("polyline")
            .data(this._pie_data, this.get_data_key);

        polyline.exit().remove();

        polyline = polyline.enter()
            .append("polyline")
            .merge(polyline);

        polyline.transition().duration(1000)
            .attrTween("points", function(d){
                this._current = this._current || d;
                var interpolate = d3.interpolate(this._current, d);
                this._current = interpolate(0);
                return function(t) {
                    var d2 = interpolate(t);
                    var pos = scope.outerArc.centroid(d2);
                    pos[0] = scope.radius * 0.95 * (mid_angle(d2) < Math.PI ? 1 : -1);
                    return [scope.arc.centroid(d2),scope. outerArc.centroid(d2), pos];
                };
            });
    }
}

cmk_figures.figure_registry.register(PieChart);
