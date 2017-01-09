var fs = require('fs');
var argv = require('yargs').argv;
var jsonfile = require('jsonfile');
var nodejieba = require("nodejieba");

var IN_FOLDER_PATH = '../data/';
var IN_LABEL_FOLDER_PATH = '../label/';
var OUT_FOLDER_PATH = '../processed-data/';

function main() {

  /* Argv handling */
  if (argv.f) {
    var filename = argv.f;

    prepareToProcess(filename);

  } else {
    console.log('No specified -f (<filename>.json) argument.');
    console.log('Example usage: node preprocess.js -f 唐伯虎點秋香.json');
  }
}

/* Read jsonfile from specified file path, then process it */
function prepareToProcess(filename) {

  var filepath = IN_FOLDER_PATH + filename;
  var labelpath = IN_LABEL_FOLDER_PATH + filename.replace('json', 'txt');
  var outpath = OUT_FOLDER_PATH + filename;

  // read labels first
  console.log('Reading label text file: ' + labelpath);
  fs.readFile(labelpath, 'utf8', function(err, labelText) {

    // handle error
    if (err)
      console.log('No corresponding label data: "' + labelpath + '", ignore labeling.');

    // process label text file
    var highlightTimeRanges = (!err) ? processlabelText(labelText) : null

    // process and label data.
    console.log('Processing "' + filepath + '"...');
    jsonfile.readFile(filepath, function(err, json) {

      if (err) {
        console.log('Read file error. Please check your file path.')
        console.log('Note that your file must be placed in "' + filepath + '"');
        return;
      }

      json = process(json, highlightTimeRanges);

      writeFile(outpath, json);
    });
  });
}

/* Main data processing pipline */
function process(json, highlightTimeRanges) {

  // sort comments by time (sync with video)
  json.comments = sortCommentsByTime(json.comments);

  // for each comment
  json.comments = json.comments.map(function(comment) {

    // delete unwanted property
    delete comment.dbid;
    delete comment.hash;
    delete comment.pool;
    delete comment.mode;
    delete comment.fontsize;
    delete comment.fontcolor;
    delete comment.sendtime;

    // label comment
    if (highlightTimeRanges)
      comment.class = isTimeInRanges(comment.time, highlightTimeRanges) ? 'POS' : 'NEG';

    // covert time(second) to 'hh:mm:ss', and assign to new property 'timestamp' (for debug-friendly)
    comment.timestamp = secondTohhmmss(comment.time);

    // extract keywords from comments, and assign to new property 'keywords'
    comment.keywords = nodejieba.extract(comment.content, 100);

    // cut text to array of words
    comment.words = nodejieba.cut(comment.content, false);

    // normalize noise words
    comment.words = normalizeNoiseWords(comment.words, comment.keywords);

    return comment;
  });

  return json;
}

function sortCommentsByTime(comments) {
  return comments.sort(function(a,b) {
    return a.time - b.time;
  });
}

function secondTohhmmss(second) {
  var h = Math.floor(second / 3600);
  var m = Math.floor(second % 3600 / 60);
  var s = Math.floor(second % 3600 % 60);
  return ((h > 9) ? h : '0' + h) + ':' + ((m > 9) ? m : '0' + m) + ':' + ((s > 9) ? s : '0' + s);
}

function hhmmssToSecond(hhmmss) {
  // split it at the colons
  var time = hhmmss.split(':');
  // minutes are worth 60 seconds. Hours are worth 60 minutes.
  return (+time[0]) * 60 * 60 + (+time[1]) * 60 + (+time[2]);
}

function normalizeNoiseWords(words, keywords) {
  keywords = keywords.map(function(keywords) { return keywords.word; });
  return words
    /* Cleaning stopwords, only keep word that is keyword */
    .filter(function(word) { return keywords.indexOf(word) != -1; })
    /* Stemming, e.g., convert different length of "233333” and "哈哈哈哈哈哈" to one single "哈" */
    .map(function(word) {
      word = word.replace(new RegExp('a+'), '哈');
      word = word.replace(new RegExp('W+'), '哈');
      word = word.replace(new RegExp('w+'), '哈');
      word = word.replace(new RegExp('H+'), '哈');
      word = word.replace(new RegExp('h+'), '哈');
      word = word.replace(new RegExp('Yo+'), '哈');
      word = word.replace(new RegExp('YO+'), '哈');
      word = word.replace(new RegExp('yo+'), '哈');
      word = word.replace(new RegExp('6+'), '哈');
      word = word.replace(new RegExp('23+'), '哈');
      word = word.replace(new RegExp('3+'), '哈');
      word = word.replace(new RegExp('呵+'), '哈');
      word = word.replace(new RegExp('哈+'), '哈');
      word = word.replace(new RegExp('啊+'), '啊');
      return word;
    });
}

function processlabelText(labelText) {
  var highlightTimeRanges = [];
  labelText.replace('\r', '');
  labelText.split('\n').forEach(function(row) {
    if (row == '') return;
    time = row.split(' ');
    highlightTimeRanges.push({
      starttime: hhmmssToSecond(time[0]),
      endtime: hhmmssToSecond(time[1])
    });
  });

  return highlightTimeRanges;
}

function isTimeInRanges(time, ranges) {
  for (var i = 0; i < ranges.length; i++)
    if (ranges[i].starttime <= time && time <= ranges[i].endtime)
      return true;
  return false;
}

function writeFile(outpath, json) {

  jsonfile.spaces = 4;

  jsonfile.writeFile(outpath, json, function(err) {
    if (err) {
      console.log('Write file error: "' + outpath + '"');
      console.log('Please make a folder: "' + OUT_FOLDER_PATH + '" first.');
      return;
    }
    console.log('Process success. Write file to "' + outpath + '"');
  });
}

main();
