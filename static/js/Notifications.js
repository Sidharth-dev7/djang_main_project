//Notifications.js

 // Fetch notifications
 function fetchNotifications() {
    fetch('/get_notifications/')
        .then(response => response.json())
        .then(data => {
            console.log("Notifications data:", data);  // Debugging
            const notificationsList = document.getElementById('notificationsList');
            const notificationBadge = document.getElementById('notificationBadge');

            // Clear existing notifications
            notificationsList.innerHTML = '';

            // Update notification badge
            notificationBadge.textContent = data.notifications.length;

            // Add notifications to the dropdown
            data.notifications.forEach(notification => {
                console.log("Adding notification:", notification);  // Debugging
                const notificationItem = document.createElement('div');
                notificationItem.className = 'notification-item';
                notificationItem.innerHTML = `
                    <p>${notification.message}</p>
                    <a href="${notification.link}">View Details</a>
                    <button onclick="markNotificationAsRead(${notification.id}, this)">Mark as Read</button>
                `;
                notificationsList.appendChild(notificationItem);
            });
        })
        .catch(error => {
            console.error("Error fetching notifications:", error);  // Debugging
        });
}

// Mark a notification as read
function markNotificationAsRead(notificationId, button) {
    console.log("Marking notification as read:", notificationId);  // Debugging
    if (!notificationId) {
        console.error("Invalid notification ID:", notificationId);
        alert("Invalid notification ID. Please try again.");
        return;
    }

    fetch(`/mark_notification_read/${notificationId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            // Remove the notification item from the dropdown
            const notificationItem = button.closest('.notification-item');  // Use closest() to find the parent notification item
            if (notificationItem) {
                notificationItem.remove();
            }

            // Decrement the notification badge count
            const notificationBadge = document.getElementById('notificationBadge');
            if (notificationBadge) {
                notificationBadge.textContent = parseInt(notificationBadge.textContent) - 1;
            }
        } else {
            alert('Error marking notification as read: ' + (data.error || 'Unknown error'));
        }
    })
    .catch(error => {
        console.error("Error:", error);  // Debugging
        alert('An error occurred. Please try again.');
    });
}

// Toggle notifications dropdown
document.getElementById('notificationLink').addEventListener('click', function(event) {
    event.preventDefault();  // Prevent the link from navigating
    const dropdown = document.getElementById('notificationsDropdown');
    dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
    fetchNotifications();  // Fetch notifications when the dropdown is opened
});

// Fetch notifications every 10 seconds
setInterval(fetchNotifications, 10000);

// Initial fetch of notifications
fetchNotifications();

// Function to get CSRF token from cookies
function getCSRFToken() {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith('csrftoken=')) {
                cookieValue = cookie.substring('csrftoken='.length, cookie.length);
                break;
            }
        }
    }
    return cookieValue;
}