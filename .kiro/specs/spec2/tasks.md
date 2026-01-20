# Implementation Plan: Stock Data Explorer

## Overview

This implementation plan breaks down the Stock Data Explorer Streamlit application into discrete coding tasks. The approach follows a bottom-up strategy: first implementing core data generation logic with tests, then building the UI layer, and finally integrating all components.

## Tasks

- [x] 1. Set up project structure and dependencies
  - Create main application file `stock_explorer.py`
  - Create `requirements.txt` with Streamlit and testing dependencies
  - Add inline comments documenting the file structure
  - _Requirements: 5.4_

- [x] 2. Implement mock data generator
  - [x] 2.1 Create `generate_mock_stock_data()` function
    - Accept ticker symbol and number of points as parameters
    - Use ticker as seed for random number generator (for determinism)
    - Generate base price in realistic range ($50-$500)
    - Generate days list (1 to num_points)
    - Generate high prices with random variations
    - Generate low prices ensuring low <= high for all points
    - Return tuple of (days, high_prices, low_prices)
    - Add type hints and docstring
    - _Requirements: 3.1, 3.2, 3.4_

  - [x] 2.2 Write property test for data generation completeness
    - **Property 1: Data Generation Completeness**
    - **Validates: Requirements 3.1, 3.2**
    - Test that for any ticker, three lists of equal length are returned
    - Test that all prices are positive values
    - Configure test to run 100 iterations

  - [x] 2.3 Write property test for price invariant
    - **Property 2: Price Invariant**
    - **Validates: Requirements 3.1, 3.2**
    - Test that high_prices[i] >= low_prices[i] for all i
    - Test across multiple random tickers
    - Configure test to run 100 iterations

  - [x] 2.4 Write property test for deterministic generation
    - **Property 3: Deterministic Data Generation**
    - **Validates: Requirements 1.4, 3.5**
    - Test that same ticker produces identical data across multiple calls
    - Test with various ticker strings
    - Configure test to run 100 iterations

- [x] 3. Implement stock ticker list
  - [x] 3.1 Create hardcoded list of 20 stock tickers
    - Define STOCK_TICKERS constant with 20 major company symbols
    - Add comment explaining the list purpose
    - _Requirements: 1.1_

  - [x] 3.2 Write unit test for ticker list
    - Verify list contains exactly 20 tickers
    - Verify all tickers are non-empty strings
    - _Requirements: 1.1_

- [x] 4. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 5. Build UI components
  - [x] 5.1 Create application title
    - Use `st.title()` to display "Stock Data Explorer"
    - _Requirements: 2.1_

  - [x] 5.2 Create stock selector component
    - Use `st.selectbox()` with STOCK_TICKERS as options
    - Set default selection to first ticker
    - Add label "Select a stock ticker:"
    - Store selected value in variable
    - _Requirements: 1.2, 1.4_

  - [x] 5.3 Add caching decorator to data generator
    - Apply `@st.cache_data` to `generate_mock_stock_data()`
    - Improve performance by caching generated data
    - _Requirements: 3.1, 3.2_

- [x] 6. Implement visualization components
  - [x] 6.1 Create dot plot display function
    - Accept days, high_prices, and low_prices as parameters
    - Use matplotlib or Streamlit's scatter_chart for dot plots
    - Create first plot with "High Prices" subheader
    - Create second plot with "Low Prices" subheader
    - Set appropriate axis labels (Day, Price)
    - Ensure plots are visually clear with proper scaling
    - _Requirements: 2.3, 2.4, 2.5, 3.3, 3.4_

  - [x] 6.2 Write unit test for plot data structure
    - Test that plot function accepts correct data types
    - Test that function handles edge cases (empty data, single point)
    - _Requirements: 3.3, 3.4_

- [x] 7. Integrate components and wire application flow
  - [x] 7.1 Connect stock selector to data generation
    - Call `generate_mock_stock_data()` with selected ticker
    - Pass generated data to visualization function
    - Ensure plots update when selection changes
    - _Requirements: 1.4, 3.5_

  - [x] 7.2 Add conditional rendering
    - Display plots only after a stock is selected
    - Add helpful message if no stock selected (edge case)
    - _Requirements: 2.2, 2.3_

  - [x] 7.3 Write property test for selection triggering data generation
    - **Property 4: Stock Selection Triggers Data Generation**
    - **Validates: Requirements 1.4, 3.5**
    - Test that selecting any ticker generates new data
    - Test that data is specific to the selected ticker
    - Configure test to run 100 iterations

- [x] 8. Final polish and documentation
  - [x] 8.1 Add inline comments throughout code
    - Comment each major section (imports, constants, functions, main app)
    - Explain key logic decisions
    - Document function parameters and return values
    - _Requirements: 5.1, 5.2_

  - [x] 8.2 Verify code organization
    - Ensure logical flow: imports → constants → functions → main app
    - Use clear variable names throughout
    - Remove any unused code or imports
    - _Requirements: 5.2, 5.3_

- [x] 9. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Stage 2 Tasks: API Integration

- [-] 10. Set up API configuration and dependencies
  - [ ] 10.1 Add requests library to requirements.txt
    - Add `requests` package for HTTP API calls
    - _Requirements: 6.1_

  - [ ] 10.2 Create API configuration section
    - Define API_KEY constant with placeholder "YOUR_API_KEY_HERE"
    - Add environment variable fallback using `os.getenv("MASSIVE_API_KEY", "YOUR_API_KEY_HERE")`
    - Define API_BASE_URL constant
    - Add clear comments indicating where users should insert their API key
    - _Requirements: 6.3, 6.4, 8.7_

  - [ ] 10.3 Initialize session state for rate limiting
    - Add session state variable for last API call timestamp
    - Initialize to None on first run
    - _Requirements: 6.5_

- [ ] 11. Implement API fetcher with rate limiting
  - [ ] 11.1 Create fetch_stock_data() function
    - Accept ticker and api_key as parameters
    - Check if API key is placeholder value and return error if so
    - Implement rate limiting: check if 12 seconds have passed since last call
    - If rate limit not met, display waiting message and return None
    - Build API request URL with ticker and 2-year date range parameters
    - Make HTTP GET request with timeout (10 seconds)
    - Handle connection errors, timeouts, HTTP errors
    - Update last API call timestamp in session state
    - Return raw JSON response as dictionary or None on error
    - Add type hints and docstring
    - Add comment: "TODO Stage 3: Process and transform this data"
    - _Requirements: 6.1, 6.2, 6.5, 8.5_

  - [ ] 11.2 Write unit test for API fetcher with mock responses
    - Test successful API call returns dictionary
    - Test connection error returns None
    - Test timeout returns None
    - Test empty response handling
    - Test placeholder API key detection
    - _Requirements: 6.1, 6.7, 6.8_

  - [ ] 11.3 Write unit test for rate limiting
    - Test that rapid calls are delayed
    - Test timestamp tracking in session state
    - Verify minimum 12-second delay enforced
    - _Requirements: 6.5_

  - [ ] 11.4 Write property test for rate limit enforcement
    - **Property 5: Rate Limit Enforcement**
    - **Validates: Requirements 6.5**
    - Simulate sequence of API calls
    - Verify time between consecutive successful calls >= 12 seconds
    - Configure test to run 100 iterations

- [ ] 12. Implement raw API data display
  - [ ] 12.1 Create display_raw_api_data() function
    - Accept api_response dictionary as parameter
    - Use st.expander() with label "Raw API Data (Stage 2)"
    - Inside expander, use st.json() to display formatted response
    - Add type hints and docstring
    - _Requirements: 7.1, 7.2, 7.3, 7.4_

  - [ ] 12.2 Create display_api_error() function
    - Accept error_type and message as parameters
    - Use st.error() for connection/auth failures
    - Use st.warning() for rate limit messages
    - Use st.info() for empty responses
    - Add type hints and docstring
    - _Requirements: 6.6, 6.7, 6.8_

  - [ ] 12.3 Write unit tests for display functions
    - Test raw data display with sample JSON
    - Test error display for each error type
    - Verify correct Streamlit components used
    - _Requirements: 7.1, 7.2, 7.3_

- [ ] 13. Checkpoint - Ensure all Stage 2 tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 14. Integrate API fetcher into main application
  - [ ] 14.1 Add API data fetching to main flow
    - After stock selection, add section divider or spacing
    - Add subheader "Stage 2: Real-Time API Data"
    - Check if API key is configured (not placeholder)
    - If not configured, display warning with st.warning()
    - If configured, use st.spinner() with "Fetching data from API..."
    - Call fetch_stock_data() with selected ticker
    - If successful, call display_raw_api_data()
    - If failed, call display_api_error() with appropriate message
    - Add comment: "TODO Stage 3: Connect API data to visualizations"
    - _Requirements: 6.1, 6.6, 7.4, 8.6_

  - [ ] 14.2 Verify Stage 1 remains unchanged
    - Ensure mock data plots still appear above API section
    - Verify mock data generation still uses same logic
    - Verify no data mixing between stages
    - _Requirements: 8.1, 8.2, 8.3, 8.4_

  - [ ] 14.3 Write property test for stage separation
    - **Property 6: Stage Separation Invariant**
    - **Validates: Requirements 8.1, 8.2, 8.3, 8.4**
    - For various stock selections, verify mock data plots use generated data
    - Verify API data (if fetched) is displayed separately
    - Verify no connection between Stage 1 plots and Stage 2 API data
    - Configure test to run 100 iterations

- [ ] 15. Add comprehensive error handling and edge cases
  - [ ] 15.1 Add API key validation
    - Check for placeholder value before making requests
    - Display clear message: "Please configure your API key"
    - Provide instructions on how to set environment variable
    - _Requirements: 6.3, 6.4_

  - [ ] 15.2 Add rate limit user feedback
    - Calculate and display seconds remaining until next call allowed
    - Show countdown or wait time message
    - _Requirements: 6.5_

  - [ ] 15.3 Test all error paths
    - Test with missing API key
    - Test with invalid API key
    - Test with network disconnected (if possible)
    - Test rapid stock selections (rate limiting)
    - _Requirements: 6.7, 6.8_

- [ ] 16. Final documentation and code cleanup
  - [ ] 16.1 Add inline comments for Stage 2
    - Comment API configuration section
    - Comment rate limiting logic
    - Comment error handling sections
    - Add TODO comments for Stage 3 integration points
    - _Requirements: 5.1, 8.6, 8.7_

  - [ ] 16.2 Update module docstring
    - Add Stage 2 description to file header
    - Document API requirements and configuration
    - _Requirements: 5.1_

  - [ ] 16.3 Verify code organization
    - Ensure logical flow: Stage 1 code → Stage 2 code → main app
    - Verify clear separation between stages
    - Remove any unused imports
    - _Requirements: 5.2, 5.3_

- [ ] 17. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Stage 2 tasks build on completed Stage 1 implementation
- API integration maintains strict separation from Stage 1 mock data
- Rate limiting is enforced to respect API constraints (5 calls/minute = 12 seconds/call)
- Error handling covers all failure modes (connection, auth, rate limit, empty response)
- Code includes clear markers for Stage 3 integration points
- Property tests validate rate limiting and stage separation invariants
- Unit tests cover API fetching, error handling, and display components
