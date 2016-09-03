'use strict';
define(['angular'], function(ng) {

    var routeResolver = function() {

        this.$get = function() {
            return this;
        };

        this.routeConfig = function() {
            // pathDirectory is main paths to call from server
            // 
            var pathDirectory = '',
                controllersDirectory = '/',

                setBaseDirectories = function(viewsDir, controllersDir) {
                    pathDirectory = viewsDir;
                    controllersDirectory = controllersDir;
                },
                //given a name "app/about" append
                // the pathDirectory to the front
                //ex: "/static/app/about"
                getPath = function(name) {
                    return pathDirectory + name;
                },

                //given a path adds /index.html to current scope 
                // of the html 
                // ex: /static/app/about/index.html
                getTemplateUrl = function(path){
                    return path + '/index.html'
                },

                // given the current scopes path and controller name
                // will provide the controllers path
                // ex: //static/app/about/js/controllers/aboutCtrl.js
                getControllersPath = function(path) {
                    return path + controllersDirectory + 'app.js'
                },

                //extracts the last element of the path "app/about" -> 'about' 
                // and assigns it a name aboutCtrl
                getController = function(baseName){
                    var array = baseName.split('/'),
                        last_element = array.pop();
                    return last_element + 'Ctrl';
                };

            return {
                setBaseDirectories: setBaseDirectories,
                getControllersPath: getControllersPath,
                getPath: getPath,
                getTemplateUrl: getTemplateUrl,
                getController : getController
            };
        }();

        this.route = function(routeConfig) {

            var resolve = function(urlPath, baseName) {

                var routeDef, folderPath, controllerPath, controller;

                routeDef = {};
                folderPath = routeConfig.getPath(baseName)
                controller = routeConfig.getController(baseName)

                routeDef.templateUrl = routeConfig.getTemplateUrl(folderPath);
                routeDef.controller = controller;
                routeDef.url = urlPath;
                controllerPath = routeConfig.getControllersPath(folderPath, controller);
                
                routeDef.resolve = {
                    load: ['$q', '$rootScope',
                        function($q, $rootScope) {
                            var dependencies = [controllerPath];
                            return resolveDependencies($q, $rootScope, dependencies);
                        }
                    ]
                };

                return routeDef;
            },

                resolveDependencies = function($q, $rootScope, dependencies) {
                    var defer = $q.defer();
                    require(dependencies, function() {
                        defer.resolve();
                        $rootScope.$apply()
                    });

                    return defer.promise;
                };

            return {
                resolve: resolve
            }
        }(this.routeConfig);

    };

    var servicesApp = ng.module('routeResolverServices', []);


    //Must be a provider since it will be injected into module.config()    
    servicesApp.provider('routeResolver', routeResolver);
  
    return servicesApp
});