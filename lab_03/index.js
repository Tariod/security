const Game = require('./src/game');
const LCGStrategy = require('./src/strategies/lcg');
const User = require('./src/user');

(async () => {
  try {
    const user = await User.create();
    console.log(user);

    const lcg = new Game('Lcg');
    // const strategy = LCGStrategy(1013904223, 1664525, 4294967296);
    const strategy = LCGStrategy();

    user.game = lcg;

    const result = await user.win(strategy);
    console.log(result);

    // const mt = new Game('Mt');
    // const betterMT = new Game('BetterMt');
  } catch (error) {
    console.error(error);
  }
})();
