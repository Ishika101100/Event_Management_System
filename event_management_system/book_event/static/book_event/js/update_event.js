
$(document).on('change', '#end_time', function () {
    var from = $('#start_time').val();
    var to = $(this).val();

    if (moment(from, 'hh:mm') >= moment(to, 'hh:mm')) {
        var select_html = "<div class=\"alert alert-danger\" role=\"alert\"> End time must be greater than start time.</div>"
        $('.end_time_alert').html(select_html)
        $('.submit_button').hide()
        $('.end_time_alert').show()
    } else {
        $('.end_time_alert').hide()
        $('.submit_button').show()
    }
})

$(document).on('change', '#start_time', function () {
    var from = $(this).val();
    var to = $('#end_time').val();

    if (moment(from, 'hh:mm') >= moment(to, 'hh:mm')) {
        var select_html = "<div class=\"alert alert-danger\" role=\"alert\"> End time must be greater than start time.</div>"
        $('.end_time_alert').html(select_html)
        $('.submit_button').hide()
        $('.end_time_alert').show()
    } else {
        $('.end_time_alert').hide()
        $('.submit_button').show()
    }
})

const timeInput = document.getElementById('start_time');

timeInput.addEventListener('input', (e) => {

    let hour = e.target.value.split(':')[0]

    e.target.value = `${hour}:00`
    parseFloat($(this).val()).toFixed(2)
})

const end_time_input = document.getElementById('end_time');

end_time_input.addEventListener('input', (element) => {
    let hour = element.target.value.split(':')[0]
    element.target.value = `${hour}:00`
    parseFloat($(this).val()).toFixed(2)
})
