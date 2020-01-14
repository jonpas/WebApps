// Handle Todo checkbox change
$('[id*="task-"]').change(function() {
    const task = $(this).closest('li');
    const reminder = $('#remind-' + this.id);
    const id = this.id.substring(this.id.indexOf('-') + 1, this.id.length);

    // Update database
    const xhttp = new XMLHttpRequest();
    xhttp.open('POST', 'tasks/' + id + '/complete/', true);
    xhttp.setRequestHeader('X-CSRFToken', Cookies.get('csrftoken'));
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send('completed=' + this.checked);

    // Update style
    if (this.checked) {
        task.removeClass('border-0 border-danger');
        task.addClass('border-1 border-success font-italic');

        reminder.addClass('d-none');
    } else {
        task.removeClass('border-1 border-success border-danger font-italic');

        if (reminder.length === 0) { // No reminder element found
            task.addClass('border-0');
        } else {
            task.addClass('border-1 border-danger');
            reminder.removeClass('d-none');
        }
    }
});
