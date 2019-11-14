const { Client, logger, Variables } = require('camunda-external-task-client-js');
const moment = require('moment');
let axios = require('axios');

const config = { baseUrl: 'http://localhost:8080/engine-rest', use: logger, asyncResponseTimeout: 10000 };
const restUrl = 'http://localhost:5000';

// create a Client instance with custom configuration
const worker = new Client(config);

const axiosConfig = {
  headers: {
    'Content-Type': 'application/json',
  }
};

let instance;

/** Create order */
worker.subscribe('create-order', async function({ task, taskService }) {
  // Get a process variable
  const user_id = task.variables.get('user_id');
  const token = task.variables.get('token');
  const price = task.variables.get('price');
  const event_id = task.variables.get('event_id');
  const quantity = task.variables.get('quantity');

  let order_date = moment().format('YYYY-MM-DD hh:mm:ss');

  let processVariables = new Variables();
  
  const body = JSON.stringify({
    user_id,
    order_date
  });

  const headers = {
    'Content-Type': 'application/json',
    'Authorization': `JWT ${token}`,
  };

  instance = axios.create({
    headers
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
            processVariables.set('total_price', price * quantity);
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