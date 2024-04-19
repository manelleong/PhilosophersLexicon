document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('generate-graph').addEventListener('click', function() {
        let selectedPhilosophers = getSelectedPhilosophers();
        fetchGraphData(selectedPhilosophers);
    });
});

function getSelectedPhilosophers() {
    let checkboxes = document.querySelectorAll('input[name="philosopher"]:checked');
    let selected = [];
    checkboxes.forEach((checkbox) => {
        selected.push(checkbox.value);
    });
    return selected;
}

function fetchGraphData(selectedPhilosophers) {
    // Here, make an AJAX call to your Flask server with the selectedPhilosophers
    // For example:
    fetch('/get-topics', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ philosophers: selectedPhilosophers }),
    })
    .then(response => response.json())
    .then(data => {
        displayGraph(data); // Function to handle the display of the graph
    })
    .catch(error => console.error('Error fetching topics:', error));
}

function displayGraph(graphData) {
    // Assuming 'graphData' contains the HTML for the graph
    document.getElementById('graph-container').innerHTML = graphData;
}
