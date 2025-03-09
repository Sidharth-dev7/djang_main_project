// customer_validation.js

document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");

    const firstNameField = document.querySelector("input[name='first_name']");
    const lastNameField = document.querySelector("input[name='last_name']");
    const contactField = document.querySelector("input[name='contact']");
    const emailField = document.querySelector("input[name='email']");
    const passwordField = document.querySelector("input[name='password']");

    function showError(field, message) {
        let errorSpan = field.parentElement.querySelector(".error-message");
        if (!errorSpan) {
            errorSpan = document.createElement("span");
            errorSpan.classList.add("error-message");
            field.parentElement.appendChild(errorSpan);
        }
        errorSpan.textContent = message;
    }

    function clearError(field) {
        let errorSpan = field.parentElement.querySelector(".error-message");
        if (errorSpan) {
            errorSpan.textContent = "";
        }
    }

    form.addEventListener("submit", function (event) {
        let isValid = true;

        // Name validation (only letters)
        const nameRegex = /^[A-Za-z]+$/;
        if (!nameRegex.test(firstNameField.value.trim())) {
            showError(firstNameField, "First name must contain only letters.");
            isValid = false;
        } else {
            clearError(firstNameField);
        }

        if (!nameRegex.test(lastNameField.value.trim())) {
            showError(lastNameField, "Last name must contain only letters.");
            isValid = false;
        } else {
            clearError(lastNameField);
        }

        // Contact validation (exactly 10 digits)
        const contactRegex = /^[0-9]{10}$/;
        if (!contactRegex.test(contactField.value.trim())) {
            showError(contactField, "Contact number must be exactly 10 digits.");
            isValid = false;
        } else {
            clearError(contactField);
        }

        // Email validation
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(emailField.value.trim())) {
            showError(emailField, "Enter a valid email address.");
            isValid = false;
        } else {
            clearError(emailField);
        }

        // Password validation (8+ characters, at least 1 uppercase, 1 lowercase, 1 number, 1 special character)
        const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
        if (!passwordRegex.test(passwordField.value)) {
            showError(passwordField, "Password must be 8+ chars, include uppercase, lowercase, number & special character.");
            isValid = false;
        } else {
            clearError(passwordField);
        }

        if (!isValid) {
            event.preventDefault();
        }
    });
});
