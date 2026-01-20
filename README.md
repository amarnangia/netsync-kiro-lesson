# Stock Data Explorer

A Streamlit web application for visualizing stock price data through interactive dot plots.

## Features

- Select from 20 predefined stock tickers
- Searchable dropdown for easy stock selection
- Interactive dot plots showing high and low prices
- Mock data generation (no external API calls required)
- Deterministic data based on ticker symbol

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Start the Streamlit app:
```bash
streamlit run stock_explorer.py
```

The application will open in your default web browser at `http://localhost:8501`

## Running Tests

Run all tests:
```bash
pytest test_stock_explorer.py -v
```

Run specific test:
```bash
pytest test_stock_explorer.py::test_name -v
```

## Project Structure

- `stock_explorer.py` - Main Streamlit application
- `test_stock_explorer.py` - Test suite with unit and property-based tests
- `requirements.txt` - Python dependencies
- `.kiro/specs/stock-data-explorer/` - Specification documents
  - `requirements.md` - Feature requirements
  - `design.md` - Design document
  - `tasks.md` - Implementation tasks

## Usage

1. Launch the application
2. Use the dropdown to select a stock ticker
3. View the high and low price dot plots
4. Select different stocks to see different price patterns

## Technical Details

- Built with Streamlit for the web interface
- Uses deterministic random data generation (same ticker = same data)
- Implements property-based testing with Hypothesis
- All prices maintain the invariant: high_price >= low_price
- Data is cached for performance

## Testing

The application includes comprehensive testing:
- 4 property-based tests (100 iterations each)
- 3 unit tests
- Tests verify data generation, price invariants, and UI structure
