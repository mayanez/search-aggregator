var irc = require('xdcc').irc;
var ProgressBar = require('progress');

var myArgs = process.argv.slice(2);

if (myArgs.length < 4) {
  console.log("Usage: xdcc <server> <channel> <bot> <pack>");
  process.exit(1);
}

var user = 'desu' + Math.random().toString(36).substr(7, 3);
var server = myArgs[0];
var channel = "#"+myArgs[1];
var hostUser = myArgs[2], pack = parseInt(myArgs[3]), progress;

console.log('Connecting...');
var client = new irc.Client(server, user, {
  channels: [ channel ],
  userName: user,
  realName: user
});

client.on('join', function(channel, nick, message) {
  if (nick !== user) return;
  console.log('Joined', channel);
  client.getXdcc(hostUser, 'xdcc send #' + pack, '.');
});

client.on('xdcc-connect', function(meta) {
  console.log('Connected: ' + meta.ip + ':' + meta.port);
  progress = new ProgressBar('Downloading... [:bar] :percent, :etas remaining', {
    incomplete: ' ',
    total: meta.length,
    width: 20
  });
});

var last = 0;
client.on('xdcc-data', function(received) {
  progress.tick(received - last);
  last = received;
});

client.on('xdcc-end', function(received) {
  console.log('COMPLETE');
  process.exit(0);
});

client.on('notice', function(from, to, message) {
  if (to == user && from == hostUser) {
    console.log("NOTICE");
    process.exit(1);
  }
});

client.on('error', function(message) {
  console.error("ERROR");
  process.exit(1);
});
