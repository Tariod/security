const undoRightShift = (y, shift) => {
  let x = y;
  for (let i = shift; i < 32; i += shift) {
    x ^= y >>> i;
  }
  return x;
};

const undoLeftShift = (y, shift, mask) => {
  let x = y;
  let window = (1 << shift) - 1;
  for (let i = 0; i < Math.floor(32 / shift); i++) {
    x ^= ((window & x) << shift) & mask;
    window <<= shift;
  }

  return x;
};

const untempering = (y) => {
  y = undoRightShift(y, 18);
  y = undoLeftShift(y, 15, 0xefc60000);
  y = undoLeftShift(y, 7, 0x9d2c5680);
  y = undoRightShift(y, 11);
  return y;
};

function MTBreaker(state) {
  for (let i = 0; i < state.length; i++) {
    state[i] = untempering(state[i]);
  }
  return state;
}

module.exports = MTBreaker;
