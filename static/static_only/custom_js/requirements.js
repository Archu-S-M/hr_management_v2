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
            
            
            
        ],

        // createdRow: function (row, data, index) {

        //     console.log(JSON.stringify(data));
        // }
        

    });
}





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
            
            
        ],

      
    });
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



// Initial call to the function
create_position_table();
create_skill_table();
get_positions();
get_position_filter();
get_skills();