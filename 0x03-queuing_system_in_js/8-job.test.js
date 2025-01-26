const kue = require('kue');
const { expect } = require('chai');
const createPushNotificationsJobs = require('./8-job'); // Adjust path as necessary

describe('createPushNotificationsJobs', function () {
  let queue;

  beforeEach(function (done) {
    // Create a Kue queue for each test run
    queue = kue.createQueue();
    queue.testMode = true; // Enable Kue test mode
    done();
  });

  afterEach(function (done) {
    // Clear all jobs from the queue after each test
    queue.testMode.jobs = [];
    done();
  });

  it('should throw an error if jobs is not an array', function () {
    expect(() => createPushNotificationsJobs({}, queue)).to.throw('Jobs is not an array');
    expect(() => createPushNotificationsJobs('not an array', queue)).to.throw('Jobs is not an array');
  });

  it('should add jobs to the queue and log job creation', function (done) {
    const jobs = [
      { phoneNumber: '4153518780', message: 'This is the code 1234 to verify your account' },
      { phoneNumber: '4153518781', message: 'This is the code 4562 to verify your account' },
    ];

    // Create jobs using the provided function
    createPushNotificationsJobs(jobs, queue);

    // Check that jobs have been added
    setTimeout(() => {
      expect(queue.testMode.jobs.length).to.equal(2);

      // Ensure job details are correct
      const job1 = queue.testMode.jobs[0];
      expect(job1.data.phoneNumber).to.equal('4153518780');
      expect(job1.data.message).to.equal('This is the code 1234 to verify your account');

      const job2 = queue.testMode.jobs[1];
      expect(job2.data.phoneNumber).to.equal('4153518781');
      expect(job2.data.message).to.equal('This is the code 4562 to verify your account');

      done();
    }, 100);
  });

  it('should handle job progress, completion, and failure events correctly', function (done) {
    const jobs = [
      { phoneNumber: '4153518780', message: 'This is the code 1234 to verify your account' },
    ];

    // Create jobs using the provided function
    createPushNotificationsJobs(jobs, queue);

    // Check that jobs have been added
    setTimeout(() => {
      const job = queue.testMode.jobs[0];

      // Simulate progress and events
      job.progress(50, 100);

      // Check if the job progress is set correctly
      expect(job.progress).to.deep.equal({ completed: 50, total: 100 });

      // Simulate job completion
      job.emit('complete');

      // Check if job completion works correctly
      expect(job._state).to.equal('completed');

      // Simulate job failure
      job.emit('failed', 'Error: Failed to send notification');

      // Check if job failed correctly
      expect(job._state).to.equal('failed');

      done();
    }, 100);
  });
});
