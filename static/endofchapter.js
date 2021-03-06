var slideIndex = 0;
var thumbNum = 0;
var sourceArray = [];
var imageArray = [];
var numRows = Math.ceil(sourceArray.length / 5);

function source2img(path) {
    var newImage = new Image();
    newImage.src = path;
    return newImage;
}


////slide ////

function plusSlides(n) {
    showSlides(slideIndex += n);
    thumbIndex = slideIndex;
}

function currentSlide(n) {
    showSlides(slideIndex = n);
}

function showSlides(n) {
    var i;
    var slides = document.getElementsByClassName("mySlides");
    if (n > slides.length-1) { slideIndex = 0 }
    if (n < 0) { slideIndex = slides.length - 1 }
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    slides[slideIndex].style.display = "block";
}

var makeNewSlide = function(img) {
    newSlide = document.createElement("div");
    newSlide.setAttribute("class", "mySlides");
    img.setAttribute("class","displayImage");
    newSlide.appendChild(img);
    document.getElementById("slideMaster").appendChild(newSlide);
    showSlides(slideIndex);
}

////

//thumbnails//
function makeThumbsCol() {
    newRow = document.createElement("div");
    newRow.setAttribute("class", "row");
    for (var i = 0; i < 5; i++) {
        if (thumbNum < imageArray.length) {
            newThumb = document.createElement("div");
            newThumb.setAttribute("class", "col-md-5ths");
            img = imageArray[thumbNum];
            img.setAttribute("count", thumbNum);
            img.setAttribute("class", "thumbnails");
            newThumb.appendChild(img);
            console.log(newThumb);
            newRow.appendChild(newThumb);
            console.log("made thumbnail")
        }
        thumbNum++;
    }
    console.log("made row")
    $(".gallery-thumbnail").append(newRow);
}
///

setGalleryDesc(text){
	$(".gallery-desc").text=text;
}

setGalleryLikes(num){
	$(".gallery-desc").text=num + " likes";
}

for (var i = 0; i < sourceArray.length; i++) {
    imageArray.push(source2img(sourceArray[i]));
}

console.log(numRows);

for (var i = 0; i < numRows; i++) {
    makeThumbsCol();
}

for (var i = 0; i < sourceArray.length; i++) {
    makeNewSlide(source2img(sourceArray[i]));
}

$(function(){
	$(".thumbnails").click(function(e){
		var target= $(e.target);
		slideIndex= parseInt(target.attr("count"));
		showSlides(slideIndex);
	});
});