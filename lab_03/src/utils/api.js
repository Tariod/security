const axios = require('axios');

const api = axios.create({
  baseURL: 'http://95.217.177.249/casino',
});

module.exports = api;
