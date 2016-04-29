$(document).ready(function() {

    //Logic for donation types buttons
    $("#percent-btn").click(function() {
        $("#percent-btn").removeClass("z-depth-0");
        $("#percent").show();
        
        $("#fixed-btn").addClass("z-depth-0");
        $("#fixed").hide();
    });
    
    $("#fixed-btn").click(function() {
        $("#fixed-btn").removeClass("z-depth-0");
        $("#fixed").show();

        $("#percent-btn").addClass("z-depth-0");
        $("#percent").hide();
    });
    
    //Logic for configurations
    $("#other-fixed, #other-percent").click(function() {
        $("input[name='fixed'], input[name='percent']").prop("checked", false);
    });

    function reset(field) {
        $(field).val(-998);
        $(field).trigger("blur");
    }

    var data = {"other-percent": "#other-fixed",
                "other-fixed": "#other-percent"};
    
    $("#other-percent, #other-fixed").blur(function() {
        var amount = $(this).val();
        
        //If field is click but left empty or -998
        if(amount == "" || amount == -998)
            $(this).val("").removeClass("filled");
        else { //Otherwise if field was filled
            $(this).addClass("filled");
            reset(data[$(this).attr("id")]);
        }
    });
    
    //Toast message for selected donation
    $("input[name='fixed'], input[name='percent']").click(function() {
        for (var key in data) {
            reset("#" + key);
            $("#" + key).trigger("click");
        }
        $(this).prop("checked", true);
    });
});