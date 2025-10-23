# Complete Guide to Run Query Generation Application

This guide provides step-by-step instructions to run the entire NL2SQL Query Generation application, including setup, execution, and testing.

---

## Prerequisites

Before starting, ensure you have the following installed:

1. **Python 3.11+** - Check version:
   ```bash
   python --version
   ```

2. **Node.js 24.6.0+** - Check version:
   ```bash
   node --version
   npm --version
   ```

3. **MySQL 8.0+** - Check version:
   ```bash
   mysql --version
   ```

4. **Google API Key** - Get from: https://makersuite.google.com/app/apikey

5. **MockData Repository** - Located at: `C:\Users\srira\Documents\MockData\exports\CSV Files`

---

## Step 1: Environment Configuration

### 1.1 Navigate to Project Directory
```bash
cd C:\Users\srira\Documents\QueryGeneration
```

### 1.2 Verify .env File Exists
The `.env` file should already be configured with:
```bash
# Check if .env exists
dir .env
```

Your `.env` file contains:
```
# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=password
DB_NAME=citi_db

# LLM Configuration
GOOGLE_API_KEY=AIzaSyBGbpsR-xAtvX5aDknuiPKelKKSEX_Vz2U
LLM_MODEL=gemini-2.0-flash

# Data Loading Configuration
CSV_PATH=C:\Users\srira\Documents\MockData\exports\CSV Files
```

---

## Step 2: Python Environment Setup

### 2.1 Create Virtual Environment (if not exists)
```bash
python -m venv venv
```

### 2.2 Activate Virtual Environment
```bash
venv\Scripts\activate
```

You should see `(venv)` at the start of your command prompt.

### 2.3 Install Python Dependencies
```bash
pip install -r requirements.txt
```

This installs:
- FastAPI (web server)
- LangChain (AI orchestration)
- SQLAlchemy (database ORM)
- PyMySQL (MySQL driver)
- Pandas (data manipulation)
- Google Generative AI (Gemini)
- And more...

---

## Step 3: Database Setup

### 3.1 Start MySQL Service
Ensure MySQL is running:
```bash
# Check MySQL status (Windows)
sc query MySQL80
```

If not running, start it via Services or:
```bash
net start MySQL80
```

### 3.2 Load CSV Data into Database
```bash
python scripts/load_csv.py
```

**Expected Output:**
```
================================================================================
  CSV Loader for citi_db
================================================================================

Configuration:
  Database: citi_db
  Host: localhost:3306
  CSV Path: C:\Users\srira\Documents\MockData\exports\CSV Files

Step 1: Creating database...
✓ Database 'citi_db' ready

Step 2: Connecting to database...
  ✓ Connected to citi_db

Step 3: Loading CSV files...
  Found 11 CSV files
  Loading account_customers... ✓ 500 records
  Loading account_type... ✓ 5 records
  Loading accounts... ✓ 500 records
  Loading banking_transactions... ✓ 1000 records
  Loading branch_employees... ✓ 150 records
  Loading branches... ✓ 50 records
  Loading cc_transactions... ✓ 800 records
  Loading credit_cards... ✓ 300 records
  Loading customers... ✓ 500 records
  Loading employees... ✓ 100 records
  Loading loan... ✓ 200 records

  ✓ Total records loaded: 4105

Step 4: Verifying tables...
  ✓ Found 11 tables: account_customers, account_type, accounts, ...

================================================================================
  ✓ CSV loading completed successfully!
================================================================================
```

### 3.3 Extract Database Schema (Optional)
```bash
python scripts/extract_schema.py
```

This generates:
- `artifacts/citi_db_schema.json` - JSON representation of schema
- `artifacts/citi_db_erd.md` - Markdown ERD diagram

---

## Step 4: Frontend Setup

### 4.1 Navigate to UI Directory
```bash
cd ui
```

### 4.2 Install Node.js Dependencies
```bash
npm install
```

This installs Angular 19 and dependencies.

### 4.3 Return to Root Directory
```bash
cd ..
```

---

## Step 5: Running the Application

You need to run TWO servers: Backend (Python) and Frontend (Angular)

### 5.1 Terminal 1 - Start Backend Server

**Open first terminal:**
```bash
cd C:\Users\srira\Documents\QueryGeneration
venv\Scripts\activate
python nl2sql/server.py
```

**Expected Output:**
```
INFO:     Started server process [XXXXX]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

**Backend is now running on:** http://localhost:8000

**Available Endpoints:**
- `GET  /api/health` - Health check
- `GET  /api/schema` - Get database schema
- `POST /api/query` - Generate and execute SQL from natural language

**API Documentation:** http://localhost:8000/docs

---

### 5.2 Terminal 2 - Start Frontend Server

**Open second terminal:**
```bash
cd C:\Users\srira\Documents\QueryGeneration\ui
npm start
```

**Expected Output:**
```
✔ Browser application bundle generation complete.
✔ Browser application bundle generation complete.

Initial Chunk Files | Names         |  Raw Size
polyfills.js        | polyfills     |  90.20 kB |
main.js             | main          |  22.51 kB |
styles.css          | styles        |   1.08 kB |

** Angular Live Development Server is listening on localhost:4200, open your browser on http://localhost:4200/ **
```

**Frontend is now running on:** http://localhost:4200

---

## Step 6: Using the Application

### 6.1 Open Your Browser
Navigate to: **http://localhost:4200**

### 6.2 Query Generator Tab

**Try these example queries:**

1. **Simple Count:**
   - Type: "How many customers are there?"
   - Click: "Generate SQL"
   - See: `SELECT count(*) FROM Customers`

2. **Aggregation:**
   - Type: "What is the total balance of all accounts?"
   - Click: "Generate SQL"
   - See: `SELECT sum(Account_Balance) FROM Accounts`

3. **Filtering:**
   - Type: "List all customers from California"
   - Click: "Generate SQL"
   - See: `SELECT * FROM Customers WHERE State = 'CA'`

4. **Complex JOIN:**
   - Type: "List all employees working in New York branches"
   - Click: "Generate SQL"
   - See: 3-table JOIN query

5. **Grouping:**
   - Type: "What is the distribution of customers by state?"
   - Click: "Generate SQL"
   - See: `GROUP BY State` query

**Features:**
- Copy SQL button
- Download results as CSV
- View tables used
- See formatted results

### 6.3 Schema Browser Tab

Click on "Schema Browser" tab to:
- View all 11 database tables
- Expand tables to see columns, types, primary keys
- See foreign key relationships

---

## Step 7: Command Line Interface (Optional)

You can also query from the command line:

```bash
cd C:\Users\srira\Documents\QueryGeneration
venv\Scripts\activate
python nl2sql/cli.py "How many customers are there?"
```

**Output:**
```json
{
  "question": "How many customers are there?",
  "sql": "SELECT count(*) FROM Customers",
  "result": "[(500,)]"
}
```

---

## Step 8: Running Tests

### 8.1 Run Evaluation Tests

**Activate virtual environment (if not already):**
```bash
cd C:\Users\srira\Documents\QueryGeneration
venv\Scripts\activate
```

**Run tests:**
```bash
python tests/evaluate.py
```

**What this does:**
- Tests 40 different natural language queries
- Generates SQL for each query
- Validates SQL syntax
- Executes queries on database
- Measures success rates

**Expected Output:**
```
================================================================================
  NL2SQL Evaluation for citi_db
================================================================================

Loading examples from: tests\citi_db_examples.json
  ✓ Loaded 40 test queries

Initializing query generator...
  ✓ Generator ready

Running evaluation...
--------------------------------------------------------------------------------

[1/40] How many customers are there?
  ✓ Valid SQL generated (0.92s)
  ✓ Execution successful
  SQL: SELECT count(*) FROM Customers
  Tables: Customers

[2/40] What is the total balance of all accounts?
  ✓ Valid SQL generated (0.68s)
  ✓ Execution successful
  SQL: SELECT sum(Account_Balance) FROM Accounts
  Tables: Accounts

... (38 more queries)

================================================================================
  Evaluation Summary
================================================================================

Total Queries:           40
Syntactically Valid:     40 (100.0%)
Execution Success:       38 (95.0%)

Target Metrics:
  Syntactic Validity:    ≥90% ✓ (Actual: 100.0%)
  Execution Success:     ≥80% ✓ (Actual: 95.0%)

Results saved to: tests\evaluation_results.json

✓ All target metrics met!
```

### 8.2 View Detailed Test Results

```bash
cat tests\evaluation_results.json
```

This JSON file contains:
- Summary statistics
- Individual query results
- SQL generated for each query
- Execution status
- Tables used
- Generation time

---

## Step 9: Stopping the Application

### 9.1 Stop Frontend Server (Terminal 2)
Press: **Ctrl+C**

### 9.2 Stop Backend Server (Terminal 1)
Press: **Ctrl+C**

### 9.3 Deactivate Virtual Environment
```bash
deactivate
```

---

## Complete Workflow Summary

```
1. Prerequisites ✓
   ├─ Python 3.11+
   ├─ Node.js 24.6.0+
   ├─ MySQL 8.0+
   └─ Google API Key

2. Setup (One-time)
   ├─ Create .env file
   ├─ Create virtual environment
   ├─ Install Python dependencies
   ├─ Load CSV data to MySQL
   └─ Install Node.js dependencies

3. Run Application (Every time)
   ├─ Terminal 1: python nl2sql/server.py (Backend)
   ├─ Terminal 2: npm start in ui/ (Frontend)
   └─ Browser: http://localhost:4200

4. Use Application
   ├─ Query Generator Tab: Ask questions
   ├─ Schema Browser Tab: Explore database
   └─ CLI: python nl2sql/cli.py "question"

5. Run Tests (Optional)
   └─ python tests/evaluate.py

6. Stop Application
   ├─ Ctrl+C in both terminals
   └─ deactivate virtual environment
```

---

## Troubleshooting

### Issue: "Module not found" error
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "Cannot connect to MySQL"
**Solution:**
```bash
# Check MySQL is running
sc query MySQL80

# If not, start it
net start MySQL80
```

### Issue: "API Key quota exceeded"
**Solution:**
- Google Gemini free tier: 15 requests/minute
- Wait a few minutes between large test runs
- Or upgrade to paid tier for higher limits

### Issue: "Port 8000 already in use"
**Solution:**
```bash
# Find and kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Issue: "Port 4200 already in use"
**Solution:**
```bash
# Kill Node.js process
taskkill /IM node.exe /F
```

### Issue: Unicode errors in tests
**Solution:** Already fixed in `tests/evaluate.py` with UTF-8 encoding

---

## Quick Reference Commands

### Backend Only
```bash
cd C:\Users\srira\Documents\QueryGeneration
venv\Scripts\activate
python nl2sql/server.py
```

### Frontend Only
```bash
cd C:\Users\srira\Documents\QueryGeneration\ui
npm start
```

### Full Stack
**Terminal 1:**
```bash
cd C:\Users\srira\Documents\QueryGeneration
venv\Scripts\activate
python nl2sql/server.py
```

**Terminal 2:**
```bash
cd C:\Users\srira\Documents\QueryGeneration\ui
npm start
```

**Browser:** http://localhost:4200

### Run Tests
```bash
cd C:\Users\srira\Documents\QueryGeneration
venv\Scripts\activate
python tests/evaluate.py
```

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                     USER (Browser)                      │
│                http://localhost:4200                    │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│              Angular Frontend (Port 4200)               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Query Gen    │  │ Schema       │  │ Results      │  │
│  │ Component    │  │ Browser      │  │ Display      │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└───────────────────────┬─────────────────────────────────┘
                        │ HTTP POST/GET
                        ▼
┌─────────────────────────────────────────────────────────┐
│           FastAPI Backend (Port 8000)                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ /api/query   │  │ /api/schema  │  │ /api/health  │  │
│  └──────┬───────┘  └──────┬───────┘  └──────────────┘  │
│         │                  │                            │
│  ┌──────▼─────────────────▼────────┐                   │
│  │   QueryGenerator                │                   │
│  │   - generate_sql()              │                   │
│  │   - execute_query()             │                   │
│  │   - _clean_sql_query() [FIX]    │                   │
│  └──────┬──────────────────────────┘                   │
│         │                                               │
│  ┌──────▼──────────────────────────┐                   │
│  │   SchemaReflector               │                   │
│  │   - get_all_tables()            │                   │
│  │   - get_table_columns()         │                   │
│  └──────┬──────────────────────────┘                   │
└─────────┼───────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────┐
│              LangChain + Google Gemini                  │
│  Question + Schema → LLM → SQL Query                    │
└─────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────┐
│              MySQL Database (citi_db)                   │
│  11 Tables: customers, accounts, transactions, etc.     │
└─────────────────────────────────────────────────────────┘
```

---

## Next Steps

1. **Explore the UI** - Try different questions
2. **Check Schema Browser** - Understand database structure
3. **Run Tests** - See 40 example queries
4. **Read Code** - Explore `nl2sql/query_generator.py`
5. **Customize** - Add your own queries to tests
6. **Deploy** - See DEPLOYMENT_SUMMARY.md for production setup

---

**Happy Querying! 🎉**

For issues or questions, check:
- GitHub: https://github.com/ganne-sriram/QueryGeneration
- Google Gemini Docs: https://ai.google.dev/gemini-api/docs
- LangChain Docs: https://python.langchain.com/docs/
