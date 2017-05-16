// Thesse are the requirement functions for the super user
// Operation Global

POSITION_OPERATION = {
    id : false,
    for : false,
}

SKILL_OPERATION = {
    id: false,
    for: false,
}

filter = {position:0};

// table objects
$POSITION_TABLE = false;
$SKILL_TABLE = false;

// ==========================================================================
// global function to get the data if tr is given

function getRowData(tr=false, format="JSON") {
    if(tr) {
        
        if(format === "JSON") {
            var obj = [];
            

            tds = $(tr).find("td");
            tds.each(function() {
                var data = $(this).text();
                obj.push(data)
            });

            return obj;
        }
    }
}

// ==========================================================================
// function to create position table

function create_position_table() {
	$POSITION_TABLE = $('#position_table').dataTable({
        responsive: true,
        order: [],
        colReorder: true,


        columns:[
        	
        	{data: "position.name"},
        	{data: "description"},
            {
                data: "state",
                className: "dt-body-center",
                render: function(data, type, raw_data, meta) {
                    var label_clr = "label-success";
                    label_clr = (data === "Open")? "label-success": "label-danger";
                    var html = '<span class="label '+label_clr+'" style="display:inline-block;width: 50px !important;">'+data+'</span>';
                    return html;
                }
            },
            {data: "date"},
            {
                data: "operations",
                width: "60px",
                render: function(data, type, raw_data, meta)  {

                    var html = "No Operations";
                    if(data) {
                        var id = raw_data["position"]["id"];
                        html  = "<a class=\"btn btn-default\" onClick=\"edit_position(this, "+id+");\"> \
                                    <i class=\"fa fa-pencil\"></i> \
                                </a>";
                        html += "<a class=\"btn btn-default\" onClick=\"delete_position(this, "+id+");\"> \
                                    <i class=\"fa fa-trash\"></i> \
                                </a>";
                    }

                    return html;
                }
            }
        	
        ],

        // createdRow: function (row, data, index) {

        //     console.log(JSON.stringify(data));
        // }
		

    });
}


// ------------------------------------------------------------------------------------
// Edit the positions 
function edit_position(that, id) {

    var tr = $(that).closest("tr");
    var data = getRowData(tr);
    $('#edit_position_row input[name="id"]').val(id);
    $('#edit_position_row input[name="position"]').val(data[0]);
    $('#edit_position_row input[name="description"]').val(data[1]);
    if(data[2] === "Closed")
        $('#position_state').bootstrapSwitch('state', false);
    else
        $('#position_state').bootstrapSwitch('state', true);

    POSITION_OPERATION.id = id;
    $("#position_modal").modal("show");

}

// -------------------------------------------------------------------------------------
// Update the status
function change_pos_status(that, id) {

    var message = "<div class='alert alert-danger'>";
        message += "This operation will update the database. Do you want to continue?!"
        message += "</div>";

    POSITION_OPERATION.id = id;
    $("#general_modal_position .modal-body").html(message);
    $("#general_modal_position").modal("show");

}

// -------------------------------------------------------------------------------------
// delete the positions
function delete_position(that, id) {

    var message  = "<div class='alert alert-danger'>";
        message += "This operation will delete the values. Do you want to continue?!";
        message += "</div>";

    POSITION_OPERATION.id = id;
    $("#general_modal_position .modal-body").html(message);
    $("#general_modal_position").modal("show");
}



// =============================================================
// for bootstrap switch with position state

$("#position_state").bootstrapSwitch({
    
    onText: "Open",
    offText: "Closed",
    onColor: "success",
    offColor: "danger",              
    onSwitchChange: function(event, state) {
        
    }

});
// =============================================================
// #####################################################################################
// Skill TAB
// #####################################################################################

// ==========================================================================
// function to create skill table

function create_skill_table() {
    $SKILL_TABLE = $('#skill_table').dataTable({
        responsive: true,
        order: [],
        colReorder: true,
        columns:[
            
            {data: "skill.name"},
            {data: "description"},
            {data: "date"},
            {
                data: "operations",
                width: "60px",
                render: function(data, type, raw_data, meta)  {

                    var html = "No Operations";
                    if(data) {
                        var id = raw_data["skill"]["id"];
                        html  = "<a class=\"btn btn-default\" onClick=\"edit_skills(this, "+id+");\"> \
                                    <i class=\"fa fa-pencil\"></i> \
                                </a>";
                        html += "<a class=\"btn btn-default\" onClick=\"delete_skills(this, "+id+");\"> \
                                    <i class=\"fa fa-trash\"></i> \
                                </a>";
                    }

                    return html;
                }
            }
            
        ],

      
    });
}

// ------------------------------------------------------------------------------------
// Edit Skills
function edit_skills(that, id) {

    var tr = $(that).closest("tr");
    var data = getRowData(tr);
    $('#edit_skill_row input[name="id"]').val(id);
    $('#edit_skill_row input[name="skill"]').val(data[0]);
    $('#edit_skill_row input[name="skill_description"]').val(data[1]);
    
    SKILL_OPERATION.id = id;
    $("#skill_modal").modal("show");
}
// -------------------------------------------------------------------------------------
// delete the skills

function delete_skills(that, id) {

    var message  = "<div class='alert alert-danger'>";
        message += "This operation will delete the values. Do you want to continue?!";
        message += "</div>";

    SKILL_OPERATION.id = id;
    $("#general_modal_skill .modal-body").html(message);
    $("#general_modal_skill").modal("show");
}

// ==============================================================
// initilaizing selectize filter for skills

var $position_filter = $('#position_filter').selectize({
    
    options: [
        {value:"1",label:"Position"},
    ],
    valueField: 'value',
    labelField: 'label',
    searchField: 'label',
    persist: true,
    create: false,
    maxItems: 1,

    // on changing the selectize
    onChange: function(value) {
        if(value) {
            filter.position = value; 
        }
        else {
            filter.position = 0;
        }

        get_skills();
        
    }
    
});


// =========================================================
// update the filter value on functin call

function updateFilter(data) {
    var selectize = $position_filter[0].selectize;
    selectize.clearOptions();
    for(var i=0;i< data.length; i++) {
            selectize.addOption(data[i]);
    }   
    selectize.refreshOptions(false);
}


// =============================================================
// Update with the data

function update_details(data, $table) {
    $table.api().clear().draw();
    $table.api().rows.add(data);
    $table.api().columns.adjust().draw();
}


// #####################################################################
// get data for initial load
// #####################################################################
function get_positions() {

    $.ajax({
        url: BASE_URLS.Requirements,
        type: 'POST',
        data: {post_for: "get_position"},
        success: function (data) {
            // alert(JSON.stringify(data));
            update_details(data.data, $POSITION_TABLE);
        } 
    });
}


// get the data for position filter
// -------------------------------------------------------------------

function get_position_filter() {

    $.ajax({
        url: BASE_URLS.Requirements,
        type: 'POST',
        data: {post_for: "get_position_filter"},
        success: function (data) {
            // alert(JSON.stringify(data));
            updateFilter(data.data);
        } 
    });
}

// get the master skills for a given position
// -------------------------------------------------------------------

function get_skills() {

    var position_id = filter.position;
    $.ajax({
        url: BASE_URLS.Requirements,
        type: 'POST',
        data: {post_for: "get_skills", position: position_id},
        success: function (data) {
            // alert(JSON.stringify(data));
            update_details(data.data, $SKILL_TABLE);
        } 
    });
}

// #####################################################################
// POSTING DATA
// #####################################################################

// Adding new position
$("#form-position").on("submit", function(e) {

    e.preventDefault();
    var formData = $(this).serializeArray();
    formData.push({name:"post_for",value:"add_position"});

    $.ajax({
        url: BASE_URLS.Requirements,
        type: 'POST',
        data: formData,
        success: function (data) {
            
            $("#form-position").reset();
            get_position_filter();
            get_positions();
        }
    });

});


// Adding new skills
// ------------------------------------------------------------
$("#form-skill").on("submit", function(e) {

    e.preventDefault();
    var formData = $(this).serializeArray();
    formData.push({name:"post_for", value:"add_skill"});
    formData.push({name:"position_id", value:filter.position})
    $.ajax({
        url: BASE_URLS.Requirements,
        type: 'POST',
        data: formData,
        success: function (data) {
            // alert(JSON.stringify(data));
            $("#form-skill").reset();
            get_skills();
        },
        
    });

});

// Updating position
// -------------------------------------------------------------

$("#edit_position_row").on("submit", function(e) {

    // alert("updating");
    e.preventDefault();
    var formData = new FormData($(this)[0]);
    formData.append('post_for', "update_position");
    $.ajax({
        url: BASE_URLS.Requirements,
        type: 'POST',
        data: formData,
        success: function (data) {
            $("#position_modal").modal("hide");
            get_position_filter();
            get_positions();
        },
        contentType: false,
        processData: false
    });

});

// Updating Skill
// -------------------------------------------------------------

$("#edit_skill_row").on("submit", function(e) {

    e.preventDefault();
    var formData = new FormData($(this)[0]);
    formData.append('post_for', "update_skill");
    formData.append("position_id", filter.position);
    $.ajax({
        url: BASE_URLS.Requirements,
        type: 'POST',
        data: formData,
        success: function (data) {
            $("#skill_modal").modal("hide");
            get_skills();

        },
        contentType: false,
        processData: false,
    });

});

// ############################################################
// to get the confirmation

// for confirming position delete
$("#confirm_position").on("click", function() {
    $.ajax({
        url: BASE_URLS.Requirements,
        type: 'POST',
        data: {position_id: POSITION_OPERATION.id, post_for:"delete_position"},
        success: function (data) {
            // alert(data);
            get_position_filter();
            get_positions();
            get_skills();
        },
        
    });
});

// for confirming skill delete
$("#confirm_skill").on("click", function() {
    $.ajax({
        url: BASE_URLS.Requirements,
        type: 'POST',
        data: {skill_id: SKILL_OPERATION.id, post_for:"delete_skill"},
        success: function (data) {
            // alert(data);
            get_skills();
        },
        
    });
});


// #####################################################################
// initilalizations


// Initial call to the function
create_position_table();
create_skill_table();
get_positions();
get_position_filter();
get_skills();