$(document).ready(function(){

  function bindEditButton() {
    $('.edit-btn').unbind('click');
    $('.edit-btn').bind('click', function(){
      $(this).parents('.task:first').find('.js-edit-tsk').toggle();
    });
  };

  bindEditButton();

  function bindDeleteButton() {
    $('.delete-btn').unbind('click');
    $('.delete-btn').bind('click', function(){
      var parent = $(this).parents('.task:first');
      var id = parent.attr('id').split('_')[1];
      $(this).parents('.task:first').remove();
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

  function setUpdated(element){
      var parent = element.parents('.task:first');
      var id = parent.attr('id').split('_')[1];
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

  function updateButtonBinds() {
    $('.update-btn').on('click',function(){
      setUpdated($(this));
      $(this).parents('.task:first').find('.js-edit-tsk').toggle();
    });
  };
  updateButtonBinds();

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
      setUpdated($(this));
    });
  };
  doneButtonBinds();


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

  function filterTaskByState(){
    var tasks = $('.task');
    _.each(tasks, function(value, key, list) {
      var taskState = $(value).find('input[name=done]').val();
      (taskState.toLowerCase() == 'true') ? $(value).show() : $(value).hide();
    });
  };

  function showAllTasks(){
    var tasks = $('.task');
    $(tasks).show();
  }

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
  
  $("#expired_filter").click(function(){filterTaskByDateState(expiredTask)});
  $("#pending_filter").click(function(){filterTaskByDateState(pendingTask)});
  $("#date_filter_desc").click(function(){sortTasksByDate(true)});
  $("#date_filter_asc").click(function(){sortTasksByDate(false)});
  $("#done_filter").click(function(){filterTaskByState()});
  $("#show_all").click(function(){showAllTasks()});
  $(".input-group.date").datepicker({ autoclose: true, todayHighlight: true });


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

});

