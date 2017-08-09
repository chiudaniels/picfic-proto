var loadBookLanding = function(){
    $.ajax({
	url: "/getBookLandingImages/",
	type: "POST",
	data: {
	    "bookID": bookID
	},
	success: function(response){
	    artArray = response;
	    console.log(artArray);
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
