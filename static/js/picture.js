var slideIndex = 1;
showSlides(slideIndex);

function plusSlides(n) {
  showSlides(slideIndex += n);
}

function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  var i;
  var slides = document.getElementsByClassName("mySlides");
  if (n > slides.length) {slideIndex = 1} 
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
      slides[i].style.display = "none"; 
  }
  slides[slideIndex-1].style.display = "block";
}


var fileUpload = document.getElementById('fileUpload');

var makeNewSlide = function(img){
	text1= "<div class='mySlides newslides'>"
		$(document).ready(function(){
			$(".slideshow-images").append(text1);
			$(".newslides").prepend(img);
			//$(".slideshow-images").append(text2);
			// $(img).appendTo('');
			showSlides(slideIndex);
		});
	}


function readImage() {
    if ( this.files && this.files[0] ) {
        var FR= new FileReader();
        FR.onload = function(e) {
           var img = new Image();
           img.src = e.target.result;
           img.onload = function() {
             makeNewSlide(img);
           };
        };       
        FR.readAsDataURL( this.files[0] );
    }
}

fileUpload.onchange = readImage;