let roomID = JSON.parse(document.getElementById('room-id').textContent);

// Initialize messaging
let chatSocket = new WebSocket(
    'ws://' + window.location.host +
    '/ws/doodle/' + roomID + '/');

chatSocket.onmessage = function(e) {
    let chatLog = document.getElementById('chat-log');
    let data = JSON.parse(e.data);
    let msgtype = data['type'];
    let message = data['message'];

    if (msgtype == 'chat') {
        logMessage(message);
    } else if (msgtype == 'draw') {
        draw(message.from, message.to);
    } else if (msgtype == 'user_connect') {
        addUser(message['id'], message['name']);
    } else if (msgtype == 'user_disconnect') {
        removeUser(message);
    }
};

chatSocket.onclose = function(e) {
    logMessage('Connection lost!');
};

// Chat
document.getElementById('chat-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.getElementById('chat-submit').click();
    }
};

document.getElementById('chat-submit').onclick = function(e) {
    let messageInputDom = document.getElementById('chat-input');
    let message = messageInputDom.value;

    chatSocket.send(JSON.stringify({
        'type': 'chat',
        'message': message
    }));

    messageInputDom.value = '';
};

function logMessage(message) {
    let chatLog = document.getElementById('chat-log');
    chatLog.value += (message + '\n');
    chatLog.scrollTop = chatLog.scrollHeight;
}

// Drawing
function sendDraw(from, to) {
    chatSocket.send(JSON.stringify({
        'type': 'draw',
        'message': {from, to}
    }));
}

// Members
function addUser(id, name) {
    let userExists = document.getElementById('user-' + id);
    if (userExists === null) {
        let userList = document.getElementById('user-list');

        let userNode = document.createElement('a');
        userNode.setAttribute('href', '/accounts/' + id);
        userNode.setAttribute('id', 'user-' + id);

        let userBadge = document.createElement('span');
        userBadge.setAttribute('class', 'badge badge-success');

        let userName = document.createTextNode(name);

        userList.appendChild(userNode);
        userNode.appendChild(userBadge);
        userBadge.appendChild(userName);
    }
}

function removeUser(id) {
    let userNode = document.getElementById('user-' + id);
    userNode.parentNode.removeChild(userNode); // Browser compatibility
}
