$(function() {

    $("#profile").click(function() {
        // console.log($("#profile1").html())
        profile();
        if (!$("#profile1").html()) {
            update();
        }
    })

    $("#drafts").click(function() {
        drafts();
    })

    $("#notifications").click(function() {
        notifications();
    })

    $("#history").click(function() {
        history();
    })

    $("#outpass").click(function() {
      //console.log("asdasdadsada")
      //console.log(access_token)
      //console.log("asd")
      $.ajax({
          "type": 'GET',
          "url": "http://127.0.0.1:8000/student/isVerified",
          "headers": {
              "Authorization": "Bearer "+access_token
          },
          success: function(data) {
              var message = data.message;
              console.log(message)
              if(message==="Verified"){
                  createOutpass();

              }
              else{
                profile();
                alert("You Have No Warden Assigned Yet!!");
                $("#createOutpass1").html("");
                $("#profile").attr({
                  class: "mdc-list-item mdc-list-item--activated",
                  "aria-selected":true,
                  tabindex:0
                })
                $("#outpass").attr({
                  class: "mdc-list-item",
                  tabindex:-1
                })
                $("#outpass").removeAttr("aria-selected")
              }
            }
          })
        })
})
