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
        columns:[
        	
        	{
                data: "activities.activity"
            },
        	{
                data: "date",
                width: "120px"
            },
        	
        ],

        createdRow: function (row, data, index) {

            consultancy_id = data.activities.consultancy_id;
            candidate_id = data.activities.candidate_id;
            question_id = data.activities.question_id;
            requirements_id = data.activities.requirements_id;

            if(consultancy_id) {
                $(row).addClass("danger");
            }
            else if(candidate_id) {
                $(row).addClass("info");
            }
            else if(question_id) {
                $(row).addClass("warning");
            }
            else if(requirements_id) {
                $(row).addClass("success");
            }


        }
		

    });
}

// =============================================================
// Update with the data

function update_details(data, $table) {
    
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
