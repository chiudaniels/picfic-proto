$car = $('#headerCarousel');
$gal = $('#bookgallery');

$car.not('.slick-initialized').slick({
    slidesToShow: 1,
    slidesToScroll: 1,
    autoplay: true,
    autoplaySpeed: 2500,
    dots: false,
    infinite: true,
    fade: true,
    arrows: false
});

$('#bookgallery').not('.slick-initialized').slick({
    dots: true,
    arrows: false,
    autoplay: true,
    autoplaySpeed: 5000,
    infinite: true,
    pauseOnDotsHover: true,
    speed: 300,
    slidesToShow: 4,
    slidesToScroll: 4,
    responsive: [{
        breakpoint: 1024,
        settings: {
            slidesToShow: 3,
            slidesToScroll: 3,
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

$('#about').click(function (e) {
    event.preventDefault();
    $('html, body').animate({
	scrollTop: $( $.attr(this, 'href') ).offset().top
    }, 1000);
});

console.log("Launchpad JS loaded.");
