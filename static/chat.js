$(document).ready(function() {

    // Send message to chatbot API
    function sendMessage(text) {
      $.ajax({
        type: 'POST',
        url: '/chatbot',
        data: {'message': text},
        success: handleMessage
      });
    }

    // Handle chatbot response
    function handleMessage(response) {
      var message = $('<div class="message chatbot-message"></div>').text(response.response);
      var timestamp = $('<span class="timestamp"></span>').text(getFormattedTime());
      var row = $('<div class="row message-row"></div>').append(message).append(timestamp);
      $('#chat-window').append(row);
      scrollToBottom();
      $('#send-btn').removeAttr('disabled');  // Re-enable send button
    }

    // Handle new user message
    $('#chat-form').submit(function(event) {
      event.preventDefault();
      var text = $('#user-message').val();
      var message = $('<div class="message user-message"></div>').text(text);
      var timestamp = $('<span class="timestamp"></span>').text(getFormattedTime());
      var row = $('<div class="row message-row"></div>').append(message).append(timestamp);
      $('#user-message').val('');  // Clear input box
      $('#chat-window').append(row);
      scrollToBottom();
      $('#send-btn').attr('disabled', 'disabled');  // Disable send button
      sendMessage(text);
    });

    // Scroll to the bottom of the chat window
    function scrollToBottom() {
      $('#chat-window').scrollTop($('#chat-window')[0].scrollHeight);
    }

    // Get formatted timestamp
    function getFormattedTime() {
      var now = new Date();
      var hours = now.getHours();
      var minutes = now.getMinutes();
      return hours + ':' + minutes;
    }

  });