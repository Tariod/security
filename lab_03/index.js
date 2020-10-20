'use strict';

const axios = require('axios').create({ baseURL: 'http://95.217.177.249/' });

const getUser = (id) =>
  axios
    .get('/casino/createacc', {
      params: { id },
    })
    .catch((error) => {
      if (error.response && error.response.status === 409) {
        return getUser(id + 1);
      }
      throw error;
    });

const play = (game, id, bet, number) =>
  axios.get(`/casino/play${game}`, {
    params: { id, bet, number },
  });

class User {
  constructor({ id, money, deletionTime }) {
    this.id = id;
    this.money = money;
    this.deletionTime = new Date(deletionTime);
  }

  async winGame(strategy) {
    while (this.money < 1000000 && new Date() < this.deletionTime) {
      this.money += await strategy();
    }
    console.log(`You win ${this.money}`);
  }
}

class Game {
  constructor(name) {
    this.name = name;
  }

  play(id, bet, number) {
    return play(this.name, id, bet, number);
  }
}

(async () => {
  try {
    // const { data } = await getUser(0);
    const data = {
      id: '11',
      money: 1000,
      deletionTime: '2020-10-20T09:54:32.703Z',
    };

    const user = new User(data);
    console.log(user);

    const lsg = new Game('Lcg');
    // const results = [];
    // for (let i = 0; i < 10; i++) {
    //   const { data: res } = await lsg.play(
    //     user.id,
    //     1,
    //     Math.floor(Math.random() * 1000000000)
    //   );
    //   results.push(res.realNumber);
    // }
    // console.log(results);

    const { data: res } = await lsg.play(
      user.id,
      1,
      // Math.floor(3159853902)
      Math.floor(Math.random() * 1000000000)
    );
    console.log(res);

    // const mt = new Game('Mt');
    // const betterMT = new Game('BetterMt');
  } catch (error) {
    console.error(error);
  }
})();
