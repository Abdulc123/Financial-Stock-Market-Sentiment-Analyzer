let stock_dict = {};

// Show the loading spinner and hide the content container
function showLoading() {
    document.getElementById('loading').style.display = 'block';
    const contentContainer = document.querySelector('.content-container');
    contentContainer.style.opacity = 0; // Make content invisible
    contentContainer.style.display = 'none'; // Hide content from the flow
}

// Hide the loading spinner and fade in the content container
function hideLoading() {
    document.getElementById('loading').style.display = 'none';
    const contentContainer = document.querySelector('.content-container');
    
    // First set it to display flex so that it's visible
    contentContainer.style.display = 'flex';

    // Give the browser a small delay to render the container before applying the opacity change
    setTimeout(() => {
        contentContainer.style.transition = 'opacity 1s ease'; // Apply fade-in transition
        contentContainer.style.opacity = 1; // Start the fade-in
    }, 10); // Short delay to trigger the transition
}

// Load the stock dictionary
async function loadStockDictionary() {
    try {
        const response = await fetch('/static/stock_dict.json'); // Adjust the path as needed
        stock_dict = await response.json();
        console.log("Stock dictionary loaded:", stock_dict);
    } catch (error) {
        console.error("ERROR: Error loading stock dictionary", error);
    }
}

// Function to filter stock_dict based on user input
function autocompleteSearch(input) {
    const inputVal = input.value.toLowerCase();
    const suggestions = Object.entries(stock_dict).filter(([ticker, name]) => {
        return ticker.toLowerCase().startsWith(inputVal) || name.toLowerCase().includes(inputVal);
    });

    // Display suggestions in the autocomplete list
    displaySuggestions(input, suggestions);
}

// Display the filtered suggestions under the input field
function displaySuggestions(input, suggestions) {
    const list = document.getElementById('autocomplete-list');
    list.innerHTML = '';  // Clear previous suggestions

    suggestions.forEach(([ticker, name]) => {
        const option = document.createElement('li');
        option.classList.add('autocomplete-item');
        option.innerHTML = `<strong>${ticker}</strong> - ${name}`;
        
        option.addEventListener('click', function() {
            // Set input value to ticker when clicked
            input.value = ticker;
            list.innerHTML = '';  // Clear the list after selection

            // Trigger form submission programmatically
            document.getElementById('stockForm').dispatchEvent(new Event('submit'));
        });

        list.appendChild(option);
    });

    if (suggestions.length === 0) {
        const noResult = document.createElement('li');
        noResult.classList.add('autocomplete-item');
        noResult.textContent = 'No results found';
        list.appendChild(noResult);
    }
}

// Fetch and display stock data
function fetchStockData(ticker) {
    showLoading('left-loading'); // Show loading spinner when data is being fetched (for the left container)

    // Fetch stock data from the backend
    fetch('/analyze_stock', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ ticker })
    })
    .then(response => {
        // Check if the response is okay, if not, throw an error
        if (!response.ok) {
            throw new Error(`Error: Failed to fetch stock data for ${ticker}. Please check the ticker symbol.`);
        }
        return response.json();
    })
    .then(data => {
        hideLoading(); // Hide loading spinner after the data is fetched
        
        // Check if data contains valid stock info
        if (data.error || Object.keys(data).length === 0) {
            // If no valid data, display an error message
            displayErrorMessage(`No data found for ticker: ${ticker}. Please enter a valid ticker symbol.`);
        } else {
            // Otherwise, display the stock data on the page
            displayStockData(data);
        }
    })
    .catch(error => {
        hideLoading(); // Hide loading spinner after the data is fetched
        console.error('Error fetching stock data:', error);
        displayErrorMessage(`Error fetching stock data: ${error.message}`);
    });
}

// Display error message to the user
function displayErrorMessage(message) {
    const resultContainer = document.getElementById('resultData');
    resultContainer.innerHTML = `<div class="error-message">${message}</div>`;
}

// Display the stock data in a table
function displayStockData(data) {
    const parameters = [
        { name: "Ticker", value: data.ticker },
        { name: "Current Price", value: `$${data.current_price.toFixed(2)}` },
        { name: "Open Price", value: `$${data.open_price.toFixed(2)}` },
        { name: "High Price", value: `$${data.high_price.toFixed(2)}` },
        { name: "Low Price", value: `$${data.low_price.toFixed(2)}` },
        { name: "Volume", value: data.volume.toLocaleString() },
        { name: "Market Cap", value: `$${data.market_cap.toLocaleString()}` },
        { name: "P/E Ratio", value: data.pe_ratio.toFixed(2) },
        { name: "EPS", value: `$${data.eps.toFixed(2)}` },
        { name: "Dividend Yield", value: `${data.dividend_yield.toFixed(2)}%` },
        { name: "Year High", value: `$${data.year_high.toFixed(2)}` },
        { name: "Year Low", value: `$${data.year_low.toFixed(2)}` },
    ];

    // Generate table rows dynamically
    const rows = parameters.map(param => `
        <tr>
            <td>${param.name}</td>
            <td>${param.value}</td>
        </tr>
    `).join('');

    // Display results in a table
    document.getElementById('resultData').innerHTML = `
    <table class="table table-bordered">
        <thead>
            <tr>
                <th>Parameter</th>
                <th>Value</th>
            </tr>
        </thead>
        <tbody>
            ${rows}
        </tbody>
    </table>
    `;

    // Display the JSON data in the toggle container but keep it hidden initially
    const jsonData = JSON.stringify(data, null, 2);
    document.getElementById('jsonData').textContent = jsonData;
}

// Initialize the stock dictionary and set up event listeners
window.onload = function () {
    loadStockDictionary();

    const tickerInput = document.getElementById('ticker');
    tickerInput.addEventListener('input', function () {
        autocompleteSearch(this);
    });

    const form = document.getElementById('stockForm');
    form.addEventListener('submit', function (e) {
        e.preventDefault();
        const ticker = tickerInput.value;
        fetchStockData(ticker); // Fetch data when the form is submitted
    });
};
