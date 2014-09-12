$(function() {
	checkScreen();
	window.onresize = checkScreen;

});

var checkScreen = function(){
	var md =992;

	var screenSize = $(window).width();


	if(screenSize < md){ //smaller screen
		$(".double-row").removeClass("row-eq-height").addClass("row");
		$(".second").addClass("col-second");
	}else{	//bigger screen
		$(".double-row").removeClass("row").addClass("row-eq-height");
		$(".second").removeClass("col-second");
	}
}