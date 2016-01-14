const app = require('./app');

const RoomControlCli = module.exports;

RoomControlCli.run = function (args) {
  const port = process.env.port || 9000;

  console.log('Received', args);

  app.listen(port, () => {
    console.log('Running roomcontrol on port', port, '!');
  });
};
