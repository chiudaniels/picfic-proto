var cookieParser = require( 'cookie-parser' );
var expressSession = require( 'express-session' );
var passwordless = require( 'passwordless' );
var MongoStore = require( 'passwordless-mongostore' );
var email = require( 'emailjs' );

var yourEmail = 'picfic2017@outlook.com';
var yourPwd = process.env.OUTLOOK_PASSWORD;
var yourSmtp = 'smtp-mail.outlook.com';
var smtpServer  = email.server.connect({
  user:    yourEmail, 
  password: yourPwd,
  timeout: 60000,
  host: yourSmtp, 
  tls: { ciphers: 'SSLv3' }
});
// MongoDB setup (given default can be used)
var pathToMongoDb = "/data/db";
// Path to be send via email
var host = 'https://www.picfic.net/';


// Setup of Passwordless
passwordless.init( new MongoStore( pathToMongoDb ));
passwordless.addDelivery(
    function( tokenToSend, uidToSend, recipient, callback ) {
	// Send out token
	smtpServer.send({
	    text: 'Hello!\nYou can now access your account here:'
		+ host + '?token=' + tokenToSend + '&uid='
		+ encodeURIComponent(uidToSend),
	    from: yourEmail, 
	    to: recipient,
	    subject: 'Token for ' + host,
	    attachment: [
		{
		    data: "<html>INSERT HTML STRING LINKING TO TOKEN</html>",
		    alternative: true
		}
	    ]
	}, function( err, message ) { 
            if( err ) {
		console.log( err );
            }
            callback( err );
        });
    });
