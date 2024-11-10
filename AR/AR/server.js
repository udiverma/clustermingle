const exp = require('constants');
const express = require('express');
const app = express();
const path = require('path');
const cors = require('cors');

const sqlite3 = require('sqlite3').verbose();

// Allow CORS for all origins, was needed for the api gateway via ngroc to work as CORS is normally blocked 
app.use(cors());


app.set("/", "html");
app.use(express.static(path.join(__dirname, "/")));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));

// Connect to the SQLite database

const dbPath = path.join(__dirname, './RiddleDB.db');
const db = new sqlite3.Database(dbPath, (err) => {
    if (err) {
        console.error('Error connecting to the SQLite database:', err.message);
    } else {
        console.log('Connected to the SQLite database.');
    }
});

// Route to fetch a random riddle
app.get('/api/riddle', (req, res) => {
    db.all("SELECT * FROM riddles", (err, rows) => {
        if (err) {
            console.error('Error retrieving data from SQLite database:', err.message);
            res.status(500).json({ error: 'Failed to retrieve riddle.' });
        } else {
            if (rows.length > 0) {
                // Pick a random riddle
                const randomRiddle = rows[Math.floor(Math.random() * rows.length)];
                res.json(randomRiddle);
            } else {
                res.status(404).json({ error: 'No riddles found.' });
            }
        }
    });
});

// Serve the main page
app.get('/', (req, res) => {
    res.render('index');
});

// Start the server
app.listen(8098, () => {
    console.log("Server is running on http://localhost:8098");
});
