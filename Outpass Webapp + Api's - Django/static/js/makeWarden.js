function makeWarden(){
    if ($("#overview1").html()) {
      $("#profile1").attr("style", "display:none;");
      $("#request11").attr("style", "display:none;");
      $("#notifications1").attr("style", "display:none;");
      $("#history1").attr("style", "display:none;");
      $("#overview1").attr("style", "display:none;");
      $("#makeWarden1").attr("style", "display:block;");

    } else {
      $("#load").show();
      $("#main1111").attr("class","blur");
      $("#profile1").attr("style", "display:none;");
      $("#request11").attr("style", "display:none;");
      $("#notifications1").attr("style", "display:none;");
      $("#history1").attr("style", "display:none;");
      $("#overview1").attr("style", "display:none;");
      $("#makeWarden1").attr("style", "display:block;");

      $.ajax({
        url: "http://127.0.0.1:8000/warden/makeWardenRequests",
        type: "GET",
        headers: {
          Authorization: "Bearer " + access_token
        },
        success: function(data) {
          console.log(JSON.parse(data.warden_requests));
          var warden_requests = JSON.parse(data.warden_requests);
          var html="";
          for (var i = 0; i < warden_requests.length; i++) {

              html += `<div class="card" id="card-`+warden_requests[i]["er_no"]+`">
              <h5>` +
              warden_requests[i]["first_name"] +
              ` ` +
              warden_requests[i]["last_name"] +
              ` &emsp; :- ` +
              warden_requests[i]["er_no"] +
              `</h5>
                <div class="title"><b>Contact:- ` +
              warden_requests[i]["phone"] +
              `</b></div>
                <div class="desc"><b> Year:- `+
                warden_requests[i]["year"]+` &emsp; Semester:- `+warden_requests[i]["semester"]+` &emsp; Hostel:- `+warden_requests[i]["hostel"]+
            `</b></div>
                <div class="actions" id="`+warden_requests[i]["er_no"]+`">`;

            html +=
              `<button id="accept-request" class="accept-request"><i class="fa fa-check"></i><b>&nbsp;Accept</b></button>&nbsp;
            <button id="reject-request" class="reject-request"><i class="fa fa-times-rectangle"></i><b>&nbsp;Reject</b></button>`;

            html +=
              `
                </div>
              <img src="/media/` +
              warden_requests[i]["picture"] +
              `" class="profile-img" />

              </div>
              <br>
              <br>
                `;
          }
          $("#makeWarden1").html(html);
          $("#load").hide();
          $("#main1111").removeClass("blur");

          $(".accept-request").click(function(){
            var id = $(this)
              .parent()
              .attr("id");

              if(confirm("Are You Sure You Want To Accept The Request!!\nYou will Officially Make Him A Warden!!")){

            console.log(id);

            $.ajax({
              url: "http://127.0.0.1:8000/warden/acceptWardenRequest",
              type: "PUT",
              headers: {
                Authorization: "Bearer " + access_token
              },
              data:{
                "id":id
              },
              success: function(data) {

                if(data.status==="200"){
                $("#card-" + id)
                  .next()
                  .remove();
                $("#card-" + id)
                  .next()
                  .remove();
                  $("#card-" + id).remove();
                  alert("Successfully Accepted The Warden's Request")
                }
                else if(data.status="404"){
                  $("#card-" + id)
                    .next()
                    .remove();
                  $("#card-" + id)
                    .next()
                    .remove();
                }
                else{
                  alert("Sorry Some Error Occured!! Please Try Again Later!!")
                }
              }
            })
          }

          })



          $(".reject-request").click(function(){
            var id = $(this)
              .parent()
              .attr("id");
            if(confirm('Are You Sure This Is a Fake Account??')){
              if(confirm("A Second Level Check To assure that this account will be deleted if you report it!!\n Do You Want To Continue??")){
                $.ajax({
                  url: "http://127.0.0.1:8000/warden/deleteFakeWarden",
                  type: "DELETE",
                  headers: {
                    Authorization: "Bearer " + access_token
                  },
                  data:{
                    "id":id
                  },
                  success: function(data) {
                    if(data.status==="200"){
                    $("#card-" + id)
                      .next()
                      .remove();
                    $("#card-" + id)
                      .next()
                      .remove();
                      $("#card-" + id).remove();
                      alert("Successfully Deleted Account!!")
                    }
                    else if(data.status==="404"){
                      $("#card-" + id)
                        .next()
                        .remove();
                      $("#card-" + id)
                        .next()
                        .remove();
                      $("#card-" + id).remove();
                      alert("This Account is already deleted!!");

                    }
                    else{
                      alert("Sorry Some Error Occured!!")
                    }
                  }
                })
              }
            }
          })

        }
      })
    }
}
