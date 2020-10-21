const lcg = require('./lcg');
const { randInt32 } = require('../../utils/randInt');

function* LSGStrategy(increment, multiplier, modulus) {
  const lcgGetNext = lcg.bind(null, increment, multiplier, modulus);
  let previous = null;
  while (true) {
    const next = previous !== null ? lcgGetNext(previous) : randInt32();
    previous = yield next;
  }
}

module.exports = LSGStrategy;
