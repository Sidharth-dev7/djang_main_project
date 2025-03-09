document.addEventListener("DOMContentLoaded", function () {
    function checkLogin(event) {
        event.preventDefault(); // Stop default link behavior

        fetch("/check-login/") // API call to check login status
            .then(response => response.json())
            .then(data => {
                if (data.is_authenticated) {
                    window.location.href = event.target.href; // Redirect if logged in
                } else {
                    let modal = document.getElementById("login-modal");
                    if (modal) {
                        modal.style.display = "flex"; // Show login modal
                    } else {
                        console.error("Login modal not found!");
                    }
                }
            })
            .catch(error => console.error("Error checking login:", error));
    }

    let requestHelp = document.getElementById("requestHelp");
    let requestAssistance = document.getElementById("requestAssistance");
    let findGarages = document.getElementById("findGarages");

    if (requestHelp) requestHelp.addEventListener("click", checkLogin);
    if (requestAssistance) requestAssistance.addEventListener("click", checkLogin);
    if (findGarages) findGarages.addEventListener("click", checkLogin);

    // Close modal when clicking outside or on the close button
    let modal = document.getElementById("login-modal");
    let closeModal = document.querySelector("#login-modal .close");

    function closeLoginModal() {
        if (modal) modal.style.display = "none";
    }

    if (closeModal) {
        closeModal.addEventListener("click", closeLoginModal);
    }

    window.addEventListener("click", function (event) {
        if (event.target === modal) {
            closeLoginModal();
        }
    });

    // ✅ Handle Login Form Submission via AJAX
    let loginForm = document.getElementById("login-form");
    let errorMessage = document.getElementById("loginError");

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
                    "X-Requested-With": "XMLHttpRequest",
                },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload(); // ✅ Refresh the page to show logged-in state
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
    } else {
        console.error("Login form not found!");
    }
});
