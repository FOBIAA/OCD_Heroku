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

    var data = {"other-percent": ["#p1", "#other-fixed", "%"],
                "other-fixed": ["#a1", "#other-percent", "AED"]};
    
    $("#other-percent, #other-fixed").blur(function() {
        var amount = $(this).val();
        var index = $(this).attr("id");
        
        //If field is click but left empty
        if(amount == "") {
            $(data[index][0]).trigger("click");
            $(this).removeClass("filled");
        //If other field is click (which sends -998)
        } else if(amount == -998) {
            $(this).val("");
            $(this).removeClass("filled");
        //Otherwise if field was filled
        } else {
            $(this).addClass("filled");
            reset(data[index][1]);
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