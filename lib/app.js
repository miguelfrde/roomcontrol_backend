const bodyParser = require('body-parser')
  , express = require('express')
  , morgan = require('morgan')
  , path = require('path');

const app = express();

app.use(express.static(path.resolve(__dirname, '/public')));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));
app.use(morgan('dev'));

app.get('/', (req, res) => {
  res.send('Hello World!');
});

module.exports = app;
