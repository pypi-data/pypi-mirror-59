'use strict';

const {src, dest, watch, series, parallel} = require('gulp');
const sass = require('gulp-sass');
const rename = require('gulp-rename');
const uglify = require('gulp-uglify');
const file = require('gulp-file');
const filesize = require('gulp-filesize');
const fs = require('fs');

const src_scss = './common/static/scss/styles.scss';
const dest_css = './common/static/css';
const dest_js = './common/static/js';

// copy bootstrap css
function copyBootstrapCSS() {
    return src('./node_modules/bootstrap/dist/css/*.min.css').pipe(dest(dest_css));
}

// copy bootstrap js
function copyBootstrapJS() {
    return src('./node_modules/bootstrap/dist/js/*.min.js').pipe(dest(dest_js));
}

// copy resources
exports.copy = series(copyBootstrapCSS, copyBootstrapJS);


// copy bootstrap css
function createCSS() {
    var str = '';
    // return fs.writeFileSync(dest_css + '/styles.css', 'tttttt');
    return file('styles.css', str, {src: true}).pipe(dest(dest_css));
}

function createJS() {
    var str = '';
    // return fs.writeFileSync(dest_js + '/main.js', '1.2.3');
    return file('main.js', str, {src: true}).pipe(dest(dest_js));
}

// create files
exports.create = series(createCSS, createJS);

// compile scss into css
function css() {
    return src(src_scss)
    // .pipe(sass().on('error', sass.logError))
    // .pipe(dest(dest_css))
    // .pipe(filesize())

        .pipe(sass({outputStyle: 'compressed'}).on('error', sass.logError))
        .pipe(rename({suffix: '.min'}))
        .pipe(dest(dest_css))
        .pipe(filesize());
}

exports.css = css;

function watchDefault() {
    // You can use a single task
    watch('./common/static/scss/**/*.scss', css);
    // Or a composed task
    // watch('src/*.js', series(clean, javascript));
}

exports.default = watchDefault;
