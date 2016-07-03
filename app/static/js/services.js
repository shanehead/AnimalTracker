'use strict';
var animalTracker = angular.module('AngularAnimalTracker');

animalTracker.factory('AuthService', ['$q', '$timeout', '$http',
    function ($q, $timeout, $http) {
        // user variable for this service
        var user = null;

        // return available functions for use in controllers
        return ({
            isLoggedIn: isLoggedIn,
            getUser: getUser,
            post_user: post_user,
            login: login,
            logout: logout
        });

    function isLoggedIn() {
        if (user != null) {
            return true;
        } else {
            return false;
        }
    };

    function getUser() {
        return user;
    };

    function post_user(userData) {
        console.log("post_user start");
        $http.post('/api/users', {name: userData.name, email: userData.email, avatar: userData.picture})
            .success(function (data, status) {
                if (status === 200 || status === 201 && data.result) {
                    console.log("post_user post successful");
                    console.log(data);
                    user = data;
                    return user;
                } else {
                    return null;
                }
            })
            .error(function (data) {
                console.log("post_user failed");
                return null;
            });
    };

    function login(userData) {
        var deferred = $q.defer();
        console.log("AuthService.login start");
        $http.get('/api/users', {
            params: {'q': {'filters': [{"name": "email", "op": "==", "val": userData.email}]}}
        }).then(function (response) {
            var data = response.data;
            console.log("Get users returned " + data.num_results + " results");
            console.log(data);
            if (data.num_results == 0) {
                console.log("No user returned, post new one");
                user = post_user(userData);
                console.log("User posted");
                if (user === null) {
                    console.log("User was null, reject");
                    deferred.reject()
                } else {
                    console.log("User was not null, resolve");
                    console.log(user);
                    deferred.resolve();
                }
            } else {
                console.log("User returned")
                user = data.objects[0];
            }
            console.log("User stored is now");
            console.log(user);
            deferred.resolve();
        }, function (x) {
            if (post_user(userData) === null) {
                deferred.reject();
            } else {
                deferred.resolve();
            }
        });
        console.log('AuthService.login return');
        return deferred.promise;
    };

    function logout() {
        user = null;
    };
}]);

animalTracker.service('fileUpload', ['$http', '$q',
    function ($http, $q) {
        this.uploadFileToUrl = function (file, uploadUrl) {
            var deferred = $q.defer();
            console.log("fileUpload");
            console.log(file);
            var fd = new FormData();
            fd.append('file', file);
            $http.post(uploadUrl, fd, {
                transformRequest: angular.identity,
                headers: {'Content-Type': undefined}
            })
            .success(function (data, status) {
                console.log("fileUpload success");
                console.log(status);
                console.log(data);
                deferred.resolve(data.photo_uri);
            })
            .error(function () {
                console.log("fileUpload error");
                deferred.reject();
            })
            return deferred.promise;
        }
    }
]);

animalTracker.service('AnimalService', ['$http',
    function ($http) {
        this.getAnimal = function (animalId) {
            console.log("AnimalService");
            console.log("animal_id");
            console.log(animalId);
            return $http.get('/api/animals/' + animalId);
        }
    }
]);
