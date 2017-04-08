var label;
var key;
function load() {
  $.get( "symbol", function( data ) {
    console.log(data.name);
    var src = "data:image/png;base64," + data.image;
    $("#snippet").attr("src", src);
    data.labels.sort(function(a,b) { return a.probability < b.probability; });
    label = data.labels[0].name;
    key = data.key;
    $("#description").html( data.labels[0].name + "?");
  }, "json" );
}

$(function() {
  load();
  $("#button-right").click(function() { $.post("symbol?key="+key+"&label=" +label+"&yes=1",
      function( data ) {
        load();
      });
    });
  $("#button-wrong").click(function() { $.post("symbol?key="+key+"&label=" +label+"&no=1",
    function( data ) {
      load();
    });
  });
});
