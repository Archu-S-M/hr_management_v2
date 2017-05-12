// Initiate the filteres if needed

var Filters = {
	"start_date": "",
	"end_date": ""
}

var $ACTIVITY_TABLE = null;


// ==========================================================================
// function to create activity table

function create_activity_table() {
	$ACTIVITY_TABLE = $('#activity_table').dataTable({
        responsive: true,
        order: [],
        colReorder: true,
        // dom: 'Bfrtip',
        columns:[
        	
        	{
                data: "activities.activity"
            },
        	{data: "date"},
        	
        ],

        createdRow: function (row, data, index) {

            console.log(JSON.stringify(data));
        }
		

    });
}

// =============================================================
// Update with the data

function update_details(data, $table) {
    // alert(JSON.stringify(data));
    $table.api().clear().draw();
    $table.api().rows.add(data);
    $table.api().columns.adjust().draw();
}


//  Get the consultacy values
// ===================================================
function get_activities() {

	// call ajax function
	$.ajax({
		url: URL_DICT.dashboard,
        type: 'POST',
        data: {filter: Filters, submit: "get_activities"},
        success: function (data) {
        	// alert(JSON.stringify(data));
            update_details(data.data, $ACTIVITY_TABLE);
        }
	});
}


// =========================================================================
// Initialize functions

create_activity_table();
get_activities();
