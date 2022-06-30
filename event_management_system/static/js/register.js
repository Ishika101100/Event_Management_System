$(document).ready(function(){
    $("#user_type").change(function(){
        var user_type_val = $("#user_type").val();
        if(user_type_val == 2) {
            $("#venue_location_div").show()
            $("#venue_charges_div").show()
            $("#venue_capacity_div").show()
        }
        else
        {
            $("#venue_location_div").hide()
            $("#venue_charges_div").hide()
            $("#venue_capacity_div").hide()
        }
    })
})