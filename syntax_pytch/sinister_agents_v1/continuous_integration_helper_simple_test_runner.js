javascript
const { exec } = require('child_process'); 

/**
* Runs tests using a shell command and logs output.
* @param {string} testCommand - Command to run tests (e.g., 'npm test').
*/
function runTests(testCommand = 'npm test') {
  exec(testCommand, (error, stdout, stderr) => {
    if (error) {
      console.error(`Test run error: ${error.message}`);
      return;
    }
    if (stderr) {
      console.error(`Test run stderr: ${stderr}`);
    }
    console.log(`Test run output:\n${stdout}`);
  });
} 

// Example usage:
// runTests(); 

module.exports = { runTests };