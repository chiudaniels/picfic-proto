$(document).ready(function() {
    $("#sign-in-button").click(function() {
	$.ajax({
	    type: "POST",
	    url: '/login/',
	    username: username;
	    password: password;
	    dataType: 'json',
	})
	    .done(function(resp){
		if resp == 
	    }
	return false;
    });
});
