const api = require('../utils/api');

const getUser = (id) =>
  api.get('/createacc', { params: { id } }).catch((error) => {
    if (error.response && error.response.status === 409) {
      return getUser(id + 1);
    }

    throw error;
  });

const createUser = async (initialID) => {
  const {
    data: { id, money, deletionTime },
  } = await getUser(initialID);

  return { id, money, deletionTime: new Date(deletionTime) };
};

module.exports = {
  createUser,
};
