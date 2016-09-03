/* ===============================================
----------- Uknack Main Js File ---------- */
(function ($) {
	"use strict";
	var Uknacks = {
		initialised: false,
		mobile: false,
		masonryContainer: $('#item-container'),
		init: function () {

			if(!this.initialised) {
				this.initialised = true;
			} else {
				return;
			}

			// Check for mobile
			this.checkMobile();
			this.customScrollbar();
			this.selectAll();
			this.mobileSearch();
			this.toggleSidebar();
			this.tooltip();
			this.popup();
			this.dropdownFix();

			/* Call function if slightslider plugin is included */
			if ( $.fn.lightSlider ) {
				this.gallery();
			}

			/* Call function if lightGallery plugin is included  */
			if ($.fn.magnificPopup) {
				this.knackGallery();
			}

			/* Call function if noUiSlider plugin is included */
			if (typeof noUiSlider === "object") {
				this.filterSliders();	
			}

			var self = this;
			/* Imagesloaded plugin included in isotope.pkgd.min.js */
			/* Call masonry with images loaded plugin */
			if ( $.fn.isotope) {
				/* */
				imagesLoaded(self.masonryContainer, function() {
					// fixe
					setTimeout(function () {
						self.masonryActivate();
						self.masonrySort();
					}, 500);
					
				});
			}
		},
		checkMobile: function () {
			/* Mobile Detect*/
			if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
				this.mobile = true;
			} else {
				this.mobile = false;
			}
		},
		customScrollbar: function () {
			if ($.fn.niceScroll) {
				/* Side Menu Custom Scrollbar with nicescroll plugin */
				$('.sidebar-wrapper').niceScroll({
					zindex: 9999,
					autohidemode: true,
					background: '' ,
					cursorcolor: '#d7e0e1',
					cursorwidth: '5px',
					cursorborder: 'none',
					cursorborderradius: '4px'
				})


				/* Chats custom scrollbar */
				$('.chats-wrapper').niceScroll({
					zindex: 9999,
					autohidemode: true,
					background: '' ,
					cursorcolor: '#cedfe1',
					cursorwidth: '5px',
					cursorborder: 'none',
					cursorborderradius: '4px'
				})
			}
		},
		selectAll: function () {
			// Check all checkboxes
			var checkboxes = $('#category-boxes').find('input'),
				selected = false;

			$('.select-all').on('click', function (e) {
				if (selected) {
					$('#category-boxes').find('input').each(function() {
						this.checked = false;
					});
					$(this).text('Select All');
					selected = false;
				} else {
					$('#category-boxes').find('input').each(function() {
						this.checked = true;
					});
					$(this).text('Unselect All');
					selected = true;
				}
				e.preventDefault();
			});
		},
		gallery: function () {
			// Call carousel + lightbox
			$('#item-gallery').lightSlider({
                gallery:true,
                item:1,
                loop:true,
                thumbItem:4,
                thumbMargin:21,
                slideMargin:0,
                galleryMargin:21,
                enableDrag: true,
                currentPagerPosition:'left',
                responsive: [
                	{
                		breakpoint:991,
                		settings: {
                			thumbMargin:15,
			                galleryMargin:15,
                		}
                	},
                	{
                		breakpoint:767,
                		settings: {
                			thumbMargin:12,
			                galleryMargin:12,
                		}
                	},
                	{
                		breakpoint:480,
                		settings: {
                			thumbItem:3
                		}
                	}
                ]
            }); 
		},
		knackGallery:function () {
			/* This is for gallery images */
			$('.popup-gallery').magnificPopup({
				delegate: '.zoom-item',
				type: 'image',
				closeOnContentClick: false,
				closeBtnInside: false,
				mainClass: 'mfp-with-zoom mfp-img-mobile',
				image: {
					verticalFit: true,
				},
				gallery: {
					enabled: true
				},
				zoom: {
					enabled: true,
					duration: 400, // Duration for zoom animation 
					opener: function(element) {
						return element.find('img');
					}
				}
			});
		},
		filterSliders:function () {
			// Slider For category pages / filter price
			var priceSlider  = document.getElementById('price-slider');

			noUiSlider.create(priceSlider, {
				start: [ 40, 200 ],
				connect: true,
				step: 10,
				range: {
					'min': 0,
					'max': 240
				}
			});

			this.sliderText(priceSlider, '$');

			// Slider For category pages / filter price
			var ageSlider  = document.getElementById('age-slider');

			noUiSlider.create(ageSlider, {
				start: [ 10, 50 ],
				connect: true,
				step: 1,
				range: {
					'min': 0,
					'max': 60
				}
			});

			this.sliderText(ageSlider);
		},
		sliderText: function(slider, currency) {
			// add slider values as a text 
			// check for currency too
			var currencyVar = (currency) ? '$' : null,
				divHandles = slider.getElementsByClassName('noUi-handle'),
				divs = [];

			// Add divs to the slider handles.
			for ( var i = 0; i < divHandles.length; i++ ){
				divs[i] = document.createElement('div');
				divHandles[i].appendChild(divs[i]);
			}

			// When the slider changes, write the value to the tooltips.
			slider.noUiSlider.on('update', function( values, handle ){
				divs[handle].innerHTML = ( currencyVar) ? (currencyVar + values[handle]) : Math.round(values[handle]);
			});
		},
		masonryActivate: function() {
			// Trigger for isotope plugin
			this.masonryContainer.isotope({
            	itemSelector: '.item-wrapper',
            	layoutMode: 'fitRows',
            	getSortData: {
					popular: '[data-recently]',
					recently: '[data-popular]'
				},
				sortBy: 'recently'
        	});
		},
		masonrySort: function () {
			var self = this;
			$('#item-sort').on('change', function () {
				var sortByVal = $(this).val();
				self.masonryContainer.isotope({sortBy: sortByVal});
				console.log(sortByVal);
			});
		},
		mobileSearch: function () {
			// mobile search from show/hide
			$('.mobile-search-btn, .search-close-btn').on('click', function (e) {
				$('.search-form').toggleClass('open');
				e.preventDefault();
			});
		},
		toggleSidebar: function () {
			// Toggle - show/hide sidebar for small devices
			$('#sidebar-toggle-btn, .sidebarbg-mobile').on('click', function (e) {
				$('body').toggleClass('sidebar-open');
				e.preventDefault();
			});
		},
		tooltip: function () {
			// Bootstrap tooltip
			$('[data-toggle="tooltip"]').tooltip();
		},
		popup: function () {
			// Bootstrap Popover
			$('[data-toggle="popover"]').popover()
		},
		dropdownFix: function () {
			// Prevent event bubbling on input dropdown
			$('.dropdown-menu input, .dropdown-menu button').click(function(e) {
		        e.stopPropagation();
		    });
		}


	};

	// init
	Uknacks.init();

})(jQuery);