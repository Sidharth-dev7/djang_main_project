// home.js

document.addEventListener("DOMContentLoaded", function () {
    var modal = document.getElementById("login-modal");
    var btns = document.querySelectorAll("#openModal");
    var closeBtn = document.querySelector(".close");
    var loginForm = modal.querySelector("form");
    var errorMessage = document.createElement("p"); // Error message element
    errorMessage.style.color = "red";
    loginForm.appendChild(errorMessage);

    // Hide modal on page load
    modal.style.display = "none";

    // Open modal on button click
    btns.forEach(function (btn) {
        btn.onclick = function (event) {
            event.preventDefault();
            modal.style.display = "flex"; 
            document.body.classList.add("modal-active");
        };
    });

    // Close modal
    closeBtn.onclick = function () {
        modal.style.display = "none";
        document.body.classList.remove("modal-active");
        errorMessage.textContent = ""; // Clear error on close
    };

    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
            document.body.classList.remove("modal-active");
            errorMessage.textContent = "";
        }
    };

    // Handle login form submission
    loginForm.addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent normal form submission

        let formData = new FormData(loginForm);

        fetch("{% url 'user_login' %}", {  // Use Django URL for login
            method: "POST",
            body: formData,
            headers: {
                "X-Requested-With": "XMLHttpRequest",
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = data.redirect_url; // Redirect on success
            } else {
                errorMessage.textContent = data.message; // Show error in modal
            }
        })
        .catch(error => {
            console.error("Error:", error);
            errorMessage.textContent = "Something went wrong. Please try again.";
        });
    });
});
