const Utils = {
  calculateNumber(type, a, b) {
    const ra = Math.round(a);
    const rb = Math.round(b);

    if (type === 'SUM') return ra + rb;
    if (type === 'SUBTRACT') return ra - rb;
    if (type === 'DIVIDE') {
      if (rb === 0) return 'Error';
      return ra / rb;
    }
    return 'Error';
  },
};

module.exports = Utils;
