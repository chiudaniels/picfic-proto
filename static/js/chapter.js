var slideIndex = 0;
var thumbIndex = 0;
//var sourceArray = ["../static/img1.jpg", "../static/img2.jpg", "../static/img2.jpg", "../static/img2.jpg", "../static/img2.jpg", "../static/img2.jpg"];
//var captionArray = ["", "", "", "", "", ""];
var artArray = [];

var imageArray = [];
var imageArray2 = [];
var thumbs = document.getElementsByClassName("thumbnails");

function source2img(path) {
    var newImage = new Image();
    newImage.src = path;
    newImage.setAttribute("class", "slideImages");
    return newImage;
}

var loadArt = function() {
    for (var i = 0; i < artArray.length; i++) {
        imageArray.push(source2img(artArray[i]["urlName"]));
        imageArray2.push(source2img(artArray[i]["urlName"]));
    }
}

// slideshow //
// function plusSlides(n) {
//     showSlides(slideIndex += n);
// }

// function currentSlide(n) {
//     showSlides(slideIndex = n);
// }

// function showSlides(n) {
//     var i;
//     var slides = document.getElementsByClassName("mySlides");
//     if (n > slides.length - 1) { slideIndex = 0 }
//     if (n < 0) { slideIndex = slides.length - 1 }
//     for (i = 0; i < slides.length; i++) {
//         slides[i].style.display = "none";
//     }
//     slides[slideIndex].style.display = "block";
//     //document.getElementById("galDesc").innerHTML = captionArray[n];
//     //console.log(captionArray[n]);
// }

// var makeNewSlide = function(img) {
//     newSlide = document.createElement("div");
//     newSlide.setAttribute("class", "mySlides");
//     newSlide.appendChild(img);
//     document.getElementById("slideMaster").appendChild(newSlide);
//     showSlides(slideIndex);
// }


// for (var i = 0; i < sourceArray.length; i++) {
//     makeNewSlide(source2img(sourceArray[i]));
// }

////////////////

function setProgressBar(percent) {
    $(function() {
        $(".progress-bar").css("width", percent)
    });
}

var fileUpload = document.getElementById('fileUpload');


//thumbnail///

function makeThumbnail(img) {
    newThumb = document.createElement("div");
    img.setAttribute("class", "thumbnails")
    newThumb.appendChild(img);
    $("#gallery-thumbnail").append(newThumb);
}

/*
for (var i = 0; i < imageArray.length; i++) {
    makeThumbnail(imageArray[i]);
}
*/
function makeSlides(img) {
    newSlide = document.createElement("div");
    img.setAttribute("class", "mySlides")
    newSlide.appendChild(img);
    $("#slideMaster").append(newSlide);
}

function resetImages() {
    //remove all children
    $('#gallery-thumbnail').empty();
    $('#slideMaster').empty();
    console.log("images emptied...");
}


function setGallery() {
    resetImages();
    for (var i = 0; i < imageArray.length; i++) {
        makeThumbnail(imageArray2[i]);
        makeSlides(imageArray[i]);
        console.log("gallery debug");
        //  console.log($();
        //this better come in soon...
        //$('#gallery-thumbnail').innerHTML;
    }

    $(document).ready(function() {
        $('.slideshow-images').not('.slick-initialized').slick({
            slidesToShow: 1,
            slidesToScroll: 1,
            arrows: false,
            fade: true,
            asNavFor: '.gallery-thumbnail'
        });

        $('.gallery-thumbnail').not('.slick-initialized').slick({
            infinite: true,
            slidesToShow: 3,
            slidesToScroll: 3,
            asNavFor: '.slideshow-images',
            focusOnSelect: true
        });
    });
}







//upload functions //
var fanart = document.getElementsByClassName("fanartIcon");
var paragraph = document.getElementsByClassName("paragraph");
var picture = document.getElementsByClassName("picture");

var upload = document.getElementById("upload");

var iconClick = function(pos) {
    console.log(pos);
}

var highlightedText = "";

function clickedSomewhere() {
    $("body").mousedown(function(e) {
        var target = $(e.target);
        if (target.hasClass("upload")) {
            $("#upload-desc").text(highlightedText);
            //console.log("clicked upload");
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

if (!document.all) document.captureEvents(Event.MOUSEUP);
//////////////////

// Joel's code -- hi joel //

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

var uploadArt = function() {
    //    console.log("i'm try");
    //augmentForm();
    //document.getElementById("my-awesome-dropzone").submit(); //what a name...
}

//formSubmit.addEventListener("click", "uploadArt");

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