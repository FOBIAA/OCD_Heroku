$(document).ready(function() {
    
    $("#checkbox-input").click(function() {
        if($("#checkbox-input").val() == "2.5")
            $("#checkbox-input").val("");
    })

    $("#checkbox-input").blur(function() {
        if($("#checkbox-input").val() == "")
            $("#checkbox-input").val("2.5");
    })
    
    // Config for charity slider
    $(".carousel").carousel();
    $(".carousel").carousel("next");
    
    $("#done").click(function() {
        $(".carousel").carousel("next");
        
        if($("#hide-it").val() == "true")
            $("#ocd-title, #ocd-button").hide();
        
        // Condition to enable ocd section
        // if($("#regular").val() == "true")
        
        $("#ocd-modal").closeModal();
    });
    
    $("#customize").click(function() {
        $(".carousel").carousel("prev");
    });

    $(".modal-trigger").leanModal({
        opacity: .3,
        complete: function() {
            $(".carousel").carousel("next");
        }
    });
    
    // hide it and regular logic and link between them
    $("#hide-it, #regular").click(function() {
        if($(this).val() == "false") {
            $(this).removeClass("z-depth-0");
            $(this).val("true");
            
            // Disable other button if it's pressed
            var other = "#" + get_other($(this).attr("id"));
            if($(other).val() == "true") {
                $(other).addClass("z-depth-0");
                $(other).val("false");
            }
        } else if($(this).val() == "true") {
            $(this).addClass("z-depth-0");
            $(this).val("false");
        }
    });
    
    function get_other(id) {
        if(id == "regular")
            return "hide-it";
        else if(id == "hide-it")
            return "regular";
    }
});