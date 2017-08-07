//variable divs
var storyBody = document.getElementById('storyBody'); 
var progressBar = document.getElementById('progressBar'); 
var imgGallery = document.getElementById('imageGallery'); 
//interactive
var prevPgBtn = document.getElementById('prevPgBtn'); 
var nextPgBtn = document.getElementById('nextPgBtn'); 
var likes = document.getElementById('likes');

//var storyText = "";

var loadPage = function(data){
    //console.log(data);
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
    console.log("doing images");

    artArray = data["imageData"]
    for (i = 0; i < artArray.length; i++){
	console.log(artArray[i]);
	console.log("debugging");
	artArray[i]["urlName"] = '/static/data/images/' + artArray[i]["urlName"];
    }
    
    loadArt();
    
    if (artArray.length != 0)
	setGallery();
    
    //gotta reset the gallery...
    if (artArray.length == 0){
	imgGallery.setAttribute("style", "display:none");
    }
    else {
	imgGallery.setAttribute("style", "display:inline");
    }
    

    //update globals and misc
    //console.log(data["pgData"]);
    curCC = data["pgData"]["curCC"];
    
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
    
    progressBar.setAttribute("aria-valuenow", Math.ceil(100.0 * curPg / chLength));
    progressBar.setAttribute("style", "width:" + String(Math.ceil(100.0 * curPg/ chLength)) + "%");
}
/*
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
    progressBar.setAttribute("aria-valuenow", Math.ceil(100.0 * curPg / chLength));
    progressBar.setAttribute("style", "width:" + String(Math.ceil(100.0 * curPg/ chLength)) + "%");
}
*/
//for refactoring
var changePg = function(){

}

var nextPage = function(){
    //do a chapter check
    //do next page logic
    if (curPg == chLength){
	curChapter += 1;
	curCC = 0;
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
	
	//getPageData(bookID, curChapter, curPg );
	//bookmark();
    }
    return null;
}

var prevPage = function(){
    if (curPg == 1){
	curChapter -= 1;
	//get end of last chapter
	$.ajax({
	    url: "/getEndOfChPage/",
	    type: "POST",
	    data: {
		"bookID": bookID,
		"chNum": curChapter,
	    },
	    success: function(response){
		curCC = JSON.parse(response)["endOfChCC"];
		bookmark();
		window.location.href = "/books/" + bookID + "/read/" + curChapter; 		
	    }
	});	
	
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
		"curCC": curCC,
		"curPg": curPg
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
	
	//getPageData(bookID, curChapter, curPg);
	//bookmark();
    }

    return null;
}


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

//refactoring
//window.onload = function(){
 //   loadPage();
//}

console.log("alive!");
//Change it to onpageload
/*
var getPageData = function( bID, chN, pgN ){
    $.ajax({
	url: "/getPage/",
	type: "POST",
	data: {
	    "bookID": bID,
	    "chNum": chN,
	    "pgNum": pgN,
	},
	success: function(response){
	    console.log("page data gotten");
	    return response;
	},
	error: function(data){
	    console.log("page data error");
	}
    });
}
*/
var initializePage = function(){
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

initializePage();
//update galDesc
