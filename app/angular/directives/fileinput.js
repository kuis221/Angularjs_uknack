define(['angularAMD'], function(app) {
    app.directive('fdInput', ['$timeout', '$modal', function ($timeout, $modal) {
	    return {
	        link: function (scope, element, attrs) {
	            element.on('change', function  (evt) {
	                if (evt.target.files.length == 0)
                    {
                        scope.clearUpload();
                        return;
                    }
                    var submodalInstance = $modal.open({
                        animation: true,
                        templateUrl: 'views/modals/cropping-modal.html',
                        controller: 'CroppingModalCtl',
                        windowClass: 'vcenter-modal',
                        scope:scope,
                        backdrop:'static'
                        // resolve: {
                        //     sourceImage: function () {
                        //         return scope.sourceImage;
                        //     },
                        //     croppedImage: function () {
                        //         return null;
                        //     }
                        // }
                    });
                    submodalInstance.result.then(function () {
                            scope.sourceImage = null;
                        }, function () {
                            scope.sourceImage = null;
                        }
                    );
	            });
	        }
	    }
    }]);
    app.directive('profileFdInput', ['$timeout', '$modal', '$resource', function ($timeout, $modal, $resource) {
        return {
            link: function (scope, element, attrs) {
                element.on('change', function  (evt) {
                    var files = evt.target.files;

                    var submodalInstance = $modal.open({
                        animation: true,
                        templateUrl: 'views/modals/profile-cropping-modal.html',
                        controller: 'ProfileCroppingModalCtl',
                        windowClass: 'vcenter-modal',
                        resolve: {
                            message: function () {
                                return null;
                            }
                        }
                    });
                    submodalInstance.result.then(function (data) {
                            console.log('Image loaded');
                        }, function () {
                            console.info('Modal dismissed at: ' + new Date());
                        }
                    );
                });
            }
        }
    }]);
});
