// profile_icon.js

document.addEventListener("DOMContentLoaded", function () {
    const profileIcon = document.getElementById("profileIcon");
    const profilePopup = document.getElementById("profilePopup");

    if (profileIcon && profilePopup) {
        // Toggle pop-up visibility
        profileIcon.addEventListener("click", function (e) {
            e.stopPropagation();  // Prevent the click from propagating to the window
            profilePopup.style.display = profilePopup.style.display === "block" ? "none" : "block";
        });

        // Close pop-up when clicking outside
        window.addEventListener("click", function (event) {
            if (event.target !== profileIcon && !profileIcon.contains(event.target)) {
                profilePopup.style.display = "none";
            }
        });

        // Allow links inside the pop-up to work
        const popupLinks = profilePopup.querySelectorAll("a");
        popupLinks.forEach(link => {
            link.addEventListener("click", function (e) {
                e.stopPropagation();  // Prevent the click from closing the pop-up
                // Allow the link to navigate to its destination
            });
        });
    }
});