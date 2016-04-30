$(document).ready(function() {
    
    $("#transfer-btn").click(function() {
        if($("#money").val() == "")
            Materialize.toast("Please Fill Transaction Amount", 2000);
        else {
            var type;
            var form = $("<form></form>");
            form.prop("method", "post");

            if($("#percent-btn").hasClass("z-depth-0"))
                type = "fixed";
            else
                type = "percent";

            form.append($("<input/>").prop({ name: "money", value: $("#money").val() }));
            form.append($("<input/>").prop({ name: "ocd", value: $("#tick").is(":checked") }));
            form.append($("<input/>").prop({ name: "type", value: type }));
            form.append($("<input/>").prop({ name: "amount", value: $("#checkbox-input").val() }));
            form.append($("<input/>").prop({ name: "hide", value: $("#hide-it").val() }));
            form.append($("<input/>").prop({ name: "enabled", value: $("#regular").val() }));

            $(document.body).append(form);
            form.submit();
        }
    });

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
        
        if($("#fixed-btn").hasClass("z-depth-0")) {
            if($("#other-percent").hasClass("filled")) {
                $("#checkbox-input").val($("#other-percent").val());
            } else {
                $("#checkbox-input").val($("input[name='percent']:checked").val());
            }
            $("#currency").text("%");
        } else if($("#percent-btn").hasClass("z-depth-0")) {
            if($("#other-fixed").hasClass("filled")) {
                $("#checkbox-input").val($("#other-fixed").val());
            } else {
                $("#checkbox-input").val($("input[name='fixed']:checked").val());
            }
            $("#currency").text("AED");
        }
        if($("#checkbox-input").val() == "") $("#checkbox-input").val(2.5);

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

    $("#money").click(function() {
        $("#currency-select>option:eq(3)").prop("selected", true);
    });
});