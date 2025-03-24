// profile_icon.js

document.addEventListener("DOMContentLoaded", function () {
    const profileIcon = document.getElementById("profileIcon");
    const profilePopup = document.getElementById("profilePopup");
    const heroText = document.querySelector(".hero-content h1");
    const sections = document.querySelectorAll("section");
    const navbar = document.querySelector(".navbar");

    // Animated Heading - Word by Word (moved up to avoid duplicate DOMContentLoaded)
    function animateHeading() {
        const animatedHeading = document.getElementById("animatedHeading");
        if (!animatedHeading) return;
    
        // Preserve original HTML including spaces
        const originalHTML = animatedHeading.innerHTML;
        
        // Split by both spaces and HTML space entities
        const wordElements = [];
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = originalHTML;
        
        // Process child nodes to preserve spaces
        Array.from(tempDiv.childNodes).forEach(node => {
            if (node.nodeType === Node.TEXT_NODE) {
                // Split text nodes by spaces
                const words = node.textContent.split(/(\s+)/);
                words.forEach(word => {
                    if (word.trim() !== '') {
                        const span = document.createElement('span');
                        span.textContent = word;
                        span.classList.add('word');
                        wordElements.push(span);
                    } else if (word !== '') {
                        // Preserve multiple spaces
                        const spaceSpan = document.createElement('span');
                        spaceSpan.textContent = word;
                        spaceSpan.style.display = 'inline'; // Ensure spaces are visible
                        wordElements.push(spaceSpan);
                    }
                });
            } else {
                // Handle other HTML elements that might be in the heading
                wordElements.push(node.cloneNode(true));
            }
        });
    
        // Clear and rebuild with animation
        animatedHeading.innerHTML = '';
        wordElements.forEach((element, i) => {
            if (element.classList && element.classList.contains('word')) {
                element.style.animation = `fadeInWord 0.6s ease-out ${i * 0.3}s forwards`;
            }
            animatedHeading.appendChild(element);
        });
    }

    // Profile Popup Functionality
    if (profileIcon && profilePopup) {
        profileIcon.addEventListener("click", function (e) {
            e.stopPropagation();
            // Toggle display directly instead of using class
            profilePopup.style.display = profilePopup.style.display === "block" ? "none" : "block";
        });

        document.addEventListener("click", function (event) {
            if (!profileIcon.contains(event.target) && !profilePopup.contains(event.target)) {
                profilePopup.style.display = "none";
            }
        });
    }

    // Initialize animations
    animateHeading();

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
    
    // Initial reveal check
    revealSections();
    window.addEventListener("scroll", revealSections);

    // Navbar scroll effect
    window.addEventListener("scroll", function () {
        navbar.classList.toggle("scrolled", window.scrollY > 50);
    });
});