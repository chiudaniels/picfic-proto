//variable divs
var storyBody = document.getElementById('storyBody'); 
var progressBar = document.getElementById('progressBar'); 
var imgGallery = document.getElementById('imageGallery'); 
var $artGallery = $('#artGallery');

//interactive
var prevPgBtn = document.getElementById('prevPgBtn'); 
var nextPgBtn = document.getElementById('nextPgBtn'); 
var likes = document.getElementById('likes');

var pageMetaData = null;

var loadPage = function(data) {
    // Remove Text From Story 
    while (storyBody.hasChildNodes()){
	storyBody.removeChild(storyBody.lastChild);
    }
    artArray = [] // Clear Art
    data = JSON.parse(data);
    pageMetaData = data;
    // console.log(data); // Debugging
    artArray = data["imageData"]
    console.log("ARTARRAY ================\n", artArray);
    if (artArray.length != 0) {
	$artGallery.css("display", "block");
	setGallery();
    } else {
	$artGallery.css("display", "none");
    }
    if ("pgNum" in data) {
	if (data["chapterNum"] == data["bookLength"]) {
	    nextPgBtn.setAttribute("style", "visibility:hidden");
	}
	prevPgBtn.setAttribute("style", "visibility:visible");
    }
    else {
	console.log("loadPage thinks this a normal page");
	console.log(data); // Debugging

	// Repopulate Story
	var i;
	for (i = 0; i < data["pgData"]["text"].length; i++){
	    var p = document.createElement("p");
	    p.setAttribute("class", "paragraph");
	    p.innerHTML = data["pgData"]["text"][i];
	    storyBody.appendChild(p);
	}
	
	//update images
	console.log("doing images");
	
	// Updating Globals
	curCC = data["pgData"]["curCC"];
	nextPgBtn.setAttribute("style", "visibility:visible");
	if (data["chNum"] == 1 && data["pgData"]["pgNum"] == 1) {
	    prevPgBtn.setAttribute("style", "visibility:hidden");
	}
	else {
	    prevPgBtn.setAttribute("style", "visibility:visible");
	}
	progressBar.setAttribute("aria-valuenow", Math.ceil(100.0 * curPg / chLength));
	progressBar.setAttribute("style", "width:" + String(Math.ceil(100.0 * curPg/ chLength)) + "%");
    }
}

//for refactoring
var changePg = function() {
}

var nextPage = function() {
    // Check to make sure there's a page to go forward to
    data = pageMetaData;
    if (data["chapterNum"] == data["bookLength"]) {
	return; // Terminate
    }
    // There are pages
    if (curPg == -1) { // On Gallery Page
	curChapter += 1;
	curCC = 0;
	window.location.href = "/books/" + bookID + "/read/" + curChapter;
	bookmark();
    }
    if (curPg == chLength) { // Page Before Gallery - Go To Gallery
	curPg = -1;
	curCC = -1;
	console.log("next page to the gallery");
	$.ajax({
	    url: "/chapterGallery/",
	    type: "POST",
	    data: {
		"bookID": bookID,
		"chNum": curChapter
	    },
	    success: function(response) {
		loadPage(response);
		bookmark();
	    },
	    error: function(data) {
		console.log("gallery loading error: ", data);
	    }
	});
    }
    else {
	curPg += 1;
	$.ajax({
	    url: "/getPage/",
	    type: "POST",
	    data: {
		"bookID": bookID,
		"chNum": curChapter,
		"curCC": curCC,
		"curPg": curPg
	    },
	    success: function(response){
		loadPage(response);
		bookmark();
	    },
	    error: function(data){
		console.log("nextpage error");
	    }
	});
    }
    return null;
}

// Previous Page Function
var prevPage = function(){
    // Check to make sure there's a page to go back to
    data = pageMetaData;
    if (data["chNum"] == 1 && data["pgData"]["pgNum"] == 1) {
	return; // Terminate
    }
    // There are pages
    if (curPg == 1) {
	curPg = -1;
	curChapter -= 1;
	curCC = -1;
	bookmark();
	window.location.href = "/books/" + bookID + "/read/" + curChapter;
    }
    else if (curPg == -1) { // End of Chapter
	$.ajax({
	    url: "/getEndOfChPage/",
	    type: "POST",
	    data: {
		"bookID": bookID,
		"chNum": curChapter,
	    },
	    success: function(response) {
		console.log("prevPage debug");
		curPg = JSON.parse(response)["chLength"];
		curCC = JSON.parse(response)["endOfChCC"];
		console.log(curPg);
		console.log(curCC);
		initializePage();
		//loadPage(response);
		bookmark();
	    },
	    error: function(data) {
		console.log("end of chapter error: ", data);
	    }
	});	
    }
    else {
	curPg -= 1;
	$.ajax({
	    url: "/getPage/",
	    type: "POST",
	    data: {
		"bookID": bookID,
		"chNum": curChapter,
		"curCC": curCC,
		"curPg": curPg
	    },
	    success: function(response) {
		loadPage(response);
		bookmark();
	    },
	    error: function(data) {
		console.log("prevpage error: ", data);
	    }
	});
	//getPageData(bookID, curChapter, curPg);
	//bookmark();
    }
    return null;
}

// Bookmarking Function
var bookmark = function(){
    $.ajax({
	url : "/bookmark/",
	type: "POST",
	data: {
	    "chNum": curChapter,
	    "ccStart": curCC,
	    "bookID": bookID
	},
	dataType: "json",
	success: function(response) {
	    if (response['status'] == 1) {
		console.log("user reading bookmarked");
	    };
	},
	error: function(data) {
	    console.log(data);
	}
    });
    return null;
}

/* Must Turn ASync Off 
// Helper - Username From UserID
var getUsername = function(userID) {
    var author = "";
    author = 
	$.ajax({
	    url : "/getUsername/",
	    type: "POST",
	    data: JSON.stringify({
		"uID" : userID
	    }),
	    dataType: "json",
	    contentType: "application/json",
	    success: function(response) {
		if (response['status'] == "OK") {
		    console.log("username retrieved: ", response['username']);
		    return response['username'];
		}
	    },
	    error: function(data) {
		console.log(data);
	    }
	});
    return author;
}
*/

// Initializing Page
prevPgBtn.addEventListener("click", prevPage);
nextPgBtn.addEventListener("click", nextPage);
var initializePage = function(){
    if (curCC != -1){
	$.ajax({
	    url: "/getPage/",
	    type: "POST",
	    data: {
		"bookID": bookID,
		"chNum": curChapter,
		"curCC": curCC,
		"curPg": curPg
	    },
	    success: function(response){
		console.log("page data gotten");
		loadPage(response);	
	    },
	    error: function(data){
		console.log("page data error");
	    }
	});
    }
    else{
	console.log("prev page/loading to the gallery");
	$.ajax({
	    url: "/chapterGallery/",
	    type: "POST",
	    data: {
		"bookID": bookID,
		"chNum": curChapter
	    },
	    success: function(response){
		loadPage(response);
		bookmark();
	    },
	    error: function(data){
		console.log("nextpage error");
	    }
	});
    }
}

$(document).ready(initializePage());
//update galDesc
