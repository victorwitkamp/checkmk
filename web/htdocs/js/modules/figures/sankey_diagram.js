import * as d3 from "d3";
import * as cmk_figures from "cmk_figures";

function guid() {
    function _p8(s) {
        var p = (Math.random().toString(16)+"000000000").substr(2,8);
        return s ? "-" + p.substr(0,4) + "-" + p.substr(4,4) : p ;
    }
    return _p8() + _p8(true) + _p8(true) + _p8();
}


function get_data() {
    const links = d3.csvParse(content, d3.autoType);
    links.forEach(link=>{link.value += Math.random() * 250;});
    const nodes = Array.from(new Set(links.flatMap(l => [l.source, l.target])), name => ({name}));
    return {nodes, links};
}

class SankeyDiagram extends cmk_figures.FigureBase {
    static ident() {
        return "sankey_diagram";
    }

    initialize() {
        this._scope.svg = this._div_selection.append("svg")
            .attr("width", this._size.width)
            .attr("height", this._size.height);

        this._scope.g = this._scope.svg.append("g")
            .attr("stroke", "#000");

        this._scope.link = this._scope.svg.append("g")
            .attr("fill", "none")
            .attr("stroke-opacity", 0.5);

        this._scope.g_texts = this._scope.svg.append("g")
            .style("font", "10px sans-serif");


        this._scope.color = d3.scaleOrdinal(d3.schemeCategory10);
        this._transition_duration = 1800;

        this._scope.align = "Justify";
        this._scope.edgeColor = "path";

        this._add_scheduler_debugging();
        this._add_own_debugging();
    }

    show() {
        this.scheduler.force_update();
        this.scheduler.enable();
    }

    _add_own_debugging() {
        this._add_dropdown_choice("color", this._div_selection, ["input", "output", "path", "none"], "path", ()=>this._change_edge());
        this._add_dropdown_choice("align", this._div_selection, ["Left", "Right", "Center", "Justify"], "path", ()=>this._change_align());
    }

    _change_edge() {
        this._scope.edgeColor = d3.event.target.value;
        this._scope.link.selectAll("*").remove();
        this.scheduler.force_update();
    }

    _change_align() {
        this._scope.align = d3.event.target.value;
        this.scheduler.force_update();
    }


    _add_dropdown_choice(name, into_selection, choices, default_choice, callback_function) {
        var select = into_selection.selectAll("select."+name).data([name]);
        select = select.enter().append("select").merge(select)
            .classed(name, true)
            .style("width", "100%");

        var options = select.on("change", callback_function)
            .selectAll("option")
            .data(choices);
        options.exit().remove();
        options = options.enter().append("option").merge(options);

        options.property("value", d=>d)
            .property("selected", d=>d==default_choice)
            .text(d=>d);
    }

    _get_sankey_func(width, height) {
        const sankey_graph = sankey.sankey()
            .nodeId(d=>d.name)
            .nodeAlign(sankey["sankey" + this._scope.align])
            .nodeWidth(15)
            .nodePadding(10)
            .extent([[1, 5], [width - 1, height - 5]]);
//            .layout(0);
        return ({nodes, links}) => sankey_graph({
            nodes: nodes.map(d => Object.assign({}, d)),
            links: links.map(d => Object.assign({}, d))
        });
    }

    color(name) {
        return this._scope.color(name.replace(/ .*/, ""));
    }

    _render_rects(nodes) {
        let rects = this._scope.g.selectAll("rect");

        rects = rects.data(nodes).enter().append("rect")
            .attr("x", d => d.x0)
            .attr("y", d => d.y0 + (d.y1 - d.y0)/2)
            .attr("height", 0)
            .attr("width", d => d.x1 - d.x0).merge(rects);

        rects.transition().duration(this._transition_duration)
            .attr("x", d => d.x0)
            .attr("y", d => d.y0)
            .attr("height", d => d.y1 - d.y0)
            .attr("width", d => d.x1 - d.x0)
            .attr("fill", d => this.color(d.name))
//            .append("title")
//            .text(d => d.name);

    }

    _fetch_data() {
        let data = get_data();
        this.update_gui(data);
    }

    update_gui(data) {
        let sankey_func = this._get_sankey_func(this._size.width, this._size.height);
        const {nodes, links} = sankey_func(data);

        this._render_rects(nodes);
        this._render_paths(links);
        this._render_texts(nodes);
    }

    _render_paths(links) {
        let link_selection = this._scope.link.selectAll("path")
            .data(links);

        link_selection.exit().remove();

        let new_links = link_selection.enter().append("g")
            .style("mix-blend-mode", "multiply");

        console.log(this._scope.edgeColor);
        if (this._scope.edgeColor === "path") {
            const gradient = new_links.append("linearGradient")
                .attr("id", d => (d.uid = guid()))
                .attr("gradientUnits", "userSpaceOnUse")
                .attr("x1", d => d.source.x1)
                .attr("x2", d => d.target.x0);

            gradient.append("stop")
                .attr("offset", "0%")
                .attr("stop-color", d => this.color(d.source.name));

            gradient.append("stop")
                .attr("offset", "100%")
                .attr("stop-color", d => this.color(d.target.name));
        }

        new_links.append("title")
            .text(d => `${d.source.name} → ${d.target.name}\n${d.value}`);

        new_links.append("path")
            .attr("stroke", d => {
                if (this._scope.edgeColor === "none")
                    return "#aaa";
                if (this._scope.edgeColor === "path")
                    return "url('#" + d.uid + "')";
                if (this._scope.edgeColor === "input")
                    return this.color(d.source.name);
                return this.color(d.target.name);
            });

        link_selection = this._scope.link.selectAll("g")
            .select("path")
            .data(links)
            .transition().duration(this._transition_duration)
            .attr("d", sankey.sankeyLinkHorizontal())
            .attr("stroke-width", d => Math.max(1, d.width));
    }

    _render_texts(nodes) {
        let texts = this._scope.g_texts
            .selectAll("text")
            .data(nodes);

        texts = texts.enter().append("text")
            .attr("x", d => d.x0 < this._size.width / 2 ? d.x1 + 6 : d.x0 - 6)
            .attr("y", d => (d.y1 + d.y0) / 2)
            .merge(texts);

        texts.transition().duration(this._transition_duration)
            .attr("x", d => d.x0 < this._size.width / 2 ? d.x1 + 6 : d.x0 - 6)
            .attr("y", d => (d.y1 + d.y0) / 2)
            .attr("dy", "0.35em")
            .attr("text-anchor", d => d.x0 < this._size.width / 2 ? "start" : "end")
            .text(d => d.name);

    }
}

cmk_figures.figure_registry.register(SankeyDiagram);
var content = `source,target,value
Agricultural 'waste',Bio-conversion,124.729
Bio-conversion,Liquid,0.597
Bio-conversion,Losses,26.862
Bio-conversion,Solid,280.322
Bio-conversion,Gas,81.144
Biofuel imports,Liquid,35
Biomass imports,Solid,35
Coal imports,Coal,11.606
Coal reserves,Coal,63.965
Coal,Solid,75.571
Coal,Iron,75.571
Iron,Green,75.571
Green,Gas,22
District heating,Industry,10.639
District heating,Heating and cooling - commercial,22.505
District heating,Heating and cooling - homes,46.184
Electricity grid,Over generation / exports,104.453
Electricity grid,Heating and cooling - homes,113.726
Electricity grid,H2 conversion,27.14
Electricity grid,Industry,342.165
Electricity grid,Road transport,37.797
Electricity grid,Agriculture,4.412
Electricity grid,Heating and cooling - commercial,40.858
Electricity grid,Losses,56.691
Electricity grid,Rail transport,7.863
Electricity grid,Lighting & appliances - commercial,90.008
Electricity grid,Lighting & appliances - homes,93.494
`;
