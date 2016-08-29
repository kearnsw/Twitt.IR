angular.module('activeDateService', ['dashboard'])
    .factory('activeDate', function() {
        var data = {
        activeDate: ''
    };

    return {
        getDate: function () {
            return data.activeDate;
        },
        setDate: function (date) {
            console.log("set");
            data.activeDate = date;
        }
    };
    });