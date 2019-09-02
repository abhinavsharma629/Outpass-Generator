function makeUniqueCode(id) {
  $("#load").show();
  $("#main1111").attr("class","blur");
  var code = "token-" + access_token + "-outpassId-" + id;
  var qrcode = new QRCode("qrcode");
  var uniqueHashedCode = generateUniqueCode(code, id);

  $.ajax({
    url: "http://127.0.0.1:8000/student/generateHash/",
    type: "PUT",
    headers: {
      Authorization: "Bearer " + access_token
    },
    data: {
      code: uniqueHashedCode,
      outpassId: id
    },
    success: function(data) {
      console.log(data);
      if (data.status === "200") {
        qrcode.makeCode(data.hashedCode);
        $("#qr-coModal").modal("toggle");
        $("#load").hide();
        $("#main1111").removeClass("blur");
      } else {
        $("#load").hide();
        $("#main1111").removeClass("blur");
        alert("Sorry some Error Occured!! Please Try Again Later!!");

      }
    }
  });
}

function generateUniqueCode(code, outpassId) {
  var hashedCode = "";
  function s4() {
    return Math.floor((1 + Math.random()) * 0x10000)
      .toString(16)
      .substring(1);
  }
  var id =
    s4() +
    s4() +
    "-" +
    code +
    s4() +
    "-" +
    s4() +
    "-" +
    s4() +
    "-" +
    s4() +
    s4() +
    s4();
  return id;
}
