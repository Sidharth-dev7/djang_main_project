// loign_check.js

document.addEventListener("DOMContentLoaded", function () {
    // Handle Login Form Submission via AJAX
    let loginForm = document.getElementById("login-form");
    let errorMessage = document.getElementById("loginError");
    let modal = document.getElementById("login-modal");

    if (loginForm) {
        loginForm.addEventListener("submit", function (event) {
            event.preventDefault(); // Stop normal form submission

            let formData = new FormData(loginForm);
            let csrfTokenInput = document.querySelector("input[name='csrfmiddlewaretoken']");
            let csrfToken = csrfTokenInput ? csrfTokenInput.value : "";

            fetch("/user-login/", {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrfToken,
                    "X-Requested-With": "XMLHttpRequest", // Ensure this header is sent
                    "Content-Type": "application/x-www-form-urlencoded", // Add this header
                },
                body: new URLSearchParams(formData).toString(), // Convert FormData to URL-encoded string
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Redirect to the user dashboard after successful login
                    window.location.href = "/user-dashboard/";
                } else {
                    if (errorMessage) {
                        errorMessage.textContent = data.error || "Invalid credentials.";
                    }
                }
            })
            .catch(error => {
                console.error("Login error:", error);
                if (errorMessage) {
                    errorMessage.textContent = "Something went wrong. Please try again.";
                }
            });
        });
    }

    // Function to show the login modal
    function showLoginModal() {
        if (modal) {
            modal.style.display = "flex"; // Show login modal
        } else {
            console.error("Login modal not found!");
        }
    }

    // Function to close the login modal
    function closeLoginModal() {
        if (modal) {
            modal.style.display = "none";
            if (errorMessage) {
                errorMessage.textContent = ""; // Clear error message when closing the modal
            }
        }
    }

    // Attach event listeners to buttons/links that require login
    let requestHelp = document.getElementById("requestHelp");
    let requestAssistance = document.getElementById("requestAssistance");
    let findGarages = document.getElementById("findGarages");

    if (requestHelp) requestHelp.addEventListener("click", function (event) {
        event.preventDefault(); // Stop default link behavior
        showLoginModal(); // Show login modal
    });

    if (requestAssistance) requestAssistance.addEventListener("click", function (event) {
        event.preventDefault(); // Stop default link behavior
        showLoginModal(); // Show login modal
    });

    if (findGarages) findGarages.addEventListener("click", function (event) {
        event.preventDefault(); // Stop default link behavior
        showLoginModal(); // Show login modal
    });

    // Close modal when clicking outside or on the close button
    let closeModal = document.querySelector("#login-modal .close");
    if (closeModal) {
        closeModal.addEventListener("click", closeLoginModal);
    }

    window.addEventListener("click", function (event) {
        if (event.target === modal) {
            closeLoginModal();
        }
    });
});