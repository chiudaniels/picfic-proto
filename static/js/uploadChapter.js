var artArray = [];
var imageArray = [];

function source2img(path) {
    var newImage = new Image();
    newImage.src = path;
    newImage.setAttribute("class", "slideImages");
    return newImage;
}

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

    var quill = new Quill('#storyArea', {
        modules: { toolbar: true },
        theme: 'snow'
    });
})

var form = document.querySelector('form');
form.onsubmit = function() {
  // Populate hidden form on submit
  var about = document.querySelector('input[name=about]');
  about.value = JSON.stringify(quill.getContents());
  console.log("Submitted", $(form).serialize(), $(form).serializeArray());
  
  // No back end to actually submit to!
  alert('Open the console to see the submit data!')
  return false;
};
