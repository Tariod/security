const gcd = (a, b) => {
  if (b) {
    return gcd(b, a % b);
  } else {
    return Math.abs(a);
  }
};

// const egcd = (a, b) => {
//   if (b === 0) {
//     return [1, 0, a];
//   }

//   const [g, x, y] = egcd(b, a % b);
//   return [x, g - Math.floor(a / b) * x, y];
// };

const egcd = (a, b) => {
  let [lastRemainder, remainder] = [Math.abs(a), Math.abs(b)];
  let x = 0;
  let lastX = 1;
  let y = 1;
  let lastY = 0;
  while (remainder !== 0) {
    const tempRemainder = remainder;
    const quotient = Math.floor(lastRemainder / remainder);
    remainder = lastRemainder % remainder;
    lastRemainder = tempRemainder;

    const tempX = x;
    x = lastX - quotient * tempX;
    lastX = tempX;

    const tempY = y;
    y = lastY - quotient * tempY;
    lastY = tempY;
  }

  return [lastRemainder, lastX * (a < 0 ? -1 : 0), lastY * (b < 0 ? -1 : 0)];
};

const modinv = (a, n) => {
  const [g, x] = egcd(a, n);
  if (g !== 1) {
    throw new Error(`Modular inverse for ${a} does not exist`);
  }
  return x % n;
};

const state = new Int32Array([
  492598420,
  -217590045,
  -1348579610,
  -279013107,
  125626120,
  -241443129,
  1569426810,
  1741536913,
  402155196,
  1968640747,
  -1135113394,
]);

const lcg = (increment, multiplier, modulus, last) => {
  return (multiplier * last + increment) % modulus;
};

const crack_increment = (states, modulus, multiplier) => {
  const temp = states[1] - states[0] * multiplier;
  const increment = temp < 0 ? modulus - (-temp % modulus) : temp % modulus;
  return increment;
};

const crack_multiplier = (states, modulus) => {
  const temp =
    BigInt(states[2] - states[1]) *
    BigInt(modinv(states[1] - states[0], modulus));

  const multiplier = parseInt(
    temp < 0
      ? BigInt(modulus) - (-temp % BigInt(modulus))
      : temp % BigInt(modulus)
  );

  return multiplier;
};

const crack_modulus = (states) => {
  const tn = [];
  for (let i = 0; i < states.length - 1; i++) {
    tn.push(states[i + 1] - states[i]);
  }

  const un = [];
  for (let i = 0; i < tn.length - 2; i++) {
    un.push(Math.abs(tn[i + 2] * tn[i] - tn[i + 1] * tn[i + 1]));
  }

  // console.log(un);
  const modulus = un.reduce(gcd);

  return modulus;
};

const modulus = crack_modulus(state);
console.log('Modulus: ' + modulus);

const multiplier = crack_multiplier(state, modulus);
console.log('Multiplier: ' + multiplier);

const increment = crack_increment(state, modulus, multiplier);
console.log('Increment: ' + increment);
const res = lcg(increment, multiplier, modulus, 1224743509);
const temp = new Int32Array(1);
temp[0] = lcg(increment, multiplier, modulus, 1224743509);
console.log('Next: ' + res);
console.log('Next: ' + (res >> 0));
console.log(temp[0]);
