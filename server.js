const http = require('http');
const express = require('express');
const app = express();

// Serve the index.html file as the default page
app.get('/', (request, response) => {
  response.sendFile(__dirname + '/index.html');
});

const server = http.createServer(app);
server.listen(process.env.PORT);