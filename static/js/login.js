// Login
var $signin = $('#signInButton');
var $signinForm = $('#signInForm');
var $failMsg = $('#loginFail');
$failMsg.hide();

// Register
var $register = $('#registerButton');
var $registerForm = $('#registerForm');
var $failMsgReg = $('#registerFail');
$failMsgReg.hide();

console.log($failMsgReg);

// On Ready
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

    $register.click(function (e) {
	e.preventDefault();
	var em = $('#makeEmail').val();
	var un = $('#username').val();
	$.ajax({
	    type : 'POST',
	    url : '/ajaxRegister/',
	    data : JSON.stringify({
		'email' : em,
		'username' : un
	    }),
	    dataType : "json",
	    contentType : "application/json",
	    success : function(response) {
		if (response['status'] == "OK") {
		    $registerForm.submit();
		} else {
		    $failMsgReg.show();
		}
	    },
	    error: function (error) {
		console.log(error);
	    }
	});
    });
});
