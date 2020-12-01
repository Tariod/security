const { randUint32 } = require('../utils/randInt');

function* DefaultStrategy() {
  while (true) {
    yield randUint32();
  }
}

module.exports = DefaultStrategy;
