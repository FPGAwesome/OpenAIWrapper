function setModel() {
  var dropdown = document.getElementById("models");
  var selectedModel = dropdown.options[dropdown.selectedIndex].value;

  // AJAX call to server to set the model
  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/select_model', true);
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.onload = function() {
    if (xhr.status === 200) {
      console.log('Selected model: ' + selectedModel);
    }
  };
  xhr.send(JSON.stringify({model: selectedModel}));
}

$(document).ready(function() {

    // Toggle side panel
    $('#toggle-panel-btn').click(function(){
        $('#side-panel').toggleClass('open');
    });

    // Send system prompt to chatbot API
    $('#submit-system-prompt-btn').click(function(e){
        e.preventDefault();
        var systemPrompt = $('#system-prompt').val();
        // send systemPrompt to the backend
        console.log(systemPrompt);
    });

    // Send message to chatbot API
    function sendMessage(text) {
      $.ajax({
        type: 'POST',
        url: '/chatbot',
        data: {'message': text},
        success: handleMessage
      });
    }

    $('#load-chat-form').submit(function(e) {
        e.preventDefault();
      
        var fileInput = $('input[type="file"][name="file"]')[0];
      
        if (!fileInput.files || fileInput.files.length === 0) {
          alert('Please select a file');
          return;
        }
      
        var formData = new FormData();
        formData.append('file', fileInput.files[0]);
      
        $.ajax({
          type: 'POST',
          url: '/load_messages',
          data: formData,
          contentType: false,
          processData: false,
          success: function(response) {
            $('#chat-window').empty(); // Clear existing messages
            var messages = response.messages;
            if (messages.length > 0) {
              for (var i = 0; i < messages.length; i++) {
                console.log(messages[i].role)
                var message = $('<div class="message '+ (messages[i].role == 'user' ? 'user-message' : 'chatbot-message') + '"></div>').text(messages[i].content);
                //var timestamp = $('<span class="timestamp"></span>').text(messages[i].time);
                var row = $('<div class="row message-row"></div>').append(message)//.append(timestamp);
                $('#chat-window').append(row);
              }
              scrollToBottom();
            }
          },
          error: function(error) {
            alert('An error occurred while uploading the file, please try again');
          },
        });
      });

    // Handle chatbot response
    function handleMessage(response) {
    var messages = response.messages;
    if (messages && messages.length > 0) {
        $('#chat-window').empty();  // Clear existing messages
        for(var i=0; i < messages.length; i++) {
            var message = $('<div class="message '+ messages[i].type+'"></div>').text(messages[i].text);
            var timestamp = $('<span class="timestamp"></span>').text(messages[i].time);
            var row = $('<div class="row message-row"></div>').append(message).append(timestamp);
            $('#chat-window').append(row);
        }
    } else {
        var message = $('<div class="message chatbot-message"></div>').text(response.response);
        var timestamp = $('<span class="timestamp"></span>').text(getFormattedTime());
        var row = $('<div class="row message-row"></div>').append(message).append(timestamp);
        $('#chat-window').append(row);
    }
    scrollToBottom();
    $('#send-btn').removeAttr('disabled');  // Re-enable send button
    }

    // Handle new user message on enter key press without shiftKey
    $('#user-message').keydown(function(event){
        if (event.keyCode == 13 && !event.shiftKey){
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
        }
    });

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

    // Clear chat history from screen
    $('#clearForm').submit(function(event) {
          event.preventDefault();
          $.ajax({
              type: 'POST',
              url: '/clear_message',
              success: function(response){
                if ($('#chat-window').is(':empty')) {
                    alert('Chat is already cleared.');
                } else {
                    $('#chat-window').empty(); // Clear existing messages
                    alert('Chat history cleared.');
                }
            },
            error: function(error){
                alert('Error occurred while clearing chat history.');
            },
      });
    });

  });