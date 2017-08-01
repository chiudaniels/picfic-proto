var slideIndex = 0;
var thumbIndex = 0;
var sourceArray = ["/static/img1.jpg", "/static/img2.jpg","/static/img2.jpg","/static/img2.jpg","/static/img2.jpg","/static/img2.jpg"];
var thumbs = document.getElementsByClassName("thumbnails");

function source2img(path) {
    var newImage = new Image();
    newImage.src = path;
    newImage.setAttribute("class","slideImages");
    return newImage;
}

function plusSlides(n) {
    showSlides(slideIndex += n);
    thumbIndex = slideIndex;
    setThumbnails();
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
    newSlide.appendChild(img);
    document.getElementById("slideMaster").appendChild(newSlide);
    showSlides(slideIndex);
    //console.log(document.getElementById.childNodes);
    /*
    $(document).ready(function() {
        $(".slideshow-images").append(newSlide)
        //$(".slideshow-images").append(text2);
        // $(img).appendTo('');
        showSlides(slideIndex);
    });
    */
    //console.log("slide made");
    //console.log(document.getElementsByClassName("mySlides"));
}

function setThumbnails() {
    if (sourceArray.length == 1) {
        $(function() {
            $("#thumbnail1").attr("src", sourceArray[thumbIndex])
        })
    }
    if (sourceArray.length == 2) {
        $(function() {
            $("#thumbnail1").attr("src", sourceArray[thumbIndex])
        })
        $(function() {
            $("#thumbnail2").attr("src", sourceArray[thumbIndex + 1])
        })
    }
    if (sourceArray.length >= 3 && thumbIndex <= sourceArray.length - 3) {
        $(function() {
            $("#thumbnail1").attr("src", sourceArray[thumbIndex])
        })
        $(function() {
            $("#thumbnail2").attr("src", sourceArray[thumbIndex + 1])
        })
        $(function() {
            $("#thumbnail3").attr("src", sourceArray[thumbIndex + 2])
        })
    }

    $(function() {
        $("#thumbnail1").attr("thumbCount", thumbIndex)
    })
    $(function() {
        $("#thumbnail2").attr("thumbCount", thumbIndex + 1)
    })
    $(function() {
        $("#thumbnail3").attr("thumbCount", thumbIndex + 2)
    })
};

function clickedThumbArrow() {
    $(document).ready(function() {
        $(".gallery-prev").click(function() {
            if (thumbIndex != 0 && sourceArray.length > 3) {
                thumbIndex--;
                setThumbnails();
            }
        })
        $(".gallery-next").click(function() {
            if (thumbIndex != sourceArray.length - 3 && sourceArray.length > 3) {
                thumbIndex++;
                setThumbnails()
            }
        })
    });
}

function setProgressBar(percent){
    $(function(){
        $(".progress-bar").css("width",percent)
    });
}

var fileUpload = document.getElementById('fileUpload');


var thumbnailClick = function() {
    $(function() {
        $("#thumbnail1").click(function() {
            slideIndex = parseInt($("#thumbnail1").attr("thumbCount"));
            console.log(slideIndex);
            showSlides(slideIndex);
        })
    });
    $(function() {
        $("#thumbnail2").click(function() {
            slideIndex = parseInt($("#thumbnail2").attr("thumbCount"));
            console.log(slideIndex);
            showSlides(slideIndex);
        })
    });
    $(function() {
        $("#thumbnail3").click(function() {
            slideIndex = parseInt($("#thumbnail3").attr("thumbCount"));
            console.log(slideIndex);
            showSlides(slideIndex);

        })
    });

}



for (var i = 0; i < sourceArray.length; i++) {
    makeNewSlide(source2img(sourceArray[i]));
}


//showSlides(slideIndex);
setThumbnails();
thumbnailClick();
clickedThumbArrow();

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
	    console.log("clicked upload");
	    augmentForm();
        } else {
            clearHighlight();
	    console.log("clicked not upload")
        }
    });
}

function highlight(e) {
    //highlightedText = (document.all) ? document.selection.createRange().text : document.getSelection();
    if (window.getSelection) {
        highlightedText = window.getSelection().toString();
    } else if (document.selection && document.selection.type == "Text") {
        highlightedText = document.selection.createRange().text;
    }
    // if (window.getSelection) {
    //    text = window.getSelection().toString();
    if (highlightedText != '') {
        console.log("highlight worked")
        upload.style.display = "inline";
        upload.style.top = event.pageY - 100 + 'px';
    }
}

function clearHighlight() {
    upload.style.display = "none";
    console.log(upload.style.display);
}


function wait(e){
  setTimeout(highlight(e),100);
}


document.onmousedown = clickedSomewhere;
document.onmouseup = highlight;

if (!document.all) document.captureEvents(Event.MOUSEUP);


// Joel's code

var formBookID = document.getElementById("artUploadBookID");
var formCaption = document.getElementById("artUploadCaption");
var formStartCC = document.getElementById("artUploadStartCC");
var formEndCC = document.getElementById("artUploadEndCC");
var formChNum = document.getElementById("artUploadChapterNum");
var formSubmit = document.getElementById("artUploadSubmit");

var augmentForm = function(){
    
    formBookID.setAttribute("value", bookID);
    formCaption.setAttribute("value", highlightedText);
    //console.log(highlightedText.indexOf("\n"));
    //console.log(highlightedText);
    //console.log(storyBody.innerHTML);
    //scrape text
    var i;
    var bodyText = "";
    for (i = 0; i < storyBody.childNodes.length; i++){
	if (storyBody.childNodes[i].innerHTML){
	    bodyText += storyBody.childNodes[i].innerHTML;
	    bodyText += "\n\n";
	}
    }

    //console.log(bodyText);
    var index = bodyText.indexOf(highlightedText);
    console.log(highlightedText.indexOf("\n"));
    console.log(index);
    console.log(JSON.stringify(highlightedText));
    console.log(JSON.stringify(bodyText));
    console.log("That's the index");
    formStartCC.setAttribute("value", curCC + index); //figure this out
    formEndCC.setAttribute("value", curCC + index + highlightedText.length); //doesn't include end index
    console.log(curCC);
    console.log(curCC + index);
    console.log(curCC + index + highlightedText.length);
    //console.log(ccEnd);
    formChNum.setAttribute("value", curChapter);
}

var uploadArt = function(){
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
