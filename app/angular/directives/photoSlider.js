define(['angularAMD'], function(app) {
    app.directive("photoSlider", ['$timeout', function ($timeout) {
        return {
            restrict: 'AE',
            link: function ($scope, $element, $attributes) { 
                $timeout(function() {
                    var options = {
                        item: 1,
                        thumbItem: 5,
                        pager: $attributes.gallery && $attributes.gallery == 'false' ? false : true,
                        gallery: $attributes.gallery && $attributes.gallery == 'false' ? false : true
                    };
                    var slider = $($element).lightSlider(options);
                    slider.refresh();
                }, 500);
                /*    
                var photos = [], loadedPhotos = 0;
                var size = $attributes.sliderSize;

                $element.parent().addClass('slider-loading').addClass(size);

                $attributes.$observe('sliderPhotos', function(value){
                    if(value == '' || value == undefined) return;

                    photos = value;
                    photos = photos.replace(/'/g, '"');
                    photos = JSON.parse(photos);

                    for (var i=0; i<photos.length; i++) {
                        var img = new Image();
                        img.src = photos[i];
                        img.onload=function() {
                            photosLoaded();
                        }
                        img.onerror=function() {
                            photosLoaded();
                        }
                    }
                });

                function photosLoaded() {
                    loadedPhotos++;

                    if (loadedPhotos == photos.length) {
                        $element.parent().removeClass('slider-loading').removeClass(size);

                        $timeout(function() {
                            var options = {
                                item: 1,
                                thumbItem: 5,
                                pager: $attributes.gallery && $attributes.gallery == 'false' ? false : true,
                                gallery: $attributes.gallery && $attributes.gallery == 'false' ? false : true
                            };
                            var slider = $($element).lightSlider(options);
                            slider.refresh();
                        }, 500);    
                    }                    
                }
                */                
            }
        }
    }]);
});