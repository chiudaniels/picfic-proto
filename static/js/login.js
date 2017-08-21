var $signin = $('#signInButton');
var $signinForm = $('#signInForm');
var $failMsg = $('#loginFail');
$failMsg.hide();

$(function() {
    $signin.click(function (e) {
	e.preventDefault();
	var em = $('#loginEmail').val();
	var pw = $('#loginPass').val();
	$.ajax({
	    type : 'POST',
	    url : '/ajaxLogin/',
	    data : JSON.stringify({
		'email' : em,
		'pass' : pw
	    }),
	    dataType : "json",
	    contentType : "application/json",
	    success : function(response) {
		if (response['status'] == "OK") {
		    $signinForm.submit();
		} else {
		    $failMsg.show();
		}
	    },
	    error: function (error) {
		console.log(error);
	    }
	});
    });
});

