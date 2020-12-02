const Game = require('./src/game');
const {
  BetterMTStrategy,
  LCGStrategy,
  MTStrategy,
} = require('./src/strategies');
const User = require('./src/user');

(async () => {
  try {
    const user = await User.create();
    console.log(user);

    const lcg = new Game('Lcg');
    const lcgStrategy = LCGStrategy(); // const strategy = LCGStrategy(1013904223, 1664525, 4294967296);
    user.game = lcg;
    const lcgResult = await user.win(lcgStrategy);
    console.log(lcgResult);

    console.log('$'.repeat(40));
    console.log('Spend million');
    console.log(await user.spendMillion());
    console.log('$'.repeat(40));

    const mt = new Game('Mt');
    user.game = mt;
    const mtStrategy = MTStrategy(Math.floor(user._deletionTime / 1000));
    const mtResult = await user.win(mtStrategy);
    console.log(mtResult);

    console.log('$'.repeat(40));
    console.log('Spend million');
    console.log(await user.spendMillion());
    console.log('$'.repeat(40));

    const betterMT = new Game('BetterMt');
    user.game = betterMT;
    const betterMTStrategy = BetterMTStrategy();
    const betterMTResult = await user.win(betterMTStrategy);
    console.log(betterMTResult);
  } catch (error) {
    console.error(error);
  }
})();
