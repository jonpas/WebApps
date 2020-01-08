var roomID = JSON.parse(document.getElementById('room-id').textContent);
console.log(roomID)

// Initialize chat
var chatSocket = new WebSocket(
    'ws://' + window.location.host +
    '/ws/doodle/' + roomID + '/');

chatSocket.onmessage = function(e) {
    var chatLog = document.getElementById('chat-log')
    var data = JSON.parse(e.data);
    var message = data['message'];

    chatLog.value += (message + '\n');
    chatLog.scrollTop = chatLog.scrollHeight;
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

// Enter message
document.getElementById('chat-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.getElementById('chat-submit').click();
    }
};

document.getElementById('chat-submit').onclick = function(e) {
    var messageInputDom = document.getElementById('chat-input');
    var message = messageInputDom.value;

    chatSocket.send(JSON.stringify({
        'message': message
    }));

    messageInputDom.value = '';
};

// Add user to list
//document.getElementById('user-list')
