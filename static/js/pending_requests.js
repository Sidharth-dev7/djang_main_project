// pending_requests.js

document.addEventListener("DOMContentLoaded", function() {
    const workerItems = document.querySelectorAll('.popup-content li');

    workerItems.forEach(item => {
        item.addEventListener('click', function() {
            // Check if the worker is available
            if (item.classList.contains('worker-available')) {
                // Highlight the selected worker
                item.classList.add('selected-worker');
                item.classList.remove('worker-available');
                item.classList.add('worker-available-selected');
                
                // Enable the confirm button
                document.getElementById('confirmButton').disabled = false;
            } else {
                // If the worker is not available, do not enable the Confirm button
                document.getElementById('confirmButton').disabled = true;
            }
        });
    });
});

function openAssignWorkerPopup(requestId) {
    // Sample data for testing workers (Assuming this data comes from your backend)
    const testData = {
        success: true,
        workers: [
            { id: 1, name: "Worker 1", status: 'worker-available' },  // Available worker
            { id: 2, name: "Worker 2", status: 'worker-busy' },       // Busy worker
            { id: 3, name: "Worker 3", status: 'worker-unavailable' }  // Unavailable worker
        ]
    };

    const workerList = document.getElementById(`worker-list-${requestId}`);
    workerList.innerHTML = '';  // Clear previous list

    if (testData.success) {
        testData.workers.forEach(worker => {
            const li = document.createElement('li');
            li.textContent = worker.name;

            // Add color coding based on status
            if (worker.status === 'worker-available') {
                li.classList.add('worker-available');
            } else if (worker.status === 'worker-busy') {
                li.classList.add('worker-busy');
            } else if (worker.status === 'worker-unavailable') {
                li.classList.add('worker-unavailable');
            }

            // Add click handler
            li.onclick = (event) => selectWorker(worker.id, requestId, event);
            workerList.appendChild(li);
        });
    } else {
        const li = document.createElement('li');
        li.textContent = testData.message;
        workerList.appendChild(li);
    }

    document.getElementById(`assignWorkerPopup-${requestId}`).style.display = "block";
}

function selectWorker(workerId, requestId, event) {
    // Disable the Confirm button initially
    let confirmButton = document.getElementById(`confirmWorkerButton-${requestId}`);
    confirmButton.disabled = true;  // Disable Confirm button initially

    let workerList = document.getElementById(`worker-list-${requestId}`);
    let workers = workerList.getElementsByTagName('li');

    // Remove selected state from all workers
    Array.from(workers).forEach(worker => worker.classList.remove('selected-worker'));

    // Ensure we target the correct element (li) and highlight it only if it is available
    let clickedWorker = event.target.closest('li');
    if (clickedWorker && clickedWorker.classList.contains('worker-available')) {
        clickedWorker.classList.add('selected-worker');  // Highlight the worker
        confirmButton.disabled = false;  // Enable Confirm button when an available worker is selected
    }
}

function confirmWorkerSelection(requestId) {
    // Get the selected worker ID
    const workerId = document.getElementById(`confirmWorkerButton-${requestId}`).getAttribute('data-worker-id');

    // Perform any further actions for worker selection confirmation here
    // After the worker is confirmed, turn the Approve button green

    // Example: Change the Approve button color to green
    let approveButton = document.getElementById(`approve-btn-${requestId}`);
    approveButton.classList.remove('disabled');
    approveButton.classList.add('enabled');
    approveButton.style.backgroundColor = "#28a745";  // Turn green

    // Close the popup after confirmation
    closeAssignWorkerPopup(requestId);
}

function closeAssignWorkerPopup(requestId) {
    // Hide the specific popup based on requestId
    document.getElementById(`assignWorkerPopup-${requestId}`).style.display = "none";
}

// Function to get CSRF token
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

