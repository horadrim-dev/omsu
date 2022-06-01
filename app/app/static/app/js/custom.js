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

$(document).ready(function () {
	// вешаем lightbox на все картинки в #content
	$('#content img').wrap(function () {
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

	// кнопка "назад"
	$('#back').click(function () {
		history.back();
	});

	// заставляем dropdown выпадать по hover (на больших экранах)
	if ($(window).width() > '1000') {
		$('.dropdown').hover(function () {
			$(this).find('.dropdown-menu').first().addClass('show');
		}, function () {
			$(this).find('.dropdown-menu').first().removeClass('show');
		});

		$('.dropdown-menu .dropend, .dropdown-menu .dropstart').hover(function () {
			$(this).find('.dropdown-menu').first().addClass('show');
			$(this).find('.dropdown-menu').first().attr('data-bs-popper', 'none')
		}, function () {
			$(this).find('.dropdown-menu').first().removeClass('show');
			$(this).find('.dropdown-menu').first().removeAttr('data-bs-popper')
		});
		
	};

	// при клике по tab обновляем хеш в URL
	$('a[role="tab').click(function (e) {
		window.location.hash = this.hash;
	});
	// обрабатываем хеш из URL (открываем вкладку)
	var lastTab = window.location.hash;
	if (lastTab) {
		$('[href="' + lastTab + '"]').tab('show');
	};

	// ajax
	// $( document ).ajaxStart(function() {
	// // $( "#loading" ).show();
	// 	$(block).wrap( '<div class="main_overlay_block"></div>' );
	// 	$('.main_overlay_block').prepend('<div class="overlay_block"></div>');
	// 	$(block).addClass('loading_process');
	// });

	// $( document ).ajaxComplete(function() {
	// 	$(block).unwrap();
	// 	$('.overlay_block').remove();
	// 	$(block).removeClass('loading_process');
	// });
	// $('a.ajax').on('click', function (e) {
	// 	// alert(this.href + " /// " + this.target);
	// 	var target = "#" + this.target;
	// 	$.ajax({
	// 		url: this.href,
	// 		method: 'get',
	// 		dataType: 'html',
	// 		success: function (data) {
	// 			$(target).html(data);
	// 		}
	// 	});
	// 	e.preventDefault();
	// });

	// плавающие блоки
	$("#right-side-content").stick_in_parent({offset_top:100});
	$("#mainmenu-bar").stick_in_parent({parent:'body'});

	// активируем подсказки
	const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
	const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

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