const request = require('supertest');
const { app, sequelize } = require('../src/server');

beforeAll(async () => {
  // Sync database, force true to drop tables and start clean for tests
  await sequelize.sync({ force: true });
});

afterAll(async () => {
  await sequelize.close();
});

describe('API Health Check', () => {
  it('should return 200 OK', async () => {
    const res = await request(app).get('/api/health');
    expect(res.statusCode).toEqual(200);
    expect(res.body.status).toEqual('ok');
  });
});

describe('Donors API', () => {
  let createdDonorId;

  it('should create a new donor', async () => {
    const res = await request(app)
      .post('/api/donors')
      .send({
        name: 'John Doe',
        email: 'john.doe@example.com',
        phone: '1234567890',
        donor_type: 'Individual'
      });
    expect(res.statusCode).toEqual(201);
    expect(res.body).toHaveProperty('id');
    expect(res.body.name).toEqual('John Doe');
    createdDonorId = res.body.id;
  });

  it('should get all donors', async () => {
    const res = await request(app).get('/api/donors');
    expect(res.statusCode).toEqual(200);
    expect(Array.isArray(res.body)).toBeTruthy();
    expect(res.body.length).toBeGreaterThan(0);
  });

  it('should get a single donor by id', async () => {
    const res = await request(app).get(`/api/donors/${createdDonorId}`);
    expect(res.statusCode).toEqual(200);
    expect(res.body.name).toEqual('John Doe');
  });
});

describe('Campaigns API', () => {
  let createdCampaignId;

  it('should create a new campaign', async () => {
    const res = await request(app)
      .post('/api/campaigns')
      .send({
        name: 'Annual Fundraiser',
        description: 'Raising funds for the new wing.',
        start_date: '2023-01-01',
        end_date: '2023-12-31'
      });
    expect(res.statusCode).toEqual(201);
    expect(res.body).toHaveProperty('id');
    expect(res.body.name).toEqual('Annual Fundraiser');
    createdCampaignId = res.body.id;
  });

  it('should get all campaigns', async () => {
    const res = await request(app).get('/api/campaigns');
    expect(res.statusCode).toEqual(200);
    expect(Array.isArray(res.body)).toBeTruthy();
    expect(res.body.length).toBeGreaterThan(0);
  });
});