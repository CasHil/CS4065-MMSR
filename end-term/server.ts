const express = require('express');
const cors = require('cors');

const app = express();

// Enable CORS for all routes
app.use(cors());

// Add your API routes here
// For example:
app.get('/api/data', (req, res) => {
  res.json({ message: 'Hello from the API' });
});

// Start the server
const port = 5000; // Choose any port number you prefer
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
