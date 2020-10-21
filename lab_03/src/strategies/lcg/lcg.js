const toInt32 = require('../../utils/toInt32');

const lcg = (increment, multiplier, modulus, last) => {
  return toInt32((multiplier * last + increment) % modulus);
};

module.exports = lcg;
