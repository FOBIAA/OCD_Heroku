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
    $("#other-amount, #other-percentage").click(function() {
        $("input[name='amount'], input[name='percentage']").prop("checked", false);
    });

    function reset(field) {
        $(field).val(-998);
        $(field).trigger("blur");
    }

    var data = {"other-percentage": ["#p1", "#other-amount", "%"],
                "other-amount": ["#a1", "#other-percentage", "AED"]};
    
    $("#other-percentage, #other-amount").blur(function() {
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
    $("input[name='amount'], input[name='percentage']").click(function() {
        for (var key in data) {
            reset("#" + key);
            $("#" + key).trigger("click");
        }
        $(this).prop("checked", true);
    });

    $("#percent-btn").trigger("click");
});