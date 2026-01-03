const assert = require('assert');
const calculateNumber = require('./1-calcul');

describe('calculateNumber', function () {
  describe('SUM', function () {
    it('should return 6 for SUM 1.4 and 4.5', function () {
      assert.strictEqual(calculateNumber('SUM', 1.4, 4.5), 6);
    });

    it('should handle rounding up/down correctly', function () {
      assert.strictEqual(calculateNumber('SUM', 1.5, 3.7), 6); // 2 + 4
    });
  });

  describe('SUBTRACT', function () {
    it('should return -4 for SUBTRACT 1.4 and 4.5', function () {
      assert.strictEqual(calculateNumber('SUBTRACT', 1.4, 4.5), -4);
    });

    it('should handle rounding correctly', function () {
      assert.strictEqual(calculateNumber('SUBTRACT', 2.6, 1.2), 2); // 3 - 1
    });
  });

  describe('DIVIDE', function () {
    it('should return 0.2 for DIVIDE 1.4 and 4.5', function () {
      assert.strictEqual(calculateNumber('DIVIDE', 1.4, 4.5), 0.2);
    });

    it('should return Error when rounded b is 0', function () {
      assert.strictEqual(calculateNumber('DIVIDE', 1.4, 0), 'Error');
    });

    it('should also return Error when b rounds to 0', function () {
      assert.strictEqual(calculateNumber('DIVIDE', 1.4, 0.2), 'Error'); // round(0.2)=0
    });
  });
});
