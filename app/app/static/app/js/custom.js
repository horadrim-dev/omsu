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

	// На больших экранах заставляем dropdown выпадать по hover
	if ($(window).width() > '1000') {
		$('.dropdown').hover(function () {
			$(this).find('.dropdown-menu').first().addClass('show');
		}, function () {
			$(this).find('.dropdown-menu').first().removeClass('show');
		});
	};
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