const { randInt32 } = require('../utils/randInt');

function* DefaultStrategy() {
  while (true) {
    yield randInt32();
  }
}

module.exports = DefaultStrategy;
