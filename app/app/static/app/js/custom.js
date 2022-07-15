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
	$('#content a[role="tab"]').click(function (e) {
		window.location.hash = this.hash;
	});
	// обрабатываем хеш из URL (открываем вкладку)
	var lastTab = window.location.hash;
	if (lastTab) {
		$('[href="' + lastTab + '"]').tab('show');
	};


	// BOOSTRAP MODAL NESTED MODALS
	// (function ($, window) {
	// 	'use strict';

	// 	var MultiModal = function (element) {
	// 		this.$element = $(element);
	// 		this.modalCount = 0;
	// 	};

	// 	MultiModal.BASE_ZINDEX = 1040;

	// 	MultiModal.prototype.show = function (target) {
	// 		var that = this;
	// 		var $target = $(target);
	// 		var modalIndex = that.modalCount++;

	// 		$target.css('z-index', MultiModal.BASE_ZINDEX + (modalIndex * 20) + 10);

	// 		// Bootstrap triggers the show event at the beginning of the show function and before
	// 		// the modal backdrop element has been created. The timeout here allows the modal
	// 		// show function to complete, after which the modal backdrop will have been created
	// 		// and appended to the DOM.
	// 		window.setTimeout(function () {
	// 			// we only want one backdrop; hide any extras
	// 			if (modalIndex > 0)
	// 				$('.modal-backdrop').not(':first').addClass('hidden');

	// 			that.adjustBackdrop();
	// 		});
	// 	};

	// 	MultiModal.prototype.hidden = function (target) {
	// 		this.modalCount--;

	// 		if (this.modalCount) {
	// 			this.adjustBackdrop();

	// 			// bootstrap removes the modal-open class when a modal is closed; add it back
	// 			$('body').addClass('modal-open');
	// 		}
	// 	};

	// 	MultiModal.prototype.adjustBackdrop = function () {
	// 		var modalIndex = this.modalCount - 1;
	// 		$('.modal-backdrop:first').css('z-index', MultiModal.BASE_ZINDEX + (modalIndex * 20));
	// 	};

	// 	function Plugin(method, target) {
	// 		return this.each(function () {
	// 			var $this = $(this);
	// 			var data = $this.data('multi-modal-plugin');

	// 			if (!data)
	// 				$this.data('multi-modal-plugin', (data = new MultiModal(this)));

	// 			if (method)
	// 				data[method](target);
	// 		});
	// 	}

	// 	$.fn.multiModal = Plugin;
	// 	$.fn.multiModal.Constructor = MultiModal;

	// 	$(document).on('show.bs.modal', function (e) {
	// 		$(document).multiModal('show', e.target);
	// 	});

	// 	$(document).on('hidden.bs.modal', function (e) {
	// 		$(document).multiModal('hidden', e.target);
	// 	});
	// }(jQuery, window));

	// $('.modal').on('hidden.bs.modal', function (event) {
	// 	$(this).removeClass('fv-modal-stack');
	// 	$('body').data('fv_open_modals', $('body').data('fv_open_modals') - 1);
	// });

	// $('.modal').on('shown.bs.modal', function (event) {
	// 	// keep track of the number of open modals
	// 	if (typeof ($('body').data('fv_open_modals')) == 'undefined') {
	// 		$('body').data('fv_open_modals', 0);
	// 	}

	// 	// if the z-index of this modal has been set, ignore.
	// 	if ($(this).hasClass('fv-modal-stack')) {
	// 		return;
	// 	}

	// 	$(this).addClass('fv-modal-stack');
	// 	$('body').data('fv_open_modals', $('body').data('fv_open_modals') + 1);
	// 	$(this).css('z-index', 1040 + (10 * $('body').data('fv_open_modals')));
	// 	$('.modal-backdrop').not('.fv-modal-stack').css('z-index', 1039 + (10 * $('body').data('fv_open_modals')));
	// 	$('.modal-backdrop').not('fv-modal-stack').addClass('fv-modal-stack');

	// });
	// $(document).on('hidden.bs.modal', function () {
	// 	if ($('.modal.show').length) {
	// 		$('body').addClass('modal-open');
	// 	}
	// });
jQuery(document).ready(function () {
    $('#ipsum').modally('ipsum', {
        max_width: 800
    });
    $('#lorem').modally();
    $('#dolor').modally();
});
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
	// $("#right-side-content").stick_in_parent({offset_top:100});
	$("#mainmenu-bar").stick_in_parent({
		parent: 'body'
	});

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