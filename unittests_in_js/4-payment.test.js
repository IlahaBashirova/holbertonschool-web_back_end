const sinon = require('sinon');
const { expect } = require('chai');

const Utils = require('./utils');
const sendPaymentRequestToApi = require('./4-payment');

describe('sendPaymentRequestToApi', function () {
  it('should stub Utils.calculateNumber and log the correct total', function () {
    const stub = sinon.stub(Utils, 'calculateNumber').returns(10);
    const logSpy = sinon.spy(console, 'log');

    sendPaymentRequestToApi(100, 20);

    expect(stub.calledOnceWithExactly('SUM', 100, 20)).to.equal(true);
    expect(logSpy.calledOnceWithExactly('The total is: 10')).to.equal(true);

    stub.restore();
    logSpy.restore();
  });
});
