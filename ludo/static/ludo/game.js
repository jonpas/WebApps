const board = document.getElementById('board');
const colors = ['blue', 'red', 'green', 'yellow'];

prepareBoard();
//resetBoard();

// Board
function prepareBoard() {
    // Tokens in bases
    for (const color of colors) {
        for (let i = 1; i <= 4; i++) {
            const base = document.getElementById('b-' + color + '-' + i);
            placeToken(color, i);
        }
    }
}

function updateBoard() {
    // Base
    for (const color of colors) {
        for (let i = 1; i <= 4; i++) {
            const base = document.getElementById('b-' + color + '-' + i);
            base.firstChild.innerHTML = 'test';
        }
    }

    // Fields
    for (let i = 1; i <= 40; i++) {
        const field = document.getElementById('f-' + i);
        if (field.firstChild.id === '') {
            field.firstChild.innerHTML = 'test';
        } else {
            // Entrance
            field.firstChild.innerHTML = 'E';
        }
    }

    // Entrances
    /*for (const color of colors) {
        const entrance = document.getElementById('e-' + color);
        entrance.innerHTML = 'e';
    }*/

    // Homes
    for (const color of colors) {
        for (let i = 1; i <= 4; i++) {
            const home = document.getElementById('h-' + color + '-' + i);
            home.firstChild.innerHTML = 'H' + home.id.charAt(home.id.length - 1);
        }
    }
}

function resetBoard() {
    const overlays = document.getElementsByClassName('board-overlay');
    for (const overlay of overlays) {
        overlay.id = '';
    }
}

function placeToken(color, i) {
    const overlay = getOverlay(document.getElementById('b-' + color + '-' + i));
    overlay.id = 't-' + color + '-' + i;
    overlay.innerHTML = color.charAt(0).toUpperCase() + i;
}

function moveToken(from, to) {
    let boxFrom = document.getElementById(from);
    let boxTo = document.getElementById(to);

    if (from.startsWith('e-')) {
        boxFrom = boxFrom.parentNode;
    }
    if (to.startsWith('e-')) {
        boxTo = boxTo.parentNode;
    }

    const overlayFrom = getOverlay(boxFrom);
    const overlayTo = getOverlay(boxTo);

    overlayTo.id = overlayFrom.id;
    overlayTo.innerHTML = overlayFrom.innerHTML;
    overlayFrom.id = '';
    overlayFrom.innerHTML = '';
}

// Board Helpers
function getCell(element) {
    // Cell is always first child
    return element.children[0];
}

function getOverlay(element) {
    // Overlay is always second child
    return element.children[1];
}

// Game
function startGame() {
    prepareBoard();
}

function playRollEffects() {
    // Sound effect
    let audio = document.getElementById('audio-roll');
    audio.play();

    // TODO Animation
}

function playWinEffects() {
    // Sound effect
    let audio = document.getElementById('audio-win');
    audio.play();

    // Animation
    board.style.backgroundColor = 'green';

    // Restore animation
    setTimeout(function() {
        board.style.backgroundColor = 'transparent';
    }, 1000);
}
