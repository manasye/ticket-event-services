"use strict";

var soap = require('strong-soap').soap;
// wsdl of the web service this client is going to invoke. For local wsdl you can use, url = './wsdls/stockquote.wsdl'
var url = 'http://127.0.0.1:80/ticket?WSDL';

var requestArgs = {

};

var options = {};
soap.createClient(url, options, function(err, client) {
	// var method = client['CreateOrder'];
	// console.log(client);
  	
	method(requestArgs, function(err, result, envelope, soapHeader) {
		if(err){
			console.log(err);
		}
		else {
			//response envelope
		    console.log('Response Envelope: \n' + envelope);
		    //'result' is the response body
		    console.log('Result: \n' + JSON.stringify(result));
		}
	});
  
});