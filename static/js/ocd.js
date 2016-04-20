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

        $(document.body).append(form);
        form.submit();
    });

    $(".modal-trigger").leanModal({opacity: .3});
});