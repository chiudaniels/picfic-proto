var artArray = null;

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
	},
	error: function(data){
	    console.log("book landing error");
	}
    });
}

$(function () {
    loadBookLanding();    
    $('#art-slideshow').slick({
	slidesToShow: 1,
	slidesToScroll: 1,
	autoplay: true,
	autoplaySpeed: 4000,
	dots: true,
	infinite: true,
	arrows: true,
    });
    console.log("Book Landing JS loaded.");
});

