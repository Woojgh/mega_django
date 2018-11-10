$("#greenTab").click(function() {
  if($(this).hasClass("isUp")) {
      $(this).css({'transition':"left linear .5s",'left':"-100px"}).removeClass("isUp")
      $("#greenBody").css({'left':"-1700px"})
  }
    else {
        $(this).css({"transition":"left linear .5s",'left':"690px"})
    .addClass("isUp")
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
    $(this).css({'transition':"left linear .5s",'left':"700px"})
    .addClass("isUp")
    $("#yellowBody").css({'left':"-50px"}) 
  }
});

$("#brownTab").click(function() {
  if($(this).hasClass("isUp")) {
    $(this).css({'transition-delay':".08s",'transition-timing-function':"ease-in",'bottom':"-50px"})
    .removeClass("isUp")
    $("#brownBody").css({'bottom':"-250px"})
  }
  else {
    $(this).css({'transition':"bottom linear .7s",'bottom':"250px"})
    .addClass("isUp")
    $("#brownBody").css({'bottom':"50px"})
  }
});