$(document).ready(function() {
    $("#checkbox-input").click(function() {
        if($("#checkbox-input").val() == "2.5")
            $("#checkbox-input").val("");
    })

    $("#checkbox-input").blur(function() {
        if($("#checkbox-input").val() == "")
            $("#checkbox-input").val("2.5");
    })
    
    $("#done").click(function() {
        $("#modal1").closeModal();
    });
    
    $("#customize").click(function() {
        $('.carousel').carousel('next');
    });

    $('.carousel').carousel();
});