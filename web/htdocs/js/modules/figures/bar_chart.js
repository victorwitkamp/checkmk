import * as d3 from "d3";
import * as cmk_figures from "cmk_figures";

class BarChart extends cmk_figures.FigureBase {
    static ident() {
        return "bar_chart";
    }

    initialize(with_debugging=false) {
        this._margin = {top: 20,right: 20,bottom: 50,left: 40};

        // Parameters used for zoom
        this._max_zoom = 12;
        this._last_zoom = d3.zoomIdentity;

        // The complete figure
        this._figure_svg = this._div_selection.append("svg");


        // The g element, handles translation and contains the axis
        this._bar_chart_g = this._figure_svg.append("g")
            .attr("transform", "translate(" + this._margin.left + "," + this._margin.top + ")");

        // The svg which renders the bars
        this._bar_chart_svg = this._bar_chart_g
            .append("svg")
            .classed("bars", true);

        // Setup scales
        this._x_scale_time = d3.scaleTime();
        this._y_scale = d3.scaleLinear();

        // Setup axis
        this._x_axis = this._bar_chart_g.append("g");
        this._x_axis.append("svg");
        this._y_axis = this._bar_chart_g.append("g");
        this._y_axis.append("text")
            .classed("ylabel", true)
            .attr("fill", "#000")
            .attr("y", -15)
            .attr("dy", "0.71em")
            .attr("text-anchor", "end");

        this.resize();

        /*this.color_range = d3.scaleSequential()
            .interpolator(d3.interpolateInferno)
            .domain([1,100]);*/
        this.color_range = d3.scaleLinear().domain([0, 40, 100]).range(["#00ff00", "#ffff00", "#ff0000"]);

        if (with_debugging)
            this._add_scheduler_debugging();
        this._tooltip = new cmk_figures.FigureTooltip(this._div_selection);

        this._orig_size = {};
        this._orig_size.width = this._size.width;
        this._orig_size.height= this._size.height;
    }

    _add_zoom() {
        const extent = [[this._margin.left, this._margin.top], [this._inner_svg_width - this._margin.right, this._bar_height - this._margin.top]];
        this._figure_svg.call(d3.zoom()
            .scaleExtent([1, this._max_zoom])
            .translateExtent(extent)
            .extent(extent)
            .on("zoom", ()=>this._zoomed()));
    }

    _zoomed() {
        this._last_zoom = d3.event.transform;
        this._bar_chart_svg.selectAll(".bars rect").interrupt();
        this.update_data(this._data);
        this.update_gui(this._data);
    }

    random_size_change() {
        this._size.height = this._orig_size.height * Math.max(0.3, Math.random());
        this._size.width = this._orig_size.width * Math.max(0.3, Math.random());
        this.resize();
        this.update_data(this._data);
        this.update_gui(this._data);
    }

    register_on_resize() {
        // TODO:
    }

    resize() {
        this._figure_svg
            .attr("width", this._size.width)
            .attr("height", this._size.height);
        this._inner_svg_width = +this._figure_svg.attr("width") - this._margin.left - this._margin.right;
        this._bar_height = +this._figure_svg.attr("height") - this._margin.top - this._margin.bottom;

        // Resize y scale, the x scale depends also on zoom and is calibrated in update_data
        this._y_scale.rangeRound([this._bar_height, 0]);
        this._bar_chart_g.selectAll("rect").interrupt()
            .attr("height", 0)
            .attr("y", this._bar_height);

        this._figure_svg.call(()=>this._add_zoom());
    }

    show() {
        this.scheduler.force_update();
    }

    // Data format
    // data = {
    //   title: "My title",
    //   elements: [{
    //          "label": "Element A",
    //          "tooltip": "Tooltip for this element",
    //          "value": 100,
    //          "css": ["host_bar"],    // assign the following css style(s) to this bar
    //          "url": "target.py",     // url on click
    //      },
    //      {
    //          "label": "Element B",
    //          "value": 200,
    //      }
    //  ]
    // }

    _get_y_max(data) {
        return d3.max(data.elements, d=>d.value);
    }

    update_data(data) {
        this._data = data;
        let elements = data.elements;
        elements.forEach(element=>{ element.date = new Date(1000 * element.timestamp); });
        let last_element = elements[elements.length - 1];
        // Adjust scale to new values
        this._x_scale_time.range([0, this._inner_svg_width].map(d => this._last_zoom.applyX(d)));
        this._x_scale_time.domain([elements[0].date, new Date(1000 * (last_element.timestamp + last_element.timestep))]);

        this._y_scale.domain([0, this._get_y_max(data)]);

        this.color_range.domain([0, 40, this._get_y_max(data)]);

    }

    update_gui(data) {
        let elements = data.elements;
        this._update_title(data);

        // Adjust axis
        this._x_axis.attr("transform", "translate(0," + this._bar_height + ")");
        this._x_axis.select("svg")
            .call(d3.axisBottom(this._x_scale_time)
                .tickFormat(d=>{
                    if (d.getHours() === 0 && d.getMinutes() === 0)
                        return d3.timeFormat("%d %b")(d);
                    else
                        return d3.timeFormat("%H:%M")(d);
                })
                .ticks(6*this._last_zoom.k)
            );

        this._y_axis.call(d3.axisLeft(this._y_scale).ticks(4));
        this._y_axis.select("text.ylabel").text(data.ylabel || "");

        // Adjust bars
        let bars = this._bar_chart_svg.selectAll("rect").data(elements);
        bars.exit().remove();

        bars.enter().append("a")
            .attr("xlink:href", d=>d.url)
            .append("rect")
            // Add new bars
            .each((d, idx, nodes)=>{this._tooltip.add_support(nodes[idx]);})
            .classed("bar", true)
            .attr("y", this._bar_height)
            .merge(bars)
            // Update new and existing bars
            .attr("x", d=>this._x_scale_time(d.date))
            .attr("width", d=>{
                return this._x_scale_time(new Date(1000 * (d.timestamp + d.timestep))) -
                    this._x_scale_time(d.date);
            })
            .each(function(d) { // Update classes
                let rect = d3.select(this);
                this.classList.forEach(classname=>{
                    rect.classed(classname, false);
                });
                let classes = d.classes;
                rect.classed("bar", true);
                if  (classes == undefined)
                    return;
                classes.forEach(new_class=>{
                    rect.classed(new_class, true);
                });
            })
            .transition().duration(1000)
            //.attr("fill", "#0f0f0f")
            .attr("y", d=>this._y_scale(d.value))
            .attr("height", d=>{return this._bar_height - this._y_scale(d.value);});
    }

    _update_title(data) {
        let titles = [];
        if (data.title)
            titles = [data.title];
        this._bar_chart_g.selectAll(".title").data(titles)
            .join("text")
            .text(d=>d)
            .attr("y", -10)
            .attr("x", this._inner_svg_width/2)
            .attr("text-anchor", "middle")
            .classed("title", true);

    }
}

cmk_figures.figure_registry.register(BarChart);


class BarBarChart extends BarChart {
    static ident() {
        return "barbar_chart";
    }

    initialize() {
        BarChart.prototype.initialize.call(this);
        this._barbar_chart_svg = this._bar_chart_g
            .insert("svg", "svg.bars")
            .classed("barbars", true);
    }

    update_data(data) {
        this._data = data;
        this._enclosing_bars = data.grouped_elements;
        this._enclosing_bars.forEach(element=>{
            element.date = new Date(1000 * element.timestamp);
        });
        BarChart.prototype.update_data.call(this, data);
    }

    _get_y_max() {
        return d3.max(this._enclosing_bars, d=>d.value);
    }

    update_gui(data) {
        this._render_enclosing_bars();

        BarChart.prototype.update_gui.call(this, data);
        // The already rendered bars have a higher resolution, hide them when zoomed out
        let opacity_scale = d3.scaleLinear().range([0.6, 0.9]).domain([1, this._max_zoom]);
        this._bar_chart_svg.selectAll("rect").attr("opacity", opacity_scale(this._last_zoom.k));
    }

    _render_enclosing_bars() {
        let enclosing_bars = this._enclosing_bars;
        let opacity_scale = d3.scaleLinear().range([0.6, 0.9]).domain([this._max_zoom, 1]);

        let bars = this._barbar_chart_svg.selectAll("rect.barbar").data(enclosing_bars);
        // Remove obsolete bars
        bars.exit().remove();

        bars.enter().append("a")
            .attr("xlink:href", d=>d.url)
            .append("rect")
            // Add new bars
            .each((d, idx, nodes)=>{this._tooltip.add_support(nodes[idx]);})
            .attr("y", this._bar_height)
            .merge(bars)
            // Update new and existing bars
            .attr("opacity", opacity_scale(this._last_zoom.k))
            .attr("x", d=>this._x_scale_time(d.date))
            .attr("width", d=>{
                return this._x_scale_time(new Date(1000 * (d.timestamp + d.timestep))) -
                    this._x_scale_time(d.date);
            })
            .each(function(d) { // Update classes
                let rect = d3.select(this);
                this.classList.forEach(classname=>{
                    rect.classed(classname, false);
                });
                rect.classed("barbar", true);
                let classes = d.classes;
                if  (classes == undefined)
                    return;
                classes.forEach(new_class=>{
                    rect.classed(new_class, true);
                });
            })
            .transition().duration(1000)
            .attr("fill", d=>this.color_range(d.value))
            .attr("y", d=>this._y_scale(d.value))
            .attr("height", d=>{return this._bar_height - this._y_scale(d.value);});
    }
}

cmk_figures.figure_registry.register(BarBarChart);




// Unused experimental, do not commit in master
class HorizonalBarChart extends cmk_figures.FigureBase {
    static ident() {
        return "horizontal_bar_chart";
    }

    initialize(with_debugging=false) {
        this.margin = {top:10, right:30, bottom:30, left:10};
        this.width = this._size.width - this.margin.left - this.margin.right;
        this.height = this._size.height - this.margin.top - this.margin.bottom;
        this.default_inner_svg_width = this.width;

        this.svg = this._div_selection.append("svg")
            .attr("width", this._size.width)
            .attr("height", this._size.height);

        // Setup scales
        this._x_scale = d3.scaleLinear().range([0, this.default_inner_svg_width]);
        this._y_scale = d3.scaleBand().rangeRound([0, this.height]).padding(0.2);

        this.g = this.svg.append("g")
            .attr("transform", "translate(" + this.margin.left + "," + this.margin.top + ")");

        // Setup axis
        this._x_axis = this.g.append("g");

        this.color_range = d3.scaleSequential()
            .interpolator(d3.interpolateInferno)
            .domain([1,100]);

        if (with_debugging)
            this._add_scheduler_debugging();
        this._tooltip = new cmk_figures.FigureTooltip(this._div_selection);

    }

    show() {
        this.scheduler.force_update();
        this.scheduler.enable();
    }

    // Data format
    // data = {
    //   title: "My title",
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
        this._update_title(data);

        // Reset domains
        this._y_scale.domain(elements.sort(function(a,b){
            return b.value - a.value;
        })
            .map(d=>d.name));

        let bar_max = d3.max(elements, d=>d.value);
        this._x_scale.domain([0, bar_max]);

        // Update axis
        this._x_axis.attr("transform", "translate(0," + this.height + ")")
            .transition()
            .call(d3.axisBottom(this._x_scale))

        // ENTER

        //Bind new data to chart rows
        //Create chart row and move to below the bottom of the chart
        let chart_row = this.g.selectAll("g.chart_row")
            .data(elements, d=>d.name);

        let newRow = chart_row.enter()
            .append("g")
            .attr("class", "chart_row")
            .attr("transform", "translate(0," + (this.height + this.margin.top + this.margin.bottom) + ")");

        //Add rectangles
        newRow.append("rect")
            .attr("class","bar")
            .attr("x", 0)
            .style("fill", d=>this.color_range(d.value))
            .each((d, idx, nodes)=>{this._tooltip.add_support(nodes[idx]);})
            .attr("height", this._y_scale.bandwidth())
            .attr("width", d=>this._x_scale(d.value));

//        //Add value labels
//        newRow.append("text")
//            .attr("class","label")
//            .attr("y", this._y_scale.bandwidth()/2)
//            .attr("x",0)
//            .attr("opacity",0)
//            .attr("dy",".35em")
//            .attr("dx","0.5em")
//            .text(d=>d.value);

        //Add Headlines
        newRow.append("text")
            .attr("class","category")
            .attr("text-overflow","ellipsis")
            .attr("y", this._y_scale.bandwidth()/2)
            .attr("x", 10)
            .attr("opacity",0)
            .attr("dy",".35em")
            .attr("dx","0.5em")
            .style("pointer-events", "none")
            .text(d=>d.name);


        chart_row = newRow.merge(chart_row);

        chart_row.each((d, idx, nodes)=>{
                if (d.classes)
                    cmk_figures.set_classes(nodes[idx], d.classes.concat("chart_row"));
            })

        // UPDATE

        //Update bar widths
        chart_row.select(".bar")
            .on("click", d=>{
                if (d.onclick)
                    d.onclick();
            })
            .transition()
            .duration(300)
            .attr("width", d=>{
                return this._x_scale(d.value);
            })
            .attr("height", this._y_scale.bandwidth())
            .attr("opacity",1);

//        //Update data labels
//        chart_row.select(".label").transition()
//            .duration(300)
//            .attr("opacity",1)
//            .attr("y", this._y_scale.bandwidth()/2)
//            .text(d=>d.name);

        //Fade in categories
        chart_row.select(".category").transition()
            .duration(300)
            .attr("y", this._y_scale.bandwidth()/2)
            .attr("opacity",1);

        // EXIT

        //Fade out and remove exit elements
        chart_row.exit().transition()
            .style("opacity","0")
            .attr("transform", "translate(0," + (this.height + this.margin.top + this.margin.bottom) + ")")
            .remove();


        ////////////////
        //REORDER ROWS//
        ////////////////

        var delay = function(d, i) { return 200 + i * 30; };

        chart_row.transition()
            .delay(delay)
            .attr("transform", (d)=>{return "translate(0, " + this._y_scale(d.name) + ")";});
    }


    _update_title(data) {
        let titles = [];
        if (data.title)
            titles = [data.title];
        this.g.selectAll(".title").data(titles)
            .join("text")
            .text(d=>d)
            .attr("y", -10)
            .attr("x", this._inner_svg_width/2)
            .attr("text-anchor", "middle")
            .classed("title", true);

    }
}

cmk_figures.figure_registry.register(HorizonalBarChart);
