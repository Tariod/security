const Game = require('./src/game');
const LSGStrategy = require('./src/strategies/lcg');
const User = require('./src/user');

(async () => {
  try {
    const user = await User.create();
    console.log(user);

    const lsg = new Game('Lcg');
    const strategy = LSGStrategy(1013904223, 1664525, 4294967296);

    user.game = lsg;

    const result = await user.win(strategy);
    console.log(result);

    // const mt = new Game('Mt');
    // const betterMT = new Game('BetterMt');
  } catch (error) {
    console.error(error);
  }
})();
