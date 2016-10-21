function populateList() {
    console.log('populating list!');
    $.get("/grumblr/get-changes-profile")
      .done(function(data) {
            console.log('get-changes returned');
          var list = $("#post-list");
          list.data('max-time', data['max-time']);
          console.log(list.data('max-time'));
          list.html('')

          getUpdates();
          for (var i = 0; i < data.posts.length; i++) {
              post = data.posts[i];
              var new_post = $(post.html);
              new_post.data("post-id", post.id);
              list.prepend(new_post);
//              console.log(new_post.data("post-id"));
          }
      });
}

function addComment(post_id){
    console.log('adding comment!')
//    var post_id = $(e.target).parents("well").data("post-id");
    var commentField = $("#comment-field"+post_id);
    console.log("adding comment: " + commentField.val() + " to post: " + post_id);
    $.post("/grumblr/add-comment/" + post_id, {comment: commentField.val()})
      .done(function(data) {
            console.log('comment added');
            console.log('getting updates');
          getUpdates();
      });
}

function getUpdates() {
    var list = $("#post-list")
    var max_time = list.data("max-time")
    console.log('getting changes');
    $.get("/grumblr/get-changes-profile/" + max_time)
      .done(function(data) {
            console.log('changes got');
          list.data('max-time', data['max-time']);
          // update the posts
          for (var i = 0; i < data.posts.length; i++) {
              var post = data.posts[i];
              var new_post = $(post.html);
              new_post.data("post-id", post.id);
              list.prepend(new_post);
          }

            console.log('posts updated, updating comments');
          // update the comments
          var all_posts = list.children("div.post-item");
          console.log(all_posts.length);
          console.log(data.posts.length);
          for (var j = 0; j < all_posts.length; j++) {
              post = all_posts[j];
              console.log('updating comments for post ' + post.id);
              updateComments(post.id);
          }
      });
}

function updateComments(id) {
    var list = $("#comment-list" + id);
    var max_time = list.data("max-time")
    console.log('updating comment list ' + id);
    $.get("/grumblr/get-comments-changes-profile/" + max_time + "/" + id)
      .done(function(data) {

              console.log('get comments done.');
          list.data('max-time', data['max-time']);
          for (var i = 0; i < data.comments.length; i++) {
              var comment = data.comments[i];
              var new_comment = $(comment.html);
              var max_time = list.data("max-time");
              list.append(new_comment);
          }
      });
}

$(document).ready(function () {
  // Add event-handlers
  console.log("ready!!");

  // Set up to-do list with initial DB items and DOM data
  populateList();
  console.log('list populated')

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
