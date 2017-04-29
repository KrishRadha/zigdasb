var eventsapp=angular.module('eventsApp',[]);
console.log('HI1');

eventsapp.controller('EventCont',['$scope','$http', '$compile','$sce',


    function EventCont($scope,$http,$compile,$sce){
    // console.log('HI1');

      $scope.Register_Now=function(){

        data={user:$scope.user}

        $http.post('/register',data).then(function(response){
            resp=response['data']
            if(resp.hasOwnProperty('error')){

              $('#error_name').html(response['error']);
              $('#userpre').hide();
              $('#usereg').hide();
              $('#error_div').show();


            }

            else if(resp.hasOwnProperty('done')){
              console.log('eheheheeheh');
              $("#regidiv").html(resp['regid']);
              $('#userpre').hide();
              $('#usereg').hide();
              $('#us_done_reg_div').show();
              //setInterval(function(){window.location='/';},5000);


            }


        });


        }

    }]);

eventsapp.directive("fileread", [function () {
    return {
        scope: {
            fileread: "="
        },
        link: function (scope, element, attributes) {
            element.bind("change", function (changeEvent) {
                var reader = new FileReader();
                reader.onload = function (loadEvent) {
                    scope.$apply(function () {
                        scope.fileread = loadEvent.target.result;
                    });
                }
                reader.readAsDataURL(changeEvent.target.files[0]);
            });
        }
    }
}]);
