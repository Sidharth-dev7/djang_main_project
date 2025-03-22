document.addEventListener("DOMContentLoaded", function () {
    const requestHelpBtn = document.querySelector(".request-help");

    if (!requestHelpBtn) return; // Exit if button not found

    const modal = document.createElement("div");
    const successModal = document.createElement("div");

    // Modal HTML structure for Request Help
    modal.classList.add("modal");
    modal.style.display = "none"; // 👈 Hide modal by default
    modal.innerHTML = `
    <div class="modal-content">
        <span class="close-modal">&times;</span>
        <h2>Request Help</h2>
        <form id="requestHelpForm">
            <label for="car-manufacturer">Car Manufacturer:</label>
            <input type="text" id="car-manufacturer" name="car_manufacturer" placeholder="Enter car manufacturer" required>

            <label for="car-model">Car Model:</label>
            <input type="text" id="car-model" name="car_model" placeholder="Enter car model" required>

            <label for="problem-description">Describe the issue:</label>
            <textarea id="problem-description" name="issue_description" rows="4" placeholder="Explain the problem" required></textarea>
            
            <button type="submit" class="submit-request">Request</button>
        </form>
    </div>
    `;

    // Success Modal HTML structure
    successModal.classList.add("modal");
    successModal.style.display = "none"; // 👈 Hide modal by default
    successModal.innerHTML = `
    <div class="modal-content">
        <span class="close-modal">&times;</span>
        <h2>Request Sent Successfully!</h2>
        <p>Your request has been sent to the garage. We will get back to you shortly.</p>
    </div>
    `;

    document.body.appendChild(modal); // Add Request Help modal to body
    document.body.appendChild(successModal); // Add Success modal to body

    const requestForm = modal.querySelector("#requestHelpForm");
    const closeModalBtn = modal.querySelector(".close-modal");
    const closeSuccessModalBtn = successModal.querySelector(".close-modal");

    // Get the garage ID from the button's data-garage-id attribute
    const garageId = requestHelpBtn.getAttribute("data-garage-id");

    if (!garageId) {
        console.error("Garage ID is missing!");
        return; // Exit if garageId is missing
    }

    // Show Request Help Modal
    requestHelpBtn.addEventListener("click", function () {
        modal.style.display = "flex";
    });

    // Close Request Help Modal when clicking the "×"
    closeModalBtn.addEventListener("click", function () {
        modal.style.display = "none";
    });

    // Close Success Modal when clicking the "×"
    closeSuccessModalBtn.addEventListener("click", function () {
        successModal.style.display = "none";
    });

    // Close Modals when clicking outside of them
    window.addEventListener("click", function (event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
        if (event.target === successModal) {
            successModal.style.display = "none";
        }
    });

    // Handle Form Submission (Send Data via AJAX)
    requestForm.addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent page reload

        // Collect form data
        const formData = {
            car_manufacturer: document.getElementById("car-manufacturer").value,
            car_model: document.getElementById("car-model").value,
            issue_description: document.getElementById("problem-description").value,
        };

        console.log("Form Data:", JSON.stringify(formData));
        console.log("Garage ID:", garageId);

        // Send AJAX request to Django
        fetch(`/garage/${garageId}/request/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken(),  // Ensure CSRF token is sent properly
            },
            body: JSON.stringify(formData),
        })
        .then(response => response.json()) // Expect a JSON response
        .then(data => {
            if (data.success) {
                modal.style.display = "none"; // Hide Request Help Modal
                successModal.style.display = "flex"; // Show Success Modal
            } else {
                alert(`Failed to send request: ${data.message}`);
            }
        })
        .catch(error => {
            alert("Error sending request. Please try again.");
        });
    });

    // Function to get CSRF token
    function getCSRFToken() {
        const cookieValue = document.cookie
            .split("; ")
            .find(row => row.startsWith("csrftoken="))
            ?.split("=")[1];
        return cookieValue || "";
    }
});
