const { expect } = require('chai');
const request = require('request');

describe('API integration tests', () => {
  describe('GET /available_payments', () => {
    it('should return correct payment methods', (done) => {
      request.get('http://localhost:7865/available_payments', (err, res, body) => {
        expect(res.statusCode).to.equal(200);
        expect(JSON.parse(body)).to.deep.equal({
          payment_methods: {
            credit_cards: true,
            paypal: false,
          },
        });
        done();
      });
    });
  });

  describe('POST /login', () => {
    it('should return welcome message', (done) => {
      const options = {
        url: 'http://localhost:7865/login',
        method: 'POST',
        json: { userName: 'Betty' },
      };

      request(options, (err, res, body) => {
        expect(res.statusCode).to.equal(200);
        expect(body).to.equal('Welcome Betty');
        done();
      });
    });
  });
});
