const express = require('express');
const bodyParser = require('body-parser');
const mongoose = require('mongoose');

const app = express();
app.use(bodyParser.json());

// Connect to MongoDB
mongoose.connect('mongodb://localhost/word_descriptions', { useNewUrlParser: true, useUnifiedTopology: true });
const db = mongoose.connection;
db.on('error', console.error.bind(console, 'MongoDB connection error:'));

// Create a schema for word descriptions
const wordSchema = new mongoose.Schema({
  word: String,
  description: String,
});

const WordDescription = mongoose.model('WordDescription', wordSchema);

app.get('/word/:word', async (req, res) => {
  const { word } = req.params;

  // Check if the word exists in the database
  const existingDescription = await WordDescription.findOne({ word });

  if (existingDescription) {
    res.json({ description: existingDescription.description });
  } else {
    res.status(404).json({ error: 'Word not found' });
  }
});

app.post('/word', async (req, res) => {
  const { word, description } = req.body;

  // Save the word and its description to the database
  const newDescription = new WordDescription({ word, description });
  await newDescription.save();

  res.json({ message: 'Description saved successfully' });
});

const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});