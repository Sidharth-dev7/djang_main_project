// profile_icon.js

document.addEventListener("DOMContentLoaded", function () {
    const profileIcon = document.getElementById("profileIcon");
    const profilePopup = document.getElementById("profilePopup");

    if (profileIcon && profilePopup) {
        // Toggle pop-up visibility
        profileIcon.addEventListener("click", function () {
            profilePopup.style.display = profilePopup.style.display === "block" ? "none" : "block";
        });

        // Close pop-up when clicking outside
        window.addEventListener("click", function (event) {
            if (event.target !== profileIcon && !profileIcon.contains(event.target)) {
                profilePopup.style.display = "none";
            }
        });
    }
});