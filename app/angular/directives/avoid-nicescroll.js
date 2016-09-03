(function () {
    'use strict';

    angular
        .module('angular-nicescroll', [])
        .directive('ngNicescroll', ngNicescroll);

    ngNicescroll.$inject = ['$rootScope','$parse'];

    /* @ngInject */
    function ngNicescroll($rootScope,$parse) {
        // Usage:
        //
        // Creates:
        //
        var directive = {
            link: link
        };
        return directive;

        function link(scope, element, attrs, controller) {           


        }
    }


})();
