/*
 * Module connects to redis server.
 * Publishes a message to ALXchannel channel.
 */
const redis = require('redis');


const client = redis.createClient();

client.on('connect', () => {
  console.log("Redis client connected to the server");
});

client.on('error', (err) => {
  console.log(`Redis client not connected to the server: {err.message}`);
});

// Function to publish message
function publishMessage(message, time) {
  setTimeout(() => {
    console.log("About to send MESSAGE");
    client.publish('ALXchannel', message);
  }, time);
}

// Call the publishMessage function with different messages and times
publishMessage('ALX Student #1 starts course', 100);
publishMessage('ALX Student #2 starts course', 200);
publishMessage('KILL_SERVER', 300);
publishMessage('ALX Student #3 starts course', 400);
