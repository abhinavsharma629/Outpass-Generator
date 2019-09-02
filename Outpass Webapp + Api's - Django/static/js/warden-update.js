function colleges() {
  $("#load").show();
  $("#main1111").attr("class","blur");
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
            colleges[i]["shortHand"] +
            `">` +
            makeName +
            `</option>`
        );
      }

      $("#college").change(function() {
        console.log("College Changed")
      });
      details();

    }
  });
}


function details() {
  $.ajax({
    type: "GET",
    url: "http://127.0.0.1:8000/warden/wardenDetails",
    headers: {
      Authorization: "Bearer " + access_token
    },
    success: function(data) {
      var warden = JSON.parse(data.warden_details);
      console.log(warden);

      $("#er_no").val(warden[0]["er_no"]);
      $("#hostel").val(warden[0]["hostel"]);
      $("#year").val(warden[0]["year"]);
      $("#sem1").val(warden[0]["semester"]);
      $("#gridCheck").attr("checked", true);

      try{
      if (warden[0]["college"]["shortHand"]) {
        var makeName = (
          warden[0]["college"]["shortHand"] +
          " - " +
          warden[0]["college"]["fullName"] +
          "..."
        ).substr(0, 38);
        $("option[value='" + warden[0]["college"]["shortHand"] + "']").attr(
          "selected",
          true
        );
      }
    }
    catch{
      console.log("No Details")
    }

      var context = document.getElementById("signature-pad").getContext("2d");
      var image = new Image();

      function drawPattern() {
        context.fillStyle = context.createPattern(image, "repeat");
        context.fillRect(0, 0, 300, 300);
      }

      image.src = warden[0]["signature"];
      image.onload = drawPattern;

      document.getElementById('start').classList.add("hidden");
      document.getElementById('response').classList.remove("hidden");
      document.getElementById('notimage').classList.add("hidden");
      // Thumbnail Preview
      document.getElementById('file-image').classList.remove("hidden");
      document.getElementById('file-image').src = warden[0]['id_card']
      $("#load").hide();
      $("#main1111").removeClass("blur");

    }
  });
}
