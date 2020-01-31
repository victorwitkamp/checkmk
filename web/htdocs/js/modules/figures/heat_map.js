import * as d3 from "d3";
import * as cmk_figures from "cmk_figures";

class HeatMap extends cmk_figures.FigureBase {
    static ident() {
        return "heat_map";
    }

    initialize() {
        let margin = {
            top: 20,
            left: 20,
            right: 20,
            bottom: 20,
        };

        this._scope.svg = this._div_selection.append("svg")
            .attr("width", this._size.width)
            .attr("height", this._size.height);

        this._scope.width = this._size.width - margin.left - margin.right;
        this._scope.height = this._size.height - margin.top - margin.bottom;

        this._scope.g = this._scope.svg.append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        this._scope.x = d3.scaleBand()
            .range([0, this._scope.width])
            .padding(0.05);

        this._scope.y = d3.scaleBand()
            .range([this._scope.height, 0])
            .padding(0.05);

        this._scope.axis_left = this._scope.g.append("g")
            .style("font-size", 15);

        this._scope.axis_bottom = this._scope.g.append("g")
            .style("font-size", 15)
            .attr("transform", "translate(0," + this._scope.height + ")");

        this._scope.svg_content = this._scope.g.append("svg");

        this._scope.color_range = d3.scaleSequential()
            .interpolator(d3.interpolateInferno)
            .domain([1,100]);

        this._tooltip = new cmk_figures.FigureTooltip(this._div_selection);

        this._add_scheduler_debugging();
    }

    show() {
        this.scheduler.force_update();
        this.scheduler.enable();
    }

    //
    // Data format
    // [{"label": "Element A",
    //   "value": 100,
    //   "color": "blue",        // optional
    //   "css": ["host_bar"],    // assigns the following css style(s) to this bar
    //   },
    // {"label": "Element B",
    //   "value": 200,
    //   "color": "green"}]

    _get_x_axis_fields(data) {
        return data["x_axis"];
    }

    _get_y_axis_fields(data) {
        return data["y_axis"];
    }

    _arrange_fields(data) {
        return data;
    }

    update_gui(data) {
        data = this._arrange_fields(data);
        let x_fields = this._get_x_axis_fields(data);
        let y_fields = this._get_y_axis_fields(data);

        // adjust scale to new values
        this._scope.x.domain(x_fields);
        this._scope.y.domain(y_fields);

        // adjust axis
        this._scope.axis_bottom.attr("transform", "translate(0," + (this._scope.height) + ")")
            .call(d3.axisBottom(this._scope.x))
            .selectAll("text")
            .attr("y", 0)
            .attr("x", 9)
            .attr("transform", "rotate(90)");
        this._scope.axis_left.call(d3.axisLeft(this._scope.y));

        let transition_duration = 1800;

        let elements = data.elements;
        let blocks = this._scope.svg_content.selectAll("rect")
            .data(elements, d=>d.name);
        blocks.exit()
            .transition().duration(transition_duration)
            .attr("x", d=>{return (this._scope.x(d.x) + this._scope.x.bandwidth() / 2) || 0;})
            .attr("y", d=>{return (this._scope.y(d.y) + this._scope.y.bandwidth() / 2) || 0;})
            .attr("height", "0")
            .attr("width", "0")
            .remove();

        blocks.enter()
            .append("rect")
            .attr("rx", 4)
            .attr("ry", 4)
            .style("fill", d=>this._scope.color_range(d.value))
            .style("stroke-width", 4)
            .style("stroke", "none")
            .style("opacity", 0.8)
            .attr("x", d=>{
                return this._scope.x(d.x) + this._scope.x.bandwidth() / 2;
            })
            .attr("y", d=>{
                return this._scope.y(d.y) + this._scope.y.bandwidth() / 2;
            })
            .attr("height", "0")
            .attr("width", "0")
            .each((d, idx, nodes)=>{this._tooltip.add_support(nodes[idx]);})
            .transition().duration(transition_duration)
            .attr("x", d=>{return this._scope.x(d.x);})
            .attr("y", d=>{return this._scope.y(d.y);})
            .attr("width", 20)
            .attr("height", 20)
            .attr("width", this._scope.x.bandwidth())
            .attr("height", this._scope.y.bandwidth());

        blocks
            .style("fill", d=>this._scope.color_range(d.value))
            .transition().duration(transition_duration)
            .attr("x", d=>{return this._scope.x(d.x);})
            .attr("y", d=>{return this._scope.y(d.y);})
            .attr("width", this._scope.x.bandwidth())
            .attr("height", this._scope.y.bandwidth());
    }
}

cmk_figures.figure_registry.register(HeatMap);

class HeatBucket extends HeatMap {
    static ident() {
        return "heat_bucket";
    }

    _arrange_fields(data) {
        let max_columns = Math.sqrt(data.elements.length) + 1;
        let rows = [];
        let current_row = [];
        data.elements.forEach(element=>{
            if (current_row.length > max_columns) {
                rows.push(current_row);
                current_row = [];
            }
            element["x"] = "X" + current_row.length;
            element["y"] = "Y" + rows.length;
            current_row.push(element);
        });
        if (current_row.length > 0)
            rows.push(current_row);

        data = {"elements": data.elements,
            "x_axis": Array.from({length:max_columns+1},(v,k)=>"X" + (k)),
            "y_axis": Array.from({length:rows.length},(v,k)=>"Y" + k),
        };
        return data;
    }
}

cmk_figures.figure_registry.register(HeatBucket);
