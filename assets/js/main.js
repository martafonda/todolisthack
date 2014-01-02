$(document).ready(function(){
    var app = function() {

    this.init = function() {

    };

    this.getList = function() {
      $.ajax({
        success: function(response) {
          _.uniq();
        }
      });
    };

    this.init();

  }();

});