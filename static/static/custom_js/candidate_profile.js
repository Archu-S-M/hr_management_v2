/*************************************************
 * Global variables and constants
 ************************************************/

// Set on new employee reset othervise
var CANDIDATE_NEW = true;
var CANDIDATE_SELECTED = false;
var SUBMIT_VALUE = "";
// for setting and resetting the confirmation of delete
var DELETE = false;

// candidate short details table object
// it will reset to table object on first load
$CANDIADTE_SHORT_DETAILS = false;

// skillset row number initialy 0
var SKILL_ROW_NO = 0;

// Filter object
// ================================================================================
//  Default filter to call using ajax. The filter values will change on each fields
var Filters = {
	status: "",
	position: "",
	consultancy: "",
	skills : "",
	experience : "",
	location : "",
	expected_ctc : [],
	notice_period : "",
	candidate_status : "",
	submit : "get_filtered_data",
};
    

// object_array for filters
var filter_object_array = {};


// Available skillset arry on first load
var availableSkillset = [];
var availablePositions = [];
var availableStatus = [
	{label: "New", value: "New"},
	{label: "Hold", value: "Hold"},
	{label: "Tellephonic", value: "Tellephonic"},
	{label: "Face to Face", value: "Face to Face"},
	{label: "Shortlisted", value: "Shortlisted"},
	{label: "Selected", value: "Selected"},
	{label: "Rejeceted", value: "Rejeceted"},
];


if(availablePositions.length === 0) {
	$("#top_message").show();
	$("#candidate_details").hide();
}

// #####################################################################################
/* *************************************
 * Filters and its managing functions
 * *************************************/


// function to reset the form to create new employee
$("#new_candidate").on("click", function() {

	$("#candidate_details").fadeIn();
	$("#candidate_short_details_panel").fadeOut();

	CANDIDATE_NEW = true;

	var $form = $("#candidate_details");

	resetForm( $form );

	var video = document.getElementById('interview_video_play');
	var sources = video.getElementsByTagName('source');
    sources[0].src = "#";
    video.load();

	$("#interview_video_download").attr("href", "#");
	$("#resume_download").attr("href", "#");

	$('#candidate_status').prop("disabled", CANDIDATE_NEW);
	$('#delete').prop("disabled", CANDIDATE_NEW);

});

// ================================================================
// function to reset the form

function resetForm( form ) {
	form[0].reset();

	// delete the skills in the skill table
	while (SKILL_ROW_NO>0) {
		row_id = "skill_row" + SKILL_ROW_NO;
		delete_skill_row( row_id );
	}


	// reset the resume and video file input
	resume_input_initial();
	video_input_initial();
}



// ========================================================================
// to create position filter

var $status_filter = $('#status_filter').selectize({
    options: availableStatus,
    valueField: 'value',
    labelField: 'label',
    searchField: 'label',
    persist: true,
    create: false,
    maxItems: 1,
    // on changing the selectize
    onChange: function(value) {
		Filters["status"] = value;
		CANDIDATE_NEW = false;
		$("#candidate_details").fadeOut();
		$("#candidate_short_details_panel").fadeIn();
		$("#collapse_can_details").collapse("show");
		get_filterd_data();
	}
    
});


// add to object array
filter_object_array["status"] = $status_filter;


// ========================================================================
// to create position filter

var $position_filter = $('#position_filter').selectize({
	plugins: ['remove_button'],
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
		Filters["position"] = value;
		CANDIDATE_NEW = false;
		$("#candidate_details").fadeOut();
		$("#candidate_short_details_panel").fadeIn();
		$("#collapse_can_details").collapse("show");
		get_filterd_data();
	}
    
});


// add to object array
filter_object_array["position"] = $position_filter;


// ========================================================================
// to create filters

var $consultancy_filter = $('#consultancy_filter').selectize({
	plugins: ['remove_button'],
    options: [
        {value:"1",label:"Consultancy"},
    ],
    valueField: 'value',
    labelField: 'label',
    searchField: 'label',
    persist: true,
    create: false,
    maxItems: 1,
    // on changing the selectize
    onChange: function(value) {
		Filters["consultancy"] = value;
		CANDIDATE_NEW = false;
		$("#candidate_details").fadeOut();
		$("#candidate_short_details_panel").fadeIn();
		$("#collapse_can_details").collapse("show");
		get_filterd_data();
	}
    
});

// add a new functionality
// add to object array
filter_object_array["consultancy"] = $consultancy_filter;

// ========================================================================


// filter to get the vales of skills
// it is a multi box with bootstrap styles
var $skill_filter = $('#skill_filter').selectize({
    plugins: ['drag_drop','remove_button'],
    // delimiter: ',',
    options: [
        {value:"Skill1",label:"Skill1"}, 
        {value:"Skill2",label:"Skill2"}, 
        {value:"Skill3",label:"Skill3"}, 
        {value:"Skill4",label:"Skill4"}, 
    ],
    valueField: 'value',
    labelField: 'label',
    searchField: 'label',
    persist: true,
    create: false,

    // on changing the selectize
    onChange: function(value) {
		Filters["skills"] = value;
		CANDIDATE_NEW = false;
		$("#candidate_details").fadeOut();
		$("#candidate_short_details_panel").fadeIn();
		$("#collapse_can_details").collapse("show");
		get_filterd_data();
	}
    
});

// add to object array
filter_object_array["skills"] = $skill_filter;

// =============================================================
// selectize for the experience

var $experience_filter = $("#experience_filter").selectize({
	options: [
		{value:"1", label:"1 Year"},
		{value:"2", label:"2 Years"},
		{value:"3", label:"3 Years"},
		{value:"1.5", label:"1.5 Years"},
	],
	valueField: 'value',
    labelField: 'label',
    searchField: 'label',

    // on changing the selectize
    onChange: function(value) {
		Filters["experience"] = value;
		CANDIDATE_NEW = false;
		$("#candidate_details").fadeOut();
		$("#candidate_short_details_panel").fadeIn();
		$("#collapse_can_details").collapse("show");
		get_filterd_data();
	}
});

// add to object array
filter_object_array["experience"] = $experience_filter;

// =============================================================
// selectize for the location

var $location_filter = $("#location_filter").selectize({
	maxItems: 1,
	options: [
		{value:"India", label:"India"},
		{value:"Australia", label:"Australia"},
		{value:"United States", label:"United States"},
		{value:"China", label:"China"},
	],
	valueField: 'value',
    labelField: 'label',
    searchField: 'label',

    // on changing the selectize
    onChange: function(value) {
		Filters["location"] = value;
		CANDIDATE_NEW = false;
		$("#candidate_details").fadeOut();
		$("#candidate_short_details_panel").fadeIn();
		$("#collapse_can_details").collapse("show");
		get_filterd_data();
	}
});

// add to object array
filter_object_array["locations"] = $location_filter;


// fill the filters with data
// =======================================================
function fill_filters(filter_name) {

	// call ajax function
	$.ajax({
		url: "{% url 'CandidateProfile' %}",
        type: 'POST',
        data: {filter: filter_name, submit: "fill_filters"},
        success: function (data) {
        	update_filters(data, filter_name);
        	// to update the data in the candiate skills
        	if(filter_name === "skills") {
        		availableSkillset = [];
        		for(var i=0;i<data[filter_name].length; i++) {
        			availableSkillset.push(data[filter_name][i]["label"]);
        		}
        		initiateSkillDropdown();

        	}
        	else if(filter_name === "position") {
        		availablePositions = [];
        		for(var i=0;i<data[filter_name].length; i++) {
        			availablePositions.push(data[filter_name][i]["label"]);
        		}

        		if(availablePositions.length === 0) {
					$("#top_message").show();
				}
				else {
					$("#top_message").hide();
				}

        		initiatePositionDropdown();
        	}

        }
	});
}

// ========================================================
// functtion to update the filters
function update_filters(data, filter_name) {
	
	if(data[filter_name].length>0) {
    	var selectize = filter_object_array[filter_name][0].selectize;
    	selectize.clearOptions();
    	for(var i=0;i< data[filter_name].length; i++) {
    		selectize.addOption(data[filter_name][i]);
    	}
    	selectize.refreshOptions(false);
	}
	
	
}


// =======================================================
// function to get the filtered data from server while passing the filters values


function get_filterd_data() {

	// alert(JSON.stringify(Filters));
	$.ajax({
        url: "{% url 'CandidateProfile' %}",
        type: 'POST',
        data: Filters,
        success: function (data) {
            // alert(JSON.stringify(data));
            candidate_data = data.candidate_details
            update_short_details(candidate_data, $CANDIADTE_SHORT_DETAILS);
        }
        
    });

}


// *****************************************************************************
/* **************************************
 * Showing and managing short details
 * *************************************/

 // ========================================================
// Function to create datatables for the candidate short details

function candidate_short_details () {
	
    var $candidate_table = $('#candidate_short_details').dataTable({
        responsive: true,
        order: [],
        colReorder: true,
        
        columns:[
        	{
        		data: "candidate.name",
        		render: function(data, type, raw_data, meta) {
        			candidate_id = raw_data["candidate"]["id"];
        			return "<a class=\"btn btn-default btn-block\" onClick=\"get_full_details('"+candidate_id+"');\">"+data+"</a>"; 
        		}
        	},
        	{data: "consultancy"},
        	{data: "experience"},
        	{data: "skills"},
        	{data: "current_ctc"},
        	{data: "expected_ctc"},
        	{data: "notice"},
        	{
        		data: "status",
        		render: function(data, type, raw_data, meta) {
        			var label = "";
        			switch(data) {
        				case "New": label = "label-default";break;
        				case "Hold": label = "label-info";break;
        				case "Tellephonic": label = "label-warning";break;
        				case "Face to Face": label = "label-warning";break;
        				case "Shortlisted": label = "label-primary";break;
        				case "Selected": label = "label-success";break;
        				case "Rejeceted": label = "label-danger";break;
        			}

        			return '<div class="label '+label+'" style="display:inline-block;width: 75px !important;">'+data+'</div>';

        		}
        	}
        ]
		

    });

    // Adding a custom button for reset the table to the initial condition
    $("#candidate_short_details_wrapper").prepend(
		'<div class="row" style="padding-bottom:10px"> \
			<div class="col-lg-12"> \
				<a class="btn btn-image pull-right" data-toggle="tooltip" data-placement="auto"\
					title="Reset Table" onClick="ResetTable();"> \
					<i class="fa fa-undo" aria-hidden="true"></i> \
				</a> \
			</div> \
		</div>'
	);

    return $candidate_table;
      
}

//===============================================================
// function to reset the entire table
function ResetTable() {
	$CANDIADTE_SHORT_DETAILS.fnSortNeutral();
	$CANDIADTE_SHORT_DETAILS.api().colReorder.reset();
}



// ==============================================================
// Update the short details in the table
function update_short_details(data, $table) {

	$table.api().clear().draw();
	$table.api().rows.add(data);
	$table.api().columns.adjust().draw();
}



// ##############################################################################
/***************************************************************
* functions to show and manage the complete detais of candidates
****************************************************************/

/**
 * dnamically convrt skill input field to dropdown
 * data to show initially
 */

function initiateSkillDropdown() {


	$( ".skill_input" ).autocomplete({
		minLength: 0,
    	source: availableSkillset

    }).focus(function(){            
    	$(this).autocomplete("search");
    });
}

// convert position input to dropdown
function initiatePositionDropdown() {
	$("#position").autocomplete({
		minLength: 0,
		source: availablePositions,
		change: function (event, ui) {
                if(!ui.item){
                    $("#position").val("");
                }

        }
	}).focus(function(){            
    	$(this).autocomplete("search");
    });
}


// function to create table skills row style dynamically
function skill_row_style( identifiers ) {
                    


	var row_id     = identifiers["row_id"],
		input_name = identifiers["input_name"],
		value      = identifiers["skills"],
		input_id   = identifiers["input_id"];



	// Creating html table row for the skillsets
	var tr = '<tr id="'+ row_id +'">';
	tr += '<td class="col-lg-10">';
	tr += '<div class="form-group">';
	tr += '<input id="'+input_id+'" class="form-control skill_input" type="text" name="'+ input_name +'" placeholder="Skill" value="'+value+'">'
	tr += '</div>';
	tr += '</div>';
	tr += '</td>';
	tr += '<td class="col-lg-2">';
	tr += '<div class="form-group">';
	tr += '<a class="btn btn-info" onClick="append_skill_row();" ><i class="fa fa-plus" aria-hidden="true"></i></a>';
	tr += '</div>';
	tr += '</td>';
	tr += '<td class="col-lg-2">';
	tr += '<div class="form-group">';
	tr += '<a class="btn btn-danger" onClick="delete_skill_row(\''+ row_id +'\');"><i class="fa fa-trash" aria-hidden="true"></i></a>'
	tr += '</div>';
	tr += '</td>';
	tr += '</tr>';

	return tr;

}


// =======================================================


// function append the table row after the last row
function append_skill_row(skills="") {

	
	SKILL_ROW_NO++;  

	identifiers = {
		"row_id" : "skill_row" + SKILL_ROW_NO,
		"input_name" : "skills",
		"skills": skills,
		"input_id": "skill_input" + SKILL_ROW_NO,
	};

	var tr = skill_row_style( identifiers );
	
	// Append the row
	$("#skill_table").append( tr );

	// adding dropdown properties to the input after creating the input
	initiateSkillDropdown();

	return true
}


// ===========================================================
// Function to delete a row

function delete_skill_row( row_id ) {

	  
	$('#'+row_id).remove();


	SKILL_ROW_NO--;

	return true;
}



// ========================================================================
// Function to generate autocomlete for google map
function initGoogleAutocomplete() {
  // Create the autocomplete object, restricting the search to geographical
  // location types.
  autocomplete = new google.maps.places.Autocomplete(
      /** @type {!HTMLInputElement} */
      (document.getElementById('location')),
      {types: ['geocode']});

  // When the user selects an address from the dropdown, populate the address
  
}


// ==============================================================
// function to show the detailed data on filter 

function get_full_details(can_id) {
	// alert(can_id);
	$.ajax({
		url: "{% url 'CandidateProfile' %}",
		type: 'POST',
		data: {id: can_id, submit: "get_full_details"},
		success: function (data) {
			// alert(data);
			show_full_details(data.candidate_details);
		}
	});
}

// ============================================================
// funtion to fill the data from filters to show details of employee
function show_full_details(data) {

	CANDIDATE_NEW = false;
	var $form = $("#candidate_details");

	resetForm( $form );

	// getting form details
	var candidate_name = data["candidate_name"],
		position = data["position"],
		status = data["status"],
		age = data["age"],
		experience = data["experience"],
		preferred_location = data["location"],
		current_ctc = data["current_ctc"],
		expected_ctc = data["expected_ctc"],
		email = data["email"],
		contact_no = data["contact_no"],
		skills = data["skills"],
		notice_period = data["notice_period"],
		interview_time = data["interview_time"],
		resume_url = data["resume_url"],
		video_url = data["video_url"];

	$("#candidate_details").fadeIn();
	$("#collapse_can_details").collapse("toggle");

	// load the values in the table
	$("#position").val(position);
	$("#status").val(status);
	$("#name").val(candidate_name);
	$("#age").val(age);
	$("#experience").val(experience);
	$("#location").val(preferred_location);
	$("#current_ctc").val(current_ctc);
	$("#expected_ctc").val(expected_ctc);
	$("#email").val(email);
	$("#contact_no").val(contact_no);
	$("#notice_period").val(notice_period);
	$("#interview_time").val(interview_time);
	// $("#interview_video").val(video_url);
	// $("#resume").val(resume_url);
	
	$("#skill_input0").val(skills[0]);
	initiateSkillDropdown();
	if(skills.length > 1) {
		for(var i=1; i<skills.length; i++) {
			append_skill_row(skills[i]);
		}
	}

	// var video = document.getElementById('interview_video_play');
	// var sources = video.getElementsByTagName('source');
 // 	sources[0].src = video_url;
	// video.load();

	$("#interview_video_download").attr("href", video_url);
	$("#resume_download").attr("href", resume_url);

	$('#delete').prop("disabled", CANDIDATE_NEW);
	// $('#delete').disabled = false;

	// alert(video_url);
	// refresh the file input with new values
	// =================================================
	if(resume_url !== "/media/#" && resume_url !== "#") {
		resume_input_withfile(resume_url);
	}

	else {
		resume_input_initial();
	}

	// -------------------------------------------------
	if(video_url !== "/media/#" && video_url !== "#") {
		video_input_withfile(video_url);
	}
	else {
		video_input_initial();
	}
	

	
}

// ========================================================================
// on button click remove the form

$("#remove_form").on('click', function() {
	$("#candidate_details").fadeOut();
	$("#candidate_short_details_panel").fadeIn();
	$("#collapse_can_details").collapse("show");
	
});

// ========================================================================

/**
 * This is the main post response
 * what are the notifications and actions to trigger after form submission
 * (Form Candidate Details)
 * @param  {[JSON]} data [from server]
 * @return {[null]} 
 */
function post_response(data) {


	// -------------------------------------------------------------------
	// re;oad the interview video or audio for valid paths
	if((data["video_url"] != "/media/#") && (data["video_url"] != "#")){
		
		   video_input_withfile(data["video_url"]);
		$("#interview_video_download").attr("href", data["video_url"]);
	}

	// ----------------------------------------------------------------------
	// Reload the candidate resume for valid path 
	if((data["resume_url"] != "/media/#") && (data["resume_url"] != "#")){

		resume_input_withfile(data["resume_url"]);
		$("#resume_download").attr("href", data["resume_url"]);
	}

	// ------------------------------------------------
	// get the response values
	var errors = data.errors,
		info   = data.info,	
		message = data.message,
		method = data.method;

	// ------------------------------------------------
	// If the method is delete
	if(method === "Delete") {
		$("#candidate_details").fadeOut();
		$("#candidate_short_details_panel").fadeIn();
		$("#collapse_can_details").collapse("show");
	}

	// ------------------------------------------------
	// If there are errors
	if(errors.length) {
		$.each(errors, function(key, value) {
			showNotifications(value, "danger");
		});
	}

	// ------------------------------------------------
	// If there are informations
	if(info.length) {
		// CANDIDATE_NEW = false;
		// after response from server about the new candidite reload the filters
		reload_filters();
		$.each(info, function(key, value) {
			showNotifications(value, "info");
		});
	}

	// ---------------------------------------------------------------------------
	// If there are messages successfull or errors on form input to database
	if(!($.isEmptyObject(message))) {
		
		
		// after response from server about the new candidite reload the filters
		$.each(message, function(key, value) {
			
			// -------------------------------------
			// If success
			if(key === "success") {
				CANDIDATE_NEW = false;
				var msg = "<strong>Success!</strong>"+value;
				showNotifications(msg, "success");
				reload_filters();
				get_filterd_data();
				
				
			}
			// ------------------------------------
			// If errors
			else if(key === "error") {
				var msg = "<strong>Error!</strong>"+value;
				showNotifications(msg, "danger");
			}
		});
	}


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
		delay: 2000,
		mouse_over: "pause",
		placement:{from: "top",
					align: "left"}
		
	});
}



// ##################################################################################

/* Initializastion of Candidate Profile Page
 * If the candidate is new deactivate the activate and delete buttons
 * It depends on the candidate dropdown.
 * if the candidate is seleced from dropdown CANDIDATE_NEW reset else set
 */

	
$('#candidate_status').prop("disabled", CANDIDATE_NEW);
$('#delete').prop("disabled", CANDIDATE_NEW);


// Datetime pipcker for interview time
$('#interview_time').datetimepicker({
	ignoreReadonly: true,
	showTodayButton: true,
	format: "DD/MM/YYYY hh:mm A"
});

// ================================================================
// function to find which submit button is clicked?!!!
$("#candidate_details input[type='submit']").on("click", function(e) {
	SUBMIT_VALUE = $(this).val();

});

// =================================================================
// candidate delete confirmation





// =================================================================
// function to show the file input

// ----------------------------------------------------------
// to load resume input initially
function resume_input_initial() {
	
	$("#resume").fileinput({
		maxFileSize: 1024, // 1 MB
        showUpload: false, 
        showUploadedThumbs: false,
        allowedFileTypes: ["pdf", "object"],
        allowedFileExtensions: ["docx", "doc", "pdf"]
	}).fileinput('clear');
}

// --------------------------------------------------------
// to load video input initially
function video_input_initial() {
	
	$("#interview_video").fileinput({
		maxFileSize: 51200, // 50 MB
        showUpload: false,
        showUploadedThumbs: false,
        allowedFileTypes: ["video", "object"],
        allowedFileExtensions: ["mpeg4", "mp4", "mp3", "wav", "ogg"]
	}).fileinput('clear'); 
}

// ---------------------------------------------------------
// to load resume input with file
function resume_input_withfile(file_url) {
	
	$('#resume').fileinput('refresh', {
		maxFileSize: 1024,
		showUpload: false, 
		showRemove: false,
		showClose: false,
		showUploadedThumbs: false,
		initialPreviewShowDelete: false,
    	overwriteInitial : true,
		initialPreviewAsData: true, 
        initialPreviewFileType: 'pdf', 
        initialPreview: [
            file_url,
        ],
        initialPreviewConfig: [
            {caption:"Resume", showZoom: true}
        ],
        allowedFileExtensions: ["docx", "doc", "pdf"]
	});
}

// ---------------------------------------------------------
// to load video input with file
function video_input_withfile(file_url) {
	
	$("#interview_video").fileinput('refresh',{
		maxFileSize: 51200,
		showUpload: false, 
		showRemove: false,
		showClose: false,
		showUploadedThumbs: false,
		initialPreviewShowDelete: false,
    	overwriteInitial : true,
    	initialPreviewAsData: true,
    	initialPreviewFileType: 'video',
		initialPreview: [
            file_url,
        ],
        initialPreviewConfig: [
            {caption:"Interview", showZoom: true, filetype: "video/mp4"}
        ],
        allowedFileTypes: ["video", "audio"],
        allowedFileExtensions: ["mpeg4", "mp4", "mp3", "wav", "ogg"]
	});
}
// =================================================================
// fill the filters with default value on page load

function reload_filters() {
	var Filters = {
		position : "",
		consultancy: "",
		skills : "",
		experience : "",
		location : "",
		expected_ctc : [],
		notice_period : "",
		candidate_status : "",
		submit : "get_filtered_data",
	};
	fill_filters("skills");
	fill_filters("locations");
	fill_filters("experience");
	fill_filters("consultancy");
	fill_filters("position");
	// fill_dropddown("skills");
}


// ==================================================================
// to get all available Master Skills

// ==================================================================
// initially show all the candidates

$CANDIADTE_SHORT_DETAILS = candidate_short_details();
reload_filters();
get_filterd_data();


