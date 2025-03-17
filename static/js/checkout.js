// checkout.js

document.addEventListener("DOMContentLoaded", function () {
    const paymentOptions = document.querySelectorAll('input[name="payment-method"]');
    const paymentSection = document.getElementById("payment-section");
    const onlinePayment = document.getElementById("online-payment");
    const cashPayment = document.getElementById("cash-payment");

    paymentOptions.forEach(option => {
        option.addEventListener("change", function () {
            paymentSection.classList.remove("hidden");

            if (this.value === "online") {
                onlinePayment.classList.remove("hidden");
                cashPayment.classList.add("hidden");
            } else {
                cashPayment.classList.remove("hidden");
                onlinePayment.classList.add("hidden");
            }
        });
    });

    // Simulated Payment Processing
    document.getElementById("pay-now").addEventListener("click", function () {
        alert("Redirecting to payment gateway...");
        // Redirect logic or API call for online payment
    });

    document.getElementById("confirm-cash").addEventListener("click", function () {
        alert("Cash payment confirmed!");
        // Update payment status in backend
    });
});
