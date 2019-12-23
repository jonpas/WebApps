// Handle Todo checkbox change
$('[id*="task-"]').change(function() {
    var task = $(this).closest('li');
    var reminder = $('#remind-' + this.id);

    // TODO Update database

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
