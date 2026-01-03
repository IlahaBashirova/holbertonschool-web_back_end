const sinon = require('sinon');
const { expect } = require('chai');

const Utils = require('./utils');
const sendPaymentRequestToApi = require('./3-payment');

describe('sendPaymentRequestToApi', function () {
  it('should call Utils.calculateNumber with SUM, 100, 20 and log the total', function () {
    const spy = sinon.spy(Utils, 'calculateNumber');
    const logSpy = sinon.spy(console, 'log');

    sendPaymentRequestToApi(100, 20);

    expect(spy.calledOnceWithExactly('SUM', 100, 20)).to.equal(true);
    expect(logSpy.calledOnceWithExactly('The total is: 120')).to.equal(true);

    spy.restore();
    logSpy.restore();
  });
});
