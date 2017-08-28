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
    infinite: false,
    arrows: false,
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

console.log("Carousel JS loaded.");
