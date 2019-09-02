$(function() {

    $("#profile").click(function() {
        // console.log($("#profile1").html())
        profile();
        if (!$("#profile1").html()) {
            update();
        }
    })

    $("#notifications").click(function() {
        notifications();
    })

    $("#history").click(function() {
        history();
    })

    $("#request1").click(function() {
      requests()
    })

    $("#overview").click(function() {
      overview()
    })

    $("#makeWarden").click(function(){
      makeWarden();
    })
})
