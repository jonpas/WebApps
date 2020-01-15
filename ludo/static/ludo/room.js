const roomID = JSON.parse(document.getElementById('room-id').textContent);
let timeout = null;

// Initialize messaging
const chatSocket = new WebSocket(
    'ws://' + window.location.host +
    '/ws/ludo/' + roomID + '/');

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const msgtype = data['type'];
    console.log(data);

    if (msgtype == 'user_connect') {
        addUser(data['id'], data['name']);
    } else if (msgtype == 'user_disconnect') {
        removeUser(data['id'], data['name']);
    } else if (msgtype == 'game_ready') {
        allowStart(data['ready']);
    } else if (msgtype == 'game_start') {
        const allowedActions = data['actions'];
        toggleActions(allowedActions);

        const state = data['state'];
        updateBoard(state);

        logMessage('GAME', 'Roll the die!');
        clearTimeout(timeout);
        timeout = setTimeout(sendTimeout, data['timeout'] * 1000);
    } else if (msgtype == 'game_roll') {
        const roll = data['roll'];
        const player = data['player']['name'];
        logMessage('GAME', '\'' + player + '\' rolled ' + data['roll'] + '!');

        if (data['rolled']) {
            toggleActions([]);
            playRollEffects();
        }
    } else if (msgtype == 'game_turn') {
        const allowedActions = data['actions'];
        toggleActions(allowedActions);

        const state = data['state'];
        updateBoard(state);

        clearTimeout(timeout);
        const player = data['player']['name'];
        if (allowedActions.includes('roll')) {
            if (allowedActions.length == 0) {
                logMessage('GAME', '\'' + player + '\' rolling the die!');
            } else {
                logMessage('GAME', 'Roll the die!');
                timeout = setTimeout(sendTimeout, data['timeout'] * 1000);
            }
        } else {
            if (allowedActions.length == 0) {
                logMessage('GAME', '\'' + player + '\' making a move!');
            } else {
                logMessage('GAME', 'Make a move!');
                timeout = setTimeout(sendTimeout, data['timeout'] * 1000);
            }
        }

        if (data['knock']) {
            playKnockEffects();
        }

    } else if (msgtype == 'game_player_finish') {
        const finisher = data['finisher']['name'];
        const position = data['position'];
        const positions = ['1st', '2nd', '3rd', '4th'];
        logMessage('GAME', '\'' + finisher + '\' finished ' + positions[position - 1] + '!');
        playWinEffects();
    } else if (msgtype == 'game_end') {
        const state = data['state'];
        updateBoard(state);

        logMessage('GAME', 'Finished!');
        toggleActions([]);
        clearTimeout(timeout);
    } else if (msgtype == 'game_timeout') {
        const player = data['player']['name'];
        logMessage('GAME', '\'' + player + '\' timed out!');
    }
};

chatSocket.onclose = function(e) {
    logMessage('ROOM', 'Connection lost!');
    toggleActions([]);
};

// Chat
function logMessage(sender, message) {
    const chatLog = document.getElementById('log');
    chatLog.value += ('[' + sender + '] ' + message + '\n');
    chatLog.scrollTop = chatLog.scrollHeight;
}

// Members
function addUser(id, name) {
    const userExists = document.getElementById('user-' + id);
    if (userExists === null) {
        const userList = document.getElementById('user-list');

        const userNode = document.createElement('a');
        userNode.setAttribute('href', '/accounts/' + id);
        userNode.setAttribute('id', 'user-' + id);

        const userBadge = document.createElement('span');
        userBadge.setAttribute('class', 'badge badge-success');

        const userName = document.createTextNode(name);

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

// Game
if (document.getElementById('start-button') !== null) {
    document.getElementById('start-button').onclick = function(e) {
        toggleActions([]);
        chatSocket.send(JSON.stringify({
            'type': 'game_start'
        }));
    }
}

if (document.getElementById('roll-button') !== null) {
    document.getElementById('roll-button').onclick = function(e) {
        toggleActions([]);
        chatSocket.send(JSON.stringify({
            'type': 'game_roll'
        }));
    }
}

for (let i = 1; i <= 4; i++) {
    if (document.getElementById('move-' + i + '-button') !== null) {
        document.getElementById('move-' + i + '-button').onclick = function(e) {
            toggleActions([]);
            chatSocket.send(JSON.stringify({
                'type': 'game_turn',
                'token': i
            }));
        }
    }
}

function sendTimeout() {
    toggleActions([]);
    chatSocket.send(JSON.stringify({
        'type': 'game_timeout'
    }));
}
