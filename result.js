
// Import the necessary modules.
const mysql = require('mysql');
const util = require('util');

// Create a database connection.
const connection = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: '',
  database: 'test'
});

// Convert the connection to a promise-based interface.
connection.query = util.promisify(connection.query);

// Execute the query.
const [rows, fields] = await connection.query('SELECT * FROM posts LIMIT 12, 8');

// Log the results.
console.log(rows);

// Close the database connection.
connection.end();
 