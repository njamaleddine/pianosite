// Stop all other audio when current audio is played
try {
  var players = Array.from(document.querySelectorAll('.js-audio-player')).map(function (player) {
    return new Plyr(player, {controls: ['play', 'progress', 'current-time', 'mute', 'volume']})
  });

  players.forEach(function (player) {
    player.on('play', function () {
      var otherPlayers = players.filter(function (otherPlayer) {return otherPlayer != player});
      otherPlayers.forEach(function (otherPlayer) {
        otherPlayer.pause();
      })
    });
  });
} catch (error) {
  console.log(error);
  console.log('Plyr initialization failed, defaulting to html5 audio');

  document.addEventListener('play', function(e){
      var audios = document.getElementsByTagName('audio');
      for(var i = 0, len = audios.length; i < len; ++i){
          if(audios[i] != e.target){
              audios[i].pause();
          }
      }
  }, true);
}
