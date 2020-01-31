import * as d3 from "d3";
import * as dc from "dc";
import * as cmk_figures from "cmk_figures";

// Basic dc table with pagination
class DCTableFigure extends cmk_figures.FigureBase {
    constructor(div_selector, group) {
        super(div_selector);
        this._graph_group = group;
        this._offset = 0;
        this._pages = 20;
        this._dimension = null;
        this._columns = null;
    }

    static ident() {
        return "dc_table";
    }

    initialize(debug) {
        if (debug)
            this._add_scheduler_debugging();
        this._setup_paging();
        this._setup_chart();
    }

    update_gui() {
        this._chart.redraw();
    }

    _setup_paging() {
        let paging = this._div_selection.append("div").attr("id", "dc_table_paging").attr("id", "paging");
        paging.append("label").text("Showing").style("margin-right", "5px");
        paging.append("span").attr("id", "begin");
        paging.append("label").text("-");
        paging.append("span").attr("id", "end").style("margin-right", "5px");
        paging.append("label").text("of").style("margin-right", "5px");
        paging.append("span").attr("id", "size");
        paging.append("span").attr("id", "totalsize").style("margin-right", "15px");
        paging.append("input").attr("type", "button").property("value", "Last").on("click", ()=>this.last());
        paging.append("input").attr("type", "button").property("value", "Next").on("click", ()=>this.next());
    }


    _setup_chart() {
        let table_selection = this._div_selection.append("div").attr("id", "dc_table_figure");
        this._chart = new dc.dataTable(table_selection, this._graph_group);
        this._chart
            .dimension(this._dimension)
            .size(Infinity)
            .showSections(false)
            .columns(this._columns)
            .sortBy(this._sort_by)
            .order(d3.descending)
            .on("preRender", ()=>this._update_offset())
            .on("preRedraw", ()=>this._update_offset())
            .on("pretransition", ()=>this._display());
        this._chart.render();
    }

    get_dc_chart() {
        return this._chart;
    }

    set_columns(columns) {
        this._columns = columns;
    }

    set_sort_by(sort_by_func) {
        this._sort_by = sort_by_func;
    }

    set_crossfilter(crossfilter) {
        this._crossfilter = crossfilter;
    }

    set_dimension(dimension) {
        this._dimension = dimension;
    }

    _update_offset() {
        let totFilteredRecs = this._crossfilter.groupAll().value();
        this._offset = this._offset >= totFilteredRecs ? Math.floor((totFilteredRecs - 1) / this._pages) * this._pages : this._offset;
        this._offset = this._offset < 0 ? 0 : this._offset;

        this._chart.beginSlice(this._offset);
        this._chart.endSlice(this._offset+this._pages);
    }

    _display() {
        let totFilteredRecs = this._crossfilter.groupAll().value();
        var end = this._offset + this._pages > totFilteredRecs ? totFilteredRecs : this._offset + this._pages;
        d3.select("#begin")
            .text(end === 0? this._offset : this._offset + 1);
        d3.select("#end")
            .text(end);
        d3.select("#last")
            .attr("disabled", this._offset-this._pages<0 ? "true" : null);
        d3.select("#next")
            .attr("disabled", this._offset+this._pages>=totFilteredRecs ? "true" : null);
        d3.select("#size").text(totFilteredRecs);
        if (totFilteredRecs != this._crossfilter.size()){
            d3.select("#totalsize").text("(filtered Total: " + this._crossfilter.size() + " )");
        } else {
            d3.select("#totalsize").text("");
        }
    }

    next() {
        this._offset += this._pages;
        this._update_offset();
        this._chart.redraw();
    }

    last() {
        this._offset -= this._pages;
        this._update_offset();
        this._chart.redraw();
    }
}

cmk_figures.figure_registry.register(DCTableFigure);
