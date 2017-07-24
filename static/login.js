$(document).ready(function(){

  //When the user click on the login button    
  $("#submit").click(function(){

    //Get each input value in a veriable.
    var username = $("#inputUSer").val();
    var password = $("#inputPass").val();

    //Check if the username and/or the password input are empty.
    if((username == "") || (password == "")) {
      $("#message").html("<div class=\"alert alert-danger alert-dismissable\"><button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-hidden=\"true\">&times;</button>Please enter a username and a password</div>");
    }
    else {
      $.ajax({
        type: "POST",
        url: "../utils/users.py",
        data: "uN="+username+"pwd="+password,
        success: function(html){    
          if(html=='true') { //if the return value = 'true' then redirect to 'login_success.php
            window.location="/";
          }
          else { //if the return value != 'true' then add the error message to the div.#message
            $("#message").html(html);
          }
        },
        beforeSend:function()
        { //loading gif 
          $("#message").html("<p class='text-center'><img src='images/ajax-loader.gif'></p>")
        }
      });
    }
    return false;
  });
});
