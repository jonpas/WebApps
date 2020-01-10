// Game
function playWinEffects() {
    // Sound effect
    let audio = document.getElementById('audio-win');
    audio.play();

    // TODO Animation
    //canvas.style.backgroundColor = 'green';

    // TODO Restore animation
    setTimeout(function() {
        //canvas.style.backgroundColor = 'white';
    }, 1000);
}
