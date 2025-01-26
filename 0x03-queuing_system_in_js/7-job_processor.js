const kue = require('kue');

// Create a queue
const queue = kue.createQueue();

// Array of blacklisted phone numbers
const blacklistedNumbers = ['4153518780', '4153518781'];

// Function to send a notification
function sendNotification(phoneNumber, message, job, done) {
  // Track the progress at 0%
  job.progress(0, 100);

  // Check if the phone number is blacklisted
  if (blacklistedNumbers.includes(phoneNumber)) {
    // If the number is blacklisted, fail the job with an error
    const error = new Error(`Phone number ${phoneNumber} is blacklisted`);
    // Only call done with the error to indicate the failure
    return done(error); 
  }

  // If the number is not blacklisted, track the progress to 50%
  job.progress(50, 100);
  console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);

  // Simulate completing the job
  setTimeout(() => {
    job.progress(100, 100); // Complete the job
    done(); // Call done to mark the job as completed
  }, 1000); // Simulating a delay of 1 second for sending the notification
}

// Queue processing: process jobs in 'push_notification_code_2' queue
queue.process('push_notification_code_2', 2, (job, done) => {
  const { phoneNumber, message } = job.data;
  sendNotification(phoneNumber, message, job, done);
});

// To ensure the job processor is listening and running, log to the console
queue.on('job complete', (id, result) => {
  console.log(`Job ${id} completed!`);
});

queue.on('job failed', (id, errorMessage) => {
  console.log(`Job ${id} failed: ${errorMessage}`);
});
