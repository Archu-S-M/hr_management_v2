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
    		question_input_initial();
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


	var file_url = data["question_url"];
	// alert(data.question_id)
 	if(data["question_id"] != 0) {
		filter.question_id = data["question_id"];
		question_input_withfile(file_url);
		$("#question_download").removeClass('disabled');
		$("#question_download").attr("href", file_url);
		
	}
	else {
		filter.question_id = 0;
		$("#question_download").addClass('disabled');
	}
		

}



// =========================================================
// for the file input 

function question_input_initial() {
	
	$("#question_file").fileinput({
		maxFileSize: 1024, // 1 MB
        showUpload: true,
        overwriteInitial : true,
        allowedFileTypes: ["pdf"],
        allowedFileExtensions: ["pdf"]

	}).fileinput('clear');
}


// ===========================================================
// for the question input with initial file
function question_input_withfile( file_url ) {

	$('#question_file').fileinput('refresh', {
			maxFileSize: 1024,
			showUpload: true, 
        	overwriteInitial : true,
        	allowedFileTypes: ["pdf"],
        	allowedFileExtensions: ["pdf"],
			initialPreviewAsData: true, 
	        initialPreviewFileType: 'pdf',
	        initialPreview: [
	            file_url,
	        ],
	        initialPreviewConfig: [
	            {caption:"Questions", showZoom: true}
	        ]
		});
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
			console.log(JSON.stringify(data));
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
// to post the questionnaire

$("#questionnaire").on("submit", function(e) {

	
	e.preventDefault();
    var formData = new FormData($(this)[0]);
    formData.append('post_for', "upload_questionnaire");
    formData.append('question_id', filter.question_id);
    formData.append('position_id', filter.position_id);
    $.ajax({
        url: BASE_URLS.Questionnaire,
        type: 'POST',
        data: formData,
        async: false,
        success: function (data) {

        	showNotifications(data.message, data.msg_type);
        	if(msg_type === "success") {
        		$("#question_download").attr("href", data.data.question_url);
				$("#question_download").removeClass('disabled');
        	}
        },
        cache: false,
        contentType: false,
        processData: false
    });
});




// ========================================================================
get_position_filter();
question_input_initial();
