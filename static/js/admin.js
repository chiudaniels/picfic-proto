// Add Event Listeners
var formButtons = document.getElementsByClassName("adminForm");
var tabs = document.getElementsByClassName("customTab");
var tabDOM = document.getElementsByClassName("customTabDOM");

// Function to Submit AJAX Call
var submitAdminForm = function(){
    $.ajax({
	type : "POST",
	url : "/adminAction/",
	data : JSON.stringify({
	    "rowID" : this.getAttribute("rowID"),
	    "act" : this.getAttribute("act"),
	    "type" : this.getAttribute("type")
	}),
	dataType : "json",
	contentType : "application/json",
	success: function(response) {
	    console.log("AJAX Success!");
	    console.log("Response: ", response);
	    console.log(response['status']);
	    if (response['status'] == "OK") {
		var act = response['act'];
		var type = response['type'];
		var rowid = response['rowid'];
		if (act == "delete") {
		    var id = '#' + type + rowid; // e.g. story1
		    console.log(id); // Debugging
		    $(id).remove();
		}
		else if (act == "approve" || act == "promote") {
		    var id = '#' + type + act + rowid; // e.g. storyapprove1
		    var id2 = '#storyapproval' + rowid; // e.g. storyapproval1
		    // console.log(id); // Debugging
		    // console.log(id2); // Debugging
		    $(id).remove();
		    $(id2).html("1");
		}
	    } else {
		console.log("Something went wrong...");
	    }
	},
	error: function(error) {
	    console.log("AJAX Failure!");
	    console.log(error);
	}
    });	
};

// Function to Hide Tab
var clearTabDOM = function(){
    for (var i = 0; i < tabs.length; i++){
	if (tabs[i].getAttribute("href") != this.getAttribute("href")){
	    tabDOM[i].setAttribute("style", "display:none");
	}
	else{
	    tabDOM[i].setAttribute("style", "display:inline");
	}
    }
}

for (var i = 0; i < formButtons.length; i++){
    formButtons[i].addEventListener("click", submitAdminForm);
}
for (var i = 0; i < tabs.length; i++){
    tabs[i].addEventListener("click", clearTabDOM);
}
