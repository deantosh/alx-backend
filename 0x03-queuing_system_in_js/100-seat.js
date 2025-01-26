const express = require('express');
const redis = require('redis');
const kue = require('kue');
const { promisify } = require('util');

// Initialize Express app
const app = express();
const port = 1245;

// Initialize Redis client and promisify necessary functions
const client = redis.createClient();
const setAsync = promisify(client.set).bind(client);
const getAsync = promisify(client.get).bind(client);

// Initialize Kue queue
const queue = kue.createQueue();

// Initialize reservationEnabled and availableSeats
let reservationEnabled = true;
const initialSeats = 50;

// Set initial number of seats in Redis
async function initializeSeats() {
  await setAsync('available_seats', initialSeats);
}

initializeSeats();

// Helper functions to interact with Redis
async function reserveSeat(number) {
  await setAsync('available_seats', number);
}

async function getCurrentAvailableSeats() {
  const availableSeats = await getAsync('available_seats');
  return parseInt(availableSeats, 10);
}

// Express routes

// Route to get the number of available seats
app.get('/available_seats', async (req, res) => {
  const availableSeats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats: availableSeats.toString() });
});

// Route to reserve a seat
app.get('/reserve_seat', async (req, res) => {
  if (!reservationEnabled) {
    return res.json({ status: 'Reservation are blocked' });
  }

  // Add job to the queue
  const job = queue.create('reserve_seat', {})
    .save((err) => {
      if (err) {
        return res.json({ status: 'Reservation failed' });
      }
      return res.json({ status: 'Reservation in process' });
    });
});

// Route to process the queue
app.get('/process', async (req, res) => {
  res.json({ status: 'Queue processing' });

  // Start processing the job queue
  queue.process('reserve_seat', async (job, done) => {
    try {
      let availableSeats = await getCurrentAvailableSeats();

      if (availableSeats <= 0) {
        reservationEnabled = false;
        return done(new Error('Not enough seats available'));
      }

      // Decrease available seats by 1
      availableSeats -= 1;
      await reserveSeat(availableSeats);

      if (availableSeats === 0) {
        reservationEnabled = false;
      }

      console.log(`Seat reservation job ${job.id} completed`);
      done();
    } catch (error) {
      console.log(`Seat reservation job ${job.id} failed: ${error.message}`);
      done(error);
    }
  });
});

// Start the server
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
