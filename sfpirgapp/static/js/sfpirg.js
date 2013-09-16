$(function() {

	// Make sure the headers in the project carousel are the right height

	function restyleProjectCarouselHeaders() {
		$('#project-carousel .slide').each(function(index, slide) {
			slide = $(slide);
			var header = slide.find('h4');
			var height = header.height();
			console.log('Header ' + header.text() + ' height: ' + height);
			slide.removeClass('oneline').removeClass('twoline').removeClass('threeline').removeClass('fourline');
			var lineheight = 22;
			if (height < 2 * lineheight ) {
				slide.addClass('oneline');
			} else if (height < 3 * lineheight) {
				slide.addClass('twoline');
			} else if (height < 4 * lineheight) {
				slide.addClass('threeline');
			} else {
				slide.addClass('fourline');
			}
		});
	}


	window.setTimeout(restyleProjectCarouselHeaders, 200);

	$(window).resize(function() {window.setTimeout(restyleProjectCarouselHeaders, 200);});
})