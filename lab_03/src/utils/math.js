const mod = (first, second) =>
  first < 0 ? second - (-first % second) : first % second;

const sign = (number) => {
  if (number < 0n) {
    return -1n;
  } else if (number > 0n) {
    return 1n;
  } else {
    return 0n;
  }
};

const abs = (number) => {
  return sign(number) * number;
};

module.exports = { abs, mod, sign };
