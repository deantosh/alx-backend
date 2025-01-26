/*
 * Module creates the Job creator.
 */
const kue = require('kue');


const queue = kue.createQueue();

const jobData = {
  phoneNumber: '12345678',
  message: 'This is a test notification message',
}

try {
  // Create a job in 'push_notification_code' queue
  const job = queue.create('push_notification_code', jobData);

  // Save the job
  job.save((err) => {
    if (err) {
      throw new Error(`Error creating job: ${err}`);
    } else {
      console.log(`Notification job created: ${job.id}`);
    }
  });

  // Handle the job completion event
  job.on('complete', () => {
    console.log('Notification job completed');
  });

  // Handle the job failure event
  job.on('failed', () => {
    console.log('Notification job failed');
  });
} catch (error) {
  // Catch any errors and log them
  console.log(`Error: ${error.message}`);
}
