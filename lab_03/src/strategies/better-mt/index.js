const { randUint32 } = require('../../utils/randInt');
const Queue = require('../../utils/queue');
const MTBreaker = require('./mtBreaker');
const mtFromState = require('./mt-from-state');

function* BetterMTStrategy() {
  const N = 624;
  const queue = new Queue(N);
  for (let i = 0; i < N; i++) {
    const previous = yield randUint32();
    queue.push(previous);
  }

  console.log('Initial state received.');

  let sync = false;
  let mtGetNext;
  do {
    const state = MTBreaker(queue.toArray());
    mtGetNext = mtFromState(state);
    const expected = mtGetNext.next().value;
    const previous = yield expected;

    if (expected === previous) {
      sync = true;
      console.log('Mersenne Twister is broken!');
    } else {
      queue.push(previous);
    }
  } while (!sync);

  while (true) {
    yield mtGetNext.next().value;
  }
}

module.exports = BetterMTStrategy;
