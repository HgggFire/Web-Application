function populateList() {
    $.get("/grumblr/get-changes")
      .done(function(data) {
          var list = $("#post-list");
          list.data('max-time', data['max-time']);
          console.log(list.data('max-time'));
          list.html('')
          for (var i = 0; i < data.posts.length; i++) {
              post = data.posts[i];
              var new_post = $(post.html);
              new_post.data("post-id", post.id);
              list.prepend(new_post);
          }
      });
}

function addPost(){
    var postField = $("#post-field");
    $.post("/grumblr/post", {post: postField.val()})
      .done(function(data) {
          getUpdates();
          postField.val("").focus();
      });
}


function getUpdates() {
    console.log('get changes!');
    var list = $("#post-list")
    var max_time = list.data("max-time")
    $.get("/grumblr/get-changes/"+ max_time)
      .done(function(data) {
          list.data('max-time', data['max-time']);
          for (var i = 0; i < data.posts.length; i++) {
              var post = data.posts[i];
              var new_post = $(post.html);
              new_post.data("post-id", post.id);
              list.prepend(new_post);
          }
      });
}

$(document).ready(function () {
  // Add event-handlers
  console.log("ready!!");
  $("#post-button").click(addPost);

  // Set up to-do list with initial DB items and DOM data
  populateList();
  $("#post-field").focus();

  // Periodically refresh to-do list every 5 seconds
  window.setInterval(getUpdates, 5000);

  // CSRF set-up copied from Django docs
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }
  var csrftoken = getCookie('csrftoken');
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  });
});
