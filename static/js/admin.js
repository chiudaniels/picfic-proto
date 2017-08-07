//add event listeners
var formButtons = document.getElementsByClassName("adminForm");
var tabs = document.getElementsByClassName("customTab");
var tabDOM = document.getElementsByClassName("customTabDOM");
var submitAdminForm = function(){
    $.ajax({
	    url: "/adminAction/",
	    type: "POST",
	    data: {
		"rowID": this.getAttribute("rowID"),
		"act" : this.getAttribute("act"),
		"type" : this.getAttribute("type")
	    },
	    success: function(response){
		console.log("form submitted");
	    },
	    error: function(data){
		console.log("form error");
	    }
	});	
    //some ajax
}

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
