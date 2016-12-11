socket = new WebSocket("ws://" + window.location.host + "/room1");
console.log("ws://" + window.location.host + "/room1");
socket.onmessage = function(e) {
    console.log("Got message");
    $("ul").append("<li>" + e.data + "</li>");
}


function sendMessage(){
    console.log("sending: " + $("#message-field").val());
    socket.send($("#message-field").val())
}

$(document).ready(function () {
  // Add event-handlers
  $("#send-button").click(sendMessage);

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
