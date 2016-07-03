'use strict';

var animalTracker = angular.module('AngularAnimalTracker', [
    'ui.router', 'ngCookies', 'angular-google-gapi', 'AngularAnimalTrackerRouter',
    'formly', 'formlyBootstrap', 'angularMoment', 'ja.qr', 'highcharts-ng']);
var router = angular.module('AngularAnimalTrackerRouter', []);

router.config(['$urlRouterProvider',
		function ($urlRouterProvider) {
            $urlRouterProvider.otherwise("/login");
        }]);

router.config(['$stateProvider',
    function ($stateProvider) {
        $stateProvider
            .state('login', {
                url: '/login',
                templateUrl: 'static/partials/login.html',
                controller: 'LoginController'
            })
            .state('user', {
                url: '/user',
                templateUrl: 'static/partials/user.html',
                controller: 'UserController',
                cache: false,
                data: {requireLogin: true}
            })
            .state('add_animal', {
                url: '/add_animal',
                templateUrl: 'static/partials/add_animal.html',
                controller: 'AddAnimalController',
                data: {requireLogin: true}
            })
            .state('animal', {
                url: '/animal/:animalId',
                templateUrl: 'static/partials/animal.html',
                controller: 'AnimalController',
                resolve: {
                    animal: function (AnimalService, $stateParams) { 
                        return AnimalService.getAnimal($stateParams.animalId);
                    }
                },
                data: {requireLogin: true}
            })
            .state('qrcode', {
                url: '/qrcode/:animalId',
                templateUrl: 'static/partials/qrcode.html',
                controller: 'QRController',
            })
            //.state('animal_note', {
            //    url: '/animal_note/:animalId',
            //    templateUrl: 'static/partials/animal_note.html',
            //    controller: 'AnimalNoteController'
            //})
            .state('animal_weight', {
                url: '/animal_weight/:animalId',
                templateUrl: 'static/partials/animal_weight.html',
                controller: 'AnimalWeightController',
                data: {requireLogin: true}
            })
            //.state('alerts', {
            //    url: '/alerts',
            //    templateUrl: 'static/partials/alerts.html',
            //    controller: 'AlertController'
            //})
    }
]);

animalTracker.run(['GAuth', 'GData', 'AuthService', 'formlyConfig', '$state', '$rootScope', '$cookies',
                   '$window',
    function (GAuth, GData, AuthService, formlyConfig, $state, $rootScope, $cookies, $window) {
        $rootScope.gdata = GData;
        var CLIENT = '671703668524-m8gn0i797rop7u95hpbrqdc18duu5q5d.apps.googleusercontent.com';
        GAuth.setClient(CLIENT);
        GAuth.setScope("https://www.googleapis.com/auth/userinfo.email");

        // var currentUser = $cookies.get('userId');
        // if (currentUser) {
        //     GData.setUserId(currentUser);
        //     GAuth.checkAuth().then(
        //         function() {
        //             console.log("checkAuth.then");
        //             AuthService.login(GData.getUser()).then( function () {
        //                 console.log("CheckAuth.then -> AuthService.login.then");
        //                 if ($state.is('login')) {
        //                     $state.go('user');
        //                 }
        //             });
        //         },
        //         function () {
        //             console.log("checkAuth else");
        //             $state.go('login');
        //         }
        //     );
        // } else {
        //     console.log("run function else");
        //     $state.go('login');
        // }

        formlyConfig.setType({
            name: 'upload',
            extends: 'input',
            wrapper: ['bootstrapLabel', 'bootstrapHasError'],
            link: function(scope, el, attrs) {
                el.on("change", function (changeEvent) {
                    console.log("setType");
                    console.log(changeEvent);
                    var file = changeEvent.target.files[0];
                    if (file) {
                        var fileProp = {};
                        for (var properties in file) {
                            if (!angular.isFunction(file[properties])) {
                                fileProp[properties] = file[properties];
                            }
                        }
                        scope.fc.upload_file = file;
                        scope.fc.$setViewValue(fileProp);
                    } else {
                        scope.fc.$setViewValue(undefined);
                    }
                });
                el.on("focusout", function (focusoutEvent) {
                    // don't run validation, user is still opening file dialog
                    if ($window.document.activeElement.id === scope.id) {
                        // set it untouched
                        scope.$apply(function (scope) {
                            scope.fc.$setUntouched();
                        });
                    } else {
                        // element lost focus so trigger validation
                        scope.fc.$validate();
                    }
                });
            },
            defaultOptions: {
                templateOptions: {
                    type: 'file',
                    required: true
                }
            }
        });

        $rootScope.logout = function() {
            GAuth.logout().then(function () {
                console.log("rootscope logout");
                $cookies.remove('userId');
                $state.go('login');
            });
        };

        $rootScope.$on('$stateChangeStart', function(event, toState, toParams, fromState) {
            console.log('statechangeStart');
            console.log(event)
            console.log('toState');
            console.log(toState)
            console.log('fromstate');
            console.log(fromState)
            var shouldLogin = toState.data !== undefined &&toState.data.requireLogin 
                              && !AuthService.isLoggedIn();
            
            // Not authenticated, send to login
            if (shouldLogin) {
                var currentUser = $cookies.get('userId');
                 if (currentUser) {
                     console.log("shouldLogin, but has cookie");
                    GData.setUserId(currentUser);
                    GAuth.checkAuth().then(
                        function() {
                            console.log("stateChangestart: checkAuth.then");
                            AuthService.login(GData.getUser()).then( function () {
                                console.log("stateChangestart: CheckAuth.then -> AuthService.login.then");
                                if ($state.is('login')) {
                                    $state.go('user');
                                }
                            });
                        },
                        function () {
                            console.log("stateChangestart: checkAuth else");
                            $state.go('login');
                        }
                    );
                    return; 
                } else {
                     console.log("shouldLogin, sending to login")
                     $state.go('login');
                     event.preventDefault();
                     return;
                }
            }
            
            // authenticated previously, coming not to root main
            if (AuthService.isLoggedIn()) {
                var shouldGoToUser = fromState.name === "" && toState.name !== "user";
                console.log("shouldGoToUser, sending to user");
                if (shouldGoToUser) {
                    $state.go('user');
                    event.preventDefault();
                    return;
                }
            }
        });
        $rootScope.$on('$stateChangeSuccess', function(event, toState, toParams, fromState, fromParams, options) {
            console.log('statechangeSuccess');
            /*
            console.log(event)
            console.log('toState');
            console.log(toState)
            console.log('fromstate');
            console.log(fromState)
            */
        });
}]);
