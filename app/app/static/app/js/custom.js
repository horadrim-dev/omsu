//https://dimsemenov.com/plugins/magnific-popup/
$(document).on('click tap', '#content img', function (e) {
	// Already wrapped a fancybox href around the clicked image
	/*
     if ($(this).parent().is('a')) {
         return false;
     }

    $(this)
    //.wrap('<a href="' + this.src + '" class="" title="' + this.alt + '" />')
    .parent()
    .magnificPopup({
		type: 'image',
		closeOnContentClick: true,
		closeBtnInside: false,
		fixedContentPos: true,
		mainClass: 'mfp-no-margins mfp-with-zoom', // class to remove default margin from left and right side
		image: {
			verticalFit: true
		},
		zoom: {
			enabled: true,
			duration: 300 // don't foget to change the duration also in CSS
		}
	})
    .trigger('click');
    */
});


document.addEventListener('click', function (e) {
	// Hamburger menu
	if (e.target.classList.contains('hamburger-toggle')) {
		e.target.children[0].classList.toggle('active');
	}
})



function app_js_after_ajax(selector){

	// вешаем lightbox на все картинки 
	$(selector + ' img').wrap(function () {
			return '<a href="' + this.src + '" class="zoom-wrapper" title="' + this.alt + '" />';
		})
		.parent()
		.magnificPopup({
			type: 'image',
			closeOnContentClick: true,
			closeBtnInside: false,
			fixedContentPos: true,
			mainClass: 'mfp-no-margins mfp-with-zoom', // class to remove default margin from left and right side
			image: {
				verticalFit: true
			},
			zoom: {
				enabled: true,
				duration: 300 // don't foget to change the duration also in CSS
			}
		})

};

jQuery.fn.extend({
    ajax_wrapper: function (parent, target, loaded_block) {
			
		$.ajax({
			url: "",
			method: 'get',
			dataType: 'html',
			beforeSend: function(xhr){
				// старт анимации загрузки
				$(target).wrap( '<div class="main_overlay_block"></div>' );
				$(parent + ' .main_overlay_block').prepend('<div class="overlay_block"></div>');
				$(target).addClass('loading_process');
			},
			success: function (data) {
				$(target).replaceWith(data); // добавляем полученный html
				app_js_after_ajax(loaded_block);
				// прокрутка к блоку
				$("html,body").animate({
					scrolltop: $(loaded_block).offset().top - 100
				}, 200);
			},
			complete: function (){
				// снимаем анимацию загрузки
				$(target).removeClass('loading_process');
				$(parent + ' .overlay_block').remove();
				$(target).unwrap();
			}
		});
        // var text = $(this).text();
        // var zigzagText = '';
        // var toggle = true; //lower/uppper toggle
		// 	$.each(text, function(i, nome) {
		// 		zigzagText += (toggle) ? nome.toUpperCase() : nome.toLowerCase();
		// 		toggle = (toggle) ? false : true;
		// 	});
		// return zigzagText;
    }
});

$(document).ready(function () {

	// функции загружаемые также после ajax вызовов
	app_js_after_ajax('body');

	// кнопка "назад"
	$(document).on('click', '#back', function () {
		history.back();
	});

	// заставляем dropdown выпадать по hover (на больших экранах)
	if ($(window).width() > '1000') {
		$('header .dropdown').hover(function () {
			$(this).find('.dropdown-menu').first().addClass('show');
		}, function () {
			$(this).find('.dropdown-menu').first().removeClass('show');
		});

		$('header .dropdown-menu .dropend, header .dropdown-menu .dropstart').hover(function () {
			$(this).find('.dropdown-menu').first().addClass('show');
			$(this).find('.dropdown-menu').first().attr('data-bs-popper', 'none')
		}, function () {
			$(this).find('.dropdown-menu').first().removeClass('show');
			$(this).find('.dropdown-menu').first().removeAttr('data-bs-popper')
		});

	};

	// при клике по tab обновляем хеш в URL
	$(document).on('click', '#content a[role="tab"]', function (e) {
		window.location.hash = this.hash;
	});
	// обрабатываем хеш из URL (открываем вкладку)
	var lastTab = window.location.hash;
	if (lastTab) {
		$('[href="' + lastTab + '"]').tab('show');
	};


	// MODALLY PLUGIN (NESTED MODALS)
	// https://www.jqueryscript.net/lightbox/nested-modal-modally.html
	$('#modal-1').modally('modal-1', {
		max_width: 800,
		in_duration: 0,
		in_easing: 0,
		out_duration: 0,
		out_easing: 0
	});
	$('#modal-2').modally('modal-2', {
		max_width: 600,
	});
	$('#modal-3').modally();
	

	// плавающие блоки
	// $("#right-side-content").stick_in_parent({offset_top:100});
	$("#mainmenu-bar").stick_in_parent({
		parent: 'body'
	});

	// активируем подсказки
	const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
	const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))


	// переключатель фильтров
	$(document).on('click', '.filter-toggle', function (e) {
		var target = $($(this).attr('target'));
		target.slideToggle('fast');
	});

});
/*
	$('#content').magnificPopup({
		type: 'image',
		closeOnContentClick: true,
		mainClass: 'mfp-img-mobile',
		image: {
			verticalFit: true
		}
		
	});
	$('.image-popup-fit-width').magnificPopup({
		type: 'image',
		closeOnContentClick: true,
		image: {
			verticalFit: false
		}
	});

	$('.image-popup-no-margins').magnificPopup({
		type: 'image',
		closeOnContentClick: true,
		closeBtnInside: false,
		fixedContentPos: true,
		mainClass: 'mfp-no-margins mfp-with-zoom', // class to remove default margin from left and right side
		image: {
			verticalFit: true
		},
		zoom: {
			enabled: true,
			duration: 300 // don't foget to change the duration also in CSS
		}
	});

});
    */