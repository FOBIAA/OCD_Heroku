$(document).ready(function() {

    //Logic for donation types buttons
    $("#percent-btn").click(function() {
        $("#percent").show();
        $("#fixed").hide();
        
        $("input[name='percentage']").prop("checked", false);
    });
    
    $("#fixed-btn").click(function() {
        $("#fixed").show();
        $("#percent").hide();
    });
    
    //Logic for percentage radio buttons
    $("#other-percentage").click(function() {
        $("input[name='percentage']").prop("checked", false);
    });
    
    $("#other-percentage").blur(function() {
        var percentage = $("#other-percentage").val();
        
        if(percentage == "") {
            $("#p1").trigger("click");
            $("#other-percentage").removeClass("filled");
        } else if(percentage == -998) {
            $("#other-percentage").val("");
            $("#other-percentage").removeClass("filled");
        } else {
            $("#other-percentage").addClass("filled");
            Materialize.toast("Wow, you'll donate " + percentage + "% !", 3000);
        }
    });
    
    $("input[name='percentage']").click(function(event) {
        $("#other-percentage").val(-998);
        $("#other-percentage").trigger("blur");
        Materialize.toast("Wow, you'll donate " + $(this).next("label").text() + " !", 3000);
    });

    //Logic for fixed amount radio buttons
    $("#other-amount").click(function() {
        $("input[name='amount']").prop("checked", false);
    });
    
    $("#other-amount").blur(function() {
        var percentage = $("#other-amount").val();
        
        if(percentage == "") {
            $("#a1").trigger("click");
            $("#other-amount").removeClass("filled");
        } else if(percentage == -998) {
            $("#other-amount").val("");
            $("#other-amount").removeClass("filled");
        } else {
            $("#other-amount").addClass("filled");
            Materialize.toast("Wow, you'll donate " + percentage + "AED !", 3000);
        }
    });
    
    $("input[name='amount']").click(function(event) {
        $("#other-amount").val(-998);
        $("#other-amount").trigger("blur");
        Materialize.toast("Wow, you'll donate " + $(this).next("label").text() + " !", 3000);
    });
    
    $("#percent-btn").trigger("click");
});