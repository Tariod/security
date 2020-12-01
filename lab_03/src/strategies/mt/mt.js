const toUint32 = require('../../utils/toUint32');

/* Period parameters */
const N = 624;
const M = 397;
const MatrixA = 0x9908b0df;
const UpperMask = 0x80000000;
const LowerMask = 0x7fffffff;

/* Tempering parameters */
const TemperingMaskB = 0x9d2c5680;
const TemperingMaskC = 0xefc60000;

const temperingShiftU = (y) => y >>> 11;

const temperingShiftS = (y) => y << 7;

const temperingShiftT = (y) => y << 15;

const temperingShiftL = (y) => y >>> 18;

const init = (seed) => {
  const state = new Uint32Array(N);
  state[0] = seed;
  for (let i = 1; i < N; i++) {
    const x = state[i - 1] ^ (state[i - 1] >>> 30);
    state[i] =
      ((((x & 0xffff0000) >>> 16) * 1812433253) << 16) +
      (x & 0x0000ffff) * 1812433253 +
      i;
  }
  return state;
};

const twist = (state) => {
  for (let i = 0; i < N; i++) {
    const x = (state[i] & UpperMask) + (state[(i + 1) % N] & LowerMask);
    state[i] = state[(i + M) % N] ^ (x >>> 1);
    state[i] = x & 1 ? state[i] ^ MatrixA : state[i];
  }
  return state;
};

function* mt(seed = Date.now()) {
  const state = init(seed);

  do {
    twist(state);

    for (let i = 0; i < N; i++) {
      let y = state[i];
      y ^= temperingShiftU(y);
      y ^= temperingShiftS(y) & TemperingMaskB;
      y ^= temperingShiftT(y) & TemperingMaskC;
      y ^= temperingShiftL(y);
      yield toUint32(y);
    }
  } while (true);
}

module.exports = mt;
