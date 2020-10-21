const isSomeEmpty = (...items) => items.some((item) => !item);

const isEveryEmpty = (...items) => items.every((item) => !item);

module.exports = { isSomeEmpty, isEveryEmpty };
