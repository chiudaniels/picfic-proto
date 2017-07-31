//variable divs
var storyBody = document.getElementById('storyBody'); 
var markerTracker = document.getElementById('markerTracker');
var imgGallery = document.getElementById('imageGallery'); 
//interactive
var prevPgBtn = document.getElementById('prevPgBtn'); 
var nextPgBtn = document.getElementById('nextPgBtn'); 

var loadPage = function(data){
//    console.log(data);
    data = JSON.parse(data);
    //update body
    while (storyBody.hasChildNodes()){
	storyBody.removeChild(storyBody.lastChild);
    }
    console.log(data);
    var i;
    
    for (i = 0; i < data["pgData"]["text"].length; i++){
	var p = document.createElement("p");
	p.setAttribute("class", "paragraph");
	p.innerHTML = data["pgData"]["text"][i];
	storyBody.appendChild(p);
    }
    
    //update images
    for (i = 0; i < data["imageData"].length; i++){
	var img = document.createElement("img");
	img.setAttribute("src", "../../../../static/" + data["imageData"][i]["url"]);
	storyBody.appendChild(img);
    }
    

    //update globals and misc
    console.log(data["pgData"])
    curCC = data["pgData"]["curCC"]
    
    if (data["chNum"] == data["bookLength"] && data["pgData"]["pgNum"] == data["pgData"]["chLength"]){
	nextPgBtn.setAttribute("style", "visibility:hidden");
    }
    else {
	nextPgBtn.setAttribute("style", "visibility:visible");
    }
    if (data["chNum"] == 1 && data["pgData"]["pgNum"] == 1){
	prevPgBtn.setAttribute("style", "visibility:hidden");
    }
    else {
	prevPgBtn.setAttribute("style", "visibility:visible");
    }

    if (markerTracker)
	markerTracker.setAttribute("value", data["markerData"]["markerID"]);
    
}

var initializeButtons = function(){
    if (curChapter == bookLength && curPg == chLength){
	nextPgBtn.setAttribute("style", "visibility:hidden");
    }
    else {
	nextPgBtn.setAttribute("style", "visibility:visible");
    }
    if (curChapter == 1 && curPg == 1){
	prevPgBtn.setAttribute("style", "visibility:hidden");
    }
    else {
	prevPgBtn.setAttribute("style", "visibility:visible");
    }
}

//for refactoring
var changePg = function(){

}

var nextPage = function(){
    //do a chapter check
    //do next page logic
    if (curPg == chLength){
	curChapter += 1;
	console.log(curChapter);
	window.location.href = "/books/" + bookID + "/read/" + curChapter; 
	bookmark();
    }
    else {
	curPg += 1;
	//need ajax call
	$.ajax({
	    url: "/getPage/",
	    type: "POST",
	    data: {
		"bookID": bookID,
		"chNum": curChapter,
		"pgNum": curPg
	    },
	    success: function(response){
		console.log("next paged");
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

var prevPage = function(){
    if (curPg == 1){
	curChapter -= 1;
	window.location.href = "/books/" + bookID + "/read/" + curChapter; 
	bookmark();
    }
    else{
	curPg -= 1;
	//need ajax call
	$.ajax({
	    url: "/getPage/",
	    type: "POST",
	    data: {
		"bookID": bookID,
		"chNum": curChapter,
		"pgNum": curPg,
		"ccStart": curCC
	    },
	    success: function(response){
		console.log("next paged");
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


var bookmark = function(){
    
    $.ajax({
	url : "/bookmark/",
	type: "POST",
	data: {
	    "chNum": curChapter,
	    "pgNum": curPg,
	    "ccStart": curCC,
	    "bookID": bookID
	},
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


prevPgBtn.addEventListener("click", prevPage);
nextPgBtn.addEventListener("click", nextPage);

initializeButtons();




console.log("alive!");
//Change it to onpageload
