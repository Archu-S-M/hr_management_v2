// Initiate the filteres if needed

var Filters = {
	"start_date": "",
	"end_date": "",
    "id": 0,
}

var $CANDIDTATE_TABLE = null;

// ==========================================================================
// function to create activity table

function create_consultancy_table() {
	$CANDIDTATE_TABLE = $('#consultancy_table').dataTable({
        responsive: true,
        order: [],
        colReorder: true,
        // dom: 'Bfrtip',
        columns:[
        	
        	{data: "consultancy.name"},
        	{data: "website"},
            {data: "phone_no"},
            {
                data: "status",
                render: function(data, type, raw, meta) {
                    var consultancy = raw["consultancy"]["id"];
                    var checked = (data)?"checked":"";
                    var data_on_text = "Approved";
                    var data_off_text = (data)?"Blocked":"Waiting";
                    var data_on_color = "success";
                    var data_off_color = (data)?"danger":"warning";

                    var checkbox = "<input class=\"bootstrap_switch\" \
                                    data-on-text=\""+data_on_text+"\" \
                                    data-off-text=\""+data_off_text+"\" \
                                    data-on-color=\""+data_on_color+"\" \
                                    data-off-color=\""+data_off_color+"\" \
                                    type=\"checkbox\" name=\""+consultancy+"\" \
                                    "+checked+">"; 
                    return checkbox;
                }
            },
            {data: "datetime"},
        	
        ]
		

    });

    return $CANDIDTATE_TABLE;
}


// ==========================================================
// get consultancy values

function get_consultancy() {

	// call ajax function
	$.ajax({
		url: "{% url 'ManageConsultancy' %}",
        type: 'POST',
        data: {filter: Filters, submit: "get_consultancy"},
        success: function (data) {
        	update_details(data.data, $CANDIDTATE_TABLE);
        }
	});
}


// =============================================================
// Update with the data
// ==============================================================
// Update the short details in the table
function update_details(data, $table) {
    // alert(JSON.stringify(data));
    $table.api().clear().draw();
    $table.api().rows.add(data);
    $table.api().columns.adjust().draw();
}


// ===============================================================
// function to change the status of consultancy
function update_consultancy() {
    // call ajax function
    $.ajax({
        url: "{% url 'ManageConsultancy' %}",
        type: 'POST',
        data: {filter: Filters, submit: "update_consultancy"},
        success: function (data) {
            alert("Consultancy Status Updated");
        }
    });
}



// =============================================
// initiate a bootstrap switch
function create_bootstrapSwitch() {

    
    $(".bootstrap_switch").bootstrapSwitch({
        
        onSwitchChange: function(event, state) {
            var id = $(this).attr("name");
            Filters["id"] = id;
            update_consultancy();
        }


    });
}


// =========================================================================
// Initialize functions
create_consultancy_table();
get_consultancy();

$(document).ready(function() {
    setTimeout(function() {
        create_bootstrapSwitch();
    }, 100); 
});




