// User_PopUp.js

document.addEventListener("DOMContentLoaded", function () {
    // Function to open modal with animation
    function openModal(modal) {
        if (modal) {
            modal.style.display = "flex"; // Use flex to center the modal
            modal.style.animation = "fadeIn 0.3s ease-out"; // Add fade-in animation
        }
    }

    // Function to close modal with animation
    function closeModal(modal) {
        if (modal) {
            modal.style.animation = "fadeOut 0.3s ease-out"; // Add fade-out animation
            setTimeout(() => {
                modal.style.display = "none";
                modal.style.animation = ""; // Reset animation
            }, 300); // Match the duration of the animation
        }
    }

    // My Requests Pop-Up
    const myRequestsLink = document.getElementById("myRequestsLink");
    const myRequestsModal = document.getElementById("myRequestsModal");
    const myRequestsClose = myRequestsModal?.querySelector(".close");

    if (myRequestsLink && myRequestsModal) {
        myRequestsLink.addEventListener("click", function (event) {
            event.preventDefault();
            openModal(myRequestsModal); // Open modal with animation
            fetchMyRequests();
        });

        if (myRequestsClose) {
            myRequestsClose.addEventListener("click", function () {
                closeModal(myRequestsModal); // Close modal with animation
            });
        }

        window.addEventListener("click", function (event) {
            if (event.target === myRequestsModal) {
                closeModal(myRequestsModal); // Close modal when clicking outside
            }
        });
    }

    // Notifications Pop-Up
    const notificationsLink = document.getElementById("notificationsLink");
    const notificationsModal = document.getElementById("notificationsModal");
    const notificationsClose = notificationsModal?.querySelector(".close");

    if (notificationsLink && notificationsModal) {
        notificationsLink.addEventListener("click", function (event) {
            event.preventDefault();
            openModal(notificationsModal); // Open modal with animation
            fetchNotifications();
        });

        if (notificationsClose) {
            notificationsClose.addEventListener("click", function () {
                closeModal(notificationsModal); // Close modal with animation
            });
        }

        window.addEventListener("click", function (event) {
            if (event.target === notificationsModal) {
                closeModal(notificationsModal); // Close modal when clicking outside
            }
        });
    }

    // Function to fetch My Requests
    function fetchMyRequests() {
        const requestsList = document.getElementById("requestsList");
        if (!requestsList) return;

        // Show loading state
        requestsList.innerHTML = "<p>Loading requests...</p>";

        fetch("/my-requests/")  // Replace with your backend endpoint
            .then(response => response.json())
            .then(data => {
                if (data.length > 0) {
                    requestsList.innerHTML = data.map(request => `
                        <div class="request-item">
                            <h3>${request.service}</h3>
                            <p>Status: ${request.status}</p>
                            <p>Date: ${request.date}</p>
                        </div>
                    `).join("");
                } else {
                    requestsList.innerHTML = "<p>No requests found.</p>";
                }
            })
            .catch(error => {
                console.error("Error fetching requests:", error);
                requestsList.innerHTML = "<p>Failed to load requests. Please try again later.</p>";
            });
    }

    // Function to fetch Notifications
    function fetchNotifications() {
        const notificationsList = document.getElementById("notificationsList");
        if (!notificationsList) return;

        // Show loading state
        notificationsList.innerHTML = "<p>Loading notifications...</p>";

        fetch("/notifications/")  // Replace with your backend endpoint
            .then(response => response.json())
            .then(data => {
                if (data.length > 0) {
                    notificationsList.innerHTML = data.map(notification => `
                        <div class="notification-item">
                            <p>${notification.message}</p>
                            <small>${notification.timestamp}</small>
                        </div>
                    `).join("");
                } else {
                    notificationsList.innerHTML = "<p>No new notifications.</p>";
                }
            })
            .catch(error => {
                console.error("Error fetching notifications:", error);
                notificationsList.innerHTML = "<p>Failed to load notifications. Please try again later.</p>";
            });
    }
});