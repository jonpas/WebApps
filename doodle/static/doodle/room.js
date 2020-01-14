const roomID = JSON.parse(document.getElementById('room-id').textContent);
let timeout = null;

// Initialize messaging
const chatSocket = new WebSocket(
    'ws://' + window.location.host +
    '/ws/doodle/' + roomID + '/');

chatSocket.onmessage = function(e) {
    const chatLog = document.getElementById('chat-log');
    const data = JSON.parse(e.data);
    const msgtype = data['type'];

    if (msgtype == 'chat') {
        const sender = data['sender']['name'];
        logMessage(sender, data['message']);
    } else if (msgtype == 'draw') {
        draw(data['from'], data['to']);
    } else if (msgtype == 'user_connect') {
        addUser(data['id'], data['name']);
    } else if (msgtype == 'user_disconnect') {
        removeUser(data['id'], data['name']);
    } else if (msgtype == 'game_ready') {
        allowStart(data['ready']);
    } else if (msgtype == 'game_start') {
        const player = data['player']['name'];
        if (data['draw']) {
            allowDraw(true);
            logMessage('GAME', 'You are drawing a \'' + data['word'] + '\'!');
            clearTimeout(timeout);
            timeout = setTimeout(sendTimeout, data['timeout'] * 1000);
        } else {
            allowDraw(false);
            logMessage('GAME', '\'' + player + '\' is drawing! Guess!');
            clearTimeout(timeout);
        }
    } else if (msgtype == 'game_next') {
        const word = data['word'];
        if (data['guessed']) {
            const winner = data['winner']['name'];
            logMessage('GAME', '\'' + winner + '\' guessed \'' + word + '\'!');
            playWinEffects();
        } else {
            logMessage('GAME', '\'' + word + '\' remains a mystery!');
        }
        clearTimeout(timeout);
    } else if (msgtype == 'game_end') {
        allowDraw(true);
        logMessage('GAME', 'Finished!');
        clearTimeout(timeout);
    } else if (msgtype == 'game_timeout') {
        const player = data['player']['name'];
        logMessage('GAME', '\'' + player + '\' timed out!');
    }
};

chatSocket.onclose = function(e) {
    logMessage('ROOM', 'Connection lost!');
};

// Chat
document.getElementById('chat-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.getElementById('chat-submit').click();
    }
};

document.getElementById('chat-submit').onclick = function(e) {
    const messageInputDom = document.getElementById('chat-input');
    let message = messageInputDom.value;

    chatSocket.send(JSON.stringify({
        'type': 'chat',
        'message': message
    }));

    messageInputDom.value = '';
};

function logMessage(sender, message) {
    const chatLog = document.getElementById('chat-log');
    chatLog.value += ('[' + sender + '] ' + message + '\n');
    chatLog.scrollTop = chatLog.scrollHeight;
}

// Members
function addUser(id, name) {
    const userExists = document.getElementById('user-' + id);
    if (userExists === null) {
        const userList = document.getElementById('user-list');

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
    const userNode = document.getElementById('user-' + id);
    userNode.parentNode.removeChild(userNode); // Browser compatibility
    logMessage('ROOM', '\'' + name + '\' left!');
}

// Drawing
function sendDraw(from, to) {
    chatSocket.send(JSON.stringify({
        'type': 'draw',
        'from': from,
        'to': to
    }));
}

// Game
if (document.getElementById('start-button') !== null) {
    document.getElementById('start-button').onclick = function(e) {
        chatSocket.send(JSON.stringify({
            'type': 'game_start'
        }));
    }
}

function sendTimeout() {
    chatSocket.send(JSON.stringify({
        'type': 'game_timeout'
    }));
}
