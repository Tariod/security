const toInt32 = require('./toInt32');

const randInt = (maxVal) => Math.floor(Math.random() * maxVal);

const randInt32 = () => toInt32(randInt(Number.MAX_SAFE_INTEGER));

const randUint32 = () => Math.abs(randInt32());

module.exports = {
  randInt,
  randInt32,
  randUint32,
};
