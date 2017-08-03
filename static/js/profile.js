var slideIndex = 0;
var thumbIndex = 0;
var uploadArray = ["../static/img1.jpg", "../static/img2.jpg","../static/img2.jpg","../static/img2.jpg","../static/img2.jpg","../static/img2.jpg"];
var likedArray = ["../static/img1.jpg", "../static/img2.jpg","../static/img2.jpg","../static/img2.jpg","../static/img2.jpg","../static/img2.jpg"];
var thumbs = document.getElementsByClassName("thumbnails");

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

    