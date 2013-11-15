$(function() {

	function getCookie(name) {
		var cookieValue = null;
		if (document.cookie && document.cookie != '') {
			var cookies = document.cookie.split(';');
			for (var i = 0; i < cookies.length; i++) {
				var cookie = jQuery.trim(cookies[i]);
				// Does this cookie string begin with the name we want?
				if (cookie.substring(0, name.length + 1) == (name + '=')) {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}
			}
		}
		return cookieValue;
	}

	var csrftoken = getCookie('csrftoken');

	function csrfSafeMethod(method) {
		// these HTTP methods do not require CSRF protection
		return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}


	$.ajaxSetup({
		crossDomain : false, // obviates need for sameOrigin test
		beforeSend : function(xhr, settings) {
			if (!csrfSafeMethod(settings.type)) {
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
			}
		}
	});

	// Make sure the headers in the project carousel are the right height

	function restyleProjectCarouselHeaders() {
		$('#project-carousel .slide').each(function(index, slide) {
			slide = $(slide);
			var header = slide.find('h4');
			var height = header.height();
			console.log('Header ' + header.text() + ' height: ' + height);
			slide.removeClass('oneline').removeClass('twoline').removeClass('threeline').removeClass('fourline');
			var lineheight = 22;
			if (height < 2 * lineheight) {
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

	$(window).resize(function() {
		window.setTimeout(restyleProjectCarouselHeaders, 200);
	});

	$('input[name=date_start]').datepicker({
		dateFormat : 'yy-mm-dd'
	});

	$('.filtercontainer').accordion({
		collapsible: true,
		active: false
	});

	$('a.noparams').each(function() {
		var t = $(this);
		t.after('<a href="' + window.location.pathname + '">' + t.text() + '</a>');
		t.remove();
	});

	window.setTimeout(function() {
		$("a#responsive_menu_button, #responsive_current_menu_item").click(function() {
			$(".js #main-nav .menu").slideToggle(function() {
				if ($(this).is(":visible")) {
					$("a#responsive_menu_button").addClass("responsive-toggle-open");
				} else {
					$("a#responsive_menu_button").removeClass("responsive-toggle-open");
					$(".js #main-nav .menu").removeAttr("style");
				}
			});
		});

		$("a#responsive_menu_button_footer, #responsive_current_menu_item_footer").click(function() {
			$(".js #footer-nav .menu").slideToggle(function() {
				if ($(this).is(":visible")) {
					$("a#responsive_menu_button_footer").addClass("responsive-toggle-open");
				} else {
					$("a#responsive_menu_button_footer").removeClass("responsive-toggle-open");
					$(".js #footer-nav .menu").removeAttr("style");
				}
			});
		});
	}, 200);
});