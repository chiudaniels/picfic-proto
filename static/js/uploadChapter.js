var artArray = [];
var imageArray = [];

function source2img(path) {
    var newImage = new Image();
    newImage.src = path;
    newImage.setAttribute("class", "slideImages");
    return newImage;
}

// Styling Quill Editor
var quill = new Quill('#storyArea', {
    modules : {
	toolbar : false
    }, // Add Later Once Style Parsing Is Done
    theme : 'snow',
    placeholder : "Use *** to denote a page break."
});
document.getElementById('storyArea').setAttribute("style", "font-size:14px");

// Alerts - For Upload Failure
var alerts = document.getElementById("alerts");
console.log("alerts: ", alerts);

// Form Submission
var chapterForm = document.getElementById("uploadChapterForm");
chapterForm.onsubmit = function() {
    var about = quill.getContents(); // Change to getText later
    console.log("about: ", about);

    // Populate hidden form on submit
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

// AJAX for Editing
var $chapterSelect = $('#chapterSelect');
var $chapterTitle = $('#chapterTitle');

$(function() {
    $chapterSelect.change(function (e) {
	var cID = $chapterSelect.val();
	// alert("A change has been detected!"); // Debugging
	$.ajax({
	    type : 'POST',
	    url : '/ajaxUploadChapter/',
	    data : JSON.stringify({
		'chapterid' : cID,
	    }),
	    dataType : "json",
	    contentType : "application/json",
	    success : function(response) {
		// alert("Success."); // Debugging 
		if (response['status'] == "OK") {
		    var title = response['cTitle'];
		    var text = response['cText'];
		    $chapterTitle.val(title);
		    quill.setText(text);
		}
	    },
	    error : function(error) {
		// alert("Failure."); // Debugging
		console.log(error);
	    }
	});
    });
});

/*
var oldEditor = document.getElementById('editor');
var editor = new Quill('#editor', {
    modules : { toolbar : true },
    theme : 'snow'
});
oldEditor.parentNode.replaceChild(editor, oldEditor);
*/

console.log("Uploading Chapter JS Loaded...");

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
