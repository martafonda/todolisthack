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
    $.ajax({
      url: '/task',
      data: {title: title, description: description, author: author},
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
      $.ajax({
        url: '/task',
        data: {id: id, title: title, description: description, author: author, done: done},
        type: 'post',
        success: function() {
            parent.find('.js-author').text('by ' + author);
            parent.find('.js-title').text('title: ' + title);
            parent.find('.js-description').text('task: ' + description);
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
  }
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
  }
  doneButtonBinds();

  function sortTasks() {
    var tasks = $('.task');
    tasks = _.sortBy(tasks, function(element){ 
      var value = $(element).find('input[name=date]').val();
      value = value.replace(' a.m.').replace(' p.m.');
      return new Date(value).getTime(); 
    });
    $('#boardTitle').siblings('article').remove();
    $('#boardTitle').after(tasks.reverse());
    bindEditButton();
    bindDeleteButton();
    updateButtonBinds();
    doneButtonBinds();
  }
});

