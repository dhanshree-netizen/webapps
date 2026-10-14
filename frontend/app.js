var app = angular.module("rescueApp", []);

app.service("VolunteerService", function ($http) {
    var baseUrl = "http://localhost:5000";

    this.getVolunteers = function () {
        return $http.get(baseUrl + "/volunteers");
    };

    this.addVolunteer = function (volunteer) {
        return $http.post(baseUrl + "/volunteers", volunteer);
    };

    this.updateVolunteer = function (id, volunteer) {
        return $http.put(baseUrl + "/volunteers/" + id, volunteer);
    };

    this.deleteVolunteer = function (id) {
        return $http.delete(baseUrl + "/volunteers/" + id);
    };

    this.getStatus = function () {
        return $http.get(baseUrl + "/status");
    };
});

app.directive("rescueTitle", function () {
    return {
        restrict: "E",
        template: "<h1>RescueConnect</h1>"
    };
});

app.controller("MainController", function ($scope, VolunteerService) {
    $scope.page = "login";
    $scope.volunteers = [];
    $scope.search = "";
    $scope.editingId = null;
    $scope.message = "";
    $scope.errorMessage = "";
    $scope.mode = "Checking backend...";
    $scope.newVolunteer = {
        name: "",
        city: "",
        experience: ""
    };

    $scope.checkStatus = function () {
        VolunteerService.getStatus()
            .then(function (response) {
                $scope.mode = response.data.mode;
            })
            .catch(function () {
                $scope.mode = "Backend not connected";
            });
    };

    $scope.loadVolunteers = function () {
        VolunteerService.getVolunteers()
            .then(function (response) {
                $scope.volunteers = response.data;
                $scope.errorMessage = "";
                $scope.checkStatus();
            })
            .catch(function () {
                $scope.errorMessage = "Cannot reach backend. Start it using npm run dev.";
            });
    };

    $scope.login = function () {
        if ($scope.username === "admin" && $scope.password === "1234") {
            $scope.page = "volunteers";
            $scope.error = false;
            $scope.loadVolunteers();
        } else {
            $scope.error = true;
        }
    };

    $scope.logout = function () {
        $scope.page = "login";
        $scope.username = "";
        $scope.password = "";
        $scope.message = "";
        $scope.errorMessage = "";
    };

    $scope.resetForm = function () {
        $scope.newVolunteer = {
            name: "",
            city: "",
            experience: ""
        };
        $scope.editingId = null;
    };

    $scope.addVolunteer = function () {
        if (!$scope.newVolunteer.name || !$scope.newVolunteer.city || !$scope.newVolunteer.experience) {
            $scope.errorMessage = "Please fill all fields.";
            return;
        }

        VolunteerService.addVolunteer($scope.newVolunteer)
            .then(function () {
                $scope.message = "Volunteer added successfully.";
                $scope.errorMessage = "";
                $scope.resetForm();
                $scope.loadVolunteers();
            })
            .catch(function (response) {
                $scope.errorMessage = response.data.message || "Failed to add volunteer.";
            });
    };

    $scope.editVolunteer = function (volunteer) {
        $scope.newVolunteer = {
            name: volunteer.name,
            city: volunteer.city,
            experience: volunteer.experience
        };
        $scope.editingId = volunteer._id;
        $scope.message = "Editing " + volunteer.name;
        $scope.errorMessage = "";
    };

    $scope.updateVolunteer = function () {
        if (!$scope.newVolunteer.name || !$scope.newVolunteer.city || !$scope.newVolunteer.experience) {
            $scope.errorMessage = "Please fill all fields.";
            return;
        }

        VolunteerService.updateVolunteer($scope.editingId, $scope.newVolunteer)
            .then(function () {
                $scope.message = "Volunteer updated successfully.";
                $scope.errorMessage = "";
                $scope.resetForm();
                $scope.loadVolunteers();
            })
            .catch(function (response) {
                $scope.errorMessage = response.data.message || "Failed to update volunteer.";
            });
    };

    $scope.deleteVolunteer = function (id) {
        if (!confirm("Are you sure you want to delete this volunteer?")) {
            return;
        }

        VolunteerService.deleteVolunteer(id)
            .then(function () {
                $scope.message = "Volunteer deleted successfully.";
                $scope.errorMessage = "";
                if ($scope.editingId === id) {
                    $scope.resetForm();
                }
                $scope.loadVolunteers();
            })
            .catch(function (response) {
                $scope.errorMessage = response.data.message || "Failed to delete volunteer.";
            });
    };

    $scope.cancelEdit = function () {
        $scope.resetForm();
        $scope.message = "Edit cancelled.";
        $scope.errorMessage = "";
    };
});
