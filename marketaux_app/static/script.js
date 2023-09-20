console.log("Script loaded and executed");
document.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById('stock-form').addEventListener('submit', function(event) {
        event.preventDefault();  // Prevent the form from submitting normally
    
        let symbolValue = document.getElementById('symbol').value;
    
        fetch('/sentiment/?symbol=' + symbolValue)
            .then(response => response.json())
            .then(data => {
                // Assuming the JSON returned looks like: {"result": "Positive"}
                let resultElement = document.getElementById('result');
                if (resultElement) {
                    resultElement.innerText = data.average_sentiment;
                    resultElement.style.display = 'block';
                } else {
                    console.error('Element with ID "result" not found.');
                }
            })
            .catch(error => {
                console.error('There was an error fetching sentiment:', error);
            });
    });
});





