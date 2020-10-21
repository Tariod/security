const lcg = require('./lcg');
const lcgBreaker = require('./lcgBreaker');
const { randInt32 } = require('../../utils/randInt');
const { isSomeEmpty, isEveryEmpty } = require('../../utils/isEmpty');

function* LCGStrategy(increment, multiplier, modulus) {
  let previous = randInt32();
  if (isSomeEmpty(increment, multiplier, modulus)) {
    const buffer = [];
    for (let i = 0; i < 5; i++) {
      previous = yield randInt32();
      buffer.push(previous);
    }

    let successfulAttempts = 0;
    while (successfulAttempts !== 2) {
      if (isSomeEmpty(increment, multiplier, modulus)) {
        ({ increment, multiplier, modulus } = lcgBreaker(buffer));
      }

      let expected = randInt32();
      if (!isEveryEmpty(increment, multiplier, modulus)) {
        expected = lcg(increment, multiplier, modulus, previous);
      }

      previous = yield expected;
      buffer.push(previous);

      if (expected !== previous) {
        successfulAttempts = 0;
        [increment, multiplier, modulus] = [null, null, null];
      } else {
        successfulAttempts++;
      }
    }
  }

  const lcgGetNext = lcg.bind(null, increment, multiplier, modulus);
  while (true) {
    previous = yield lcgGetNext(previous);
  }
}

module.exports = LCGStrategy;
