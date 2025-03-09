// home.js

document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("login-modal");
    const closeModalBtn = document.querySelector(".close");
    const loginForm = document.getElementById("login-form");
    const errorMessage = document.getElementById("loginError");
    const userDashboardUrl = document.getElementById("user-dashboard-url").value; // Get the URL

    // Open Modal Function
    function openModal() {
        if (modal) modal.classList.add("active");
    }

    // Close Modal Function
    function closeModal() {
        if (modal) modal.classList.remove("active");
        if (errorMessage) errorMessage.textContent = "";
    }

    // Close modal when clicking outside or on the close button
    if (closeModalBtn) closeModalBtn.addEventListener("click", closeModal);
    window.addEventListener("click", function (event) {
        if (event.target === modal) closeModal();
    });

    // Handle Login Form Submission
    if (loginForm) {
        loginForm.addEventListener("submit", function (event) {
            event.preventDefault();

            const formData = new FormData(loginForm);
            const csrfToken = document.querySelector("input[name='csrfmiddlewaretoken']").value;

            fetch("/user-login/", {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrfToken,
                    "X-Requested-With": "XMLHttpRequest",
                },
                body: formData,
            })
                .then((response) => response.json())
                .then((data) => {
                    if (data.success) {
                        window.location.href = userDashboardUrl; // Use the URL from the hidden input
                    } else {
                        if (errorMessage) errorMessage.textContent = data.error || "Invalid credentials.";
                    }
                })
                .catch((error) => {
                    console.error("Login error:", error);
                    if (errorMessage) errorMessage.textContent = "Something went wrong. Please try again.";
                });
        });
    }

    // Check login status before accessing restricted pages
    function checkLogin(event) {
        event.preventDefault();

        fetch("/check-login/")
            .then((response) => response.json())
            .then((data) => {
                if (data.is_authenticated) {
                    window.location.href = event.target.href; // Redirect if logged in
                } else {
                    openModal(); // Show login modal if not logged in
                }
            })
            .catch((error) => console.error("Error checking login:", error));
    }

    // Attach event listeners to buttons/links
    ["requestHelp", "requestAssistance", "findGarages"].forEach((id) => {
        const element = document.getElementById(id);
        if (element) element.addEventListener("click", checkLogin);
    });
});