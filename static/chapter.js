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

