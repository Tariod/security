'use strict';

const fs = require('fs');

const ALPHABET_SIZE = 256;

const decode = (msg, key) =>
  msg
    .split('')
    .map((symbol) => symbol.charCodeAt(0) ^ key)
    .map((symbol) => String.fromCharCode(symbol))
    .join('');

const msg = fs.readFileSync('lab_01/part_01/encoded.txt').toString();
console.log('Encoded message: ' + msg);

const results = [];
for (let i = 1; i < ALPHABET_SIZE; i++) {
  results.push(decode(msg, i));
}

fs.writeFileSync(
  'lab_01/part_01/brute-force.txt',
  results.map((msg, key) => `Key ${key + 1}: ${msg}`).join('\n')
);
