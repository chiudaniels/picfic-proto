/*$(document).ready(function() {
    $("#sign-in-button").click(function() {
	document.getElementById("errorMess").innerHTML = "HelloWorld";
    });
});
  */  
	/*

	  $.ajax({
	  type: "POST",
	  url: '/login/',
	  username: username;
	  password: password;
	  dataType: 'json',
	  })
	  .done(function(resp){
	  if (resp == "fail"){
	  document.getElementById("errorRegion").innerHTML = "
	  <div class='alert alert-danger'>
	  <strong>Whoops!</strong> Seems like your username or password is wrong.</div>"
	  }
	  })*/
   /* });
});
 */

function myFunction(){
    console.log("HELP");
}

/*$(".scrollDown").click(function() {
    $('html, body').animate({
        scrollTop: $(".pagefivecontent").offset().top
    }, 2000);
    });*/

$(document).on('click','.scrollDown', function(event) {
    event.preventDefault();
    $('html, body').animate({
        scrollTop: $(".pagefivecontent").offset().top
    }, 2000);
});
