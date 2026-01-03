const sinon = require('sinon');
const { expect } = require('chai');
const Utils = require('./utils');
const sendPaymentRequestToApi = require('./4-payment');

describe('sendPaymentRequestToApi', function() {
  it('should stub Utils.calculateNumber and verify console.log', function() {
    // Create a stub for Utils.calculateNumber to always return 10
    const calculateNumberStub = sinon.stub(Utils, 'calculateNumber').returns(10);
    
    // Create a spy on console.log
    const consoleLogSpy = sinon.spy(console, 'log');
    
    // Call the function we want to test
    sendPaymentRequestToApi(100, 20);
    
    // Verify the stub was called with the correct arguments
    expect(calculateNumberStub.calledOnce).to.be.true;
    expect(calculateNumberStub.calledWithExactly('SUM', 100, 20)).to.be.true;
    
    // Verify console.log was called with the correct message
    expect(consoleLogSpy.calledOnce).to.be.true;
    expect(consoleLogSpy.calledWithExactly('The total is: 10')).to.be.true;
    
    // Restore the stub and spy to prevent test pollution
    calculateNumberStub.restore();
    consoleLogSpy.restore();
  });
});
