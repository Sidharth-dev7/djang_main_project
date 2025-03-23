// checkout.js

document.addEventListener("DOMContentLoaded", function () {
    console.log("DOM fully loaded and parsed");  // Debugging: Log when the DOM is ready

    const paymentOptions = document.querySelectorAll('input[name="payment-method"]');
    const paymentSection = document.getElementById("payment-section");
    const onlinePayment = document.getElementById("online-payment");
    const cashPayment = document.getElementById("cash-payment");

    // Show/hide payment sections based on selected payment method
    paymentOptions.forEach(option => {
        option.addEventListener("change", function () {
            console.log("Payment method changed:", this.value);  // Debugging: Log the selected payment method
            paymentSection.classList.remove("hidden");

            if (this.value === "online") {
                onlinePayment.classList.remove("hidden");
                cashPayment.classList.add("hidden");
            } else {
                cashPayment.classList.remove("hidden");
                onlinePayment.classList.add("hidden");
            }
        });
    });

    // Handle Pay Now button (for online payment)
    document.getElementById("pay-now").addEventListener("click", function () {
        console.log("Pay Now button clicked");  // Debugging: Log button click
        confirmPayment("online");
    });

    // Handle Confirm Cash button (for cash payment)
    document.getElementById("confirm-cash").addEventListener("click", function () {
        console.log("Confirm Cash button clicked");  // Debugging: Log button click
        confirmPayment("cash");
    });

    // Function to confirm payment
    function confirmPayment(paymentMethod) {
        const jobId = document.getElementById("job-id").value;  // Get the job ID from the hidden field
        const csrfToken = document.getElementById("csrf-token").value;  // Get the CSRF token from the hidden field
        const userDashboardUrl = document.getElementById("user-dashboard-url").value;  // Get the user dashboard URL
        const notificationId = document.getElementById("notification-id").value;  // Get the notification ID from the hidden field
    
        const payload = {
            payment_method: paymentMethod,
            notification_id: notificationId  // Include the notification ID in the payload
        };
    
        console.log("Sending payload:", payload);  // Debugging: Log the payload
    
        fetch(`/confirm-payment/${jobId}/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrfToken,
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        })
        .then(response => {
            console.log("Response status:", response.status);  // Debugging: Log the response status
            return response.json();
        })
        .then(data => {
            console.log("Response data:", data);  // Debugging: Log the response data
            if (data.success) {
                // Decrement the notification badge count
                const notificationBadge = document.getElementById("notificationBadge");
                if (notificationBadge) {
                    const currentCount = parseInt(notificationBadge.textContent);
                    if (currentCount > 0) {
                        notificationBadge.textContent = currentCount - 1;
                    }
                }
    
                // Show the pop-up
                const popup = document.getElementById("payment-confirmation-popup");
                popup.classList.remove("hidden");
    
                // Start countdown
                let countdown = 5;  // Changed from 4 to 5
                const countdownElement = document.getElementById("countdown");
                countdownElement.textContent = countdown;
    
                const countdownInterval = setInterval(() => {
                    countdown--;
                    countdownElement.textContent = countdown;
    
                    if (countdown <= 0) {
                        clearInterval(countdownInterval);
                        window.location.href = userDashboardUrl;  // Redirect to user dashboard
                    }
                }, 1000);  // Update every 1 second
            } else {
                alert("Error: " + data.error);
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("An error occurred. Please try again.");
        });
    }
});