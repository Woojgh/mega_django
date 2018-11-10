$("#greenTab").click(function() {
  if($(this).hasClass("isUp")) {
      $(this).css({'transition':"left linear .5s",'left':"-90px"}).removeClass("isUp")
      $("#video-change-button").css({'transition':"left linear .5s",'left':"-90px"})
      $("#greenBody").css({'left':"-1700px"})
  }
    else {
        $(this).css({"transition":"left linear .5s",'left':"35em"})
    .addClass("isUp")
        $("#video-change-button").css({'transition':"left linear .5s",'left':"43.1%"})
        $("#greenBody").css({'left':"-50px"})
  }
});

$("#yellowTab").click(function() {
  if($(this).hasClass("isUp")) {
    $(this).css({'transition':"left linear .5s",'transition-timing-function':"ease-in",'left':"-90px"})
    .removeClass("isUp")
    $("#yellowBody").css({'left':"-1700px"}) 
  }
  else {
    $(this).css({'transition':"left linear .5s",'left':"35em"})
    .addClass("isUp")
    $("#yellowBody").css({'left':"-50px"}) 
  }
});

$("#brownTab").click(function() {
  if($(this).hasClass("isUp")) {
    $(this).css({'transition':"left linear .5s",'transition-timing-function':"ease-in",'left':"-90px"})
    .removeClass("isUp")
    $("#brownBody").css({'left':"-1700px"})
  }
  else {
    $(this).css({'transition':"left linear .5s",'left':"35em"})
    .addClass("isUp")
    $("#brownBody").css({'left':"-50px"})
  }
});

$("#video-change-button").click(function() {
    console.log('monkey')
    $('#workaholics').toggleClass("worka")
    $('#salty-bets').toggleClass("worka")
    });

// $("#play-pause-button").click(function() {
//     if(audio.paused)
//     {
//         $("#player-track").addClass('active');
//         checkBuffering();
//         i.attr('class','fas fa-pause');
//         audio.play();
//     }
//     else
//     {
//         $("#player-track").removeClass('active');
//         $('#album-art').removeClass('active');
//         clearInterval(buffInterval);
//         $('#album-art').removeClass('buffering');
//         i.attr('class','fas fa-play');
//         audio.pause();
//     } 
// });
