function overview() {
  if ($("#overview1").html()) {
    $("#profile1").attr("style", "display:none;");
    $("#request11").attr("style", "display:none;");
    $("#notifications1").attr("style", "display:none;");
    $("#history1").attr("style", "display:none;");
    $("#overview1").attr("style", "display:block;");
    $("#makeWarden1").attr("style", "display:none;");
    $("#myoutpass1").attr('style', "display:none;");
  } else {
    $("#load").show();
    $("#main1111").attr("class","blur");
    $("#profile1").attr("style", "display:none;");
    $("#request11").attr("style", "display:none;");
    $("#notifications1").attr("style", "display:none;");
    $("#history1").attr("style", "display:none;");
    $("#overview1").attr("style", "display:block;");
    $("#makeWarden1").attr("style", "display:none;");
    $("#myoutpass1").attr('style', "display:none;");

    $.ajax({
      url: "http://127.0.0.1:8000/warden/outpassOverview",
      type: "GET",
      headers: {
        Authorization: "Bearer " + access_token
      },
      success: function(data) {
        console.log(JSON.parse(data.overview));
        var overview = JSON.parse(data.overview);
        var html = "";
        //$("#1").html(html);
        for (var i = 0; i < overview.length; i++) {
          if (overview[i]["pending"] > 0) {
            html += `<div class="card" style="background-color:#ffff4d;">`;
          } else {
            html += `<div class="card">`;
          }

          html +=
            `<h5>` +
            overview[i]["student__user__first_name"] +
            ` ` +
            overview[i]["student__user__last_name"] +
            ` &emsp; :- ` +
            overview[i]["student__user__username"] +
            `</h5>
              <div class="title"><b>Contact:- ` +
            overview[i]["student__phone"] +
            `</b></div>
              <div class="desc">
          </div>
              <div class="actions">`;

          html +=
            `<button><i class="fa fa-check"></i><b>&nbsp;Approved:- ` +
            overview[i]["approved"] +
            `</b></button>
          <button><i class="fa fa-times-rectangle"></i><b>&nbsp;Pending:- ` +
            overview[i]["pending"] +
            `</b></button>
          `;

          html +=
            `
              </div>
            <img src="/media/` +
            overview[i]["student__photo"] +
            `" class="profile-img" />

            </div>
            <br>
            <br>
              `;
        }

        $("#overview1").html(html);
        $("#load").hide();
        $("#main1111").removeClass("blur");
      }
    });
  }
}
