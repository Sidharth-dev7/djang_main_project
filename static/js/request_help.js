// request_help.js

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
            <input type="text" id="car-manufacturer" name="carManufacturer" placeholder="Enter car manufacturer" required>
            
            <label for="car-model">Car Model:</label>
            <input type="text" id="car-model" name="carModel" placeholder="Enter car model" required>
            
            <label for="problem-description">Describe the issue:</label>
            <textarea id="problem-description" name="problemDescription" rows="4" placeholder="Explain the problem" required></textarea>
            
            <button type="submit" class="submit-request">Request</button>
        </form>
    </div>
    `;

    document.body.appendChild(modal); // Add modal to body

    const requestForm = modal.querySelector("#requestHelpForm");
    const closeModalBtn = modal.querySelector(".close-modal");

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

    // Handle Form Submission
    requestForm.addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent page reload
        console.log("Car Manufacturer:", requestForm.carManufacturer.value);
        console.log("Car Model:", requestForm.carModel.value);
        console.log("Problem Description:", requestForm.problemDescription.value);
        alert("Request Sent! (Backend integration needed)");
        modal.style.display = "none"; // Close modal after submission
    });
});
