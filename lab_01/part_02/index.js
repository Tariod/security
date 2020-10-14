'use strict';

const fs = require('fs');

const msg = fs.readFileSync('lab_01/part_02/encoded.txt').toString();

console.log('Encoded message length: ' + msg.length);

const uniqueValues = msg
  .split('')
  .filter((symbol, index) => msg.indexOf(symbol) === index);
console.log('Unique values:');
console.dir(uniqueValues); // hex

const msgUINT8 = Array.from(msg.match(/.{2}/g).map((hex) => parseInt(hex, 16)));
console.log('Encoded message in utf-8 length: ' + msgUINT8.length);

// const alphabet = msgUINT8.filter(
//   (symbol, index) => msgUINT8.indexOf(symbol) === index
// );
// console.log('Alphabet size: ' + alphabet.length);

const coincidenceIndex = (msg) => {
  const msgLength = msg.length;
  const count = msg.reduce((acc, symbol) => {
    if (acc[symbol] === undefined) acc[symbol] = 0;
    acc[symbol] += 1;
    return acc;
  }, {});

  const res = Object.values(count).reduce(
    (ic, quantity) => ic + (quantity * quantity) / (msgLength * msgLength - 1),
    0
  );

  return res;
};

console.log('Coincidence index: ' + coincidenceIndex(msgUINT8));
console.log('='.repeat(20));

for (let padding = 2; padding < 13; padding++) {
  console.log('Key size: ' + padding);
  console.log(
    'Coincidence index: ' +
      coincidenceIndex(msgUINT8.filter((_, index) => index % padding === 0))
  );
}

console.log('='.repeat(20));
console.log('Key size: 3 or 6 or 9 or 12');

// const ALPH_SIZE = 256;
// const KEY_SIZE = 3;

// const relativeCoincidenceIndex = (msg, keySize, offset) => {
//   const first = msg.filter((_, index) => index % keySize === 0);
//   const firstLen = first.length;

//   const res = [0];
//   for (let rawNumber = 1; rawNumber < keySize; rawNumber++) {
//     const raw = msg.filter((_, index) => index % keySize === rawNumber);
//     const rawLen = raw.length;

//     res.push(
//       new Array(ALPH_SIZE)
//         .fill(0)
//         .map((_, index) => {
//           const pi = first.filter((val) => val === index).length;
//           const pis = raw.filter((val) => val === (index + offset) % ALPH_SIZE)
//             .length;
//           return (pi * pis) / (firstLen * rawLen);
//         })
//         .reduce((acc, val) => acc + val, 0)
//     );
//   }

//   return res;
// };

// const results = {};
// for (let offset = 0; offset < ALPH_SIZE; offset++) {
//   const res = relativeCoincidenceIndex(msgUINT8, KEY_SIZE, offset);
//   results[offset] = res;
// }

// let maxSecondOffset = 0;
// for (let offset = 0; offset < ALPH_SIZE; offset++) {
//   if (results[offset][1] > results[maxSecondOffset][1]) {
//     maxSecondOffset = offset;
//   }
// }
// console.log(
//   `Second offset: ${maxSecondOffset} Value: ${results[maxSecondOffset]}`
// );

// let maxThirddOffset = 0;
// for (let offset = 0; offset < ALPH_SIZE; offset++) {
//   if (results[offset][2] > results[maxThirddOffset][2]) {
//     maxThirddOffset = offset;
//   }
// }
// console.log(
//   `Third offset: ${maxThirddOffset} Value: ${results[maxThirddOffset]}`
// );
// console.log('='.repeat(20));

// const decode = (msg, key) =>
//   msg
//     .map((symbol, index) => {
//       if (index % KEY_SIZE === 1) {
//         return symbol ^ (key + maxSecondOffset) % ALPH_SIZE;
//       }
//       if (index % KEY_SIZE === 2) {
//         return symbol ^ (key + maxThirddOffset) % ALPH_SIZE;
//       }
//       return symbol ^ key;
//     })
//     .map((symbol) => String.fromCharCode(symbol))
//     .join('');

// const decoded = [];
// for (let i = 0; i < ALPH_SIZE; i++) {
//   // console.log(decode(msgUINT8, i));
//   decoded.push(decode(msgUINT8, i));
// }
// fs.writeFileSync(
//   'lab_01/part_02/brute-force.txt',
//   decoded.map((msg, key) => `Key ${key + 0}: ${msg}`).join('\n')
// );
