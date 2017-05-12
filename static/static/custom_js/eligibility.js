/*
* Initial variables
*/



// ========================================================================
/**
 * [funcstion to create html string for new eligibility]
 * @param  {[string]} eligibility [eligiblity value]
 * @param  {[integer]} id          [corresponding database id]
 * @return {[boolean or string]}             [Boolean False or html string]
 */
function get_eligibility_html(eligibility, id) {
	

	 

	// alert(eligiblity)
	if(eligibility) {

		var html  = '<div class="alert alert-success alert-dismissable fade in">';
			html += eligibility;

			if(EL_CLOSE) {
				EL_CLOSE = EL_CLOSE.replace("%d", id)
				html += EL_CLOSE;
			}
			
			html += '</div>';

		return html;
	}

	else {
		return false;
	}
}



//  While adding new eligiblity
// ========================================================================
$("#new_eligibility").on("click", function() {

	var new_eligibility = $("#added_eligibility").val();
	$("#added_eligibility").val(null);
	// alert(new_eligibility);
	if(new_eligibility !== "") {

		 post_eligibility(new_eligibility);

	}
		
});


// method to decide apppend or create eligiblity
function show_eligiblity(new_eligibility, el_id) {

	if(el_id) {
			 	
	 	var html= get_eligibility_html(new_eligibility, el_id);

		 if(html) {
		 	// alert(html);
		 	// if eligibility count is grater than one add the new eligibility
			// otherwise overwrite the div
			if(Eligibility_Count>=1) {
				$("#eligibility").prepend(html);
				Eligibility_Count ++;
			}

			else {
				$("#eligibility").html(html);
				Eligibility_Count ++;
			}
		 }	
	 }

	 else {
	 	alert("Posting failed");
	 }
}

// =============================================================================
// post the newly created eligibility

function post_eligibility(new_eligibility) {

	var id = false;
	$.ajax({
		url: URL_DICT.eligibility,
		type: "POST",
		data: {submit: "post_eligibility", eligibility: new_eligibility},
		success: function(data) {

			// alert(JSON.stringify(data.id));
			id = data.id;
			if(id) {
				// alert(new_eligibility);
				show_eligiblity(new_eligibility, id);
			}

			// create_eligiblity(data.eligibility);
		}
	});

	return id;
}


// ==============================================================================

// function to get the current eligiblity when open page and reload 

function get_eligibility() {

	$.ajax({
		url: URL_DICT.eligibility,
		type: "POST",
		data: {submit: "get_eligibility"},
		success: function(data) {

			// alert(JSON.stringify(data));
			create_eligiblity(data.eligibility);
		}
	});
}





// ===============================================================================
// functin to create eligiblity

function create_eligiblity(data) {

	$.each(data, function(key, value) {
		eligibility = value.eligibility;
		var html = get_eligibility_html(eligibility, value.id);
		show_eligiblity(eligibility, value.id);
	});
}




get_eligibility();