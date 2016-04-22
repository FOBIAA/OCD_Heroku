$(document).ready(function() {
    $("#save").click(function() {
        var type, amount, frequency, charities = "";
        var form = $("<form></form>");
        form.prop("method", "post");

        if($("#percent").is(":visible")){
            type = "percent";
            if($("#other-percentage").hasClass("filled")) {
                amount = $("#other-percentage").val();
            } else {
                amount = $("input[name='percentage']:checked").val();
            }
            frequency = $("input[name='frequency']:checked").val();
        } else if($("#fixed").is(":visible")) {
            type = "fixed";
            if($("#other-amount").hasClass("filled")) {
                amount = $("#other-amount").val();
            } else {
                amount = $("input[name='amount']:checked").val();
            }
            frequency = $("input[name='period']:checked").val();
        }

        $("#charity-modal input:checked").each(function() {
            charities += $(this).prop("id") + " ";
        });

        form.append($("<input/>").prop({ name: "type", value: type }));
        form.append($("<input/>").prop({ name: "amount", value: amount }));
        form.append($("<input/>").prop({ name: "frequency", value: frequency }));
        form.append($("<input/>").prop({ name: "reveal", value: $("input[name='reveal']:checked").val() }));
        form.append($("<input/>").prop({ name: "charity", value: charities }));
        form.append($("<input/>").prop({ name: "checkbox", value: $("#hide-ocd").val() }));
        form.append($("<input/>").prop({ name: "app", value: $("#disable").val() }));

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
    $("#hide-ocd").click(function() {
        if($(this).val() == "show") {
            $(this).removeClass("z-depth-0");
            $(this).val("hide");
        } else if($(this).val() == "hide") {
            $(this).addClass("z-depth-0");
            $(this).val("show");
        }
    });

    //Disable app logic
    $("#disable").click(function() {
        if($(this).val() == "enable") {
            $(this).removeClass("z-depth-0");
            $(this).val("disable");
        } else if($(this).val() == "disable") {
            $(this).addClass("z-depth-0");
            $(this).val("enable");
        }
    });

    $(".modal-trigger").leanModal({opacity: .3});
});