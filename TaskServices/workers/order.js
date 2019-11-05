const { Client, logger, Variables } = require('camunda-external-task-client-js');
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

worker.subscribe('create-order', async function({ task, taskService }) {
  // Get a process variable
  const user_id = task.variables.get('user_id');
  const order_date = task.variables.get('order_date');

  let processVariables = new Variables();
  
  if (user_id && order_date) {
    const body = JSON.stringify({
      user_id,
      order_date
    });

    instance = axios.create(axiosConfig);
    try {
      const res = await instance.post(`${restUrl}/order`, body);  
      
      console.log('Order created');
      processVariables.set('order_id', res.data.id);
    } catch (e) {
      console.log(e);
    }
  }

  // Complete the task
  await taskService.complete(task, processVariables);
});