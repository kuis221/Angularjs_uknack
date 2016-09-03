//GruntFile

module.exports = function (grunt) {
    'use strict';
    require('load-grunt-tasks')(grunt);
    grunt.loadNpmTasks('grunt-contrib-connect');
    //Config Variables
    var configVars = {
        "www_server": "127.0.0.1",
        "www_port": "9768",
        "e2e_port": "9769"
    };

    grunt.initConfig({
        cvars: configVars,
        bower: {
            setup: {
                options: { install: true, copy: false }
            }
        },
        shell: {
            'webdriver-manager-update': {
                command: "node_modules/protractor/bin/webdriver-manager update",
                options: {
                    async: false
                }
            }
        },
        connect: {
            options: {
                port: 9100,
                hostname: '<%= cvars.www_server %>',
                livereload: 35729
            },
            "e2e-www": {
                options: {
                    port: '<%= cvars.e2e_port %>',
                    base: 'angular',
                    keepalive: false
                }
            },
            "serve-www": {
                options: {
                    port: '<%= cvars.www_port %>',
                    base: 'angular',
                    keepalive: true
                }
            },
            livereload: {
                options: {
                    open: true,
                    base: 'angular/'
                }
            }
        },
        concurrent: {
            server: {}
        },
        karma: {
            "unit": {
                configFile: 'karma.conf.js',
                singleRun: false
            },
            "unit-no-ngload": {
                configFile: 'test/conf/karma.unit.no_ngload.js',
                singleRun: false
            }
        },
        protractor: {
            options: {
                configFile: "protractor.conf.js"
            },
            "e2e-www": {
                options: {
                    keepAlive: true,
                    args: {
                        browser: "chrome",
                        baseUrl: "http://<%= cvars.www_server %>:<%= cvars.e2e_port %>"
                    }
                }
            }
        },
        watch: {
            less: {
                files: ["angular/**/*.less"],
                tasks: "less:development"
            },
            livereload: {
                options: {
                    livereload: true
                },
                files: [
                    'angular/**/*.{html,js,css}',
                    '!angular/common/**'
                ]
            }
        },
        less: {
            development: {
                files: {
                    "angular/style.css": "angular/style.less"
                }
            },
            production: {
                options: {
                    cleancss: true
                },
                files: {
                    "angular/style.css": "angular/style.less"
                }
            }
        },
    });


    //Basic Grunt Set Up
    grunt.registerTask('setup', [
        'bower:setup',
        'shell:webdriver-manager-update'
    ]);
    grunt.registerTask('test-base', [
        'setup'
    ]);

    //Unit Testing:
    grunt.registerTask('test-unit', [
        'test-base',
        'karma:unit'
    ]);
    //End to End Testing
    grunt.registerTask('test-e2e', [
        'test-base',
        'connect:e2e-www',
        'protractor:e2e-www'
    ]);

    //Web App
    grunt.registerTask('serve', [
        // 'less:development',
        'concurrent:server',
        'connect:livereload',
        'watch'
    ]);

};



