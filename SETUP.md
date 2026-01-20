# Quick Setup Guide

## Getting Started with Stock Data Explorer

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Your API Key

**Option A: Using .env file (RECOMMENDED)**

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your favorite editor
nano .env
# or
vim .env
# or
code .env
```

Add your API key to the `.env` file:
```
MASSIVE_API_KEY=your_actual_api_key_here
```

**Option B: Using environment variable**

```bash
# Temporary (current session only)
export MASSIVE_API_KEY="your_actual_api_key_here"

# Permanent (add to ~/.bashrc or ~/.zshrc)
echo 'export MASSIVE_API_KEY="your_actual_api_key_here"' >> ~/.zshrc
source ~/.zshrc
```

### 3. Run Tests

```bash
# Run all tests
pytest -v

# Should see: 24 passed
```

### 4. Start the Application

```bash
streamlit run stock_explorer.py
```

The app will open at `http://localhost:8501`

## What You'll See

### Stage 1: Mock Data (Always Works)
- Select a stock ticker from the dropdown
- See two dot plots: "High Prices" and "Low Prices"
- Mock data is deterministic (same ticker = same data)

### Stage 2: Real API Data (Requires API Key)
- Below the mock plots, you'll see "Stage 2: Real-Time API Data"
- **Without API key**: Warning message with setup instructions
- **With valid API key**: Raw JSON data from the Massive API
- Rate limit: 12 seconds between API calls

## Troubleshooting

### "API key not configured" warning
- Check that your `.env` file exists and contains `MASSIVE_API_KEY=...`
- Make sure the API key is not `YOUR_API_KEY_HERE`
- Restart the Streamlit app after changing `.env`

### Tests failing
```bash
# Check Python version (need 3.8+)
python3 --version

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Run tests with verbose output
pytest -v -s
```

### Import errors
```bash
# Make sure you're in the project directory
pwd

# Check that all files exist
ls -la

# Should see: stock_explorer.py, .env, .env.example, etc.
```

## Security Reminders

✅ **DO:**
- Keep your `.env` file private
- Use `.env.example` as a template for team members
- Add `.env` to `.gitignore` (already done)

❌ **DON'T:**
- Commit `.env` to version control
- Share your API key publicly
- Hardcode API keys in source code

## Next Steps

- **Stage 3**: Process API data and integrate with visualizations
- Add more stock tickers
- Implement data caching
- Add more visualization types

## Getting Help

- Check the main [README.md](README.md) for detailed documentation
- Review the spec documents in `.kiro/specs/stock-data-explorer/`
- Run tests to verify your setup: `pytest -v`
