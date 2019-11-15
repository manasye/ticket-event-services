 var soap = require('strong-soap').soap;
 var http = require('http');

var OrderService = {
    OrderService: {
        CreateOrder: {
            post_order: function(args){
                return {
                    ID: 12345
                };
            },

            // This is how to define an asynchronous function.
            MyAsyncFunction: function(args, callback) {
                // do some work
                callback({
                    name: args.name
                });
            },

            // This is how to receive incoming headers
            HeadersAwareFunction: function(args, cb, headers) {
                return {
                    name: headers.Token
                };
            },

            // You can also inspect the original `req`
            reallyDeatailedFunction: function(args, cb, headers, req) {
                console.log('SOAP `reallyDeatailedFunction` request from ' + req.connection.remoteAddress);
                return {
                    name: headers.Token
                };
            }
        }
    }
};

var xml = require('fs').readFileSync('ticket_wsdl.wsdl', 'utf8'),
    server = http.createServer(function(request,response) {
        response.end("404: Not Found: " + request.url);
    });

server.listen(80);
soap.listen(server, '/ticket', OrderService, xml);