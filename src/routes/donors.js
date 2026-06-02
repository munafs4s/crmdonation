const express = require('express');
const router = express.Router();
const Donor = require('../models/Donor');

// Create a donor
router.post('/', async (req, res) => {
  try {
    const donor = await Donor.create(req.body);
    res.status(201).json(donor);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

// Get all donors
router.get('/', async (req, res) => {
  try {
    const donors = await Donor.findAll();
    res.json(donors);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get donor by id
router.get('/:id', async (req, res) => {
  try {
    const donor = await Donor.findByPk(req.params.id);
    if (donor) {
      res.json(donor);
    } else {
      res.status(404).json({ error: 'Donor not found' });
    }
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Update a donor
router.put('/:id', async (req, res) => {
  try {
    const donor = await Donor.findByPk(req.params.id);
    if (donor) {
      await donor.update(req.body);
      res.json(donor);
    } else {
      res.status(404).json({ error: 'Donor not found' });
    }
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

// Delete a donor
router.delete('/:id', async (req, res) => {
  try {
    const donor = await Donor.findByPk(req.params.id);
    if (donor) {
      await donor.destroy();
      res.status(204).send();
    } else {
      res.status(404).json({ error: 'Donor not found' });
    }
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;