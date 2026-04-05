const http = require('node:http');

const port = Number(process.env.PORT || 3000);

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain; charset=utf-8' });
  res.end('Hello from a simple Node.js app!\n');
});

server.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});