define(['angularAMD'], function(app) {
    app.directive("readMore", ['$interval', function ($interval) {
        return {
            restrict: 'A',
            templateUrl: 'directives/readMore.html',
            transclude: true,                        
            scope: {
                'readMoreText': '=',
                'readMoreHeight': '@'
            },            
            link: function ($scope, $element, $attributes) {
                $scope.expanded = false;
                $scope.expandable = false;

                $interval(function() {
                    var text = $element.find('.read-more-text');

                    if($scope.expandable === false && text.outerHeight() >= $scope.readMoreHeight) {
                        $scope.expandable = true;
                        text.attr('style', 'max-height:' + $scope.readMoreHeight + 'px');
                        return;
                    }

                    if($scope.expandable === true) {
                        if($scope.expanded && text.outerHeight() < $scope.readMoreHeight) {
                            $scope.expanded = false;
                            $scope.expandable = false;
                            text.removeAttr('style');
                            return;
                        }
                    }
                }, 300);
            }
        }
    }]);
});