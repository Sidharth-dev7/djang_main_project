document.addEventListener("DOMContentLoaded", () => {
    // Make sure the buttons exist before trying to attach event listeners
    document.querySelectorAll(".approve-btn, .reject-btn").forEach(button => {
        button.addEventListener("click", () => {
            // Fetch the request ID from the button's data-id attribute
            const requestId = button.dataset.id;
            const status = button.classList.contains("approve-btn") ? "Approved" : "Rejected";

            // Send a POST request to update the status
            fetch(`/update-request-status/${requestId}/${status}/`, {
                method: "POST", // Ensure the method is POST
                headers: {
                    "X-CSRFToken": getCSRFToken(),
                    "Content-Type": "application/json"
                }
            })
            .then(response => response.json()) // Parse JSON response
            .then(data => {
                if (data.success) {
                    alert(data.message); // Show success message
                    button.parentElement.remove(); // Remove the request from UI
                } else {
                    alert("Error updating request.");
                }
            })
            .catch(error => {
                alert("Error occurred. Please try again.");
            });
        });
    });
});

// Function to get CSRF Token from cookies
function getCSRFToken() {
    const cookie = document.cookie.split('; ').find(row => row.startsWith('csrftoken'));
    return cookie ? cookie.split('=')[1] : '';
}



