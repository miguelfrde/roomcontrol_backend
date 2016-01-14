const RoomControlCli = require('../lib/cli')
    , app = require('../lib/app')
    , sinon = require('sinon');

describe('RoomControlCli', () => {
  beforeEach(() => {
    sinon.stub(app, 'listen');
  });

  afterEach(() => {
    app.listen.restore();
  });

  it('starts listening on a given port', () => {
    process.env.port = 8000;
    RoomControlCli.run();
    sinon.assert.calledOnce(app.listen);
    sinon.assert.calledWith(app.listen, process.env.port, sinon.match.func);
    delete process.env.port;
  });

  it('listens on 9000 by default', () => {
    RoomControlCli.run();
    sinon.assert.calledOnce(app.listen);
    sinon.assert.calledWith(app.listen, 9000, sinon.match.func);
  });
});
