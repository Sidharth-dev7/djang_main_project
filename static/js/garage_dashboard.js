// garage_dashboard.js

document.addEventListener("DOMContentLoaded", () => {
    let slides = document.querySelectorAll(".slide");
    let currentSlide = 0;

    function showSlides() {
        slides.forEach((slide, index) => {
            slide.style.opacity = index === currentSlide ? "1" : "0";
        });

        currentSlide = (currentSlide + 1) % slides.length;
        setTimeout(showSlides, 4000);
    }

    showSlides();
});
