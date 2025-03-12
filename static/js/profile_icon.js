// profile_icon.js

document.addEventListener("DOMContentLoaded", function () {
    const profileIcon = document.getElementById("profileIcon");
    const profilePopup = document.getElementById("profilePopup");

    if (profileIcon && profilePopup) {
        profileIcon.addEventListener("click", function (e) {
            e.stopPropagation();
            profilePopup.style.display = profilePopup.style.display === "block" ? "none" : "block";
        });

        window.addEventListener("click", function (event) {
            if (!profileIcon.contains(event.target) && !profilePopup.contains(event.target)) {
                profilePopup.style.display = "none";
            }
        });
    }
});