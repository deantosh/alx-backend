const kue = require('kue');
const queue = kue.createQueue();

// Function to create push notifications jobs
function createPushNotificationsJobs(jobs, queue) {
  // Check if jobs is an array
  if (!Array.isArray(jobs)) {
    throw new Error('Jobs is not an array');
  }

  // Iterate over each job in the array and create a job in the queue
  jobs.forEach((jobData) => {
    const job = queue.create('push_notification_code_3', jobData)
      .save((err) => {
        if (err) {
          console.log(`Error creating job: ${err}`);
        } else {
          console.log(`Notification job created: ${job.id}`);
        }
      });

    // Job progress
    job.on('progress', (progress, data) => {
      console.log(`Notification job ${job.id} ${progress}% complete`);
    });

    // Job complete
    job.on('complete', (result) => {
      console.log(`Notification job ${job.id} completed`);
    });

    // Job failed
    job.on('failed', (errorMessage) => {
      console.log(`Notification job ${job.id} failed: ${errorMessage}`);
    });
  });
}

module.exports = createPushNotificationsJobs;
