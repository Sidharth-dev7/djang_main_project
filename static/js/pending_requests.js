// pending_requests.js

document.addEventListener("DOMContentLoaded", function() {
    // No changes needed here for now
});

// Function to open the worker assignment popup and fetch workers from backend
function openAssignWorkerPopup(requestId) {
    const workerList = document.getElementById(`worker-list-${requestId}`);
    workerList.innerHTML = ''; // Clear previous list

    // Fetch worker data from Django backend
    fetch(`/get-workers/${requestId}/`)
        .then(response => response.json())
        .then(workers => {
            workers.forEach(worker => {
                const li = document.createElement('li');
                li.textContent = worker.name;
                li.classList.add('worker-item');

                // Create the status circle
                const statusIndicator = document.createElement('span');
                statusIndicator.classList.add('worker-status-circle');

                // Assign color based on worker status
                if (worker.status === 'available') {
                    statusIndicator.style.backgroundColor = '#28a745'; // Green (available)
                    li.onclick = (event) => selectWorker(worker.id, requestId, event);
                } else if (worker.status === 'assigned') {
                    statusIndicator.style.backgroundColor = '#ffc107'; // Yellow (busy)
                } else {
                    statusIndicator.style.backgroundColor = '#dc3545'; // Red (unavailable)
                }

                li.appendChild(statusIndicator);
                workerList.appendChild(li);
            });

            // Show the popup
            document.getElementById(`assignWorkerPopup-${requestId}`).style.display = "block";
        })
        .catch(error => console.error("Error fetching workers:", error));
}

// Select worker and enable confirm button
function selectWorker(workerId, requestId, event) {
    let confirmButton = document.getElementById(`confirmWorkerButton-${requestId}`);
    confirmButton.disabled = false;  
    confirmButton.setAttribute('data-worker-id', workerId);

    // Debugging: Log the worker ID and confirm button
    console.log(`Selected Worker ID: ${workerId}`);
    console.log(`Confirm Button:`, confirmButton);

    let workerList = document.getElementById(`worker-list-${requestId}`);
    let workers = workerList.getElementsByTagName('li');

    // Remove previous selection
    Array.from(workers).forEach(worker => worker.classList.remove('selected-worker'));

    // Add border highlight to the selected worker
    let clickedWorker = event.target.closest('li');
    if (clickedWorker) {
        clickedWorker.classList.add('selected-worker');
    }
}

function closeAssignWorkerPopup(requestId) {
    document.getElementById(`assignWorkerPopup-${requestId}`).style.display = "none";
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        document.cookie.split(';').forEach(cookie => {
            let trimmed = cookie.trim();
            if (trimmed.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(trimmed.substring(name.length + 1));
            }
        });
    }
    return cookieValue;
}

function confirmWorkerSelection(requestId) {
    const confirmButton = document.getElementById(`confirmWorkerButton-${requestId}`);
    const workerId = confirmButton.getAttribute('data-worker-id');

    console.log(`Assigning worker ID: ${workerId} to request ID: ${requestId}`);

    // Make an AJAX request to assign the worker
    fetch(`/assign_worker/${requestId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Include CSRF token for security
        },
        body: JSON.stringify({ worker_id: workerId })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('Data received:', data);
        if (data.success) {
            // Enable the Approve button
            const approveButton = document.getElementById(`approve-btn-${requestId}`);
            if (approveButton) {
                approveButton.classList.remove('disabled');
                approveButton.removeAttribute('disabled');
                approveButton.style.cursor = 'pointer'; // Change cursor to pointer
            }
            // Removed the alert here
        } else {
            alert(data.message); // Optional: Keep this for error messages
        }
    })
    .catch(error => {
        console.error("Error assigning worker:", error);
        alert("An error occurred while assigning the worker. Please try again.");
    });

    // Close the popup after confirming
    closeAssignWorkerPopup(requestId);
}