var slideIndex = 0;
var thumbIndex = 0;
var sourceArray = ["../static/img1.jpg", "../static/img2.jpg","../static/img2.jpg","../static/img2.jpg","../static/img2.jpg","../static/img2.jpg"];
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

    // if (sourceArray.length >= 3 && thumbIndex == sourceArray.length - 2) {
    //     $(function() {
    //         $("#thumbnail1").attr("src", sourceArray[thumbIndex - 1])
    //     })
    //     $(function() {
    //         $("#thumbnail2").attr("src", sourceArray[thumbIndex])
    //     })
    //     $(function() {
    //         $("#thumbnail3").attr("src", sourceArray[thumbIndex + 1])
    //     })
    //     console.log(4);
    // }
    // if (sourceArray.length >= 3 && thumbIndex == sourceArray.length - 1) {
    //     $(function() {
    //         $("#thumbnail1").attr("src", sourceArray[thumbIndex - 2])
    //     })
    //     $(function() {
    //         $("#thumbnail2").attr("src", sourceArray[thumbIndex - 1])
    //     })
    //     $(function() {
    //         $("#thumbnail3").attr("src", sourceArray[thumbIndex])
    //     })
    //     console.log(5);
    // }
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
clickedThumbArrow()

// function readImage() {
//     if ( this.files && this.files[0] ) {
//         var FR= new FileReader();
//         FR.onload = function(e) {
//            var img = new Image();
//            img.src = e.target.result;
//            img.onload = function() {
//              makeNewSlide(img);
//            };
//         };       
//         FR.readAsDataURL( this.files[0] );
//     }
// }

// fileUpload.onchange = readImage;


var fanart = document.getElementsByClassName("fanartIcon")
var paragraph = document.getElementsByClassName("paragraph")
var picture = document.getElementsByClassName("picture")


var iconClick = function(pos) {
    console.log(pos);
}

var t = '';

function clickedSomewhere() {
    $("body").mousedown(function(e) {
        var target = $(e.target);
        if (target.hasClass("upload")) {
            $("#upload-desc").text(t);
        } else {
            clearHighlight();
        }
    });
}

function highlight(e) {
    t = (document.all) ? document.selection.createRange().text : document.getSelection();
    if (t != '') {
        console.log("highlight worked")
        document.getElementById("upload").style.display = "inline";
        document.getElementById("upload").style.top = event.pageY - 100 + 'px';
    }
}

function clearHighlight() {
    document.getElementById("upload").style.display = "none";
    console.log(document.getElementById("upload").style.display);
}


function wait(e){
  setTimeout(highlight(e),100);
}


function clickUpload() {
    $(function() {
        $("#upload").click(function() {

        })
    });
}

document.onmousedown = clickedSomewhere;
document.onmouseup = highlight;

if (!document.all) document.captureEvents(Event.MOUSEUP);


$(document).ready(function(){
    $("#editMe").on("click", function(){
        $("#editAboutMe").attr("contenteditable","true").focus();
    });
});
