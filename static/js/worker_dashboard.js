$(document).ready(function(){
    let workerId = $("#work-toggle").data("worker-id"); // Get worker ID from HTML

    // Fetch initial worker status
    $.get(`/get_worker_status/${workerId}/`, function(data){
        if (data.status === "available") {
            $("#work-toggle").prop("checked", true);
            $("#status-text").text("Status: Ready to Work");
        } else {
            $("#work-toggle").prop("checked", false);
            $("#status-text").text("Status: Unavailable");
        }
    });

    // Save status when the "Save" button is clicked
    $("#save-status-btn").click(function(){
        let isActive = $("#work-toggle").is(":checked"); // Get the toggle status
        let status = isActive ? "available" : "unavailable";

        // Update the status text
        $("#status-text").text("Status: " + (isActive ? "Ready to Work" : "Unavailable"));

        // Send the updated status to the server
        $.ajax({
            url: "/update_worker_status/",
            type: "POST",
            headers: { "X-CSRFToken": getCSRFToken() },  // Get CSRF token dynamically
            data: JSON.stringify({ worker_id: workerId, is_active: isActive }),
            contentType: "application/json",
            success: function(response) {
                console.log("Status updated successfully:", response);
            },
            error: function(xhr, status, error) {
                console.error("Error updating status:", error);
            }
        });
    });

    // Logout button
    $("#logout-btn").click(function(){
        window.location.href = "/logout/";
    });
});

// Function to get CSRF token from cookies
function getCSRFToken() {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith("csrftoken=")) {
                cookieValue = cookie.substring("csrftoken=".length, cookie.length);
                break;
            }
        }
    }
    return cookieValue;
}
function updateAssignedRequestDetails(requestDetails) {
    document.getElementById('assigned-customer').textContent = `Customer: ${requestDetails.customer}`;
    document.getElementById('assigned-car').textContent = `Car: ${requestDetails.car}`;
    document.getElementById('assigned-issue').textContent = `Issue: ${requestDetails.issue}`;
    document.getElementById('assigned-status').textContent = `Status: ${requestDetails.status}`;
}







