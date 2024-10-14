document.getElementById('stockForm').addEventListener('submit', function (e) {
    e.preventDefault(); // Prevent the form from submitting normally

    const ticker = this.ticker.value;

    fetch('/analyze_stock', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ ticker })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').innerText = data.message;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('result').innerText = 'An error occurred.';
    });
});
