const http = require('http')
const port = 80

const requestHandler = (request, response) => {
	console.log("Request received");
	response.writeHead(200, {});
	response.write('Payment successful');
	response.end();
}

const server = http.createServer(requestHandler)

server.listen(port, (err) => {
	if(err){
		return console.log('ERROR: ', err);
	}

	console.log(`Server is listening on ${port}`);
})