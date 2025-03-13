/// request_help.js

document.addEventListener("DOMContentLoaded", function () {
    const requestHelpBtn = document.querySelector(".request-help");

    if (!requestHelpBtn) return; // Exit if button not found

    const modal = document.createElement("div");

    // Modal HTML structure
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
        <p id="statusMessage" style="display: none; color: green; font-weight: bold;"></p>
    </div>
    `;

    document.body.appendChild(modal); // Add modal to body

    const requestForm = modal.querySelector("#requestHelpForm");
    const closeModalBtn = modal.querySelector(".close-modal");
    const statusMessage = modal.querySelector("#statusMessage");

    // Get the garage ID from the button's data-garage-id attribute
    const garageId = requestHelpBtn.getAttribute("data-garage-id");

    if (!garageId) {
        console.error("Garage ID is missing!");
        return; // Exit if garageId is missing
    }

    // Show Modal
    requestHelpBtn.addEventListener("click", function () {
        modal.style.display = "flex";
    });

    // Close Modal when clicking the "×"
    closeModalBtn.addEventListener("click", function () {
        modal.style.display = "none";
    });

    // Close Modal when clicking outside of it
    window.addEventListener("click", function (event) {
        if (event.target === modal) {
            modal.style.display = "none";
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
                statusMessage.textContent = "Request Sent Successfully!";
                statusMessage.style.display = "block";
            } else {
                statusMessage.textContent = `Failed to send request: ${data.message}`;
                statusMessage.style.display = "block";
            }
        })
        .catch(error => {
            statusMessage.textContent = "Error sending request. Please try again.";
            statusMessage.style.display = "block";
        });

        // Hide modal after submission
        setTimeout(() => {
            modal.style.display = "none";
            statusMessage.style.display = "none";
        }, 3000);
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
