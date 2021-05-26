
function Main(){
    self = this;

    // Data
    self._data = []
    self._data_selected = []
    
    
    // Charts
    self._pcp = null;
    self._donutMakes = null;
    self._donutTotals = null;
    self._legend = null;
    self._dataTable = null;
    self._stats = null;

    // Other
    self._colors = {
        "selected": "#97a4bc",
        "un-selected":  "#e8eefd",
        "alfa-romero" : '#0a72ff',
        "audi" : '#1eff06',
        "bmw" : '#ff1902',
        "chevrolet" : '#2dfefe',
        "dodge" : '#827c01',
        "honda" : '#fe07a6',
        "isuzu" : '#a8879f',
        "jaguar" : '#fcff04',
        "mazda" : '#c602fe',
        "mercedes-benz" : '#16be61',
        "mercury" : '#ff9569',
        "mitsubishi" : '#05b3ff',
        "nissan" : '#8ffec2',
        "peugot" : '#3f8670',
        "plymouth" : '#e992ff',
        "porsche" : '#ffb209',
        "renault" : '#e72955',
        "saab" : '#83bf02',
        "subaru" : '#bba67b',
        "toyota" : '#fe7eb1',
        "volkswagen" : '#7570c1',
        "volvo" : "#85bfd1"
    }
    self.init();
}

Main.prototype = {
    init : function(csvFile){
        console.debug("Main: init");
        d3.csv("./data/imports-85.csv", function(d) {
        return {
            'make': d['make'],
            'fuel-type' : d['fuel-type'],
            'length' : +d['length'],
            'width' :+d['width'],
            'weight': +d['curb-weight'],
            'cylinders' : +d['num-of-cylinders'],
            'engine-size' : +d['engine-size'],
            'fuel-system': d['fuel-system'],
            'compression' : +d['compression-ratio'],
            'horsepower' : +d['horsepower'],
            'city-mpg' : +d['city-mpg'],
            'price' : +d['price'],
        };
        }, function(data) {
            self._data = data;
            self._data_selected = self._data.slice();
            self.setupCharts();
        });    
        
    },

    setupCharts : function(){
        var dimensions = ['make', 'fuel-type', 'compression', 'city-mpg' , 'cylinders', 'weight', 'engine-size','length', 'horsepower','width', 'price'];
        self._stats = stats(self._data);
        self._pcp = parallelCoordinatesChart("pcp", self._data, self._colors, dimensions, self.callback_applyBrushFilter);
        self._legend = legendChart("legend", self._data_selected, self._colors, self.callback_applyGroupFilter)
        self._donutMakes = donutChartGrouped("pie-groups", self._data_selected, "make",  self._colors, self._pcp.highlight_group);
        self._donutTotals = donutChartTotals("pie-totals", self._data_selected, self._colors);
        self._dataTable = dataTable("data-table", self._data_selected, dimensions, self._colors, self._pcp.highlight_single)
    },
    
    callback_applyBrushFilter : function(brushed_data){
        self._data_selected = brushed_data;
        self.refreshCharts();
    },

    refreshCharts : function() {
        self._donutTotals.update(self._data_selected);
        self._donutMakes.update(self._data_selected);
        self._pcp.update(self._data_selected);
        self._dataTable.update(self._data_selected);
    },
    

    callback_applyGroupFilter : function(groupFilter){
        var hide = false;
        var index = self._data_visible_groups.indexOf(groupFilter);
        if (index == -1){   // Index does not exist
            hide = false;
            // Add group as a visible group
            self._data_visible_groups.push(groupFilter);
        }else { // Index does exist    
            hide = true;
            // Remove group as visible
            self._data_visible_groups.splice(index,1);
        }
        self.refreshCharts();
        return hide;
    },
} 

function capitalize(string) { 
    return string.charAt(0).toUpperCase() + string.slice(1); 
}