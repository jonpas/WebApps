let canvas = document.getElementById('canvas');
let ctx = canvas.getContext('2d');
let allowDrawing = true;
let drawing = false;
let prevMousePos = {x: 0, y: 0};

// Responsive canvas
canvas.width = 1280;
canvas.height = 1024;
canvas.style.width = '100%';
canvas.style.height = '100%';

// Drawing
canvas.addEventListener('mousemove', moveDraw);
canvas.addEventListener('mousedown', startDraw);
canvas.addEventListener('mouseup', stopDraw);
canvas.addEventListener('mouseout', stopDraw);
canvas.addEventListener('touchmove', moveDraw);
canvas.addEventListener('touchstart', startDraw);
canvas.addEventListener('touchend', stopDraw);
canvas.addEventListener('touchleave', stopDraw);

function startDraw(e) {
    if (allowDrawing) {
        drawing = true;
        let curMousePos = getMousePosition(e);
        sendDraw({x: curMousePos.x - 1, y: curMousePos.y - 1}, curMousePos);
        prevMousePos = curMousePos;
    }
}

function stopDraw(e) {
    drawing = false;
}

function moveDraw(e) {
    if (drawing && allowDrawing) {
        let curMousePos = getMousePosition(e);
        sendDraw(prevMousePos, curMousePos);
        prevMousePos = curMousePos;
    }
}

function getMousePosition(e) {
    const clientX = e.offsetX || e.touches[0].clientX;
    const clientY = e.offsetY || e.touches[0].clientY;
    var mouseX = clientX * canvas.width / canvas.clientWidth | 0;
    var mouseY = clientY * canvas.height / canvas.clientHeight | 0;
    return {x: mouseX, y: mouseY};
}

function draw(from, to) {
    ctx.beginPath();
    ctx.moveTo(from.x, from.y);
    ctx.lineTo(to.x, to.y);
    ctx.strokeStyle = "black";
    ctx.lineWidth = 2;
    ctx.stroke();
    ctx.closePath();
}

function erase() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

// Game
function allowStart(allow) {
    let startButton = document.getElementById('start-button');
    if (allow) {
        startButton.classList.remove('disabled');
    } else {
        startButton.classList.add('disabled');
    }
}

function allowDraw(allow) {
    erase();
    allowDrawing = allow;
}

function playWinEffects() {
    // Sound effect
    let audio = document.getElementById('audio-win');
    audio.play();

    // Animation
    canvas.style.backgroundColor = 'green';

    // Restore animation
    setTimeout(function() {
        canvas.style.backgroundColor = 'white';
    }, 1000);
}
