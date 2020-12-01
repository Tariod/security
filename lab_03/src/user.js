const { DefaultStrategy } = require('./strategies');
const { UserService } = require('./services');

class User {
  static async create() {
    const { id, money, deletionTime } = await UserService.createUser(0);
    return new User(id, money, deletionTime);
  }

  static getBetSize(isSuccessful, bet) {
    return isSuccessful ? Math.min(bet * 2, 1000) : Math.ceil(bet / 2);
  }

  static log(game, message, money, number, realNumber) {
    console.log('='.repeat(20));
    console.log(
      `Game: ${game}\n` +
        `Message: ${message}\n` +
        `Money: ${money}\n` +
        `Guess: ${number} Real number: ${realNumber}`
    );
  }

  constructor(id, money, deletionTime) {
    this._id = id;
    this._money = money;
    this._deletionTime = deletionTime;
    this._bet = 1;
  }

  get game() {
    return this._game;
  }

  set game(game) {
    this._game = game;
  }

  async win(strategy = DefaultStrategy()) {
    if (this._game === null) {
      throw new Error('No game selected');
    }

    let { value: number, done } = strategy.next(null);
    while (
      this._money < 1000000 &&
      this._money > 0 &&
      this._deletionTime > new Date() &&
      !done
    ) {
      const result = await this._game.play(this._id, this._bet, number);
      const { message, money, realNumber } = result;

      this._money = money;
      this._bet = User.getBetSize(number === realNumber, this._bet);

      User.log(this._game.name, message, money, number, realNumber);

      ({ value: number, done } = strategy.next(realNumber));
    }

    return `Your balance ${this._money}`;
  }

  async spendMillion() {
    if (this._game === null) {
      throw new Error('No game selected');
    }

    const strategy = DefaultStrategy();
    const { value: number } = strategy.next(null);
    const result = await this._game.play(this._id, 1000000, number);
    const { message, money, realNumber } = result;
    this._money = money;
    this._bet = User.getBetSize(number === realNumber, this._bet);

    User.log(this._game.name, message, money, number, realNumber);

    return `Your balance ${this._money}`;
  }
}

module.exports = User;
