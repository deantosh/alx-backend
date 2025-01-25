/*
 * Module subscribes to a channel.
 * Display the message sent to the client.
 * Kill redis server if message is KILL_SERVER
 */
const redis = require('redis');


const client = redis.createClient();

client.on('connect', () => {
  console.log("Redis client connected to the server");
});

client.on('error', (err) => {
  console.log(`Redis client not connected to the server: {err.message}`);
});

client.subscribe("ALXchannel");

client.on('message', (channel, message) => {
  console.log(message);

  if (message === 'KILL_SERVER') {
    client.unsubscribe('ALXchannel');
    client.quit();
  }
});
