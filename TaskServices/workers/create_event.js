const { Client, logger, Variables } = require('camunda-external-task-client-js');
const moment = require('moment');
let axios = require('axios');

const config = { baseUrl: 'http://localhost:8080/engine-rest', use: logger, asyncResponseTimeout: 10000 };
const restUrl = 'https://ticket-soa.herokuapp.com';

// create a Client instance with custom configuration
const worker = new Client(config);

const axiosConfig = {
  headers: {
    'Content-Type': 'application/json',
  }
};

let instance;

worker.subscribe('check-login-partner', async function({ task, taskService }){

  let processVariables = new Variables();
  let token = "";
  let flag_login = 'success';

  // Login to get access token
  const username = task.variables.get('username');
  const password = task.variables.get('password');

  const body = JSON.stringify({
    username,
    password
  });

  instance = axios.create(axiosConfig);
  
  try {
    await instance.post(`${restUrl}/user/auth`, body)
      .then(async(res) => {
        if(res.status == 200){
          token = res.data.access_token;
          processVariables.set('token', res.data.access_token);
        }
        else {
        	flag_login = 'failed';
        }
      })
  }
  catch(e){
    console.log(e);
  }

  // Login to get user id
  instance = axios.create({
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `JWT ${token}`
    }
  });

  try{
  	if(flag_login == 'success'){
  		await instance.get(`${restUrl}/users`)
	      .then(async(res) => {
	        if(res.status == 200){
	          var i;
	          for(i = 0; i < res.data.users.length; i++){
	            if(res.data.users[i].username === username && res.data.users[i].role == 'partner'){
	              processVariables.set('user_id', res.data.users[i].id);
	              processVariables.set('status_login', 'success');
	            }
	          }
	        }
	        else {
	        	processVariables.set('status_login', 'failed');
	        }
	      })
  	}
  }
  catch(e){
    console.log(e);
  }
  finally{
      await taskService.complete(task, processVariables);
  }
});

worker.subscribe('check-form-event', async function({ task, taskService }){
	let processVariables = new Variables();

	const name = task.variables.get('name');
	const category = task.variables.get('category');
	const location = task.variables.get('location');
	const start_time = task.variables.get('start_time');
	const end_time = task.variables.get('end_time');
	const event_date = task.variables.get('event_date');
	const quota = task.variables.get('quota');
	const price = task.variables.get('price');

	const isFormValid = true;

	try{
		// check if null
		if(!name || !category || !location || !start_time || !end_time
			|| !event_date || !quota || !price){
			console.log("One of field is null");
			isFormValid = false; 
		}

		if(isFormValid == true){
			processVariables.set('form_accepted', 'success');
		}
		else {
			processVariables.set('form_accepted', 'failed');
		}
	}
	catch(e){
		console.log(e);
	}
	finally{
		await taskService.complete(task, processVariables);
	}
});

worker.subscribe('create-event', async function({ task, taskService }){
	let processVariables = new Variables();

	const name = task.variables.get('name');
	const category = task.variables.get('category');
	const location = task.variables.get('location');
	const start_time = task.variables.get('start_time');
	const end_time = task.variables.get('end_time');
	const event_date = task.variables.get('event_date');
	const quota = task.variables.get('quota');
	const price = task.variables.get('price');
	const token = task.variables.get('token');

	const body = JSON.stringify({
	    name,
	    category,
	    location,
	    start_time,
	    end_time,
	    event_date,
	    status: 1,
	    quota,
	    price
	  });

	instance = axios.create({
	    headers: {
	      'Content-Type': 'application/json',
	      'Authorization': `JWT ${token}`
	    }
	  });

	try{
		await instance.post(`${restUrl}/event`, body)
			.then(async(res) => {
				if(res.status == 200){
					console.log("Event created!");
				}
				else {
					console.log("Event not created!");
				}
			})
	}
	catch(e){
		console.log(e);
	}
	finally{
		await taskService.complete(task, processVariables);
	}
});