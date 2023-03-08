const express = require('express');
const MongoClient = require('mongodb').MongoClient;
const app = express();

app.post('/pnl', (req, res) => {
    const pnlData = req.body;
    // process the pnlData, e.g. save to the database
    res.status(200).send('PnL data received');
  });

app.post('/data', (req, res) => {
  const data = req.body;
  // Connect to the MongoDB database
  MongoClient.connect('mongodb://localhost:27017/mydb', { useNewUrlParser: true }, (err, client) => {
    if (err) {
      console.error(err);
      res.status(500).send('Error connecting to database');
      return;
    }
    // Get a reference to the database
    const db = client.db('mydb');
    // Insert the data into the "data" collection
    db.collection('data').insertOne(data, (err, result) => {
      if (err) {
        console.error(err);
        res.status(500).send('Error saving data to database');
        return;
      }
      console.log('Data saved to database');
      res.status(200).send('Data saved to database');
      client.close();
    });
  });
});

app.get('/goodbye', (req, res) => {
    res.send('Goodbye, world!');
  });

app.listen(3000, () => {
    console.log('Express app listening on port 3000');
  });