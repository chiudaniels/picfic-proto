var artArray = [];
var imageArray = [];

function source2img(path) {
    var newImage = new Image();
    newImage.src = path;
    newImage.setAttribute("class", "slideImages");
    return newImage;
}

/* // Gallery - Deprecated
$(document).ready(function() {
    //loadProfile();
    $('.mystories').not('.slick-initialized').slick({
        controls: true,
        infinite: false,
        speed: 300,
        slidesToShow: 4,
        slidesToScroll: 4,
        responsive: [{
            breakpoint: 1024,
            settings: {
                slidesToShow: 3,
                slidesToScroll: 3,
                infinite: true,
                dots: true
            }
        }, {
            breakpoint: 600,
            settings: {
                slidesToShow: 2,
                slidesToScroll: 2
            }
        }, {
            breakpoint: 480,
            settings: {
                slidesToShow: 1,
                slidesToScroll: 1
            }
        }]
    });
}) 
// */

// Styling Quill Editor
var quill = new Quill('#storyArea', {
    modules : {
	toolbar : false
    }, // Add Later Once Style Parsing Is Done
    theme : 'snow',
    placeholder : "Use *** to denote a page break."
});
document.getElementById('storyArea').setAttribute("style", "font-size:14px");

// Editing ChapterForm
var chapterForm = document.getElementById("uploadChapterForm");

// Alerts - For Upload Failure
var alerts = document.getElementById("alerts");
console.log("alerts: ", alerts);

chapterForm.onsubmit = function() {
    // Populate hidden form on submit
    var about = quill.getContents();
    console.log("about: ", about);

    var chapterText = document.getElementById("chapterText");
    chapterText.value = (about.ops[0]['insert']).trim();
    console.log("chapterText: ", chapterText);

    // console.log("Submitted", $(chapterForm).serialize(), $(chapterForm).serializeArray()); // Debugging
    // alert('Open the console to see the submit data!') // Debugging

    console.log(chapterText.value.length);
    if (chapterText.value.length < 10) { // Check Text
	var warning = document.createElement("div");
	warning.innerHTML = "<strong>What a short chapter!</strong> Try uploading something a little longer...";
	warning.setAttribute("class", "alert alert-warning alert-disassemble fade in");
	warning.setAttribute("style", "margin-bottom:0px");
	
	var close = document.createElement("a");
	close.innerHTML = "&times;";
	close.setAttribute("class", "close");
	close.setAttribute("data-dismiss", "alert");
	close.setAttribute("aria-label", "close");

	warning.appendChild(close);
	alerts.prepend(warning);
	alerts.scrollIntoView({
	    behavior : "smooth",
	});
	console.log(warning);
	return false; // Stop Submission
    }
};

/*
var oldEditor = document.getElementById('editor');
var editor = new Quill('#editor', {
    modules : { toolbar : true },
    theme : 'snow'
});
oldEditor.parentNode.replaceChild(editor, oldEditor);
*/

console.log("Uploading Chapter JS Loaded...");
