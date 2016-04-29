$(document).ready(function() {
    
    // Config for charity slider
    $(".carousel").carousel();
    $(".carousel").carousel("next");

    $("#customize").click(function() {
        $(".carousel").carousel("prev");
    });

    function done() {
        $(".carousel").carousel("next");
        
        if($("#hide-it").val() == "true")
            $("#ocd-title, #ocd-button").hide();
        
        if($("#regular").val() == "true") {
            Materialize.toast("Check out My Donation section", 2000);
            setTimeout('Materialize.toast("You\'ll find Magic there!", 2000)', 1500)
        }
        
        $("#ocd-modal").closeModal();
    }
    
    $("#done").click(done);
    
    $(".modal-trigger").leanModal({
        opacity: .3,
        complete: done
    });
    
    // hide it and regular logic and link between them
    $("#hide-it, #regular").click(function() {
        if($(this).val() == "false") {
            $(this).removeClass("z-depth-0").val("true");
            
            // Disable other button if it's pressed
            var other = "#" + get_other($(this).attr("id"));
            if($(other).val() == "true") {
                $(other).addClass("z-depth-0").val("false");
            }
        } else if($(this).val() == "true") {
            $(this).addClass("z-depth-0").val("false");
        }
    });
    
    function get_other(id) {
        if(id == "regular")
            return "hide-it";
        else if(id == "hide-it")
            return "regular";
    }
});