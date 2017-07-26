var prevPgBtn = document.getElementById('prevPgBtn'); 
var nextPgBtn = document.getElementById('nextPgBtn'); 

var curChapter;
var curPg;


var nextPage = function(){
    console.log("next page");
    //need ajax call
    bookmark();
}

var prevPage = function(){
    console.log("prev page");
    bookmark();
}


var bookmark = function(){
    
    $.ajax({
	    url : "/bookmark/",
	    type: "POST",
	    data: {""},
	    dataType: "json",
	    success: function(response) {
		console.log("user reading bookmarked");
	    },
	    error: function(data) {
		console.log(data);
	    }
	});
    return null;
}
