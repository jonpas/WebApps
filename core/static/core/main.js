// Change text color to black if background is considered light
$('.visible-color').addClass(function(i) {
    // Get RGB background color as list of RGB integers
    var bgColor = $(this).closest('span').css('background-color');
    bgColor = bgColor.substring(bgColor.indexOf('(') + 1, bgColor.length - 1);
    bgColor = bgColor.split(', ').map(Number);

    // Calculate luminosity per ITU-R BT.709 (0 darkest, 255 lightest)
    var luma = 0.2126 * bgColor[0] + 0.7152 * bgColor[1] + 0.0722 * bgColor[2];

    // Luminosity greater than 128 is considered light, so set text color to dark
    var color = 'white';
    if (luma > 128) {
        color = 'dark';
    }

    return 'text-' + color;
});
