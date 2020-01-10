let roomID = JSON.parse(document.getElementById('room-id').textContent);
let timeout = null;

// Initialize messaging
let chatSocket = new WebSocket(
    'ws://' + window.location.host +
    '/ws/ludo/' + roomID + '/');

chatSocket.onmessage = function(e) {
    let data = JSON.parse(e.data);
    let msgtype = data['type'];

    if (msgtype == 'user_connect') {
        addUser(data['id'], data['name']);
    } else if (msgtype == 'user_disconnect') {
        removeUser(data['id'], data['name']);
    } else if (msgtype == 'game_start') {
        let player = data['player']['name'];
        if (data['draw']) {
            logMessage('GAME', 'Make a move!');
            clearTimeout(timeout);
            timeout = setTimeout(sendTimeout, data['timeout'] * 1000);
        } else {
            logMessage('GAME', '\'' + player + '\' making a move!');
            clearTimeout(timeout);
        }
    } else if (msgtype == 'game_end') {
        let winner = data['winner']['name'];
        logMessage('GAME', '\'' + winner + '\' won!');
        playWinEffects();
        clearTimeout(timeout);
    } else if (msgtype == 'game_timeout') {
        let player = data['player']['name'];
        logMessage('GAME', '\'' + player + '\' timed out!');
    }
};

chatSocket.onclose = function(e) {
    logMessage('ROOM', 'Connection lost!');
};

// Chat
function logMessage(sender, message) {
    let chatLog = document.getElementById('log');
    chatLog.value += ('[' + sender + '] ' + message + '\n');
    chatLog.scrollTop = chatLog.scrollHeight;
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

        logMessage('ROOM', '\'' + name + '\' joined!');
    }
}

function removeUser(id, name) {
    let userNode = document.getElementById('user-' + id);
    userNode.parentNode.removeChild(userNode); // Browser compatibility
    logMessage('ROOM', '\'' + name + '\' left!');
}

// Game
function sendTimeout() {
    chatSocket.send(JSON.stringify({
        'type': 'game_timeout'
    }));
}
