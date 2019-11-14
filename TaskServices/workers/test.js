let axios = require('axios');
const paymentUrl = 'http//127.0.0.1:80';

let instance = axios.create({});

try{
	instance.request(paymentUrl)
		.then(async(res) => {
			console.log(res.status);
		})
}
catch(e){
	console.log(e);
}