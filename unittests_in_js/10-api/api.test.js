const request = require('request');
const { expect } = require('chai');

describe('Index page', () => {
  const API_URL = 'http://localhost:7865';

  it('should return status code 200', (done) => {
    request.get(API_URL, (error, response, body) => {
      expect(response.statusCode).to.equal(200);
      done();
    });
  });

  it('should return "Welcome to the payment system"', (done) => {
    request.get(API_URL, (error, response, body) => {
      expect(body).to.equal('Welcome to the payment system');
      done();
    });
  });

  it('should have the correct content type', (done) => {
    request.get(API_URL, (error, response, body) => {
      expect(response.headers['content-type']).to.include('text/html');
      done();
    });
  });
});

describe('Cart page', () => {
  const API_URL = 'http://localhost:7865';

  it('should return status code 200 when id is a number', (done) => {
    request.get(`${API_URL}/cart/12`, (error, response, body) => {
      expect(response.statusCode).to.equal(200);
      done();
    });
  });

  it('should return correct message when id is a number', (done) => {
    request.get(`${API_URL}/cart/12`, (error, response, body) => {
      expect(body).to.equal('Payment methods for cart 12');
      done();
    });
  });

  it('should return status code 404 when id is not a number', (done) => {
    request.get(`${API_URL}/cart/hello`, (error, response, body) => {
      expect(response.statusCode).to.equal(404);
      done();
    });
  });

  it('should return status code 404 for non-existent routes', (done) => {
    request.get(`${API_URL}/invalid-route`, (error, response, body) => {
      expect(response.statusCode).to.equal(404);
      done();
    });
  });
});

describe('Available payments page', () => {
  const API_URL = 'http://localhost:7865';

  it('should return status code 200', (done) => {
    request.get(`${API_URL}/available_payments`, (error, response, body) => {
      expect(response.statusCode).to.equal(200);
      done();
    });
  });

  it('should return the correct payment methods object', (done) => {
    request.get(`${API_URL}/available_payments`, (error, response, body) => {
      const expectedPaymentMethods = {
        payment_methods: {
          credit_cards: true,
          paypal: false
        }
      };
      expect(JSON.parse(body)).to.deep.equal(expectedPaymentMethods);
      done();
    });
  });
});

describe('Login page', () => {
  const API_URL = 'http://localhost:7865';

  it('should return status code 200', (done) => {
    const options = {
      url: `${API_URL}/login`,
      method: 'POST',
      json: {
        userName: 'Betty'
      }
    };
    request(options, (error, response, body) => {
      expect(response.statusCode).to.equal(200);
      done();
    });
  });

  it('should return welcome message with the username', (done) => {
    const options = {
      url: `${API_URL}/login`,
      method: 'POST',
      json: {
        userName: 'Betty'
      }
    };
    request(options, (error, response, body) => {
      expect(body).to.equal('Welcome Betty');
      done();
    });
  });

  it('should handle different usernames', (done) => {
    const options = {
      url: `${API_URL}/login`,
      method: 'POST',
      json: {
        userName: 'John'
      }
    };
    request(options, (error, response, body) => {
      expect(body).to.equal('Welcome John');
      done();
    });
  });
});