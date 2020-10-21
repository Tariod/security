const api = require('../utils/api');

const play = (game, id, bet, number) =>
  api.get(`/play${game}`, {
    params: { id, bet, number },
  });

const placeBet = async (game, id, bet, number) => {
  const {
    data: {
      message,
      account: { money },
      realNumber,
    },
  } = await play(game, id, bet, number);

  return { message, money, realNumber };
};

module.exports = {
  placeBet,
};
