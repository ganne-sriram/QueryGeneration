# QueryGeneration Setup Guide

This guide provides step-by-step instructions for setting up the QueryGeneration project.

## Prerequisites

Before starting, ensure you have:

1. **Python 3.8+** installed
2. **Node.js 18+** and npm installed
3. **MySQL 5.7+** or **8.0+** installed and running
4. **Google API Key** for Gemini (get from https://makersuite.google.com/app/apikey)
5. **MockData repository** cloned with CSV files exported

## Step-by-Step Setup

### 1. Install MySQL (if not already installed)

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install mysql-server
sudo systemctl start mysql
sudo systemctl enable mysql
```

**macOS:**
```bash
brew install mysql
brew services start mysql
```

**Windows:**
Download and install from https://dev.mysql.com/downloads/installer/

### 2. Configure MySQL

```bash
# Login to MySQL
mysql -u root -p

# Create database (optional, script will create it)
CREATE DATABASE IF NOT EXISTS citi_db;

# Exit MySQL
exit;
```

### 3. Clone and Setup QueryGeneration

```bash
cd /path/to/QueryGeneration

# Create Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your settings
nano .env  # or use your preferred editor
```

Required settings in `.env`:
```bash
# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=citi_db

# LLM Configuration
GOOGLE_API_KEY=your_google_api_key_here
LLM_MODEL=gemini-2.0-flash

# Data Loading Configuration
CSV_PATH=../MockData/exports/CSV Files
```

**Important**: Update `CSV_PATH` to point to your MockData CSV files location.

### 5. Load CSV Data

```bash
# Run the CSV loader script
python scripts/load_csv.py
```

Expected output:
```
================================================================================
  CSV Loader for citi_db
================================================================================

Configuration:
  Database: citi_db
  Host: localhost:3306
  CSV Path: ../MockData/exports/CSV Files

Step 1: Creating database...
  ✓ Database 'citi_db' ready

Step 2: Connecting to database...
  ✓ Connected to citi_db

Step 3: Loading CSV files...
  Found 11 CSV files
  Loading account_customers... ✓ 500 records
  Loading account_type... ✓ 5 records
  Loading accounts... ✓ 500 records
  Loading banking_transactions... ✓ 5000 records
  Loading branch_employees... ✓ 500 records
  Loading branches... ✓ 500 records
  Loading cc_transactions... ✓ 3000 records
  Loading credit_cards... ✓ 300 records
  Loading customers... ✓ 500 records
  Loading employees... ✓ 500 records
  Loading loan... ✓ 175 records

  ✓ Total records loaded: 10980

Step 4: Verifying tables...
  ✓ Found 11 tables: account_customers, account_type, accounts, ...

================================================================================
  ✓ CSV loading completed successfully!
================================================================================
```

### 6. Extract Schema Artifacts

```bash
# Run the schema extraction script
python scripts/extract_schema.py
```

This generates:
- `artifacts/citi_db_schema.json` - Complete schema metadata
- `artifacts/citi_db_erd.md` - Entity Relationship Diagram

### 7. Install Angular Dependencies

```bash
cd ui
npm install
cd ..
```

### 8. Test the Backend

```bash
# Start the FastAPI server
python nl2sql/server.py
```

The server should start on http://localhost:8000

Test endpoints:
- Health check: http://localhost:8000/api/health
- Schema: http://localhost:8000/api/schema

### 9. Test the Frontend

In a new terminal:

```bash
cd ui
npm start
```

The UI should open at http://localhost:4200

### 10. Run Evaluation (Optional)

```bash
# Run the evaluation suite
python tests/evaluate.py
```

This tests 40 queries and generates `tests/evaluation_results.json`.

## Troubleshooting

### MySQL Connection Issues

**Error**: `Access denied for user 'root'@'localhost'`
- Solution: Update `DB_PASSWORD` in `.env` with correct MySQL password

**Error**: `Can't connect to MySQL server`
- Solution: Ensure MySQL is running: `sudo systemctl status mysql`

### CSV Loading Issues

**Error**: `CSV directory not found`
- Solution: Update `CSV_PATH` in `.env` to correct MockData location
- Verify path: `ls "../MockData/exports/CSV Files"`

**Error**: `No CSV files found`
- Solution: Ensure MockData has been set up and CSVs exported
- Check: `ls -la "../MockData/exports/CSV Files/"`

### Google API Key Issues

**Error**: `Invalid API key`
- Solution: Get a valid key from https://makersuite.google.com/app/apikey
- Update `GOOGLE_API_KEY` in `.env`

### Angular Build Issues

**Error**: `Cannot find module '@angular/...'`
- Solution: Delete `node_modules` and reinstall:
  ```bash
  cd ui
  rm -rf node_modules package-lock.json
  npm install
  ```

### Port Already in Use

**Error**: `Port 8000 already in use`
- Solution: Kill existing process or change port in `nl2sql/server.py`

**Error**: `Port 4200 already in use`
- Solution: Use different port: `ng serve --port 4201`

## Verification Checklist

- [ ] MySQL installed and running
- [ ] Python dependencies installed
- [ ] `.env` file configured with correct values
- [ ] CSV data loaded into citi_db (11 tables)
- [ ] Schema artifacts generated
- [ ] Angular dependencies installed
- [ ] Backend starts without errors
- [ ] Frontend loads in browser
- [ ] Can generate SQL from natural language
- [ ] Schema browser displays tables

## Next Steps

Once setup is complete:

1. **Try Example Queries**:
   - "How many customers are there?"
   - "What is the total balance of all accounts?"
   - "List all customers from California"

2. **Explore Schema Browser**:
   - Click "Schema Browser" tab
   - Expand tables to see columns and relationships

3. **Run Evaluation**:
   - Execute `python tests/evaluate.py`
   - Review results in `tests/evaluation_results.json`

4. **Customize**:
   - Add more test queries in `tests/citi_db_examples.json`
   - Modify UI styling in `ui/src/app/app.component.css`
   - Adjust LLM model in `.env` (e.g., `gemini-1.5-pro`)

## Support

For issues or questions:
1. Check this guide's Troubleshooting section
2. Review README.md for architecture details
3. Examine error logs in terminal output
4. Verify all prerequisites are met
