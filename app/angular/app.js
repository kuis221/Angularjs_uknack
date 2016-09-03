/*######################################################
 This app returns a ng module which is declared to
 be the main module for the entire app.

 Logic can be applied to set up the home page
 ######################################################*/
'use strict';

define(['angularAMD',
        'jquery',
        'masonry',
        'jquery-bridget',
        'uiRouter',
        'uiBootstrap',
        'routeResolver',
        'ui.utils',
        'angularResource',
        'angularLocalStorage',
        'underscore',
        'angularFileUpload',
        'angularFileModel',
        'angularNiceScroll',
        'angularNouislider',
        'imagesloaded',
        'smoothscroll',
        'retinajs',
        'jquery.magnific-popup',
        'angular-masonry',
        'checklist-model',
        'angular-loading-bar',
        'angular-websocket',
        'modals',
        'imgLoader',
        'chatbox',
        'photoSlider',
        'readMore',
        'fileInput',
        'scrollBottom',
        'header',
        'profile',
        'footer',
        'menubar',
        'bottombar',
        'angular-headroom',
        'lightslider',
        'angular-sanitize',
        'videogular',
        'vg-controls',
        'vg-overlay-play',
        'vg-poster',
        'vg-buffering',
        'smile-emoji',
        'angular-cookies',
        'emoji-config',
        'emoji-controls',
        'angular-img-cropper',
        'djds4rce.angular-socialshare'
    ],
    function (angularAMD) {
        'use strict';
        //var webApiPath = "ec2-52-10-177-231.us-west-2.compute.amazonaws.com";
        var webApiPath = "uknack.com";
        //var webApiPath = "127.0.0.1:8000";
        var app = angular.module('app', [
            'ui.router',
            'ui.route',
            'ui.bootstrap',
            'routeResolverServices',
            'ngResource',
            'LocalStorageModule',
            'angularFileUpload',
            'file-model',
            'angular-nicescroll',
            'nouislider',
            'wu.masonry',
            'checklist-model',
            'angular-loading-bar',
            'ngWebSocket',
            'headroom',
            'ngSanitize',
            'com.2fdevs.videogular',
            'com.2fdevs.videogular.plugins.controls',
            'com.2fdevs.videogular.plugins.overlayplay',
            'com.2fdevs.videogular.plugins.poster',
            'emoji',
            'ngCookies',
            'emojiApp',
            'angular-img-cropper',
            'djds4rce.angular-socialshare'
        ]);
        app.run(function ($rootScope, $http, $resource, $state) {

            $rootScope.is_authenticated = false;
            $rootScope.profile_user = null;
            $rootScope.dashCollapsed = true;
            $rootScope.serverProtocal = "http";
            $rootScope.serverURL = "/";
            $rootScope.currentMenu = "";
            $rootScope.knackCategories = [];
            $rootScope.itemCategories = [];
            $rootScope.colleges = [];
            $rootScope.years = [];
            $rootScope.genders = [];
            $rootScope.milesCategories = [];
            $rootScope.chargeType = [];
            $rootScope.knackTypes = [];
            $rootScope.new_message_count = 0;
            $rootScope.heartbeat_msg = "--heartbeat--";
            $rootScope.new_email = "";
            $rootScope.$state = $state;
            $rootScope.isSidebarOpen = false;
            $rootScope.isMenubarOpen = false;
            $rootScope.isIdea = 'all';

            $rootScope.restProtocol = "http";
            $rootScope.restURL = webApiPath;
            //$rootScope.restURL = window.location.host;
            $rootScope.isGoToFeed = false;

            var categoryCollection = $resource(":protocol://:url/api/knacks/categories", {
                protocol: $rootScope.restProtocol,
                url: $rootScope.restURL
            });
            categoryCollection.get(function (categories) {
                angular.extend($rootScope.knackCategories, categories.results);
            });

            var itemCategoryCollection = $resource(":protocol://:url/api/items/categories", {
                protocol: $rootScope.restProtocol,
                url: $rootScope.restURL
            });
            itemCategoryCollection.get(function (categories) {
                angular.extend($rootScope.itemCategories, categories.results);
            });

            var colleges_resource = $resource(":protocol://:url/api/accounts/colleges",{
                protocol: $rootScope.restProtocol,
                url: $rootScope.restURL
            });
            colleges_resource.get(function (colleges) {
                angular.forEach(colleges.results, function(value, key) {
                    $rootScope.colleges.push(value.name);
                });
            });

            var years_resource = $resource(":protocol://:url/api/accounts/years",{
                protocol: $rootScope.restProtocol,
                url: $rootScope.restURL
            });
            years_resource.get(function (years) {
                angular.forEach(years.results, function(value, key) {
                    $rootScope.years.push(value.name);
                });
            });

            var genders_resource = $resource(":protocol://:url/api/accounts/genders", {
                protocol: $rootScope.restProtocol,
                url: $rootScope.restURL
            });
            genders_resource.get(function (genders) {
                angular.forEach(genders.results, function(value, key) {
                    $rootScope.genders.push({name: value[0]});
                });
            });

            var miles_resource = $resource(":protocol://:url/api/knacks/miles",{
                protocol: $rootScope.restProtocol,
                url: $rootScope.restURL
            });
            miles_resource.get(function (miles) {
                angular.forEach(miles.results, function(value, key) {
                    $rootScope.milesCategories.push({name: value[0]});
                });
            });

            var charge_resource = $resource(":protocol://:url/api/knacks/how_charge",{
                protocol: $rootScope.restProtocol,
                url: $rootScope.restURL
            });
            charge_resource.get(function (charges) {
                angular.forEach(charges.results, function(value, key) {
                    $rootScope.chargeType.push({name: value[0]});
                });
            });

            var types_resource = $resource(":protocol://:url/api/knacks/types",{
                protocol: $rootScope.restProtocol,
                url: $rootScope.restURL
            });
            types_resource.get(function (types) {
                angular.extend($rootScope.knackTypes, types.results);
            });

            $rootScope.genderCategories = [
                {name: 'Male'},
                {name: 'Female'},
                {name: 'Trans'},
                {name: 'Andro'},
                {name: 'Exploring'},
                {name: 'Alien'},
                {name: 'No Gender'}
            ];

            //if($rootScope.token) {
            //    $rootScope.is_authenticated = true;
            //    $http.defaults.headers.common['Authorization'] = $rootScope.token;
            //}
            $rootScope.$on('$stateChangeSuccess', function() {
               document.body.scrollTop = document.documentElement.scrollTop = 0;
            });

            if(navigator.splashscreen) {
                setTimeout(function() {
                    navigator.splashscreen.hide();
                }, 1000);
            }
        });

        app.config([
            'routeResolverProvider', '$stateProvider', '$urlRouterProvider', '$httpProvider',
            function (routeResolverProvider, $stateProvider, $urlRouterProvider, $httpProvider) {
                var route = routeResolverProvider.route;
                $stateProvider
                    //LoggedIn and LoggedOut
                    .state('home', route.resolve('/', 'views/homepage/index'))
                    .state('about', route.resolve('/about', 'views/homepage/about'))
                    .state('mission', route.resolve('/mission', 'views/homepage/mission'))
                    .state('terms', route.resolve('/terms', 'views/homepage/terms'))
                    .state('how', route.resolve('/how', 'views/homepage/how'))
                    .state('features', route.resolve('/features', 'views/homepage/features'))
                    .state('guidelines', route.resolve('/guidelines', 'views/homepage/guidelines'))
                    .state('gethired', route.resolve('/gethired', 'views/homepage/gethired'))
                    .state('economy', route.resolve('/economy', 'views/homepage/economy'))
                    .state('faqs', route.resolve('/faqs', 'views/homepage/faqs'))
                    .state('knack-offered', $.extend(route.resolve('/knacks/offered', 'views/knacks'), {data: {type: 'knack-offered'}}))
                    .state('knack-offered-single', $.extend(route.resolve('/knacks/offered/:id', 'views/knacks'), {data: {type: 'knack-offered'}}))
                    .state('knack-wanted', $.extend(route.resolve('/knacks/wanted', 'views/knacks'), {data: {type: 'knack-wanted'}}))
                    .state('knack-wanted-single', $.extend(route.resolve('/knacks/wanted/:id', 'views/knacks'), {data: {type: 'knack-wanted'}}))
                    .state('knack-ideas', $.extend(route.resolve('/knacks/ideas', 'views/knacks'), {data: {type: 'knack-ideas'}}))
                    .state('knack-ideas-single', $.extend(route.resolve('/knacks/ideas/:id', 'views/knacks'), {data: {type: 'knack-ideas'}}))
                    .state('marketplace', $.extend(route.resolve('/marketplace', 'views/marketplace'), {data: {type: 'item-offered'}}))
                    .state('item-offered', $.extend(route.resolve('/marketplace/offered', 'views/marketplace'), {data: {type: 'item-offered'}}))
                    .state('item-wanted', $.extend(route.resolve('/marketplace/wanted', 'views/marketplace'), {data: {type: 'item-wanted'}}))
                    .state('item-wanted-single', $.extend(route.resolve('/marketplace/wanted/:id', 'views/marketplace'), {data: {type: 'item-wanted'}}))
                    .state('item-offered-single', $.extend(route.resolve('/marketplace/offered/:id', 'views/marketplace'), {data: {type: 'item-offered'}}))
                    .state('messages', route.resolve('/messages', 'views/messages'))
                    .state('messages-to', route.resolve('/messages/:id', 'views/messages'))
                    .state('register', route.resolve('/register/:uuid', 'views/profile'))
                    .state('reset-password', route.resolve('/password/resetPassword/:uuid', 'views/homepage/index'))
                    .state('private-profile', {
                        url : '/private-profile',
                        controllerUrl : [
                             'views/profile/app.js'
                        ],
                        templateUrl: 'views/profile/index.html'
                    })
                    .state('public-profile', {
                        url : '/public/:public_url',
                        controllerUrl : [
                             'views/profile/app.js'
                        ],
                        templateUrl: 'views/profile/index.html'
                    })
                    .state('feed', route.resolve('/feed', 'views/feed/knacks'))          //*******//
                    .state('feed-knacks', route.resolve('/feed/knacks', 'views/feed/knacks'))
                    .state('feed-business', route.resolve('/feed/business', 'views/feed/business'));
                    // .state('page-not-found', route.resolve('/page_not_found', 'views/profile'))

                $urlRouterProvider.otherwise("/");
                $httpProvider.defaults.xsrfCookieName = 'csrftoken';
                $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
                // $httpProvider.interceptors.push('httpInterceptor');
            }
        ]);

        app.service('rest', ['$rootScope', function ($rootScope) {
            $rootScope.restProtocol = "http";
            $rootScope.restURL = webApiPath;
        }]);

        app.service('restricted', ['$rootScope', 'localStorageService', '$http',
            function ($rootScope, localStorageService, $http) {
            $rootScope.restricted = function () {
                $rootScope.token = localStorageService.get('Authorization');
                $http.defaults.headers.common['Authorization'] = localStorageService.get('Authorization');
                if ($rootScope.token === null) {
                    $rootScope.is_authenticated = false;
                    $rootScope.profile_user = null;
                } else {
                    $rootScope.is_authenticated = true;
                    $rootScope.profile_user = {
                        'user_id': localStorageService.get('user_id'),
                        'full_name': localStorageService.get('full_name'),
                        'college': localStorageService.get('college'),
                        'picture': localStorageService.get('picture') ? localStorageService.get('picture'):'images/users/no_avatar.png'
                    };
                }
                //setTimeout(function () {
                //    if ($rootScope.token === null) {
                //        console.log('Empty token auth');
                //        $rootScope.is_authenticated = false;
                //        // window.location = "#/login";
                //    }
                //}, 100);
            };
        }]);

        app.service('tokenError', ['localStorageService', '$rootScope',
            function (localStorageService, $rootScope) {
            $rootScope.checkTokenError = function (error) {
                if (error.data && error.data['detail'] == 'Invalid token') {
                    console.log('invalid token');
                    localStorageService.clearAll();
                    $rootScope.restricted();
                }
            }
        }]);

        app.factory('user', ['$http', '$rootScope', '$resource', 'restricted',
            function($http, $rootScope, $resource, restricted) {
                $rootScope.restricted();
                
                var profile_resource = $resource(":protocol://:url/api/accounts/profile", {
                    protocol: $rootScope.restProtocol,
                    url: $rootScope.restURL
                });

                var user = {};

                $rootScope.$watch(
                    function () { return $rootScope.is_authenticated; },
                    function (new_value) {
                        if (new_value) {
                            profile_resource.get(function(result) {
                                user = result;
                            });
                        } else {
                            user = {};
                        }
                    },
                    true
                );
                
                var connect_resource = $resource(":protocol://:url/api/accounts/profile/connect?id=:id", {
                    protocol: $rootScope.restProtocol,
                    url: $rootScope.restURL,
                    id: '@id'
                });
                function connect(user_to_connect) {
                    connect_resource.save({id: user_to_connect.id}, function() {
                        user.connections.push(user_to_connect);
                    })
                }
                
                var disconnect_resource = $resource(":protocol://:url/api/accounts/profile/disconnect?id=:id", {
                    protocol: $rootScope.restProtocol,
                    url: $rootScope.restURL,
                    id: '@id'
                });
                function disconnect(user_to_disconnect) {
                    disconnect_resource.save({id: user_to_disconnect.id}, function() {
                        var index = -1;
                        for (var i = 0, l = user.connections.length; i < l; i++) {
                            if (user.connections[i].id == user_to_disconnect.id) {
                                index = i;
                                break;
                            }
                        }
                        if (index != -1) {
                            user.connections.splice(index, 1);
                        }
                    })
                }
                
                return {
                    'connect': connect,
                    'disconnect': disconnect,
                    'connected_to': function(another_user_id) {
                        if (! $rootScope.is_authenticated) {
                            return false;
                        }
                        if (! user.connections) {
                            return false;
                        }

                        for (var i = 0, l = user.connections.length; i < l; i++) {
                            if (user.connections[i].id == another_user_id) {
                                return true;
                            }
                        }
                        return false;
                    },
                    'profile': function() {return user;}
                }
            }
        ]);
        
        app.factory('notification', ['$http', '$rootScope', '$resource', 'restricted',
            function($http, $rootScope, $resource, restricted) {
                $rootScope.restricted();
                
                var notifications = [];
                var notifications_resource = $resource(":protocol://:url/api/accounts/profile/notifications", {
                    protocol: $rootScope.restProtocol,
                    url: $rootScope.restURL
                });

                $rootScope.$watch(
                    function () { return $rootScope.is_authenticated; },
                    function (new_value) {
                        if (new_value) {
                            notifications_resource.get(function(result) {
                                notifications = result.results;
                            });
                        } else {
                            notifications = [];
                        }
                    },
                    true
                );
                
                function unread() {
                    var result = [];
                    for (var i = 0, l = notifications.length; i < l; i++) {
                        if (notifications[i].is_read == false) {
                            result.push(notifications[i]);
                        }
                    }
                    return result;
                }
                
                var read_notifications_resource = $resource(":protocol://:url/api/accounts/profile/notifications/read?id=:id", {
                    protocol: $rootScope.restProtocol,
                    url: $rootScope.restURL,
                    id: '@id'
                });
                
                function read(notification) {
                    read_notifications_resource.save({id: notification.id}, function(result) {
                        for (var i = 0, l = notifications.length; i < l; i++) {
                            if (notifications[i].id == notification.id) {
                                notifications[i].is_read = true;
                                break;
                            }
                        }
                    });
                }
                
                return {
                    all: function() {return notifications;},
                    unread: unread,
                    read: read
                }
            }
        ]);


        app.directive('fileModel', ['$parse', function ($parse) {
            return {
                restrict: 'A',
                link: function(scope, element, attrs) {
                    var model = $parse(attrs.fileModel);
                    var modelSetter = model.assign;

                    element.bind('change', function(){
                        scope.$apply(function(){
                            modelSetter(scope, element[0].files[0]);
                        });
                    });
                }
            };
        }]);

        app.directive("outsideClick", ['$document','$parse', function( $document, $parse ){
            return {
                link: function( $scope, $element, $attributes ){
                    var scopeExpression = $attributes.outsideClick,
                        onDocumentClick = function(event){
                            var isChild = $element.get(0) == event.target || $element.find(event.target).length > 0;
                            var isVisible = $element.is(':visible');

                            if(!isChild && isVisible) {
                                $scope.$apply(scopeExpression);
                            }
                        };

                    $document.on("click", onDocumentClick);

                    $element.on('$destroy', function() {
                        $document.off("click", onDocumentClick);
                    });
                }
            }
        }]);

        app.directive('selectOnClick', ['$window', function ($window) {
            return {
                restrict: 'A',
                link: function (scope, element, attrs) {
                    element.on('click', function () {
                        if (!$window.getSelection().toString()) {
                            // Required for mobile Safari
                            this.setSelectionRange(0, this.value.length)
                        }
                    });
                }
            };
        }]);

        app.factory('Message', function($websocket, $rootScope) {
            var last_connection = null;

            return function(token, user1_id, user2_id) {
                if (last_connection) {
                    last_connection.close();
                }

                // Generate room id
                var room_id = user1_id > user2_id ? user1_id + '&' + user2_id : user2_id + '&' + user1_id;

                var ws = $websocket('ws://' + webApiPath + '/ws/'+ room_id + '?subscribe-broadcast&publish-broadcast&echo&token=' + token);
                var collection = [];
                last_connection = ws;

                ws.onMessage(function(event) {
                    if (event.data === $rootScope.heartbeat_msg) {
                        return;
                    }

                    var res;
                    try {
                        res = JSON.parse(event.data);
                    } catch (e) {
                        res = {'username': 'anonymous', 'message': event.data};
                    }

                    collection.push({
                        data: res,
                        timeStamp: event.timeStamp
                    });
                });

                ws.onError(function(event) {
                    console.log('connection Error', event);
                });

                ws.onClose(function(event) {
                    console.log('connection closed', event);
                });

                ws.onOpen(function() {
                    console.log('connection open');
                });

                return {
                    collection: collection,                  
                    status: function () {
                        return ws.readyState;
                    },
                    send: function (message) {
                        ws.send(message);
                    }
                }
            };
        });

        app.run(function($FB){
            $FB.init('1089204291111136');
        });

        app.config(['$locationProvider', 
            function($locationProvider){
                //$locationProvider.html5Mode(true).hashPrefix('!');
            }
        ]);

        //Bootstrap Angular
        angularAMD.bootstrap(app);
        angularAMD.processQueue();

        return app;
    });
