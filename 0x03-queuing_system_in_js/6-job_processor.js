/*
 * Module creates a Job processor.
 */
const kue = require('kue');


const queue = kue.createQueue();

function sendNotification(phoneNumber, message) {
  console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);
}

queue.process('push_notification_code', (job, done) => {
  // Extract phone number and message
  const {phoneNumber, message} = job.data;

  // Sends notification
  sendNotification(phoneNumber, message);

  // Mark job as completed
  done();
});
