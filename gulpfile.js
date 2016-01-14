const childProcess = require('child_process')
    , eslint = require('gulp-eslint')
    , gls = require('gulp-live-server')
    , gulp = require('gulp')
		, istanbul = require('gulp-istanbul')
    , mocha = require('gulp-mocha');

const exec = childProcess.exec;

gulp.task('lint', () => {
  return gulp.src(['*.js', '!node_modules/**'])
    .pipe(eslint())
    .pipe(eslint.format())
    .pipe(eslint.failAfterError());
});

gulp.task('pre-test', () => {
  return gulp.src(['lib/**/*.js'])
    .pipe(istanbul())
    .pipe(istanbul.hookRequire());
});

gulp.task('test', ['lint', 'pre-test'], () => {
  return gulp.src(['test/**/*_test.js'])
    .pipe(mocha())
    .pipe(istanbul.writeReports())
    .pipe(istanbul.enforceThresholds({thresholds: {global: 85}}));  // TODO: increase coverage
});

gulp.task('coverage', ['test'], () => {
  exec('open coverage/lcov-report/index.html');
});

gulp.task('serve', () => {
  const server = gls.new('bin/roomcontrol.js');
  server.start();
  gulp.watch(['bin/roomcontrol.js', 'lib/**/*.js'], server.start.bind(server));
});

gulp.task('default', ['serve']);
