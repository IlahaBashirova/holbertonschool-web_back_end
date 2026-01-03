const sinon = require('sinon');
const { expect } = require('chai');

const sendPaymentRequestToApi = require('./5-payment');

describe('sendPaymentRequestToApi', function () {
  let logSpy;

  beforeEach(function () {
    logSpy = sinon.spy(console, 'log');
  });

  afterEach(function () {
    logSpy.restore();
  });

  it('should log "The total is: 120" when called with 100 and 20', function () {
    sendPaymentRequestToApi(100, 20);

    expect(logSpy.calledOnce).to.be.true;
    expect(logSpy.calledWithExactly('The total is: 120')).to.be.true;
  });

  it('should log "The total is: 20" when called with 10 and 10', function () {
    sendPaymentRequestToApi(10, 10);

    expect(logSpy.calledOnce).to.be.true;
    expect(logSpy.calledWithExactly('The total is: 20')).to.be.true;
  });
});
