const express = require('express');
const cors = require('cors');
const sequelize = require('./db');

const app = express();

app.use(cors());
app.use(express.json());

// Routes will be mounted here
app.use('/api/donors', require('./routes/donors'));
app.use('/api/campaigns', require('./routes/campaigns'));

app.get('/api/health', (req, res) => {
  res.status(200).json({ status: 'ok' });
});

module.exports = { app, sequelize };