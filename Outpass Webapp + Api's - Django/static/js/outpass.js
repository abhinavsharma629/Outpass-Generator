var form, a4, cache_width;

function createOutpass() {
  $("#notifications1").html("")
  console.log("Entered");
  if ($("#createOutpass1").html()) {
    console.log("asdas");
    $("#profile1").attr("style", "display:none;");
    $("#drafts1").attr("style", "display:none;");
    $("#createOutpass1").attr("style", "display:block;");
    $("#notifications1").attr("style", "display:none;");
    $("#history1").attr("style", "display:none;");
    $("#myoutpass1").attr("style", "display:none;");
  } else {
    $("#load").show();
    $("#main1111").attr("class","blur");
    $("#profile1").attr("style", "display:none;");
    $("#drafts1").attr("style", "display:none;");
    $("#createOutpass1").attr("style", "display:block;");
    $("#notifications1").attr("style", "display:none;");
    $("#history1").attr("style", "display:none;");
    $("#myoutpass1").attr("style", "display:none;");

    console.log("inside");
    $.ajax({
      type: "GET",
      url: "http://127.0.0.1:8000/student/studentDetails",
      headers: {
        Authorization: "Bearer " + access_token
      },
      success: function(data) {
        var student = JSON.parse(data.student_details);
        console.log(student);

        var html = `
                <div class="form-group">
                <label for="reason">Reason</label>
                <textarea type="text" class="form-control" id="reason" placeholder="Reason For Leave"></textarea>
                </div>

                <div class="form-group">
                <label for="addIt">Address While Leave</label>
                <textarea type="text" class="form-control" id="addIt" placeholder="Address While On Leave"></textarea>
                </div>

                <div class="form-group">
                <label for="nod">Number Of Days</label>
                <input type="number" class="form-control" id="nod" placeholder="Number Of Days">
                </div>

                <div class="form-group">
                <label for="from">From Date</label>
                <input type="date" class="form-control" id="from" placeholder="From Date">
                </div>

                <div class="form-group">
                <label for="to">To Date</label>
                <input type="date" class="form-control" id="to" placeholder="To Date">
                </div>


                <div class="form-group">
                <div class="form-check">
                <input class="form-check-input" type="checkbox" id="emergency">
                <label class="form-check-label" for="emergency">
                  Is An Emergency !!
                </label>
                </div>
                </div>


                <div class="row" style="margin-left:40%">
                <button class="btn btn-primary float-left" id="save_draft">Save</button>
                &emsp;
                <button class="btn btn-primary float-center" id="send_outpass">Send</button>
                &emsp;
                <button class="btn btn-primary float-right" id="upload11">Upload SS.</button>
                </div>
        `;

        $("#createOutpass1").html(html);
        $("#load").hide();
        $("#main1111").removeClass("blur");

        $("#upload11").click(function() {
          $("#exampleModal").modal("toggle");
        });

        $("#send_outpass").click(function() {
          var fd = new FormData();
          if (file) {
            fd.append("whtsImg", file);
          }
          fd.append("reason", $("#reason").val());
          fd.append("add", $("#addIt").val());
          fd.append("nod", $("#nod").val());
          fd.append("from", $("#from").val());
          fd.append("to", $("#to").val());
          fd.append("emergency", $("#emergency").prop("checked"));

          $.ajax({
            type: "POST",
            url: "http://127.0.0.1:8000/student/sendOutpass/",
            headers: {
              Authorization: "Bearer " + access_token
            },
            data: fd,
            processData: false,
            contentType: false,
            success: function(data) {
              var message = data.status;
              console.log(data);
              if (message === "201") {
                alert("Successfully Sent To Your Warden!!");
                $("#history1").html("");
              } else if (message === "500") {
                alert(
                  "Error!! You can't leave any field blank!!\nYou Can't Send Exactly Same Outpass Twice!!\nTry Changing And Sending Again!!"
                );
              } else {
                alert(
                  "Error!! Your Previous Outpass is already in queue!! \nYou can't send another request until your warden reviews your outpass or you delete the outpass !!"
                );
              }
            }
          });
        });

        $("#save_draft").click(function() {
          var fd = new FormData();
          if (file) {
            fd.append("whtsImg", file);
          }
          fd.append("reason", $("#reason").val());
          fd.append("add", $("#addIt").val());
          fd.append("nod", $("#nod").val());
          fd.append("from", $("#from").val());
          fd.append("to", $("#to").val());

          $.ajax({
            type: "POST",
            url: "http://127.0.0.1:8000/student/saveOutpass/",
            headers: {
              Authorization: "Bearer " + access_token
            },
            data: fd,
            processData: false,
            contentType: false,
            success: function(data) {
              var message = data.status;
              console.log(data);
              if (message === "201") {
                alert("Successfully Saved As Draft!!");
                $("#drafts1").html("");
              } else {
                alert(
                  "Error!! You Can't Save Exactly Same Draft Twice!! You can't leave any field blank!! Try Changing And Saving Again!!"
                );
              }
            }
          });
        });

        // $("#download11").click(function() {
        //     //$('body').scrollTop(0);
        //
        //     form = $('#outpass11');
        //     cache_width = form.width();
        //     a4 = [595.28, 841.89]; // for a4 size paper width and height
        //     createPDF();
        // })
      }
    });

    function createPDF() {
      console.log("inside create PDF");
      getCanvas().then(function(canvas) {
        var img = canvas.toDataURL("image/png"),
          doc = new jsPDF({
            unit: "px",
            format: "a4"
          });
        doc.addImage(img, "JPEG", 20, 20);
        doc.save("Outpass.pdf");
        form.width(cache_width);
      });
    }

    function getCanvas() {
      form.width(a4[0] * 1.33333 - 80).css("max-width", "none");
      return html2canvas(form, {
        imageTimeout: 2000,
        removeContainer: true
      });
    }
  }
}
