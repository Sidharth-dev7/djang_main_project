// garage_validation.js

document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    
    form.addEventListener("submit", function (event) {
        let isValid = true;

        // Get form inputs
        const name = document.querySelector("input[name='name']");
        const ownerName = document.querySelector("input[name='owner_name']");
        const contact = document.querySelector("input[name='contact']");
        const email = document.querySelector("input[name='email']");
        const password = document.querySelector("input[name='password']");
        const address = document.querySelector("textarea[name='address']");
        const services = document.querySelector("textarea[name='services_offered']");
        const image = document.querySelector("input[name='image']");

        // Validation functions
        function showError(input, message) {
            let errorElement = input.nextElementSibling;
            if (!errorElement || !errorElement.classList.contains("error-message")) {
                errorElement = document.createElement("div");
                errorElement.classList.add("error-message");
                errorElement.style.color = "red";
                errorElement.style.fontSize = "0.9em";
                input.parentNode.insertBefore(errorElement, input.nextSibling);
            }
            errorElement.textContent = message;
        }

        function clearError(input) {
            let errorElement = input.nextElementSibling;
            if (errorElement && errorElement.classList.contains("error-message")) {
                errorElement.textContent = "";
            }
        }

        // Name validation
        if (name.value.trim() === "") {
            showError(name, "Garage name is required.");
            isValid = false;
        } else {
            clearError(name);
        }

        // Owner name validation
        if (ownerName.value.trim() === "") {
            showError(ownerName, "Owner name is required.");
            isValid = false;
        } else {
            clearError(ownerName);
        }

        // Contact validation (10 digits)
        const contactRegex = /^[0-9]{10}$/;
        if (!contactRegex.test(contact.value.trim())) {
            showError(contact, "Enter a valid 10-digit contact number.");
            isValid = false;
        } else {
            clearError(contact);
        }

        // Email validation
        const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
        if (!emailRegex.test(email.value.trim())) {
            showError(email, "Enter a valid email address.");
            isValid = false;
        } else {
            clearError(email);
        }

        // Password validation (8 characters, 1 uppercase, 1 lowercase, 1 special character)
        const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\W).{8,}$/;
        if (!passwordRegex.test(password.value.trim())) {
            showError(password, "Password must be at least 8 characters long, with at least 1 uppercase letter, 1 lowercase letter, and 1 special character.");
            isValid = false;
        } else {
            clearError(password);
        }

        // Address validation
        if (address.value.trim() === "") {
            showError(address, "Address is required.");
            isValid = false;
        } else {
            clearError(address);
        }

        // Services offered validation
        if (services.value.trim() === "") {
            showError(services, "Please describe the services offered.");
            isValid = false;
        } else {
            clearError(services);
        }

        // Image validation (Ensure an image is selected)
        if (image.files.length === 0) {
            showError(image, "Please upload an image.");
            isValid = false;
        } else {
            clearError(image);
        }

        // Prevent form submission if validation fails
        if (!isValid) {
            event.preventDefault();
        }
    });
});
