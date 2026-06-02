const { app, sequelize } = require('./src/server');

const PORT = process.env.PORT || 3000;

async function start() {
  try {
    // Sync the database (creates tables if they don't exist)
    await sequelize.sync();
    console.log('Database synchronized successfully.');

    app.listen(PORT, () => {
      console.log(`Server is running on port ${PORT}`);
    });
  } catch (error) {
    console.error('Unable to start the server:', error);
  }
}

start();