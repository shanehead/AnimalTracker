'use strict';

var animalTracker = angular.module('AngularAnimalTracker');

animalTracker.controller('LoginController', ['$scope', 'GAuth', 'GData', 'AuthService', '$state', '$cookies',
    function ($scope, GAuth, GData, AuthService, $state, $cookies) {
        if (GData.isLogin()) {
            console.log("GAuth.isLogin -> state.go(user)")
            $state.go('user');
        }
        var ifLogin = function() {
            console.log('LoginController.ifLogin start');
            $cookies.put('userId', GData.getUserId());
            var user = GData.getUser();
            console.log(user.name + ' logged in');
            console.log(user);
            AuthService.login(user).then(function () {
                console.log('change state to user');
                $state.go('user');
            });
        };

        $scope.doLogin = function() {
            GAuth.checkAuth().then(
                function() {
                    console.log("doLogin checkAuth.then -> ifLogin")
                    ifLogin();
                },
                function() {
                    console.log("checkAuth.then -> GAuth.login")
                    GAuth.login().then(function() {
                        console.log("GAuth.login -> ifLogin")
                        ifLogin();
                    });
                }
            );
        };
}]);

animalTracker.controller('UserController', ['AuthService', '$rootScope', '$http',
    function (AuthService, $rootScope, $http) {
        console.log('UserController');
        $rootScope.user = AuthService.getUser();
        reloadUser();
        console.log("rootScope.user is now ");
        console.log($rootScope.user);

        function reloadUser(user) {
            $http.get('/api/users/' + $rootScope.user.id).then(function (response) {
                var data = response.data;
                console.log("reloadUser got updated user info");
                console.log(data);
                $rootScope.user = data;
            })
        }
    }
]);

animalTracker.controller('AnimalController', ['$stateParams', '$http', '$rootScope', 'moment',
    function ($stateParams, $http, $rootScope, moment) {
        console.log('AnimalController');
        $http.get('/api/animals/' + $stateParams.animalId)
            .then(function (response) {
                var data = response.data;
                console.log("get animal returned");
                console.log(data)
                if (data.num_results == 0) {
                   console.log("no results"); 
                }
                $rootScope.animal = data;
                // Need to calculate the age here
                var diff = moment().preciseDiff(moment(data.dob), true);
                if (diff.years > 0) {
                    if (diff.months > 0) {
                        if (diff.days > 0) {
                            $rootScope.animal.age = diff.years + " years, " + diff.months + " months, " + diff.days + " days";
                        } else {
                            $rootScope.animal.age = diff.years + " years, " + diff.months + " months"
                        }
                    } else {
                        $rootScope.animal.age = diff.years + " years"
                    }
                } else if (diff.months > 0) {
                    if (diff.days > 0) {
                        $rootScope.animal.age = diff.months + " months, " + diff.days + " days";
                    } else {
                        $rootScope.animal.age = diff.months + " months";
                    }
                } else if (diff.days > 0) {
                    $rootScope.animal.age = diff.days + " days";
                }
            }, function(x) {
                console.log("error getting animal");
            })
    }
]);

animalTracker.controller('AddAnimalController', ['fileUpload', 'AuthService', '$state', '$http',
    function (fileUpload, AuthService, $state, $http) {
        console.log('AddAnimalController');
        var vm = this;

        vm.onSubmit = onSubmit;
        vm.animal = {}
        vm.url = 'http://shanehead.ddns.net:5000/add_animal';
        vm.fileUpload = fileUpload;

        vm.animalFields = [
            {
                key: 'name',
                type: 'input',
                templateOptions: {
                    type: 'text',
                    label: 'Name',
                    placeholder: 'Animal Name',
                    required: true
                }
            },
            {
                key: 'species_common',
                type: 'input',
                templateOptions: {
                    type: 'text',
                    label: 'Species (Common)',
                    placeholder: 'Species (Common)',
                    required: true
                }
            },
            {
                key: 'species',
                type: 'input',
                templateOptions: {
                    type: 'text',
                    label: 'Species',
                    placeholder: 'Species',
                    required: false
                }
            },
            {
                key: 'dob',
                type: 'input',
                templateOptions: {
                    type: 'date',
                    label: 'Date of Birth',
                    placeholder: 'Date of Birth',
                    required: false
                }
            },
            {
                key: 'weight_units',
                type: 'select',
                templateOptions: {
                    label: 'Weight Units',
                    options: [
                        {
                            "name": "lb",
                            "value": "lb"
                        },
                        {
                            "name": "kg",
                            "value": "kg"
                        },
                        {
                            "name": "g",
                            "value": "g"
                        }
                    ]
                }
            },
            {
                key: 'avatar',
                type: 'upload',
                templateOptions: {
                    label: 'Avatar'
                }
            }
        ];

        function onSubmit() {
            console.log("onSubmit");
            console.log(vm);
            // Find our upload file.  we know it is index 5 in the vm.animalFields array
            var file = vm.animalFields[5].formControl.upload_file;
            console.log("onSubmit call upload with promise");
            var promise = vm.fileUpload.uploadFileToUrl(file, vm.url);
            promise.then(function (photo_uri) {
                vm.animal.avatar = photo_uri;
                console.log("upload worked, photo_uri is");
                console.log(photo_uri);
                console.log("avatar is ");
                console.log(vm.animal.avatar);
                var user = AuthService.getUser();
                console.log("getUser returned");
                console.log(user);
                vm.animal.owner_id = user.id;
                console.log(vm.animal);
                
                $http.post('/api/animals', {name: vm.animal.name, species: vm.animal.species, 
                                            species_common: vm.animal.species_common,
                                            dob: vm.animal.dob, avatar: vm.animal.avatar,
                                            weight_units: vm.animal.weight_units,
                                            owner_id: vm.animal.owner_id})
                .success(function (data, status) {
                    console.log("post animal success");
                    console.log(status);
                    console.log(data);
                })
                .error(function () {
                    console.log("post animal error");
                })
                $state.go('user', {}, {reload: true});
            }, function () {
                console.log("upload failed");
            });
        }
    }
]);
