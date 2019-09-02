function makePdf() {
  if ($("#myoutpass1").html()) {
    $("#profile1").attr("style", "display:none;");
    $("#request11").attr("style", "display:none;");
    $("#notifications1").attr("style", "display:none;");
    $("#history1").attr("style", "display:none;");
    $("#overview1").attr("style", "display:none;");
    $("#makeWarden1").attr("style", "display:none;");
    $("#myoutpass1").attr("style", "display:block;");

      createPdf();

  } else {
    $("#profile1").attr("style", "display:none;");
    $("#request11").attr("style", "display:none;");
    $("#notifications1").attr("style", "display:none;");
    $("#history1").attr("style", "display:none;");
    $("#overview1").attr("style", "display:none;");
    $("#makeWarden1").attr("style", "display:none;");
    $("#myoutpass1").attr("style", "display:block;");
      createPdf();
  }
}
