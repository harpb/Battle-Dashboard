BattleApp.factory('Auth', ['Base64', '$http', function (Base64, $http) {
    // initialize to whatever is in the cookie, if anything
//    $http.defaults.headers.common['Authorization'] = 'Basic ' + $cookieStore.get('authdata');

    return {
        setCredentials: function (username, password) {
            var encoded = Base64.encode(username + ':' + password);
            $http.defaults.headers.common.Authorization = 'Basic ' + encoded;
        },
        clearCredentials: function () {
            document.execCommand("ClearAuthenticationCache");
            $http.defaults.headers.common.Authorization = 'Basic ';
        }
    };
}]);