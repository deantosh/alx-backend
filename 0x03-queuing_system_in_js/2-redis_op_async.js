// Module connects to a Redis server running on localhost
import { promisify } from 'util'
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

// Promisify the 'set' method
const setAsync = promisify(client.set).bind(client);

// function set value
async function setNewSchool(schoolName, value) {
  try {
    const reply = await setAsync(schoolName, value);
    console.log(`Reply: ${reply}`);
  } catch (err) {
    console.error(err);
  }
}

// Convert a callback based to promised based function

const getAsync = promisify(client.get).bind(client);

async function displaySchoolValue(schoolName) {
  try {
    const value = await getAsync(schoolName);
    console.error(value);
  } catch (err) {
    console.log(err);
  }
}

// function calls
displaySchoolValue('ALX');
setNewSchool('ALXSanFrancisco', '100');
displaySchoolValue('ALXSanFrancisco');
