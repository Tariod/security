const mt = require('./mt');
const { randUint32 } = require('../../utils/randInt');

const secondsSinceEpoch = () => {
  return Math.floor(Date.now() / 1000);
};

function* MTStrategy(start = secondsSinceEpoch(), seed) {
  let skip = 0;
  if (!seed) {
    const attempts = 5;
    skip = 5;
    const buffer = [];
    for (let i = 0; i < attempts; i++) {
      const previous = yield randUint32();
      buffer.push(previous);
    }

    for (let tempSeed = start; tempSeed !== 0; tempSeed--) {
      if (tempSeed % 1000 === 0) {
        console.log(`TempSeed: ${tempSeed}`);
      }
      const tempMTGetNext = mt(tempSeed);
      let status = true;
      for (let i = 0; i < attempts; i++) {
        const temp = tempMTGetNext.next().value;
        if (temp !== buffer[i]) {
          status = false;
          break;
        }
      }

      if (status) {
        seed = tempSeed;
        console.log(`Seed: ${new Date(seed * 1000)}`);
        break;
      }
    }
  }

  const mtGetNext = mt(seed);
  for (let i = 0; i < skip; i++) {
    mtGetNext.next();
  }
  while (true) {
    yield mtGetNext.next().value;
  }
}

module.exports = MTStrategy;
