// garage_popup.js

document.addEventListener("DOMContentLoaded", function () {
    function openModal(modal) {
        document.querySelectorAll(".popup-modal").forEach(existingModal => {
            existingModal.style.display = "none"; // Hide other modals
        });
    
        if (modal) {
            modal.style.display = "flex";
        }
    }
    
    function closeModal(modal) {
        if (modal) {
            modal.style.display = "none";
        }
    }

    // Service Requests
    const myRequestsLink = document.getElementById("myRequestsLink");
    const myRequestsModal = document.getElementById("myRequestsModal");
    const myRequestsClose = myRequestsModal?.querySelector(".popup-close");  // Updated class

    if (myRequestsLink && myRequestsModal) {
        myRequestsLink.addEventListener("click", function (event) {
            event.preventDefault();
            openModal(myRequestsModal);
            fetchMyRequests();
        });

        if (myRequestsClose) {
            myRequestsClose.addEventListener("click", function () {
                closeModal(myRequestsModal);
            });
        }

        window.addEventListener("click", function (event) {
            if (event.target === myRequestsModal) {
                closeModal(myRequestsModal);
            }
        });
    }

    // Notifications
    const notificationsLink = document.getElementById("notificationsLink");
    const notificationsModal = document.getElementById("notificationsModal");
    const notificationsClose = notificationsModal?.querySelector(".popup-close"); // Updated class

    if (notificationsLink && notificationsModal) {
        notificationsLink.addEventListener("click", function (event) {
            event.preventDefault();
            openModal(notificationsModal);
            fetchNotifications();
        });

        if (notificationsClose) {
            notificationsClose.addEventListener("click", function () {
                closeModal(notificationsModal);
            });
        }

        window.addEventListener("click", function (event) {
            if (event.target === notificationsModal) {
                closeModal(notificationsModal);
            }
        });
    }

    function fetchMyRequests() {
        const requestsList = document.getElementById("requestsList");
        if (!requestsList) return;

        requestsList.innerHTML = "<p>Loading requests...</p>";

        fetch("/my-requests/")
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

    function fetchNotifications() {
        const notificationsList = document.getElementById("notificationsList");
        if (!notificationsList) return;

        notificationsList.innerHTML = "<p>Loading notifications...</p>";

        fetch("/notifications/")
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