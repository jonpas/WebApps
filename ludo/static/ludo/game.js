const board = document.getElementById('board');
const colors = ['blue', 'red', 'green', 'yellow'];

// Board
function updateBoard(state) {
    // Bases
    for (const color of colors) {
        for (let i = 0; i < 4; i++) {
            if (state['bases'][color][i] !== null) {
                const token = getToken(state['bases'][color][i]);
                placeToken(token.color, token.i, getLocation('b', token.color, i + 1));
            } else {
                clearLocation(getLocation('b', color, i + 1));
            }
        }
    }

    // Homes
    for (const color of colors) {
        for (let i = 0; i < 4; i++) {
            if (state['homes'][color][i] !== null) {
                const token = getToken(state['homes'][color][i]);
                placeToken(token.color, token.i, getLocation('h', token.color, i + 1));
            } else {
                clearLocation(getLocation('h', color, i + 1));
            }
        }
    }

    // Fields
    for (let i = 0; i < 40; i++) {
        if (state['fields'][i] !== null) {
            const token = getToken(state['fields'][i]);
            placeToken(token.color, token.i, getLocation('f', '', i + 1));
        } else {
            clearLocation(getLocation('f', '', i + 1));
        }
    }
}

function placeToken(color, i, location) {
    const overlay = getOverlay(location);
    overlay.id = 't-' + color + '-' + i;
    overlay.innerHTML = color.charAt(0).toUpperCase() + i;
}

function clearLocation(location) {
    const overlay = getOverlay(location);
    overlay.id = '';
    overlay.innerHTML = '';
}

function getOverlay(element) {
    // Overlay is always second child
    return element.children[1];
}

function getLocation(type, color, index) {
    if (type === 'f') {
        return document.getElementById(type + '-' + index);
    } else {
        return document.getElementById(type + '-' + color + '-' + index);
    }
}

function getToken(name) {
    const tokenVars = name.split('-');
    return {
        color: tokenVars[0],
        i: tokenVars[1]
    }
}

// Game
function allowStart(allow) {
    const startButton = document.getElementById('start-button');
    if (allow) {
        startButton.classList.remove('disabled');
    } else {
        startButton.classList.add('disabled');
    }
}

function toggleActions(allowedActions) {
    const actions = ['roll', 'move-1', 'move-2', 'move-3', 'move-4'];
    for (const action of actions) {
        const button = document.getElementById(action + '-button');
        if (allowedActions.includes(action)) {
            button.classList.remove('disabled');
        } else {
            button.classList.add('disabled');
        }
    }
}

function playRollEffects() {
    // Sound effect
    const audio = document.getElementById('audio-roll');
    audio.play();

    // Animation
    const rollIcon = document.getElementById('roll-icon');
    rollIcon.classList.add('spin');

    // Restore animation
    setTimeout(function() {
        rollIcon.classList.remove('spin');
    }, 1000);
}

function playKnockEffects() {
    // Sound effect
    const audio = document.getElementById('audio-knock');
    audio.play();

    // Animation
    board.classList.add('shake');

    // Restore animation
    setTimeout(function() {
        board.classList.remove('shake');
    }, 250);
}

function playWinEffects() {
    // Sound effect
    const audio = document.getElementById('audio-win');
    audio.play();

    // Animation
    board.style.backgroundColor = 'green';

    // Restore animation
    setTimeout(function() {
        board.style.backgroundColor = 'transparent';
    }, 1000);
}
