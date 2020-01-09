let canvas = document.getElementById('canvas');
let ctx = canvas.getContext('2d');
let flag = false;
let prevX = 0;
let prevY = 0;
let curX = 0;
let curY = 0;

canvas.addEventListener('mousemove', function(e) {
    findxy('move', e)
}, false);

canvas.addEventListener('mousedown', function(e) {
    findxy('down', e)
}, false);

canvas.addEventListener('mouseup', function(e) {
    findxy('up', e)
}, false);

canvas.addEventListener('mouseout', function(e) {
    findxy('out', e)
}, false);

function findxy(res, e) {
    if (res == 'down') {
        prevX = curX;
        prevY = curY;
        curX = e.clientX - canvas.getBoundingClientRect().left;
        curY = e.clientY - canvas.getBoundingClientRect().top;

        flag = true;
        ctx.beginPath();
        ctx.fillStyle = "black";
        ctx.fillRect(curX, curY, 2, 2);
        ctx.closePath();
    } else if (res == 'up' || res == 'down') {
        flag = false;
    } else if (res == 'move') {
        if (flag) {
            prevX = curX;
            prevY = curY;
            curX = e.clientX - canvas.getBoundingClientRect().left;
            curY = e.clientY - canvas.getBoundingClientRect().top;
            sendDraw({x: prevX, y: prevY}, {x: curX, y: curY});
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
