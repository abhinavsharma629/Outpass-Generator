function requests() {
  if ($("#request11").html()) {
    $("#profile1").attr("style", "display:none;");
    $("#request11").attr("style", "display:block;");
    $("#notifications1").attr("style", "display:none;");
    $("#history1").attr("style", "display:none;");
    $("#overview1").attr("style", "display:none;");
    $("#makeWarden1").attr("style", "display:none;");
    $("#myoutpass1").attr('style', "display:none;");
  } else {
    $("#load").show();
    $("#main1111").attr("class","blur");
    $("#profile1").attr("style", "display:none;");
    $("#request11").attr("style", "display:block;");
    $("#notifications1").attr("style", "display:none;");
    $("#history1").attr("style", "display:none;");
    $("#overview1").attr("style", "display:none;");
    $("#makeWarden1").attr("style", "display:none;");
    $("#myoutpass1").attr('style', "display:none;");

    $.ajax({
      url: "http://127.0.0.1:8000/warden/pendingOutpassRequests",
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
            pending_outpasses[i]["student"]["er_no"] +
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
          if (pending_outpasses[i]["approved_by_warden"] === false) {
            html += `
                <button class="remove" id="remove"><i class="fa fa-trash"></i></i><b>Cancel Outpass</b></button>
                <button class="close1" id="close"><i class="fa fa-times"></i></button>
                <button class="generateP" id="generateP"><i class="fa fa-check"></i><b>Accept</b></button>&nbsp;`;
          }
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

        $("#request11").html(html);
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
              if(data.status==="200"){
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
            else if (data.status === "404") {
              $("#card-" + id)
                .next()
                .remove();
              $("#card-" + id)
                .next()
                .remove();
              $("#card-" + id).remove();
              $("#history1").html("");
              $("#overview1").html("");
              $("#load").hide();
              $("#main1111").removeClass("blur");
              alert("It Seems That The Student Deleted The Outpass!!");
            }
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
              if(data.status==="200"){
              var outpassDetails = JSON.parse(data.details);
              console.log(outpassDetails);

              $("#exampleModal").modal("toggle");
              document.getElementById("start").classList.add("hidden");
              document.getElementById("response").classList.remove("hidden");
              document.getElementById("notimage").classList.add("hidden");
              // Thumbnail Preview
              $("#file-image").removeAttr("class");
              $("#file-image").attr("src", outpassDetails[0]["whatsappImg"]);
            }
            else if (data.status === "404") {
              $("#card-" + id)
                .next()
                .remove();
              $("#card-" + id)
                .next()
                .remove();
              $("#card-" + id).remove();
              $("#history1").html("");
              $("#overview1").html("");
              $("#load").hide();
              $("#main1111").removeClass("blur");
              alert("It Seems That The Student Deleted The Outpass!!");
            }
          }
          });
        });

        // $(".accept11").click(function() {
        //   console.log("Accept");
        //   var id = $(this)
        //     .parent()
        //     .attr("id");
        //   if (confirm("Are You Sure You Want To Accept The Outpass?")) {
        //     $.ajax({
        //       url: "http://127.0.0.1:8000/warden/acceptOutpass/",
        //       type: "PUT",
        //       headers: {
        //         Authorization: "Bearer " + access_token
        //       },
        //       data: {
        //         id: id
        //       },
        //       success: function(data) {
        //         console.log(data);
        //         var message = data.status;
        //         //console.log(message)
        //
        //         if (message === "200") {
        //           //console.log($("#card-"+id))
        //           $("#card-" + id)
        //             .next()
        //             .remove();
        //           $("#card-" + id)
        //             .next()
        //             .remove();
        //           $("#card-" + id).remove();
        //           $("#history1").html("");
        //           $("#overview1").html("");
        //           alert("Ok Successfully Accepted The Outpass!!");
        //         } else if (message === "404") {
        //           $("#card-" + id)
        //             .next()
        //             .remove();
        //           $("#card-" + id)
        //             .next()
        //             .remove();
        //           $("#card-" + id).remove();
        //           $("#history1").html("");
        //           $("#overview1").html("");
        //           alert("It Seems That The Student Deleted The Outpass!!");
        //         } else {
        //           alert("Sorry Some Error Occured!! Please Try Again!!");
        //         }
        //       }
        //     });
        //   }
        // });

        $(".remove").click(function() {
          if (
            confirm("Are You Sure You Want To Cancel The Outpass Request ?")
          ) {
            console.log($(this).parent());
            var id = $(this)
              .parent()
              .attr("id");
            remove(id);
            $("#history1").html("");
            $("#overview1").html("");
          }
        });

        $(".close1").click(function() {
          if (
            confirm("Are You Sure You Want To Cancel The Outpass Request ?")
          ) {
            console.log($(this).parent());
            var id = $(this)
              .parent()
              .attr("id");
            remove(id);
            $("#history1").html("");
            $("#overview1").html("");
          }
        });

        function remove(id) {
          $.ajax({
            url: "http://127.0.0.1:8000/student/removePendingOutpass",
            type: "DELETE",
            headers: {
              Authorization: "Bearer " + access_token
            },
            data: {
              id: id
            },
            success: function(data) {
              if (data.status === "200") {
                alert("Successfully Removed Pending Outpass!!");
                $("#card-" + id)
                  .next()
                  .remove();
                $("#card-" + id)
                  .next()
                  .remove();
                $("#card-" + id).remove();
              }
              else if (data.status === "404") {
                $("#card-" + id)
                  .next()
                  .remove();
                $("#card-" + id)
                  .next()
                  .remove();
                $("#card-" + id).remove();
                $("#history1").html("");
                $("#overview1").html("");
                alert("It Seems That The Student Deleted The Outpass!!");
              }
              else {
                alert("Some Error Occured!! Please Try Again Later!!");
              }
            }
          });
        }

        $(".generateP").click(function(){
          $("#load").show();
          $("#main1111").attr("class","blur");
          var id = $(this)
            .parent()
            .attr("id");
          generatePdf(id, 'warden');
        })
      }
    });
  }
}
