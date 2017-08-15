var formSubmit = document.getElementById("submitStoryBtn");

Dropzone.options.storyUploadDropzone = { // The camelized version of the ID of the form element
    // The configuration we've talked about above
    autoProcessQueue: false,
    uploadMultiple: false,
    parallelUploads: 1,
    maxFiles: 1,

    // The setting up of the dropzone
    init: function() {
	var myDropzone = this;
	formSubmit.setAttribute("display", "none");
	formSubmit.addEventListener("click", function() {
	    event.preventDefault();
	    event.stopPropagation();
	    myDropzone.processQueue(); // Tell Dropzone to process all queued files.
	});

	// You might want to show the submit button only when 
	// files are dropped here:
	this.on("addedfile", function() {
            // Show submit button here and/or inform user to click it.
            formSubmit.setAttribute("display", "inline");
	});

	// First change the button to actually tell Dropzone to process the queue.
	/*
	  this.element.querySelector("button[type=submit]").addEventListener("click", function(e) {
	  // Make sure that the form isn't actually being sent.
	  e.preventDefault();
	  e.stopPropagation();
	  myDropzone.processQueue();
	  });
	*/
	
	this.on("queuecomplete", function() {
	    alert('Upload successful!');
	    window.location = '/uploadChapter/0';
	});
	
	// Listen to the sendingmultiple event. In this case, it's the sendingmultiple event instead
	// of the sending event because uploadMultiple is set to true.
	this.on("sendingmultiple", function() {
	    // Gets triggered when the form is actually being sent.
	    // Hide the success button or the complete form.
	});
	this.on("successmultiple", function(files, response) {
	    // Gets triggered when the files have successfully been sent.
	    // Redirect user or notify of success.
	});
	this.on("errormultiple", function(files, response) {
	    // Gets triggered when there was an error sending the files.
	    // Maybe show form again, and notify user of error
	    alert('Upload not successful!');
	});
    }

}
