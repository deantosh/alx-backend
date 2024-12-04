// Create and display hash

import { createClient } from 'redis';

const client = createClient({
  url: 'redis://127.0.0.1:6379'
});

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

client.on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err}`);
});

// Use callback operations
client.hset('HolbertonSchools', 'Portland', '50', (err, reply) => {
  if (err) {
    console.error(err);
  } else {
    console.log(`Reply: ${reply}`);
  }
});
client.hset('HolbertonSchools', 'Seattle', '80', (err, reply) => {
  if (err) {
    console.error(err);
  } else {
    console.log(`Reply: ${reply}`);
  }
});
client.hset('HolbertonSchools', 'New York', '20', (err, reply) => {
  if (err) {
    console.error(err);
  } else {
    console.log(`Reply: ${reply}`);
  }
});
client.hset('HolbertonSchools', 'Bogota', '20', (err, reply) => {
  if (err) {
    console.error(err);
  } else {
    console.log(`Reply: ${reply}`);
  }
});
client.hset('HolbertonSchools', 'Cali', '40', (err, reply) => {
  if (err) {
    console.error(err);
  } else {
    console.log(`Reply: ${reply}`);
  }
});
client.hset('HolbertonSchools', 'Paris', '2', (err, reply) => {
  if (err) {
    console.error(err);
  } else {
    console.log(`Reply: ${reply}`);
  }
});


// Display the entire hash
client.hgetall('HolbertonSchools', (err, obj) => {
  if (err) {
    console.error(err)
  } else {
    console.log(obj);
  }
});
