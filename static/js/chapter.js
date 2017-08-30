// Variable Declaration
var artArray = [];
var imageArray = []; // Art

// var imageArray2 = []; // Thumbnails
var fileUpload = document.getElementById('fileUpload');
var thumbs = document.getElementsByClassName("thumbnails");

var loadArt = function() {
    imageArray = [] // Clear Array
    for (var i = 0; i < artArray.length; i++) {
	console.log("ArtArray Index: ", artArray[i]); // Debugging
	artPiece = {}
	artPiece['url'] = '/static/data/images/' + artArray[i]["urlName"];
	artPiece['author'] = artArray[i]['username'];
	artPiece['caption'] = artArray[i]['caption'];
	imageArray.push(artPiece);
    }
    console.log("ImageArray: ", imageArray); // Debugging
}

// Not Implemented
var setLikes = function(x) {
    $('#likes').text(x);
}
var setDesc = function(x) {
    $('#galDesc').text(x);
}
var setUploader = function(x) {
    $('#uploader').text(x);
}
var setDate = function(x) {
    $('#dateUploaded').text(x);
}

function setProgressBar(percent) {
    $(function() {
        $(".progress-bar").css("width", percent)
    });
}

// Gallery
var $artSlides = $('#art-slideshow');

var resetImages = function() {
    // Remove All
    $artSlides.empty();
    console.log("images emptied...");
}
var addImage = function(i) {
    var $newImage = $('<div/>')
	.addClass("artPiece text-center")
	.append(
	    $('<div/>').append(
		$("<img>")
		    .addClass("art")
		    .attr("src", imageArray[i]['url'])
		    .css("margin", "auto")
	    )
	)
	.append($('<br/>'))
	.append(
	    $('<div/>')
		.text("By: " + imageArray[i]['author'])
		.css("font-weight", "bold")
	)
	.append($('<br/>'))
	.append(
	    $('<div/>').text(imageArray[i]['caption'])
	)
    $artSlides.append($newImage);
    console.log("New image added!", $newImage);
}

var galleryLoaded = false;
function setGallery() {
    $(document).ready(function() {
	loadArt();
	if (!galleryLoaded) {
	    for (var i = 0; i < imageArray.length; i++) {
		console.log(imageArray[i]); // Debugging
		addImage(i); // Actual Art
	    }
	    slickGallery();
	    galleryLoaded = true;
	    console.log("Gallery has been loaded.");
	} else {
	    console.log("Gallery is already loaded!");
	    $artSlides.slick('unslick');
	    resetImages();
	    for (var i = 0; i < imageArray.length; i++) {
		console.log(imageArray[i]); // Debugging
		addImage(i); // Actual Art
	    }
	    slickGallery();
	}
    });
}
function slickGallery() {    
    $artSlides.slick({
	slidesToShow: 1,
	slidesToScroll: 1,
	autoplay: true,
	autoplaySpeed: 4000,
	dots: true,
	infinite: true,
	arrows: true
    });
}


// Uploading Art // 
var fanart = document.getElementsByClassName("fanartIcon");
var paragraph = document.getElementsByClassName("paragraph");
var picture = document.getElementsByClassName("picture");
var upload = document.getElementById("upload");
var highlightedText = "";
var iconClick = function(pos) {
    console.log(pos);
}

function clickedSomewhere() {
    $("body").mousedown(function(e) {
        var target = $(e.target);
        if (target.hasClass("upload")) {
            $("#upload-desc").text(highlightedText);
            // console.log("clicked upload");
            augmentForm();
        } else {
            clearHighlight();
            // console.log("clicked not upload")
        }
    });
}

function highlight(e) {
    storyEle = $("#storyBody")
    offset = storyEle.offset();
    story = document.getElementById("storyBody").getBoundingClientRect();
    bottom = offset.top + storyEle.height();
    //highlightedText = (document.all) ? document.selection.createRange().text : document.getSelection();
    if (window.getSelection) {
        highlightedText = window.getSelection().toString();
    } else if (document.selection && document.selection.type == "Text") {
        highlightedText = document.selection.createRange().text;
    }
    // if (window.getSelection) {
    //    text = window.getSelection().toString();
    if (highlightedText != '') {
        if (event.pageY > bottom) {
            console.log(1)
            upload.style.display = "inline";
            upload.style.top = bottom;
            // upload.style.bottom = bottom 'px';
        } else if (event.pageY < story.top) {
            console.log(2)
            upload.style.display = "inline";
            upload.style.bottom = 0;
            upload.style.top = story.top - 100 + 'px';
        } else {
            console.log(3)
            //console.log("highlight worked")
            upload.style.display = "inline";
            upload.style.bottom = 0;
            upload.style.top = event.pageY - 100 + 'px';
        }
    }
}
function clearHighlight() {
    upload.style.display = "none";
    //console.log(upload.style.display);
}
function wait(e) {
    setTimeout(highlight(e), 100);
}

document.onmousedown = clickedSomewhere;
document.onmouseup = highlight;
if (!document.all) {
    document.captureEvents(Event.MOUSEUP);
}

// Joel's Code //
var formBookID = document.getElementById("artUploadBookID");
var formCaption = document.getElementById("artUploadCaption");
var formStartCC = document.getElementById("artUploadStartCC");
var formEndCC = document.getElementById("artUploadEndCC");
var formChNum = document.getElementById("artUploadChapterNum");
var formSubmit = document.getElementById("artUploadSubmit");

var augmentForm = function() {
    formBookID.setAttribute("value", bookID);
    formCaption.setAttribute("value", highlightedText);
    //console.log(highlightedText.indexOf("\n"));
    //console.log(highlightedText);
    //console.log(storyBody.innerHTML);
    //scrape text
    var i;
    var bodyText = "";
    for (i = 0; i < storyBody.childNodes.length; i++) {
        if (storyBody.childNodes[i].innerHTML) {
            bodyText += storyBody.childNodes[i].innerHTML;
            bodyText += "\n\n";
        }
    }
    //console.log(bodyText);
    highlightedText = $.trim(highlightedText);
    var index = bodyText.indexOf(highlightedText);
    //modify...
    g = "\n\n";
    formStartCC.setAttribute("value", curCC + index); //figure this out
    formEndCC.setAttribute("value", curCC + index + highlightedText.length - (highlightedText.match(/is/g) || []).length);
    //console.log(ccEnd);
    formChNum.setAttribute("value", curChapter);
}

// Dropzone Code 
Dropzone.options.artDrop = {
    // Prevents Dropzone from uploading dropped files immediately
    autoProcessQueue: false,
    acceptedFiles: ".png,.jpg,.gif,.bmp,.jpeg",
    maxFilesize: 1,
    parallelUploads: 10,
    addRemoveLinks: true,

    init: function() {
        myDropzone = this; // closure
        formSubmit.setAttribute("display", "none");
        formSubmit.addEventListener("click", function() {
            myDropzone.processQueue(); // Tell Dropzone to process all queued files.
        });

        // You might want to show the submit button only when 
        // files are dropped here:
        this.on("addedfile", function() {
            formSubmit.setAttribute("display", "inline");
            // Show submit button here and/or inform user to click it.
        });

    }
};
