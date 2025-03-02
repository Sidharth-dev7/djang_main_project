// pop_up.js

document.getElementById("loginForm").addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent page reload

    let formData = new FormData(this);

    fetch("/user-login/", {
        method: "POST",
        body: formData,
        headers: {
            "X-Requested-With": "XMLHttpRequest",
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = data.redirect_url;  // Redirect to home page
        } else {
            document.getElementById("loginError").innerText = data.message;  // Show error message
        }
    })
    .catch(error => console.error("Error:", error));
});