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

animalTracker.controller('AnimalController', ['animal', '$scope', 'moment',
    function (animal, $scope, moment) {
        console.log('AnimalController');
        console.log('animal=');
        console.log(animal.data);
        $scope.animal = animal.data;
        // Need to calculate the age here
        var diff = moment().preciseDiff(moment(animal.dob), true);
        if (diff.years > 0) {
            if (diff.months > 0) {
                if (diff.days > 0) {
                    $scope.animal.age = diff.years + " years, " + diff.months + " months, " + diff.days + " days";
                } else {
                    $scope.animal.age = diff.years + " years, " + diff.months + " months"
                }
            } else {
                $scope.animal.age = diff.years + " years"
            }
        } else if (diff.months > 0) {
            if (diff.days > 0) {
                $scope.animal.age = diff.months + " months, " + diff.days + " days";
            } else {
                $scope.animal.age = diff.months + " months";
            }
        } else if (diff.days > 0) {
            $scope.animal.age = diff.days + " days";
        }
    }
]);

animalTracker.controller('AnimalWeightController', ['$stateParams', '$scope', '$http',
    function ($stateParams, $scope, $http) {
        console.log('AnimalWeightController');
        $scope.animalId = $stateParams.animalId;
            
        $scope.chartConfig = {
            options: {
                chart: {
                    type: 'line',
                    zoomType: 'x'
                }
            },
            series: [{
                name: "Weight",
                data: []
            }],
            title: {
                text: 'Weight'
            },
            xAxis: {
                type: 'datetime',
                labels: { 
                    format: '{value:%m/%d/%Y}' 
                },
                title: {text: 'Date'}
            },
            yAxis: {
                title: {text: 'Weight'}
            },
            func: function(chart) {
                $http.get('/api/weights', {
                    params: {
                        'q': {
                            'filters': [{"name": "animal_id", "op": "==", "val": $scope.animalId}],
                            'order_by': [{"field": "date", "direction": "asc"}]
                        }
                    }
                }).then(function (response) {
                    var data = response.data;
                    console.log("get weights returned");
                    console.log(data);
                    var animal = data.objects[0].animal;
                    $scope.chartConfig.yAxis.title.text = 'Weight (' + animal.weight_units + ')';
                    data.objects.forEach(function (animalWeight) {
                        chart.title.text = animalWeight.animal.name;
                        var weight_date = new Date(animalWeight.date);
                        console.log("date");
                        console.log(weight_date);
                        chart.series[0].addPoint([weight_date.getTime(), animalWeight.weight], true);
                    });
                    console.log("now");
                    console.log(Date.now());
                    console.log('chart.series');
                    console.log(chart.series);
                    console.log('chart');
                    console.log(chart);
                }), function () {
                    console.log("error getting weights");
                }
            }
        }
    }
]);

animalTracker.controller('QRController', ['$stateParams', '$scope', '$state',
    function ($stateParams, $scope, $state) {
        console.log('QRController');
        $scope.string = $state.href('animal', {animalId: $stateParams.animalId}, {absolute: true});
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

animalTracker.controller('AddAnimalWeightController', ['$stateParams', '$http', '$scope',
    function ($stateParams, $http, $scope) {
        console.log('AddAnimalWeightController');
        console.log($stateParams);
        var vm = this;

        vm.onSubmit = onSubmit;
        vm.animal_weight = {}
        vm.url = 'http://shanehead.ddns.net:5000/add_animal_weight';

        vm.animalWeightFields = [
            {
                key: 'weight',
                type: 'input',
                templateOptions: {
                    type: 'text',
                    label: 'Weight',
                    placeholder: 'Weight',
                    required: true
                }
            },
            {
                key: 'date',
                type: 'input',
                templateOptions: {
                    type: 'date',
                    label: 'Date of Weight',
                    placeholder: 'Date of Weight',
                    required: false
                }
            }
        ];

        function onSubmit() {
            console.log("onSubmit");
            console.log(vm);
            console.log($stateParams);
            vm.animal_weight.animal_id = $stateParams.animalId;
            $http.post('/api/weights', {
                animal_id: vm.animal_weight.animal_id, weight: vm.animal_weight.weight,
                date: vm.animal_weight.date
            })
                .success(function (data, status) {
                    console.log("post animal weight success");
                    console.log(status);
                    console.log(data);
                    // Update the chart
                    var chart = $scope.chartConfig.getHighcharts();
                    var weight_date = new Date(data.date);
                    console.log("weight_date");
                    console.log(weight_date);
                    chart.series[0].addPoint([weight_date.getTime(), data.weight], true);
                })
                .error(function () {
                    console.log("post animal weight error");
                })
        };
    }
]);
