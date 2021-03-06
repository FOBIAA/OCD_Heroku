$(document).ready(function() {
    $(".save").click(function() {
        var type, amount, frequency, charities = "";
        var form = $("<form></form>");
        form.prop("method", "post");

        if($("#fixed").is(":visible")) {
            type = "fixed";
            if($("#other-fixed").hasClass("filled")) {
                amount = $("#other-fixed").val();
            } else {
                amount = $("input[name='fixed']:checked").val();
            }
            frequency = $("input[name='fixed-freq']:checked").val();
        } else {
            type = "percent";
            if($("#other-percent").hasClass("filled")) {
                amount = $("#other-percent").val();
            } else {
                amount = $("input[name='percent']:checked").val();
            }
            frequency = $("input[name='percent-freq']:checked").val();
        }

        $("#charity-modal input:checked").each(function() {
            charities += $(this).prop("id") + " ";
        });

        form.append($("<input/>").prop({ name: "type", value: type }));
        form.append($("<input/>").prop({ name: "amount", value: amount }));
        form.append($("<input/>").prop({ name: "frequency", value: frequency }));
        form.append($("<input/>").prop({ name: "reveal", value: $("input[name='reveal']:checked").val() == "true" ? "true" : "false" }));
        form.append($("<input/>").prop({ name: "charity", value: charities }));
        form.append($("<input/>").prop({ name: "checkbox", value: $(".hide-ocd:visible").val() }));
        form.append($("<input/>").prop({ name: "app", value: $(".disable-ocd:visible").val() }));

        $(document.body).append(form);
        form.submit();
    });

    $("#done").click(function() {
        $("#charity-modal").closeModal();
    });

    $("#request-modal a").click(function() {
        $("#request-modal").closeModal();
    });

    // hide checkbox logic
    $(".hide-ocd").click(function() {
        if($(this).val() == "show")
            $(this).removeClass("z-depth-0").val("hide");
        else if($(this).val() == "hide")
            $(this).addClass("z-depth-0").val("show");
    });

    //Disable app logic
    $("#ocd .disable-ocd").click(function() {
        if($(this).val() == "enable")
            $(this).removeClass("z-depth-0").val("disable");
        else if($(this).val() == "disable")
            $(this).addClass("z-depth-0").val("enable");
    });

    $("#welcome-ocd .disable-ocd").click(function() {
        if($(this).val() == "disable")
            $(this).removeClass("z-depth-0").val("enable");
        else if($(this).val() == "enable")
            $(this).addClass("z-depth-0").val("disable");
    });

    $("#charity-modal input").click(function() {
        var image = $("#target img[src='/static/img/charity/" + $(this).prop("id") + ".jpg']");
        if($(this).is(":checked"))
            $(image).removeClass("hide");
        else
            $(image).addClass("hide");

        if($("#target img.hide").length != 10) {
            $("#target h4").hide();
        } else {
            $("#target h4").show();
        }
    });

    $(".modal-trigger").leanModal({opacity: .3});
    $('.collapsible').collapsible();
});