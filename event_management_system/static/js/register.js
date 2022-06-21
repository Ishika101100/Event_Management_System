$(document).ready(function(){
    $("#user_type").change(function(){
        var user_type_val = $("#user_type").val();
        if(user_type_val == 2) {
            $("#venue_location_div").show()
        }
        else
        {
            $("#venue_location_div").hide()
        }
    })
})