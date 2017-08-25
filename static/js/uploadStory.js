var $formSubmit = $('#submitStoryBtn');
var $dz = $('#coverImage');
// console.log($formSubmit, $dz); // Debugging

// Initialization of Dropzone
Dropzone.autoDiscover = false;
$(function () {
    $dz.dropzone({
	url: "/uploadStoryText/",
	addRemoveLinks: true,
	success: function (file, response) {
	    var imgName = response;
	    file.previewElement.classList.add("dz-success");
	    console.log("Successfully uploaded :" + imgName);
	},
	error: function (file, response) {
	    file.previewElement.classList.add("dz-error");
	}
    });
});

// Dropzone Config
Dropzone.options.coverImage = { 
    autoProcessQueue: false,
    uploadMultiple: false,
    parallelUploads: 1,
    maxFiles: 1,
    thumbnailWidth: 162,
    thumbnailHeight: 250,
    acceptedFiles: "image/jpeg,image/jpg,image/png,image/gif",
    
    // The setting up of the dropzone
    init: function() {
	var myDropzone = this;
	$formSubmit.click(function(e) {
	    e.preventDefault();
	    console.log(myDropzone.files);
	    myDropzone.processQueue(); // Tell Dropzone to process all queued files.
	});

	this.on("sending", function(file, xhr, formData) {
	    formData.append('title', $('#bookTitle').val());
	    formData.append('author', $('#bookAuthor').val());
	    formData.append('blurb', $('#blurbText').val());
	});
	
	this.on("success", function(files, response) {
	    alert("Successful upload!") // Debugging - Change on Final Deploy, Modal?
	    window.location = '/bookSelect/';
	});
	this.on("error", function(files, response) {
	    alert('Upload not successful!'); // Debugging - Change on Final Deploy, Modal?
	    window.location = '/uploadStory/';
	});
    }
}
// console.log("UploadStory javascript loaded."); // Debugging
