const { abs, mod, sign } = require('../../utils/math');
const swap = require('../../utils/swap');

const gcd = (first, second) => {
  return second !== 0n ? gcd(second, mod(first, second)) : abs(first);
};

const egcd = (a, b) => {
  let [lastRemainder, remainder] = [abs(a), abs(b)];
  // eslint-disable-next-line
  let x = 0n, lastX = 1n, y = 1n, lastY = 0n;
  while (remainder !== 0n) {
    const quotient = lastRemainder / remainder;
    [remainder, lastRemainder] = swap(remainder, mod(lastRemainder, remainder));
    [x, lastX] = swap(x, lastX - quotient * x);
    [y, lastY] = swap(y, lastY - quotient * y);
  }

  return [lastRemainder, lastX * sign(a), lastY * sign(b)];
};

const modinv = (first, modulus) => {
  const [g, second] = egcd(first, modulus);
  if (g !== 1n) {
    const err = new Error(`Modular inverse for ${first} does not exist`);
    err.code = 449;
    throw err;
  }
  return mod(second, modulus);
};

const crackIncrement = (state, modulus, multiplier) => {
  const increment = mod(state[1] - state[0] * multiplier, modulus);
  return [modulus, multiplier, increment];
};

const crackMultiplier = (state, modulus) => {
  const multiplier = mod(
    (state[2] - state[1]) * modinv(state[1] - state[0], modulus),
    modulus
  );

  return [state, modulus, multiplier];
};

const crackModulus = (state) => {
  const tn = [];
  for (let i = 0; i < state.length - 1; i++) {
    tn.push(state[i + 1] - state[i]);
  }

  const un = [];
  for (let i = 0; i < tn.length - 2; i++) {
    un.push(abs(tn[i + 2] * tn[i] - tn[i + 1] * tn[i + 1]));
  }

  const modulus = un.reduce(gcd);
  return [state, modulus];
};

function LCGBreaker(state) {
  const stateBigInt = state.map(BigInt);
  try {
    const [modulus, multiplier, increment] = crackIncrement(
      ...crackMultiplier(...crackModulus(stateBigInt))
    );

    console.log(
      `Modulus: ${modulus}, Multiplier: ${multiplier}, Increment: ${increment}`
    );
    return {
      modulus: parseInt(modulus),
      multiplier: parseInt(multiplier),
      increment: parseInt(increment),
    };
  } catch (err) {
    if (err.code && err.code === 449) {
      return { increment: null, multiplier: null, modulus: null };
    }
    console.error(err);
  }
}

module.exports = LCGBreaker;
