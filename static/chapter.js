var fanart=document.getElementsByClassName("fanartIcon")
var paragraph=document.getElementsByClassName("paragraph")
var picture=document.getElementsByClassName("picture")

var iconClick = function (pos){
	console.log(pos);
}

var pixClixed = function (num){
	if (picture[num].getAttribute("display") == "false"){
		picture[num].style.display="inline";
		picture[num].setAttribute("display","true")
	}
	else if (picture[num].getAttribute("display") == "true"){
		picture[num].style.display="none";
		picture[num].setAttribute("display","false");
	}
}


for (var i=0; i<paragraph.length; i++){
	fanart[i].setAttribute("num",i);
	picture[i].setAttribute("display",false);
	fanart[i].addEventListener('click',function(e){
		console.log("clicked")
		pixClixed(parseInt(e.target.getAttribute("num")));
	}
	,false);
}


$(document).ready(function() {
    $(".dropdown-toggle").dropdown();
});

$(function(){
    // When the toggle areas in your navbar are clicked, toggle them
    $("#search-button, #search-icon").click(function(e){
        e.preventDefault();
        $("#search-button, #search-form").toggle();
    });
})  

$(document).ready(function(){
  $('#search').on("click",(function(e){
  $(".form-group").addClass("sb-search-open");
    e.stopPropagation()
  }));
   $(document).on("click", function(e) {
    if ($(e.target).is("#search") === false && $(".form-control").val().length == 0) {
      $(".form-group").removeClass("sb-search-open");
    }
  });
    $(".form-control-submit").click(function(e){
      $(".form-control").each(function(){
        if($(".form-control").val().length == 0){
          e.preventDefault();
          $(this).css('border', '2px solid red');
        }
    })
  })
})
