'use strict';

const fs = require('fs');
const ms = require('ms');

const msg = fs.readFileSync('lab_01/part_02/encoded.txt').toString();

console.log('Encoded message length: ' + msg.length);

const uniqueValues = msg
  .split('')
  .filter((symbol, index) => msg.indexOf(symbol) === index);
console.log('Unique values:');
console.dir(uniqueValues); // hex

const msgUINT8 = Uint8Array.from(
  msg.match(/.{2}/g).map((hex) => parseInt(hex, 16))
);
console.log('Encoded message in utf-8 length: ' + msgUINT8.length);

const alphabet = msgUINT8.filter(
  (symbol, index) => msgUINT8.indexOf(symbol) === index
);
console.log('Alphabet size: ' + alphabet.length);

const coincidenceIndex = (msg) => {
  const msgLength = msg.length;
  const count = msg.reduce((acc, symbol) => {
    if (acc[symbol] === undefined) acc[symbol] = 0;
    acc[symbol] += 1;
    return acc;
  }, {});

  const res = Object.values(count).reduce(
    (ic, quantity) =>
      ic + (quantity * (quantity - 1)) / (msgLength * (msgLength - 1)),
    0
  );

  return res;
};

console.log('Coincidence index: ' + coincidenceIndex(msgUINT8));
