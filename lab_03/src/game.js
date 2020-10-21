const { BetService } = require('./services');

class Game {
  constructor(name) {
    this._name = name;
  }

  get name() {
    return this._name;
  }

  play(id, bet, number) {
    return BetService.placeBet(this._name, id, bet, number);
  }
}

module.exports = Game;
