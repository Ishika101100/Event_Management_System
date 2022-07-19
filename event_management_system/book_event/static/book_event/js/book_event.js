$(document).on('change', '#event', function () {
    var event_type = $('#event').val()
    var csrf_token = $('input[name="csrf_token"]').val()
    data = {'event_type': event_type}
    if (event_type != "") {
        $.ajax({
            type: 'POST',
            url: '/findEventVenue/',
            dataType: 'json',
            data: JSON.stringify(data),
            contentType: "application/json; charset=UTF-8",
            success: function (response) {
                var venues = response.venue_name

                var select_html = ""
                $("#venue").empty()
                select_html += "<option value=''>-- Select --</option>"
                $(venues).each(function (i) {
                    select_html += "<option value=" + venues[i]['id'] + ">" + venues[i]['name'] + "</option>"
                });
                $("#venue").append(select_html)
                if (event_type === '2') {
                    $('.decorator_div').hide()
                    $('.decorator_details').hide()
                } else {
                    $('.decorator_div').show()
                    $('.decorator_details').show()
                }
            }
        })
    }
})
$(document).on('change', '#venue', function () {
    var venue_id = $(this).val()
    data = {'venue_id': venue_id}
    if (venue_id != "") {
        $.ajax({
            type: 'POST',
            url: '/findVenueDetails/',
            dataType: 'json',
            data: JSON.stringify(data),
            contentType: "application/json; charset=UTF-8",
            success: function (response) {
                var details = response.venue_data
                var decorator_details = response.decorator_list
                var caterer_details = response.caterer_list
                var capacity = details.capacity
                var select_html = ""
                select_html += '<p>Charges : <input type="hidden" value=' + details.charges + ' name="venue_charge" id="venue_charge1">' + details.charges + '</p><p>Capacity : <b>' + details.capacity + '</b></p>'
                $('.venue_details').html(select_html)

                var decorator_html = "<option>-----------</option>"
                $(decorator_details).each(function (i) {
                    decorator_html += "<option value=" + decorator_details[i]['id'] + ">" + decorator_details[i]['name'] + "</option>"
                });
                $('#decorator').html(decorator_html)

                var caterer_html = "<option>-----------</option>"
                $(caterer_details).each(function (i) {
                    caterer_html += "<option value=" + caterer_details[i]['id'] + ">" + caterer_details[i]['name'] + "</option>"
                });
                $('#caterer').html(caterer_html)
                guest = document.getElementById('no_of_guests')
                guest.setAttribute("max", parseInt(capacity));
                calculateTotal();
            }
        })
    }
})

$(document).on('change', '#caterer', function () {
    var caterer_id = $(this).val()
    data = {'caterer_id': caterer_id}
    // console.log(data)
    if (caterer_id != "") {
        $.ajax({
            type: 'POST',
            url: '/findCatererDetails/',
            dataType: 'json',
            data: JSON.stringify(data),
            contentType: "application/json; charset=UTF-8",
            success: function (response) {
                var details = response.caterer_details
                // console.log(details)
                var select_html = "<table style='border: 1px solid black; padding:15px; margin:15px;'><thead><th style='border: 1px solid black;'>Food Type</th><th style='border: 1px solid black;'>Charges</th><th style='border: 1px solid black;'>Select Type</th></thead><tbody>"
                $(details).each(function (i) {
                    select_html += '<tr><td style=\'border: 1px solid black;\'><b>' + details[i]['food_category'] + '&nbsp;&nbsp;</b></td><td style=\'border: 1px solid black;\'><b>&nbsp;&nbsp;' + details[i]['charges'] + '</b></td><td style=\'border: 1px solid black;\'><input class="check_charge" data-price=' + details[i]["charges"] + ' data-id=' + details[i]["food_type_id"] + ' type="checkbox" ></td></tr>'
                });
                select_html += "</tbody></table>"
                $('.caterer_details').html(select_html)
            }
        })
    }
})

$(document).on('change', '#decorator', function () {
    var decorator_id = $(this).val()
    const data = {'decorator_id': decorator_id}
    // console.log(data)
    if (decorator_id != "") {
        $.ajax({
            type: 'POST',
            url: '/findDecoratorDetails/',
            dataType: 'json',
            data: JSON.stringify(data),
            contentType: "application/json; charset=UTF-8",
            success: function (response) {
                var details = response.decorator_details
                var select_html = "<table style='border: 1px solid black; padding:15px; margin:15px;'><thead><th style='border: 1px solid black;'>Decoration Type</th><th style='border: 1px solid black;'>Charges</th><th style='border: 1px solid black;'>Select Type</th></thead><tbody>"

                $(details).each(function (i) {
                    select_html += '<tr><td style=\'border: 1px solid black;\'><b>' + details[i]['decoration_type'] + '&nbsp;&nbsp;</b></td><td style=\'border: 1px solid black;\'><b>&nbsp;&nbsp;' + details[i]['charges'] + '</b></td><td style=\'border: 1px solid black;\'><input class="check_charge_decorator" data-price=' + details[i]["charges"] + ' data-id=' + details[i]["decoration_type_id"] + ' type="checkbox" ></td></tr>'
                });
                select_html += "</tbody></table>"
                $('.decorator_details').html(select_html)
            }
        })
    }
})

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


$(document).on('change', '.check_charge , .check_charge_decorator, #no_of_guests , #venue', function () {
    calculateTotal();
})

function calculateTotal() {
    var cartTotal = 0;
    $('.check_charge').each(function () {
        if ($(this).is(':checked')) {
            cartTotal += parseInt($(this).attr('data-price'));
        }
    });
    var no_of_guest = $('#no_of_guests').val()

    var total = parseInt(cartTotal) * parseInt(no_of_guest)

    var decoration_charge = 0
    $('.check_charge_decorator').each(function () {
        if ($(this).is(':checked')) {
            decoration_charge += parseInt($(this).attr('data-price'));
        }
    });

    var total1 = total + decoration_charge
    var venue_charge = $('#venue').parent().parent().find('input[name="venue_charge"]').val();
    total1 = parseFloat(total1 * 0.1 + total1) + parseFloat(venue_charge)

    select_html = "<p>Venue Charge : <input type='hidden' value="+ venue_charge +" name='id_venue_charge'><b>" + venue_charge + "</b></p><p>Catering Charge : <input type='hidden' value="+ total +" name='id_caterer_charge'><b>" + total + "</b></p><p>Decoration Charge : <input type='hidden' value="+ decoration_charge +" name='id_decoration_charge'><b>" + decoration_charge + "</b></p><p>Total Bill Amount <small style='color:#fa0939;'>(Including Event Management charge 10%)</small>:<input type='hidden' value="+ total1 +" name='id_total_charge'> <b>" + total1 + "</b></p>"
    $('.bill_user').html(select_html)
}

// $(document).on('click','#submit',function(){
//     var venue_charge = $(this).parent().parent().find('input[name=\'id_venue_charge\']').val()
//     var catering_charge = $(this).parent().parent().find('input[name=\'id_caterer_charge\']').val()
//     var decoration_charge = $(this).parent().parent().find('input[name=\'id_decoration_charge\']').val()
//     var total_bill = $(this).parent().parent().find('input[name=\'id_total_charge\']').val()
//     data = {'venue_charge':venue_charge,'catering_charge':catering_charge,'decoration_charge':decoration_charge,'total_bill':total_bill}
//     console.log(data)
//     $.ajax({
//         type: 'POST',
//         url: '/sendcharges/',
//         dataType: 'json',
//         data: JSON.stringify(data),
//         contentType: "application/json; charset=UTF-8",
//         success: function (response){
//             var charges_data=response.success
//             alert(charges_data)
//         }
//     })
// })