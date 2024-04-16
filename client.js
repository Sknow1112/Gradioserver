const axios = require('axios');

const client = axios.create({
  baseURL: 'https://1f405b982834104160.gradio.live/',
});

client.post('/chat', {
  message: 'Say hello world.',
})
.then((response) => {
  console.log(response.data);
})
.catch((error) => {
  console.error(error);
});