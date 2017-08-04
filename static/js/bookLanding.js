var loadBookLanding = function(){
    $.ajax({
	url: "/getBookLandingImages/",
	type: "POST",
	data: {
	    "bookID": bookID
	},
	success: function(response){
	    artArray = response;
	    setGallery();
	},
	error: function(data){
	    console.log("book landing error");
	}
    });
    
   
}

$(document).ready(function() {
    loadBookLanding();
});
