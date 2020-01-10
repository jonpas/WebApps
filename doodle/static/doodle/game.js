let canvas = document.getElementById('canvas');
let ctx = canvas.getContext('2d');
let allowDrawing = true;
let drawing = false;
let prevX = 0;
let prevY = 0;
let time = 0;

// Drawing
canvas.addEventListener('mousemove', function(e) {
    drawControl('move', e)
}, false);

canvas.addEventListener('mousedown', function(e) {
    drawControl('down', e)
}, false);

canvas.addEventListener('mouseup', function(e) {
    drawControl('up', e)
}, false);

canvas.addEventListener('mouseout', function(e) {
    drawControl('out', e)
}, false);

function drawControl(res, e) {
    if (res == 'down') {
        drawing = true;

        let curX = e.clientX - canvas.getBoundingClientRect().left;
        let curY = e.clientY - canvas.getBoundingClientRect().top;
        if (allowDrawing) {
            sendDraw({x: curX - 1, y: curY - 1}, {x: curX, y: curY});
        }
        prevX = curX;
        prevY = curY;
    } else if (res == 'up' || res == 'down') {
        drawing = false;
    } else if (res == 'move') {
        if (drawing) {
            let curX = e.clientX - canvas.getBoundingClientRect().left;
            let curY = e.clientY - canvas.getBoundingClientRect().top;
            if (allowDrawing) {
                sendDraw({x: prevX, y: prevY}, {x: curX, y: curY});
            }
            prevX = curX;
            prevY = curY;
        }
    }
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
