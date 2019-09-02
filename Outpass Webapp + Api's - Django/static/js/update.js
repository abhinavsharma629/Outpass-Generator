function update() {
  $("#notifications1").html("")
  $.ajax({
    type: "GET",
    url: "http://127.0.0.1:8000/student/pendingRequests?typeOfRequest='S'",
    headers: {
      Authorization: "Bearer " + access_token
    },
    success: function(data) {
      console.log(data);
      var sent = JSON.parse(data.sent_requests);
      if (sent.length > 0) {
        console.log("Pending Requests Persists");

        if (sent[0]["typeOfRequest"] === "S") {
          $("#warden").append(
            `<option value="` +
              sent[0]["receiver"] +
              `" selected>` +
              sent[0]["receiver"] +
              ` - Pending</option>`
          );
          $("#warden").attr("disabled", true);
        }
      }
      colleges();

    }
  });
}

function colleges() {
  $.ajax({
    type: "GET",
    url: "http://127.0.0.1:8000/student/registeredColleges",
    success: function(data) {
      var colleges = JSON.parse(data.college_list);
      for (var i = 0; i < colleges.length; i++) {
        var makeName =
          colleges[i]["shortHand"] + " - " + colleges[i]["fullName"];
        $("#college").append(
          `<option value="` +
            colleges[i]["shortHand"]+
            `">` +
            makeName +
            `</option>`
        );
      }

      $("#college").change(function() {
        //console.log($("#college option:selected").html().split("-")[1])
        console.log($("#college").val())
        try {
          warden(
            "",
            $("#college").val()
              .trim()
          );
        } catch {
          $("#warden").html("");
          $("#warden").append(
            `<option selected value="">Choose Warden..</option>`
          );
        }
      });
      details();
    }
  });
}

function warden(currentWarden, college) {

  $.ajax({
    type: "GET",
    url: "http://127.0.0.1:8000/student/collegeWardens?college=" + college,
    success: function(data) {
      console.log("Priting Warden List");
      console.log(JSON.parse(data.warden_list));
      var wardens = JSON.parse(data.warden_list);
      $("#warden").html("");
      $("#warden").append(`<option selected value="">Choose Warden..</option>`);
      for (var i = 0; i < wardens.length; i++) {
        var makeName =
          wardens[i]["first_name"] +
          " " +
          wardens[i]["last_name"];

        $("#warden").append(
          `<option value="` +
            wardens[i]["er_no"] +
            `">` +
            makeName +
            `</option>`
        );
      }
      if($("#warden").val()){
          $("#warden").val($("#warden").val())
      }
      else{
        $("#warden").val(currentWarden);
      }


    }
  });
}

function details() {
  $.ajax({
    type: "GET",
    url: "http://127.0.0.1:8000/student/studentDetails",
    headers: {
      Authorization: "Bearer " + access_token
    },
    success: function(data) {
    var ward=JSON.parse(data.warden)
      var student = JSON.parse(data.student_details);
      console.log(student);


      $("#er_no").val(student[0]["er_no"]);
      //$('#signature': dataURL,
      $("#bed_no").val(student[0]["bed_no"]);
      $("#hostel").val(student[0]["hostel"]);
      $("#room_no").val(student[0]["room_no"]);
      $("#year").val(student[0]["year"]);
      $("#sem1").val(student[0]["semester"]);
      $("#branch").val(student[0]["branch"]);
      $("#parent").val(student[0]["parent"]);
      try{
      $("#parent_contact").val(student[0]["parent_contact"].substr(3));

      $("option[value='" + student[0]["warden"] + "']").attr("selected", true);
      $("#gridCheck").attr("checked", true);
      //  $("#warden").val(student[0]['warden']['user'])

      if (student[0]["college"]["shortHand"]) {
        var makeName = (
          student[0]["college"]["shortHand"] +
          " - " +
          student[0]["college"]["fullName"] +
          "..."
        ).substr(0, 38);
        $("option[value='" + student[0]["college"]["shortHand"] + "']").attr(
          "selected",
          true
        );

        try{
          var er=ward[0]['er_no']
        }
        catch{
          var er=null;
        }
        warden(er, student[0]["college"]["fullName"]);
      }
    }
    catch{
      console.log("No Parent")
    }

      var context = document.getElementById("signature-pad").getContext("2d");
      var image = new Image();

      function drawPattern() {
        context.fillStyle = context.createPattern(image, "repeat");
        context.fillRect(0, 0, 300, 300);
      }

      image.src = student[0]["signature"];
      image.onload = drawPattern;
      $("#load").hide();
      $("#main1111").removeClass("blur");


    }
  });
}
