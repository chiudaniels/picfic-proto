var slideIndex = 0;
var thumbIndex = 0;
var uploadArray = ["../static/img1.jpg", "../static/img2.jpg","../static/img2.jpg","../static/img2.jpg","../static/img2.jpg","../static/img2.jpg"];
var likedArray = ["../static/img1.jpg", "../static/img2.jpg","../static/img2.jpg","../static/img2.jpg","../static/img2.jpg","../static/img2.jpg"];
var thumbs = document.getElementsByClassName("thumbnails");

var editMeBtn = document.getElementById('editMe');
var eAM = document.getElementById('editAboutMe');
var editAccountBtn = document.getElementById('editAccount');
var eMA = document.getElementById('editMyAccount');
var editBtn = document.getElementById('editMe');
var element = document.getElementById('editAboutMe');

editAccountBtn.addEventListener('click', function(e) {
    e.preventDefault();

    if (eMA.isContentEditable) {
	// Disable Editing
	eMA.contentEditable = 'false';
	editAccountBtn.innerHTML = 'Edit';
	// You could save any changes here.
    } else {
	eMA.contentEditable = 'true';
	eMA.focus();
	editAccountBtn.innerHTML = 'Save changes';
    }
});

editMeBtn.addEventListener('click', function(e) {
    e.preventDefault();

    if (eAM.isContentEditable) {
	// Disable Editing
	eAM.contentEditable = 'false';
	editMeBtn.innerHTML = 'Edit';
	// You could save any changes here.
    } else {
	eAM.contentEditable = 'true';
	eAM.focus();
	editMeBtn.innerHTML = 'Save changes';
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

for(var i=0; i<uploadArray.length;i++){
    makeUploads(source2img(uploadArray[i]));
}

for(var i=0; i<likedArray.length;i++){
    makeLiked(source2img(likedArray[i]));
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

