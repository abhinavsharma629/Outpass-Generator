function generatePdf(id, type) {

  console.log(id+" "+ type);
  var url;
  if(type==="warden"){
    url="http://127.0.0.1:8000/warden/generateOutpass?id=" + id;
  }
  else{
    var url="http://127.0.0.1:8000/student/generateOutpass?id=" + id;
  }
  $.ajax({
    url: url,
    type: "GET",
    headers: {
      Authorization: "Bearer " + access_token
    },
    success: function(data) {
      if (data.status === "200") {
        console.log(data);
        var details = JSON.parse(data.data);
        console.log(details);

        var html =
          `
    <page size="A4" id="outpass11" class="col-12 col-s-12">

      <div class="row col-s-12">
      <div class="col-md-2 col-s-2">
        <img src="http://127.0.0.1:8000/media/` +
          details.college_logo +
          `" class="img-circle img-responsive" alt="College Logo" width="120" height="120" style="margin-top:4%;" />

      </div>
        <div class="col-md-9 col-s-10" style="margin-top:2%; margin-left:2%;">
          &emsp;
          <b>
            <h5>` +
          details.college_fullName +
          `</h5>
          </b>
          <b>
            <i>
              <h6 style="text-align-last: center;">` +
          details.college_location +
          `</h6>
            </i>
          </b>
          <b>
            <i>
              <h6 style="text-align-last: center;">` +
          details.college_pincode +
          ` , ` +
          details.college_country +
          `</h6>
            </i>
          </b>
        </div>
      </div>
      <br>
      <br>

      <div class="row col-s-12">
        <div class="col-md-5 col-s-5">
          <pre style="float: left; margin-left:1%;">
            <b><i>Name:</i></b><b><u>` +
          details.student_fullName +
          `</u></b><u>(` +
          details.student_er_no +
          `)</u>
            <b><i>Branch:</i></b> <u><b>` +
          details.student_branch +
          `</b></u>
            <b><i>Year:</i></b> <u><b>` +
          details.student_year +
          `</b></u>
            <b><i>Semester:</i></b> <u><b>` +
          details.student_semester +
          `</b></u>
            <b><i>Hostel:</i></b> <u><b>` +
          details.student_hostel +
          `</b></u>
            <b><i>Room No:</i></b>  <u><b>` +
          details.student_room +
          `</b></u>
            <b><i>Bed No:</i></b>  <u><b>` +
          details.student_bed +
          `</b></u>
          </pre>
        </div>

        <div class="col-md-7 col-s-7">
          <pre style="float: right; margin-left:50%;">
              <b><i>Mobile:</i></b> <u><b>` +
          details.student_phone.substr(3) +
          `</b></u>
              <b><i>Email:</i></b>  <u><b>` +
          details.student_email +
          `</b></u>
              <b><i>Parent:</i></b> <u><b>` +
          details.student_parent_name +
          `</b></u>
              <b><i>Parent / Guardian Mobile Number:</i></b> <u><b>` +
          details.student_parent_phone.substr(3) +
          `</b></u>
          </pre>
        </div>
      </div>

      <br>

      <h6 style="margin-left:40%;">
        <b>APPLICATION</b>
      </h6>
      <br>
      <pre style="float: left; margin-left:1%;">
                   <b><i>To:</i></b>
                   <b><i>The Warden:</i></b>  <u><b>Mr. ` +
          details.warden_fullName +
          `</b></u>
                   <b><i>Title:</i></b> <u><b>Outpass For Leave</b></u>
                   </pre>
      <br>
      <br>
      <br>
      <br>

      <pre>I Am Applying For <b><u>` +
          details.days +
          `</u> Days</b> Of Leave <b>From</b> <u><b> ` +
          details.from +
          `</b></u> <b>To</b><u><b> ` +
          details.to +
          `</b></u> .</pre>
      <div class="row">
        &emsp;
        <pre><b>Purpose For Leave:</b> ` +
          details.purposeOfLeave +
          `.</pre>
      </div>
      <div class="row">
        &emsp;
        <pre><b>Address While On Leave:</b> ` +
          details.addressWhileLeave +
          `.</pre>
      </div>
      <br>
      <br>
      <pre><b>Note:- If In Case The outpass Is For Non-Holiday days</b>
                       <ul>
                           <li>I will be responsible for the shortage of my attendance</li>
                           <li>My parents are aware of the leave.</li>
                       </ul>
      </pre>

      <div class="row" id="signs">
        <div class="form-group signature-component col-md-6 col-s-12">
          <section>
            <p>
              <b>Warden's Signature</b>
            </p>

            <img src="`+details.warden_signature+`" id="signature-pad111" />

          </section>
        </div>
      </div>

    </page>
    <div class="modal-footer">
      <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>`;

      if(type==="warden"){
        console.log("ok")
      html+=`
      <button type="button" class="btn btn-primary ok_accept" id="ok_accept">Accept Outpass</button>`;
    }
    else{
      html+=`
      <button type="button" class="btn btn-primary ok-download" id="ok-download">Download</button>`
    }
    html+=`
    </div>
    `;
    console.log(html)

    // <div class="form-group signature-component col-md-6 col-s-12">
    //   <section>
    //     <p>
    //       <b>Student's Signature</b>
    //     </p>
    //
    //     <img src="`+details.student_signature+`" id="signature-pad112"></canvas>
    //
    //   </section>
    // </div>
        $("#myoutpass1").html(html);
        $("#full").html(html);
        $("#load").hide();
        $("#main1111").removeClass("blur");
        $("#myPdfModal").modal("toggle");


          // createPdf();


          $(".ok_accept").click(function() {
            console.log("Accept");

            if (confirm("Are You Sure You Want To Accept The Outpass?")) {
              $.ajax({
                url: "http://127.0.0.1:8000/warden/acceptOutpass/",
                type: "PUT",
                headers: {
                  Authorization: "Bearer " + access_token
                },
                data: {
                  id: id
                },
                success: function(data) {
                  console.log(data);
                  var message = data.status;
                  //console.log(message)

                  if (message === "200") {
                    //console.log($("#card-"+id))
                    $("#card-" + id)
                      .next()
                      .remove();
                    $("#card-" + id)
                      .next()
                      .remove();
                    $("#card-" + id).remove();
                    $("#history1").html("");
                    $("#overview1").html("");
                    createPdf();
                    $("#myPdfModal").modal("toggle");
                    alert("Ok Successfully Accepted The Outpass!!");
                  } else if (message === "404") {
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
                  } else {
                    alert("Sorry Some Error Occured!! Please Try Again!!");
                  }
                }
              });
            }
          });

          $(".ok-download").click(function(){
            createPdf();
          })
      }
      else{
        $("#load").hide();
        $("#main1111").removeClass("blur");
      }
    }
  });
}
