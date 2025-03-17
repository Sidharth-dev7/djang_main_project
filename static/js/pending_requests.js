// pending_requests.js

document.addEventListener("DOMContentLoaded", function() {
    const workerItems = document.querySelectorAll('.popup-content li');

    workerItems.forEach(item => {
        item.addEventListener('click', function() {
            if (item.classList.contains('worker-available')) {
                // Remove existing selections
                document.querySelectorAll('.selected-worker').forEach(el => {
                    el.classList.remove('selected-worker');
                });

                // Highlight the selected worker
                item.classList.add('selected-worker');
                
                // Enable the confirm button
                let confirmButton = document.getElementById('confirmWorkerButton');
                if (confirmButton) {
                    confirmButton.disabled = false;
                }
            }
        });
    });
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



function selectWorker(workerId, requestId, event) {
    let confirmButton = document.getElementById(`confirmWorkerButton-${requestId}`);
    confirmButton.disabled = false;  
    confirmButton.setAttribute('data-worker-id', workerId);

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
