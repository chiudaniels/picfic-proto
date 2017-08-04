var slideIndex = 0;
var thumbIndex = 0;
var uploadArray = ["../static/img1.jpg", "../static/img2.jpg", "../static/img2.jpg", "../static/img2.jpg", "../static/img2.jpg", "../static/img2.jpg"];
var likedArray = ["../static/img1.jpg", "../static/img2.jpg", "../static/img2.jpg", "../static/img2.jpg", "../static/img2.jpg", "../static/img2.jpg"];
var thumbs = document.getElementsByClassName("thumbnails");

var editMeBtn = document.getElementById('editMe');
var eAM = document.getElementById('editAboutMe');
var eAM2 = document.getElementById('editAboutMe2');
var eAM3 = document.getElementById('editAboutMe3');
var editAccountBtn = document.getElementById('editAccount');
var eMA = document.getElementById('editMyAccount');
var eMA2 = document.getElementById('editMyAccount2');
var eMA3 = document.getElementById('editMyAccount3');


editAccountBtn.addEventListener('click', function(e) {
    e.preventDefault();

    if (eMA.isContentEditable) {
        // Disable Editing
        eMA.contentEditable = 'false';
        editAccountBtn.innerHTML = 'Edit';
        // You could save any changes here.
	// Disable Editing
	eMA.contentEditable = 'false';
	eMA2.contentEditable = 'false';
	eMA3.contentEditable = 'false';
	editAccountBtn.innerHTML = 'Edit';
	// You could save any changes here.
    } else {
        eMA3.contentEditable = 'true';
        eMA3.focus();
        eMA2.contentEditable = 'true';
        eMA2.focus();
        eMA.contentEditable = 'true';
        eMA.focus();
        editAccountBtn.innerHTML = 'Save';
    }
});

editMeBtn.addEventListener('click', function(e) {
    e.preventDefault();

    if (eAM.isContentEditable) {
        // Disable Editing
        eAM.contentEditable = 'false';
        editMeBtn.innerHTML = 'Edit';
        // You could save any changes here.
	// Disable Editing
	eAM.contentEditable = 'false';
	eAM2.contentEditable = 'false';
	eAM3.contentEditable = 'false';
	editMeBtn.innerHTML = 'Edit';
	// You could save any changes here.
    } else {
        eAM3.contentEditable = 'true';
        eAM3.focus();
        eAM2.contentEditable = 'true';
        eAM2.focus();
        eAM.contentEditable = 'true';
        eAM.focus();
        editMeBtn.innerHTML = 'Save';
    }
});



function source2img(path) {
    var newImage = new Image();
    newImage.src = path;
    return newImage;
}

function makeUploads(img) {
    newSlide = document.createElement("div");
    img.setAttribute("class", "slides")
    newSlide.appendChild(img);
    $(".uploaded").append(newSlide);
}

function makeLiked(img) {
    newSlide = document.createElement("div");
    img.setAttribute("class", "slides")
    newSlide.appendChild(img);
    $(".liked").append(newSlide);
}

function setGalleries() {
    for (var i = 0; i < uploadArray.length; i++) {
        makeUploads(source2img(uploadArray[i]));
    }
     for (var i = 0; i < likedArray.length; i++) {
        makeLiked(source2img(likedArray[i]));
    }
}

$(document).ready(function() {
    $('.uploaded').slick({
        infinite: true,
        slidesToShow: 4,
        slidesToScroll: 1,
        focusOnSelect: true
    });
});


$(document).ready(function() {
    $('.liked').slick({
        infinite: true,
        slidesToShow: 4,
        slidesToScroll: 1,
        focusOnSelect: true
    });
});

if (!document.all) document.captureEvents(Event.MOUSEUP);

//LOAD GALLERIES

var loadProfile = function(){
    $.ajax({
	url: "/getProfileImages/",
	type: "POST",
	data: {
	    "username": username //I'll figure this out somehow...
	},
	success: function(response){
	    likedArray = response["liked"];
	    uploadArray = respsonse["uploaded"];
	    setGalleries();
	    console.log("Galleries set");
	},
	error: function(data){
	    console.log("book landing error");
	}
    });
    
   
}

$(document).ready(function() {
    loadProfile();
});
