const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3000;

app.use(express.json());
app.use(express.static('public'));

app.post('/add-entry', (req, res) => {
    const newEntry = req.body;
    const entriesPath = path.join(__dirname, 'blog', 'entries.json');

    fs.readFile(entriesPath, 'utf8', (err, data) => {
        if (err) {
            return res.status(500).json({ error: 'Error reading entries file' });
        }

        const entries = JSON.parse(data);
        entries.unshift(newEntry);

        fs.writeFile(entriesPath, JSON.stringify(entries, null, 2), 'utf8', (err) => {
            if (err) {
                return res.status(500).json({ error: 'Error writing entries file' });
            }

            res.status(200).json({ message: 'Entry added successfully' });
        });
    });
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
