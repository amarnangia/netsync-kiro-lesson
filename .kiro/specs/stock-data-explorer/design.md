# Design Document: Stock Data Explorer

## Overview

The Stock Data Explorer is a Streamlit-based web application that provides an interactive interface for visualizing stock price data. The application uses a simple architecture with mock data generation to establish the UI foundation for future enhancements. The design focuses on clean separation between UI components, data generation, and visualization logic.

## Architecture

The application follows a single-file Streamlit architecture with functional decomposition:

```
┌─────────────────────────────────────┐
│     Streamlit Application           │
│                                     │
│  ┌──────────────────────────────┐  │
│  │   UI Layer                   │  │
│  │  - Title                     │  │
│  │  - Stock Selector            │  │
│  │  - Plot Containers           │  │
│  └──────────────────────────────┘  │
│              │                      │
│              ▼                      │
│  ┌──────────────────────────────┐  │
│  │   Data Generation Layer      │  │
│  │  - Mock Data Generator       │  │
│  └──────────────────────────────┘  │
│              │                      │
│              ▼                      │
│  ┌──────────────────────────────┐  │
│  │   Visualization Layer        │  │
│  │  - Dot Plot Renderer         │  │
│  └──────────────────────────────┘  │
└─────────────────────────────────────┘
```

The application uses Streamlit's reactive model where user interactions trigger automatic re-execution of the script, updating the UI accordingly.

## Components and Interfaces

### 1. Stock Ticker List

A hardcoded list of 20 stock tickers representing major companies:

```python
STOCK_TICKERS = [
    "AAPL", "GOOGL", "MSFT", "AMZN", "TSLA",
    "META", "NVDA", "JPM", "V", "WMT",
    "JNJ", "PG", "MA", "HD", "DIS",
    "BAC", "NFLX", "ADBE", "CRM", "INTC"
]
```

### 2. Stock Selector Component

Uses Streamlit's `st.selectbox()` with built-in search functionality:

```python
selected_stock = st.selectbox(
    "Select a stock ticker:",
    options=STOCK_TICKERS,
    index=0
)
```

The selectbox provides:
- Searchable dropdown (native Streamlit feature)
- Clear visual feedback of selected stock
- Automatic re-rendering on selection change

### 3. Mock Data Generator

Function signature:
```python
def generate_mock_stock_data(ticker: str, num_points: int = 30) -> tuple[list[int], list[float], list[float]]
```

**Parameters:**
- `ticker`: Stock ticker symbol (used as seed for reproducibility)
- `num_points`: Number of data points to generate (default: 30)

**Returns:**
- Tuple of (days, high_prices, low_prices)
- `days`: List of integers representing day numbers (1 to num_points)
- `high_prices`: List of floats representing daily high prices
- `low_prices`: List of floats representing daily low prices

**Implementation approach:**
- Use ticker string as seed for random number generator (ensures same stock shows same data)
- Generate base price around a realistic range ($50-$500)
- Add random variations to simulate price movements
- Ensure high prices are always greater than or equal to low prices
- Generate realistic-looking price patterns with some volatility

### 4. Visualization Component

Uses Streamlit's native plotting capabilities (st.scatter_chart or matplotlib):

```python
def display_dot_plots(days: list[int], high_prices: list[float], low_prices: list[float]):
    # Display high prices dot plot
    st.subheader("High Prices")
    # Render scatter plot
    
    # Display low prices dot plot
    st.subheader("Low Prices")
    # Render scatter plot
```

The visualization will use:
- X-axis: Day number (1 to num_points)
- Y-axis: Price value
- Dots representing individual price points
- Clear axis labels and appropriate scaling

## Data Models

### StockData (Conceptual)

While not implemented as a class, the data structure represents:

```python
{
    "ticker": str,           # Stock ticker symbol
    "days": list[int],       # Day numbers [1, 2, 3, ...]
    "high_prices": list[float],  # Daily high prices
    "low_prices": list[float]    # Daily low prices
}
```

**Invariants:**
- `len(days) == len(high_prices) == len(low_prices)`
- `high_prices[i] >= low_prices[i]` for all i
- All prices are positive values

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Data Generation Completeness

*For any* stock ticker from the predefined list, the mock data generator should produce three lists (days, high_prices, low_prices) of equal length with all positive values.

**Validates: Requirements 3.1, 3.2**

### Property 2: Price Invariant

*For any* generated mock data, the high price should be greater than or equal to the low price for every data point (high_prices[i] >= low_prices[i] for all i).

**Validates: Requirements 3.1, 3.2**

### Property 3: Deterministic Data Generation

*For any* stock ticker, generating mock data multiple times should produce identical results each time (same ticker = same data).

**Validates: Requirements 1.4, 3.5**

### Property 4: Stock Selection Triggers Data Generation

*For any* stock ticker in the predefined list, selecting it should trigger the generation of new mock data specific to that ticker.

**Validates: Requirements 1.4, 3.5**

## Error Handling

### Input Validation

Since the stock selector uses a predefined list, invalid inputs are prevented by design. No additional validation needed.

### Data Generation Errors

- If random number generation fails, use fallback linear data
- Ensure all generated lists have equal length
- Validate that high >= low for all points before returning

### Visualization Errors

- If plotting fails, display error message to user
- Provide fallback text representation of data
- Log errors for debugging purposes

## Testing Strategy

### Unit Tests

1. **Test Mock Data Generator**
   - Verify correct number of data points generated
   - Verify high prices >= low prices
   - Verify deterministic output for same ticker
   - Test edge cases (empty ticker, special characters)

2. **Test Data Structure**
   - Verify list lengths match
   - Verify all prices are positive
   - Verify data types are correct

### Property-Based Tests

Property-based tests will use Hypothesis (Python PBT library) with minimum 100 iterations per test.

1. **Property Test: Data Invariants**
   - **Feature: stock-data-explorer, Property 2: Data Consistency**
   - Generate random tickers and verify high >= low for all points
   - Verify all prices are positive
   - Verify equal list lengths

2. **Property Test: Deterministic Generation**
   - **Feature: stock-data-explorer, Property 3: Data Reproducibility**
   - Generate data for same ticker multiple times
   - Verify identical output each time

3. **Property Test: Valid Output Structure**
   - **Feature: stock-data-explorer, Property 2: Data Consistency**
   - For any valid ticker, verify output is tuple of three lists
   - Verify all elements are correct types

### Integration Tests

1. **Test Stock Selection Flow**
   - Simulate selecting different stocks
   - Verify plots update correctly
   - Verify no errors occur during selection changes

2. **Test UI Rendering**
   - Verify all UI components render without errors
   - Verify correct labels and titles appear
   - Verify plots display data correctly

### Manual Testing

1. Run application and verify visual appearance
2. Test searchable dropdown functionality
3. Verify smooth transitions between stock selections
4. Check responsive behavior and layout

## Implementation Notes

- Use Streamlit version 1.x or higher
- Leverage Streamlit's caching (`@st.cache_data`) for data generation to improve performance
- Use matplotlib or Streamlit's native charting for dot plots
- Keep all code in a single `app.py` or `stock_explorer.py` file
- Add inline comments for clarity
- Use type hints for better code documentation
