define(['angularAMD'], function(app) {
    app.directive("imgLoader", function () {
        return {
            restrict: 'A',
            link: function ($scope, $element, $attributes) {
                var img = new Image();

                $element.addClass('img-loading');

                img.onload = function() {
                    $element.removeClass('img-loading');                    
                };
                img.src = $attributes.ngSrc;                
            }
        }
    });
});