const { expect } = require('chai');
const calculateNumber = require('./2-calcul_chai');

describe('calculateNumber', function () {
  describe('SUM', function () {
    it('should return 6 for SUM 1.4 and 4.5', function () {
      expect(calculateNumber('SUM', 1.4, 4.5)).to.equal(6);
    });

    it('should handle rounding correctly', function () {
      expect(calculateNumber('SUM', 1.5, 3.7)).to.equal(6); // 2 + 4
    });
  });

  describe('SUBTRACT', function () {
    it('should return -4 for SUBTRACT 1.4 and 4.5', function () {
      expect(calculateNumber('SUBTRACT', 1.4, 4.5)).to.equal(-4);
    });

    it('should handle rounding correctly', function () {
      expect(calculateNumber('SUBTRACT', 2.6, 1.2)).to.equal(2); // 3 - 1
    });
  });

  describe('DIVIDE', function () {
    it('should return 0.2 for DIVIDE 1.4 and 4.5', function () {
      expect(calculateNumber('DIVIDE', 1.4, 4.5)).to.equal(0.2);
    });

    it('should return Error when rounded b is 0', function () {
      expect(calculateNumber('DIVIDE', 1.4, 0)).to.equal('Error');
    });

    it('should return Error when b rounds to 0', function () {
      expect(calculateNumber('DIVIDE', 1.4, 0.2)).to.equal('Error');
    });
  });
});
