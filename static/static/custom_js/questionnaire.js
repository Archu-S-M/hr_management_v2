// questionnaire super user functions


var filter = {
	position_id: 0,
	question_id: 0,
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
    	// alert(value);
    	if(value) {
    		filter.position_id = value;
    		get_questions();
    	}
    	else {
    		filter.position_id = 0;
    		filter.question_id = 0;
    		update_file(false);
    	}
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

// =========================================================
// function to update the input field
function update_file(data) {

	if(data != false) {
		var file_url = data["question_url"];
	 	if(data["question_id"] != 0) {
			filter.question_id = data["question_id"];
			$("#question_download").removeClass('disabled');
			$("#question_download").attr("href", file_url);
			$("#question_body").attr("data", file_url);
			
		}
	}
		
	else {
		filter.question_id = 0;
		$("#question_download").addClass('disabled');
		$("#question_download").attr("href", "/media/#");
		$("#question_body").attr("data", "/media/#");
	}
		

}


// ========================================================================
// function to fill the position filter

function get_position_filter() {

	$.ajax({
		url: BASE_URLS.Questionnaire,
		type: 'POST',
		data: {post_for:"get_position_filter"},
		success: function(data) {
			updateFilter(data.data);
		}

	});
}

// ========================================================================
// function to get quesions

function get_questions() {

	$.ajax({
		url: BASE_URLS.Questionnaire,
		type: 'POST',
		data: {post_for:"get_questions", position_id: filter.position_id},
		success: function(data) {
			// console.log(JSON.stringify(data));
			update_file(data.data);
		}

	});
	
	
}
// =======================================================================
// function to show nootifications

function  showNotifications(msg, type) {
	$.notify({
	// options
	message: msg
	},{
		// settings
		type: type,
		
	});
}

// ========================================================================
get_position_filter();
question_input_initial();
