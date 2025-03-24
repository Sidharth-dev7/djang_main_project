// profile_icon.js

document.addEventListener("DOMContentLoaded", function () {
    const profileIcon = document.getElementById("profileIcon");
    const profilePopup = document.getElementById("profilePopup");
    const heroText = document.querySelector(".hero-content h1");
    const sections = document.querySelectorAll("section");
    const navbar = document.querySelector(".navbar");

    if (profileIcon && profilePopup) {
        profileIcon.addEventListener("click", function (e) {
            e.stopPropagation();
            profilePopup.classList.toggle("show");
        });

        window.addEventListener("click", function (event) {
            if (!profileIcon.contains(event.target) && !profilePopup.contains(event.target)) {
                profilePopup.classList.remove("show");
            }
        });
    }

// Animated Heading - Word by Word
function animateHeading() {
    const heroText = document.getElementById("animatedHeading");
    if (!heroText) return;

    const words = heroText.textContent.split(" ");
    heroText.innerHTML = ""; // Clear the original text

    words.forEach((word, i) => {
        let span = document.createElement("span");
        span.textContent = word + " ";
        span.classList.add("word");
        span.style.animation = `fadeInWord 0.6s ease-out ${i * 0.3}s forwards`;
        heroText.appendChild(span);
    });
}

document.addEventListener("DOMContentLoaded", function () {
    animateHeading(); // Run animation when page loads
});


    // Scroll Animations
    function revealSections() {
        sections.forEach(section => {
            let sectionTop = section.getBoundingClientRect().top;
            let triggerPoint = window.innerHeight - 100;
            if (sectionTop < triggerPoint) {
                section.classList.add("visible");
            }
        });
    }
    window.addEventListener("scroll", revealSections);
    revealSections();

    // Change Navbar Background on Scroll
    window.addEventListener("scroll", function () {
        if (window.scrollY > 50) {
            navbar.classList.add("scrolled");
        } else {
            navbar.classList.remove("scrolled");
        }
    });
});
