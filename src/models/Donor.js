const { DataTypes } = require('sequelize');
const sequelize = require('../db');

const Donor = sequelize.define('Donor', {
  id: {
    type: DataTypes.INTEGER,
    autoIncrement: true,
    primaryKey: true,
  },
  name: {
    type: DataTypes.STRING,
    allowNull: false,
  },
  email: {
    type: DataTypes.STRING,
    allowNull: true,
    validate: {
      isEmail: true,
    },
  },
  phone: {
    type: DataTypes.STRING,
    allowNull: true,
  },
  donor_type: {
    type: DataTypes.ENUM('Individual', 'Corporate', 'CSR', 'Foundation', 'Zakat', 'HNI', 'Partner'),
    allowNull: false,
    defaultValue: 'Individual',
  },
});

module.exports = Donor;