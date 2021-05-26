window.dataTable = function(id, data, columns, colors, callback_highlight){
	var dataTable = {};
	var _data = data;
	var columns2 = [
		{ name: "", field: "make", id: "make", sortable: true, width: 30, resizable: false , headerCssClass: "prKeyHeadColumn", formatter: MakeFormatter },
		{ name: "Fuel Type", field: "fuel-type", id: "fuel-type", sortable: true, width: 200, resizable: false , headerCssClass: "prKeyHeadColumn", formatter:StringFormatter },
	    { name: "Min.Temper", field: "min-temp", id: "min-temp", sortable: true, width: 95, resizable: false, headerCssClass: "prKeyHeadColumn", cssClass: "numericCell" },
	    { name: "Max.Temper", field: "max-temp", id: "max-temp", sortable: true, width: 90, resizable: false , headerCssClass: "prKeyHeadColumn", cssClass: "numericCell"},
	    { name: "Max. Pressure", field: "peak-rpm", id: "peak-rpm", sortable: true, width: 90, resizable: false , headerCssClass: "prKeyHeadColumn", cssClass: "numericCell"},
	    { name: "Min. Pressure", field: "highway-mpg", id: "highway-mpg", sortable: true, width: 90, resizable: false , headerCssClass: "prKeyHeadColumn", cssClass: "numericCell"},
	    { name: "Cladding Thickness", field: "stroke", id: "stroke", sortable: true, width: 90, resizable: false , headerCssClass: "prKeyHeadColumn", cssClass: "numericCell"},
	    { name: "Fluid Height", field: "height", id: "height", sortable: true, width: 75, resizable: false , headerCssClass: "prKeyHeadColumn", cssClass: "numericCell"},
	    { name: "Weight (lbs)", field: "weight", id: "weight", sortable: true, width: 85, resizable: false, headerCssClass: "prKeyHeadColumn", cssClass: "numericCell", formatter: NumberFormatter },
	    { name: "Engine-size (cm3)", field: "engine-size", id: "engine-size", sortable: true, width: 115, resizable: false , headerCssClass: "prKeyHeadColumn", cssClass: "numericCell"},
	    { name: "Length (cm)", field: "length", id: "length", sortable: true, width: 80,resizable: false , headerCssClass: "prKeyHeadColumn", cssClass: "numericCell" },
	    { name: "Width (cm)", field: "width", id: "width", sortable: true, width: 80, resizable: false  , headerCssClass: "prKeyHeadColumn", cssClass: "numericCell"},
	    { name: "COF ($)", field: "cof", id: "cof", sortable: true, width: 100, resizable: false , headerCssClass: "prKeyHeadColumn", cssClass: "numericCell", formatter: NumberFormatter}

	];

	var options = {
        enableCellNavigation: true,
        enableColumnReorder : true,
      };

	var grid = new Slick.Grid("#" + id, _data, columns2, options)

	grid.onSort.subscribe(function (e, args) {
    	var field = args.sortCol.field;
	    _data.sort(function (a, b) {
	        var result =
	            a[field] > b[field] ? 1 :
	            a[field] < b[field] ? -1 :
	            0;

	        return args.sortAsc ? result : -result;
	    });
    	grid.invalidate();
	});

	grid.onMouseEnter.subscribe(function(e,args) {
		var selected = grid.getCellFromEvent(e).row;
		callback_highlight(_data[selected]);
    });

	grid.onMouseLeave.subscribe(function(e,args) {
		callback_highlight(undefined);
    });

    function MakeFormatter(row, cell, value, columnDef, dataContext) {
        if (value == null || value == "" || typeof value == "undefined"){
            return "";
        }
        else {
			var co = value%20;
			// return  "<svg width=\"20\" height=\"20\"> <circle style=\"width:80%; height:80%;\" cy=\"12\" cx=\"10\" r=\"7\" fill=\"" + colors[value] + "\"> </circle> </svg> <text>" + capitalize(value) + " </text>";
			return  "<svg width=\"20\" height=\"20\"> <circle style=\"width:80%; height:80%;\" cy=\"12\" cx=\"10\" r=\"7\" fill=\"" + colors[co] + "\"> </circle> </svg> ";
        }
    }

    function StringFormatter(row, cell, value, columnDef, dataContext) {
		return  "<text>" + capitalize(value) + " </text>";
    }

     function NumberFormatter(row, cell, value, columnDef, dataContext) {
        if (value == null || value == "" || typeof value == "undefined"){
            return "";
        }
        else {
        	var priceWithDots = value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");

			return  "<text>" + priceWithDots + "</text>";
        }
    }

	dataTable.update = function(data){
		if (_.isEmpty(data)) return;
		_data = data;
		grid.setData(_data);
		grid.invalidate();
		grid.render();
	}

    return dataTable;

}