function history() {
  if ($("#history1").html()) {
    $("#profile1").attr("style", "display:none;");
    $("#request11").attr("style", "display:none;");
    $("#notifications1").attr("style", "display:none;");
    $("#history1").attr("style", "display:block;");
    $("#overview1").attr("style", "display:none;");
    $("#makeWarden1").attr("style", "display:none;");
    $("#myoutpass1").attr('style', "display:none;");
  } else {
    $("#load").show();
    $("#main1111").attr("class","blur");
    $("#profile1").attr("style", "display:none;");
    $("#request11").attr("style", "display:none;");
    $("#notifications1").attr("style", "display:none;");
    $("#history1").attr("style", "display:block;");
    $("#overview1").attr("style", "display:none;");
    $("#makeWarden1").attr("style", "display:none'");
    $("#myoutpass1").attr('style', "display:none;");

    $.ajax({
      url: "http://127.0.0.1:8000/warden/acceptedOutpassRequests",
      type: "GET",
      headers: {
        Authorization: "Bearer " + access_token
      },
      success: function(data) {
        var pending_outpasses = JSON.parse(data.pending_outpasses);
        console.log(pending_outpasses);
        var html = "";
        //$("#1").html(html);
        for (var i = 0; i < pending_outpasses.length; i++) {
          var from = pending_outpasses[i]["fromDate"];
          var to = pending_outpasses[i]["toDate"];
          var id = pending_outpasses[i]["outpassId"];
          var purpose = pending_outpasses[i]["purposeOfLeave"];
          from = moment(from).format("DD-MMM-YYYY");
          to = moment(to).format("DD-MMM-YYYY");

          if (pending_outpasses[i]["isEmergency"] == true) {
            html +=
              `<div class="card" id="card-` +
              id +
              `" style="background-color:#ff8080;">`;
          } else {
            html += `<div class="card" id="card-` + id + `" >`;
          }

          html +=
            `<h5>` +
            pending_outpasses[i]["student"]["other_details"]["first_name"] +
            ` ` +
            pending_outpasses[i]["student"]["other_details"]["last_name"] +
            ` &emsp; :- ` +
            pending_outpasses[i]["student"]["user"] +
            `</h5>
              <div class="title"><b>From:- </b> ` +
            from +
            ` &emsp;<b>To:- </b> ` +
            to +
            `</div>
              <div class="desc">` +
            purpose +
            `</div>
              <div class="actions" id="` +
            id +
            `">`;

          html += `<button class="view" id="view"><i class="fa fa-eye"></i><b>View Outpass</b></button>`;
          if (pending_outpasses[i]["whatsappImg"] !== null) {
            html += `<button class="view1" id="view1"><i class="fa fa-image"></i><b>ScreenShot</b></button>`;
          } else {
            html += `<button class="view11" id="view11" style="cursor: not-allowed;"><i class="fa fa-times-rectangle"></i><b>No ScreenShot</b></button>`;
          }
          html +=
            `
              </div>
              <img src="` +
            pending_outpasses[i]["student"]["photo"] +
            `" class="profile-img" />

            </div>
            <br>
            <br>
              `;
        }

        $("#history1").html(html);
        $("#load").hide();
        $("#main1111").removeClass("blur");

        $(".view").click(function() {
          $("#load").show();
          $("#main1111").attr("class","blur");
          console.log("View");
          var id = $(this)
            .parent()
            .attr("id");

          $.ajax({
            url: "http://127.0.0.1:8000/student/outpassDetails?id=" + id,
            type: "GET",
            headers: {
              Authorization: "Bearer " + access_token
            },
            success: function(data) {
              console.log(data);
              var outpassDetails = JSON.parse(data.details);
              console.log(outpassDetails);

              $("#purposeOfLeave").val(outpassDetails[0]["purposeOfLeave"]);
              $("#addressWhileLeave").val(
                outpassDetails[0]["addressWhileLeave"]
              );
              $("#fromDate").val(outpassDetails[0]["fromDate"]);
              $("#toDate").val(outpassDetails[0]["toDate"]);
              $("#num_of_days").val(outpassDetails[0]["no_of_days"]);
              $("#isEmergency").attr(
                "checked",
                outpassDetails[0]["isEmergency"]
              );
              $("#exampleModal2").modal("toggle");
              $("#load").hide();
              $("#main1111").removeClass("blur");
            }
          });
        });

        $(".view1").click(function() {
          $("#load").show();
          $("#main1111").attr("class","blur");
          console.log("View");
          var id = $(this)
            .parent()
            .attr("id");

          $.ajax({
            url: "http://127.0.0.1:8000/student/outpassDetails?id=" + id,
            type: "GET",
            headers: {
              Authorization: "Bearer " + access_token
            },
            success: function(data) {
              console.log(data);
              var outpassDetails = JSON.parse(data.details);
              console.log(outpassDetails);

              $("#exampleModal").modal("toggle");
              document.getElementById("start").classList.add("hidden");
              document.getElementById("response").classList.remove("hidden");
              document.getElementById("notimage").classList.add("hidden");
              // Thumbnail Preview
              $("#file-image").removeAttr("class");
              $("#file-image").attr("src", outpassDetails[0]["whatsappImg"]);
              $("#load").hide();
              $("#main1111").removeClass("blur");
            }
          });
        });
      }
    });
  }
}
