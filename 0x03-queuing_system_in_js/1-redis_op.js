// Module connects to a Redis server running on localhost

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

// function set value
function setNewSchool(schoolName, value) {
  client.set(schoolName, value, (err, reply) => {
    if (err) {
      console.error(err);
    } else {
      console.log(`Reply: ${reply}`);
    }
  });
}

// Function gets value
function displaySchoolValue(schoolName) {
  client.get(schoolName, (err, value) => {
    if (err) {
      console.error(err);
    }
    else {
      console.log(value);
    }
  });
}

// function calls
displaySchoolValue('ALX');
setNewSchool('ALXSanFrancisco', '100');
displaySchoolValue('ALXSanFrancisco');
