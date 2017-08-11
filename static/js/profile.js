var editPersonalBtn = document.getElementById("editPersonal");
var editAbout = document.getElementById("editAbout");
var editGenre = document.getElementById("editGenre");
var editBS = document.getElementById("editBS");
var editAuthors = document.getElementById("editAuthors");
var editAccountBtn = document.getElementById("editAccount");
var editEmail = document.getElementById("editEmail");
var editGender = document.getElementById("editGender");

editPersonalBtn.addEventListener('click', function(e) {
    e.preventDefault();
    if (editGenre.isContentEditable) {
        // Disable Editing
        editPersonalBtn.innerHTML = 'Edit';
        // You could save any changes here.
        // Disable Editing
        editAbout.contentEditable = "false";
        editBS.contentEditable = "false";
        editAuthors.contentEditable = "false";
        editGenre.contentEditable = "false";

        $.ajax({
            url: "/saveProfile/",
            type: "POST",
            data: {
                "about": editAbout.innerHTML,
                "genre": editGenre.innerHTML,
                "bs": editBS.innerHTML,
                "authors": editAuthors.innerHTML
            },
            datatype: "json",
            success: function(response) {
                console.log("profile saved");
            },
            error: function(data) {
                console.log(data);
                console.log("profile error");
            }
        });

    } else {
        editAbout.contentEditable = 'true';
        editGenre.contentEditable = 'true';
        editAuthors.contentEditable = 'true';
        editBS.contentEditable = 'true';
        editAbout.focus();
        editPersonalBtn.innerHTML = 'Save';
    }
});
/*
editAccountBtn.addEventListener('click', function(e) {
    e.preventDefault();

    if (editEmail.isContentEditable) {
        // Disable Editing
        editEmail.contentEditable = 'false';
        // You could save any changes here.
        // Disable Editing
        //editEmail.contentEditable = 'false';
        editGender.contentEditable = 'false';
        editAccountBtn.innerHTML = 'Edit';

    $.ajax({
        url : "/saveAccount/",
        type: "POST",
        data: {
        "gender": editGender.innerHTML,
        },
        dataType: "json",
        success: function(response) {
        console.log("user reading bookmarked");
        },
        error: function(data) {
        console.log(data);
        }
    });

        // You could save any changes here.
    } else {
        eAM3.contentEditable = 'true';
        eAM3.focus();
        eAM2.contentEditable = 'true';
        eAM2.focus();
        eAM.contentEditable = 'true';
        eAM.focus();
        editMeBtn.innerHTML = 'Save';
    }
});

*/

//LOAD GALLERIES

var loadProfile = function() {
    $.ajax({
        url: "/getProfileImages/",
        type: "POST",
        data: {
            "username": username //I'll figure this out somehow...
        },
        success: function(response) {
            //likedArray = response["liked"];
            //uploadArray = respsonse["uploaded"];
            //setGalleries();
            //console.log("Galleries set");
        },
        error: function(data) {
            console.log("book landing error");
        }
    });

}

$(document).ready(function() {
    //loadProfile();
    $('.mystories').not('.slick-initialized').slick({
        dots: true,
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

    $('.continuereading').not('.slick-initialized').slick({
        dots: true,
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

    $('.uploaded').not('.slick-initialized').slick({
        dots: true,
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

    $('liked').not('.slick-initialized').slick({
        dots: true,
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
});