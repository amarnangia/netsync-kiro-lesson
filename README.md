# Stock Data Explorer

A Streamlit web application for visualizing stock price data through interactive dot plots and fetching real historical data from external APIs.

## Features

### Stage 1 (Completed)
- Select from 20 predefined stock tickers
- Searchable dropdown for easy stock selection
- Interactive dot plots showing high and low prices
- Mock data generation with deterministic patterns

### Stage 2 (Current)
- Fetch real historical stock data from Massive stock market API
- Display raw API responses in formatted JSON
- Rate limiting (5 calls per minute)
- Comprehensive error handling
- Secure API key management with `.env` file

### Stage 3 (Future)
- Process and transform API data
- Integrate real data with visualizations

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure your API key (choose one method):

   **Method 1 (RECOMMENDED): Use .env file**
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env and add your API key
   # MASSIVE_API_KEY=your_actual_api_key_here
   ```

   **Method 2: Set environment variable**
   ```bash
   export MASSIVE_API_KEY="your_actual_api_key_here"
   ```

   **Method 3: Edit source code** (not recommended)
   - Open `stock_explorer.py`
   - Find line with `API_KEY = os.getenv(...)`
   - Replace `"YOUR_API_KEY_HERE"` with your actual key
   - ⚠️ Never commit your actual API key to version control!

## Running the Application

Start the Streamlit app:
```bash
streamlit run stock_explorer.py
```

The application will open in your default web browser at `http://localhost:8501`

## Running Tests

Run all tests:
```bash
# Run main application tests
pytest test_stock_explorer.py -v

# Run environment configuration tests
pytest test_env_loading.py -v

# Run all tests
pytest -v
```

Run specific test:
```bash
pytest test_stock_explorer.py::test_name -v
```

## Project Structure

- `stock_explorer.py` - Main Streamlit application
- `test_stock_explorer.py` - Test suite with unit and property-based tests
- `test_env_loading.py` - Environment configuration tests
- `requirements.txt` - Python dependencies
- `.env` - Your API key (DO NOT COMMIT - in .gitignore)
- `.env.example` - Template for .env file
- `.gitignore` - Protects sensitive files from version control
- `.kiro/specs/stock-data-explorer/` - Specification documents
  - `requirements.md` - Feature requirements
  - `design.md` - Design document
  - `tasks.md` - Implementation tasks

## Usage

### Stage 1: Mock Data Visualization
1. Launch the application
2. Use the dropdown to select a stock ticker
3. View the high and low price dot plots
4. Select different stocks to see different price patterns

### Stage 2: Real API Data
1. Configure your API key (see Installation section)
2. Select a stock ticker
3. View Stage 1 mock data plots (top section)
4. View Stage 2 raw API data (bottom section)
5. Rate limiting: Wait 12 seconds between API calls

**Note:** Without a valid API key, you'll see a warning message. Stage 1 mock data will still work.

## Security

- **Never commit your `.env` file** - it's protected by `.gitignore`
- **Never commit API keys** to version control
- Use `.env.example` as a template for team members
- The `.env` file is automatically loaded by the application

## Technical Details

### Stage 1
- Built with Streamlit for the web interface
- Uses deterministic random data generation (same ticker = same data)
- Implements property-based testing with Hypothesis
- All prices maintain the invariant: high_price >= low_price
- Data is cached for performance

### Stage 2
- Fetches up to 2 years of historical data
- Rate limiting: 5 calls per minute (12-second minimum between calls)
- Error handling for connection, timeout, auth, and empty responses
- Raw JSON display in expandable section
- Maintains strict separation from Stage 1 mock data

## Testing

The application includes comprehensive testing:

### Stage 1 Tests
- 4 property-based tests (100 iterations each)
- 3 unit tests
- Tests verify data generation, price invariants, and UI structure

### Stage 2 Tests
- 2 property-based tests (rate limiting, stage separation)
- 8 unit tests (API fetcher, error handling, display functions)
- 6 environment configuration tests

**Total: 18 application tests + 6 environment tests = 24 tests**
