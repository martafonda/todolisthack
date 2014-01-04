$(document).ready(function(){

  //Toggle client-side animation for EDIT div
  function bindEditButton() {
    $('.edit-btn').unbind('click');
    $('.edit-btn').bind('click', function(){
      $(this).parents('.task:first').find('.js-edit-tsk').toggle();
    });
  };

  bindEditButton();

  //Delete AJAX method and client-side animation
  function bindDeleteButton() {
    $('.delete-btn').unbind('click');
    $('.delete-btn').bind('click', function(){
      var parent = $(this).parents('.task:first');//Select task
      var id = parent.attr('id').split('_')[1];//Retrieve task id
      $(this).parents('.task:first').remove();//Remove task
      $.ajax({
        url: '/delete',
        data: {id: id},
        type: 'post',
        success: function(response) {
    
        },
        error: function(xhr, ajaxOptions, thrownError) {

        }
      });
    });
  };

  bindDeleteButton();

  //New Task AJAX method and clien-side animation
  $('.new-btn').on('click',function(){
    var parent = $(this).parents('.new-task:first');
    var title = parent.find('input[name=title]').val();
    var description = parent.find('input[name=description]').val();
    var author = parent.find('input[name=author]').val();
    var date = parent.find('input[name=date]').val();
    $.ajax({
      url: '/task',
      data: {title: title, description: description, author: author, date: date},
      type: 'post',
      success: function(response) {
        $('#myModal').modal('hide');
        $('.task:last').after(response);
        bindEditButton();
        bindDeleteButton();
      },
      error: function(xhr, ajaxOptions, thrownError) {

      }
    });
  });

  //Method to update task AJAX
  function setUpdated(element){
      var parent = element.parents('.task:first');//Select task
      var id = parent.attr('id').split('_')[1];
      //Get information from inputs
      var title = parent.find('input[name=title]').val();
      var description = parent.find('input[name=description]').val();
      var author = parent.find('input[name=author]').val();
      var done = parent.find('input[name=done]').val();
      var date = parent.find('input[name=date]').val();
      var parsedDate = new Date(date);
      parsedDate = (parsedDate.getMonth() + 1) + '/' + parsedDate.getDate() + '/' + parsedDate.getFullYear();
      $.ajax({
        url: '/task',
        data: {id: id, title: title, description: description, author: author, done: done, date:parsedDate},
        type: 'post',
        success: function() {
            parent.find('.js-title').text(title);
            parent.find('.js-description').text(description);
            var formatedDate = new Date(date).toString().split(' ');
            formatedDate = formatedDate[1] + '. ' + formatedDate[2] + ', ' + formatedDate[3];
            parent.find('.js-date').text(formatedDate);
        },
        error: function(xhr, ajaxOptions, thrownError) {

        }
      });
    
  };

  //Animation and call to method update
  function updateButtonBinds() {
    $('.update-btn').on('click',function(){
      setUpdated($(this));
      $(this).parents('.task:first').find('.js-edit-tsk').toggle();
    });
  };
  updateButtonBinds();

  //Animation and call to change task's done state using update method
  function doneButtonBinds() {
    $('.done-btn').on('click',function(){
      var parent = $(this).parents('.task:first');
      var input = parent.find('input[name=done]');
      var val = input.val().toLowerCase();
      if ((val == true) || (val == 'true')) {
        input.val(false); 
        parent.find(".js-task-span").unwrap();
      } else {
        input.val(true);
        parent.find(".js-task-span").wrap("<strike>");
      }
      setUpdated($(this));//Updating values from DB
    });
  };
  doneButtonBinds();

  //SORT AND FILTER METHODS

  //Sort tasks by date
  function sortTasksByDate(asc) {
    var tasks = $('.task');
    tasks = _.sortBy(tasks, function(element){ 
      var value = $(element).find('input[name=date]').val();
      value = value.replace(' a.m.').replace(' p.m.');
      return new Date(value).getTime(); 
    });
    $('#boardTitle').siblings('article').remove();
    (asc) ? $('#boardTitle').after(tasks.reverse()) : $('#boardTitle').after(tasks);
    
    bindEditButton();
    bindDeleteButton();
    updateButtonBinds();
    doneButtonBinds();
  };

  var expiredTask = function(tasksDate, nowDate) {
    return (tasksDate < nowDate) ? true : false;
  };

  var pendingTask = function(tasksDate, nowDate) {
    return (tasksDate > nowDate) ? true : false;
  };

  //Filter tasks by date state: Expired or Pending
  function filterTaskByDateState(checkState) {
    var tasks = $('.task');
    var nowDate = new Date().getTime();
    _.each(tasks, function(value, key, list) {
       var tasksDate = $(value).find('input[name=date]').val();
       tasksDate = new Date(tasksDate).getTime();
        if (checkState(tasksDate, nowDate)) {
          $(value).show();
        } else {
          $(value).hide();
        }
    }); 
  };

  //Filter task by state DONE
  function filterTaskByState(){
    var tasks = $('.task');
    _.each(tasks, function(value, key, list) {
      var taskState = $(value).find('input[name=done]').val();
      (taskState.toLowerCase() == 'true') ? $(value).show() : $(value).hide();
    });
  };

  //Search a task using title and description
  $('#searchButton').click(function(event){
    event.preventDefault();
    var searchVal = $('input[name=search]').val().toLowerCase();
    var tasks = $('.task');
    _.each(tasks, function(value, key, list) {
      var title = $(value).find('input[name=title]').val().toLowerCase();
      var description = $(value).find('input[name=description]').val().toLowerCase();
      if ( (title.indexOf(searchVal) != -1) || (description.indexOf(searchVal) != -1) ) {
        $(value).show();
      } else {
        $(value).hide();
      }
    });
  });

  //SHOW ALL TASK
  function showAllTasks(){
    var tasks = $('.task');
    $(tasks).show();
  }


  //DATE SEARCH FORM METHODS
  $("#date-search").click(function(event){
    event.preventDefault();
    var date = $('input[name=date_search]').val();
    var dateParsed = new Date(date).getTime();
    var tasks = $('.task');
    _.each(tasks, function(value, key, list) {
       var tasksDate = $(value).find('input[name=date]').val();
       tasksDate = new Date(tasksDate).getTime();
       (tasksDate == dateParsed) ? $(value).show() : $(value).hide();
    });
  });
  
  //NAVBAR SEARCHES AND FILTERS METHODS CALLS
  $("#expired_filter").click(function(){filterTaskByDateState(expiredTask)});
  $("#pending_filter").click(function(){filterTaskByDateState(pendingTask)});
  $("#date_filter_desc").click(function(){sortTasksByDate(true)});
  $("#date_filter_asc").click(function(){sortTasksByDate(false)});
  $("#done_filter").click(function(){filterTaskByState()});
  $("#show_all").click(function(){showAllTasks()});
  
  //Calendar plugin usage
  $(".input-group.date").datepicker({ autoclose: true, todayHighlight: true });

});

