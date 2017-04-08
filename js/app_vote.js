var key;
var iconNames = {"flat": "icon-flat", "background":"", "bass_clef": "icon-bass_clef", "natural": "icon-natural", "treble_clef": "icon-treble_clef", "open_note_head": "icon-nh_half", "solid_note_head": "icon-nh_quarter"};
function load() {
  $.get( "symbol", function( data ) {
    console.log(data.name);
    var src = "data:image/png;base64," + data.image;
    $("#snippet").attr("src", src);
    key = data.key;
    $.each(data.labels, function(index, label) {
      $("#button-"+index).addClass(iconNames[label.name]);
      $("#button-"+index).attr("data-label", label.name);
      if (label.name == "background")
        $("#button-"+index).html("?");
    });
  }, "json" );
}

$(function() {
  load();
  $("button").click(function() { $.post("symbol?key="+key+"&label=" + $(this).attr("data-label"),
      function( data ) {
        load();
      });
    });
});
