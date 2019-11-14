const { Client, logger, Variables } = require('camunda-external-task-client-js');
const moment = require('moment');
let axios = require('axios');

const config = { baseUrl: 'http://localhost:8080/engine-rest', use: logger, asyncResponseTimeout: 10000 };
const restUrl = 'https://ticket-soa.herokuapp.com';
const paymentUrl = 'http//127.0.0.1:80';

// create a Client instance with custom configuration
const worker = new Client(config);

const axiosConfig = {
  headers: {
    'Content-Type': 'application/json',
  }
};

let instance;

worker.subscribe('check-login', async function({ task, taskService }){

  let processVariables = new Variables();
  let token = "";

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
          processVariables.set('status_login', res.status);
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
    await instance.get(`${restUrl}/users`)
      .then(async(res) => {
        if(res.status == 200){
          var i;
          for(i = 0; i < res.data.users.length; i++){
            if(res.data.users[i].username === username){
              processVariables.set('user_id', res.data.users[i].id);
            }
          }
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

/** Create order */
worker.subscribe('create-order', async function({ task, taskService }) {
  
  // Get a process variable
  const user_id = task.variables.get('user_id');
  const token = task.variables.get('token');
  const event_quantity = task.variables.get('quantity');
  const event_name_id = task.variables.get('event_name_id');

  // Initialize other variables
  var event_id = -1;
  var event_price = 1000;
  var event_quota = -1;
  let order_date = moment().format('YYYY-MM-DD hh:mm:ss');

  // Get event_id from event's name
  instance = axios.create({
    headers:{
      'Content-Type': 'application/json',
      'Authorization': `JWT ${token}`
    }
  });

  // User entered event's id
  if(event_name_id.match(/^[0-9]+$/) != null){
    console.log("Event id");
    event_id = parseInt(event_name_id)
  }
  // User entered event's name
  else {
    console.log("Event name");
    try{
      await instance.get(`${restUrl}/events`)
        .then(async(res) => {
          if(res.status == 200){
            var i;
            for(i = 0; i < res.data.events.length; i++){
              if(event_name_id == res.data.events[i].name){
                event_id = res.data.events[i].id;
                break;
              }
            }
          }
        })
    }
    catch(e){
      console.log(e);
    }
  }

  let processVariables = new Variables();
  
  const body = JSON.stringify({
    user_id,
    order_date
  });

  try {
    await instance.get(`${restUrl}/event/${event_id}`)
      .then(async (res) => {
        if (res.data.status === 1) {
          await instance.post(`${restUrl}/order`, body)
          .then(async (res) => {
            const order_id = res.data.id;
            
            console.log('Order created');
            
            processVariables.set('order_id', order_id);
            processVariables.set('total_price', event_price * event_quantity);
          })
          .catch((err) => {
            console.log(err);

            processVariables.set('message', err.response.message);
          })
        }
      })
      .catch((err) => {
        processVariables.set('message', err.response.message);
      });
  } catch (e) {
    console.log(e);
  } finally {
    // Complete the task
    await taskService.complete(task, processVariables);
  }
});

worker.subscribe('send-payment', async function({ task, taskService }){
  const order_id = task.variables.get("order_id");
  const price = task.variables.get("total_price");
  let processVariables = new Variables();

  instance = axios.create({});

  try{
    await instance.get(`${paymentUrl}`, {})
      .then(async (res) => {
        console.log(res.status);
        processVariables.set('status_payment', res.status);
      })
  }
  catch(e){
    console.log(e);
  }
  finally{
    await taskService.complete(task, processVariables);
  }
});

/**
 * Receive Payment
 */

worker.subscribe('receive-payment', async function({ task, taskService }) {
  const order_id = task.variables.get("order_id");
  const success = task.variables.get("success");

  instance = axios.create(axiosConfig);

  let processVariables = new Variables();

  try {
    if (success) {
      processVariables.set("order_id", order_id);
    } else {
      processVariables.set("error_message", "Gagal melakukan pembayaran!");
    }
  } catch (e) {
    console.log(e);
  } finally {
    await taskService.complete(task, processVariables);
  }
});

/** Generate ticket */
worker.subscribe('generate-ticket', async function({task, taskService}) {
  const order_id = task.variables.get('order_id');
  const event_id = task.variables.get('event_id');
  const seat_num = task.variables.get('seat_num');
  const price = task.variables.get('price');
  const quantity = task.variables.get('quantity');

  const ticketBody = JSON.stringify({
    order_id,
    event_id,
    seat_num,
    price,
    quantity
  });

  instance = axios.create(axiosConfig);

  try {
    await instance.post(`${restUrl}/ticket`, ticketBody)
    .then((res) => {
      console.log('Ticket created');

      processVariables.set("order_id", res.order_id);
      processVariables.set("event_id", res.event_id);
      processVariables.set("price", res.price);
    })
    .catch((err) => {
      console.log(err);
    })
  } catch (e) {
    console.log(e);
  } finally {
    await taskService.complete(task, processVariables);
  }
})