const sinon = require('sinon');
const assert = require('assert');

const Utils = require('./utils');
const sendPaymentRequestToApi = require('./4-payment');

describe('sendPaymentRequestToApi', function () {
  afterEach(function () {
    sinon.restore(); // restores ALL stubs/spies created by sinon
  });

  it('should stub Utils.calculateNumber and log the correct total', function () {
    const stub = sinon.stub(Utils, 'calculateNumber').returns(10);
    const logSpy = sinon.spy(console, 'log');

    sendPaymentRequestToApi(100, 20);

    // verify stub called with correct args
    sinon.assert.calledOnceWithExactly(stub, 'SUM', 100, 20);

    // verify correct console output
    sinon.assert.calledOnceWithExactly(logSpy, 'The total is: 10');
  });
});
