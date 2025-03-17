$(document).ready(function(){
    // Fetch initial worker status
    $.get("/get_worker_status/", function(data){
        if (data.status === "available") {
            $("#work-toggle").prop("checked", true);
            $("#status-text").text("Status: Ready to Work");
        }
    });

    // Toggle work status
    $("#work-toggle").change(function(){
        let status = $(this).is(":checked") ? "available" : "unavailable";
        $("#status-text").text("Status: " + (status === "available" ? "Ready to Work" : "Unavailable"));

        $.post("/update_worker_status/", {
            status: status,
            csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
        });
    });

    // Logout button
    $("#logout-btn").click(function(){
        window.location.href = "/logout/";
    });
});
