#!/usr/bin/env node

const path = require('path');
const RoomControlCli = require(path.resolve(__dirname, '../lib/cli'));

process.title = 'roomcontrol';

RoomControlCli.run(process.argv);
