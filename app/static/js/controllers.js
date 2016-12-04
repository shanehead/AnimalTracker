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

animalTracker.controller('AnimalController', ['animal', '$scope',
    function (animal, $scope) {
        console.log('AnimalController');
        console.log('animal=');
        console.log(animal);
        $scope.animal = animal;
    }
]);

animalTracker.controller('AnimalWeightController', ['animal', '$stateParams', '$scope', 'AnimalService',
    function (animal, $stateParams, $scope, AnimalService) {
        console.log('AnimalWeightController');
        console.log(animal);
        $scope.animal = animal;
        var weight_series = [];
        
        $scope.animal.weights.forEach(function (animalWeight) {
            var weight_date = new Date(animalWeight.date);
            console.log("date");
            console.log(weight_date);
            weight_series.push([weight_date.getTime(), parseFloat(animalWeight.weight)]);
        });
        weight_series.sort(function(a,b) {return a[0] - b[0]});
            
        $scope.chartConfig = {
            options: {
                chart: {
                    type: 'line',
                    zoomType: 'x'
                }
            },
            series: [{
                name: "Weight",
                data: weight_series
            }],
            title: {
                text: $scope.animal.name
            },
            xAxis: {
                type: 'datetime',
                labels: { 
                    format: '{value:%m/%d/%y}' 
                },
                title: {text: 'Date'}
            },
            yAxis: {
                title: {text: 'Weight (' + $scope.animal.weight_units + ')'}
            },
            func: function(chart) {
                chart.title.text = $scope.animal.name;
                console.log('chart');
                console.log(chart);
                console.log('chart.series');
                console.log(chart.series);
            }
        }
        
        $scope.reloadAnimal = function () {
            console.log("Reload Animal");
            AnimalService.getAnimal($stateParams.animalId).then(function (response) {
                $scope.animal = response;
                console.log("$scope.animal");
                console.log($scope.animal);
                $scope.weights = $scope.animal.weights.sort(function(a,b) {
                    return (a.date > b.date) ? 1 : ((b.date > a.date) ? -1 : 0);});
                console.log($scope.weights);
            })
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

animalTracker.controller('EditAnimalWeightController', ['AnimalService', '$scope', '$stateParams', '$http',
    function (AnimalService, $scope, $stateParams, $http) {
        $scope.weight_units = function() {
            return $scope.animal.weight_units;     
        };
        
        $scope.saveWeight = function(data, id) {
            var chart = $scope.chartConfig.getHighcharts();
            var weight_date = new Date(data.date);
            console.log("current series", chart.series[0]);
            // Get the weight for the given id.  We need the existing date to be able to find it in our series
            // in case it was updated in the form. Then find it and update it
            $http.get('api/weights/' + id).then(function (response) {
                console.log("response.data: ", response.data)
                var found_weight_date = new Date(response.data.date).getTime();
                chart.series[0].data.forEach(function (animalWeight, idx) {
                    console.log("animalWeight.x: ", animalWeight.x);
                    if (animalWeight.x == found_weight_date) {
                        console.log("updating idx", idx);
                        chart.series[0].data[idx].update({x: weight_date.getTime(), y: parseFloat(data.weight)});
                        console.log("updated series, now put weight", chart.series[0]);
                        console.log(data);
                        $http.put('api/weights/' + id, {date: weight_date, weight: data.weight}).then(
                            function (response) {
                                console.log("weight has ben PUT, reload animal");
                                $scope.reloadAnimal()
                        });
                    }
                });
            });
        };
        
        $scope.removeWeight = function(in_date, id) {
            console.log("removeWeight");
            console.log(in_date);
            console.log(id);
            var chart = $scope.chartConfig.getHighcharts();
            var weight_date = new Date(in_date).getTime();
            // We need to find this date in our series and remove it
            chart.series[0].data.forEach(function(animalWeight, idx) {
                console.log("animalWeight.x: ", animalWeight.x);
                console.log("weight_date: ", weight_date);
                if (animalWeight.x == weight_date)
                {
                    console.log("removing idx", idx)
                    chart.series[0].removePoint(idx, true);
                }
            })
            return $http.delete('api/weights/' + id).then(function(response) { $scope.reloadAnimal()});
        };
        $scope.reloadAnimal();
    }
])

animalTracker.controller('EditAnimalController', ['AnimalService', '$scope', '$stateParams', '$http',
    function (AnimalService, $scope, $stateParams, $http) {
        $scope.opened = {};                
        
        $scope.weight_units = [
            {value: 'lb', text: 'lb'},
            {value: 'kg', text: 'kg'},
            {value: 'g', text: 'g'}
        ];
        
        $scope.open = function($event, elementOpened) {
            $event.preventDefault();
            $event.stopPropagation();
            $scope.opened[elementOpened] = !$scope.opened[elementOpened];            
        };
        
        $scope.saveWeight = function(data, id) {
            var chart = $scope.chartConfig.getHighcharts();
            var weight_date = new Date(data.date);
            console.log("current series", chart.series[0]);
            console.log("saveWeight");
            console.log(data);
            return $http.put('api/weights/' + id, {date: weight_date, weight: data.weight}).then(function(response) { $scope.reloadAnimal()});
        };
        
        $scope.removeWeight = function(in_date, id) {
            console.log("removeWeight");
            console.log(in_date);
            console.log(id);
            var chart = $scope.chartConfig.getHighcharts();
            var weight_date = new Date(in_date).getTime();
            // We need to find this date in our series and remove it
            chart.series[0].data.forEach(function(animalWeight, idx) {
                console.log("animalWeight.x: ", animalWeight.x);
                console.log("weight_date: ", weight_date);
                if (animalWeight.x == weight_date)
                {
                    console.log("removing idx", idx)
                    chart.series[0].removePoint(idx, true);
                }
            });
            return $http.delete('api/weights/' + id).then(function(response) { $scope.reloadAnimal()});
        };
    }
]);

animalTracker.controller('EditAnimalNoteController', ['AnimalService', '$scope', '$http', '$stateParams',
    function (AnimalService, $scope, $http, $stateParams) {
       $scope.notes = $scope.animal.notes;

       $scope.reloadNotes = function () {
            console.log("Reload Animal Notes");
            AnimalService.getAnimal($stateParams.animalId).then(function (response) {
                $scope.animal = response;
                console.log("$scope.animal");
                console.log($scope.animal);
                $scope.notes = $scope.animal.notes;
            })
        };

        $scope.saveNote = function(data, id) {
            $http.put('api/animal_notes/' + id, data).then(function (response) {
                $scope.reloadNotes();
            });
        };

        $scope.removeNote = function(id) {
            console.log("removeNote");
            console.log(id);
            return $http.delete('api/animal_notes/' + id).then(function(response) { $scope.reloadNotes()});
        };

        $scope.addNote = function() {
            $http.post('api/animal_notes', {
                animal_id: $scope.animal.id,
                date: new Date(),
                note: '',
                user_id: $scope.animal.owner_id
            }).then(
                function (response) {
                    console.log("new note created, reload Notes");
                    $scope.reloadNotes();
                }
            )
        }
        $scope.reloadNotes();
    }
]);
