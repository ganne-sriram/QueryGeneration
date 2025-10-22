# QueryGeneration - NL2SQL for citi_db

Natural Language to MySQL SQL Query Generation system for the citi_db banking database. This project converts natural language questions into executable MySQL queries using Google Gemini LLM, with an Angular 19 UI for interactive querying.

## 📚 Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Evaluation](#evaluation)
- [Project Structure](#project-structure)

## 📖 Project Overview

QueryGeneration enables non-technical users to query the citi_db banking database using natural language instead of SQL. The system:
- Converts questions like "How many customers are there?" into SQL queries
- Executes queries safely (SELECT-only, no DDL/DML)
- Displays results with tables used and formatted output
- Provides a schema browser for database exploration

This project mirrors the architecture and patterns from the textToSql reference implementation, adapted for the citi_db schema.

## 🔧 Features

- **Natural Language Processing**: Converts user questions into MySQL SQL statements using Google Gemini
- **Database Interaction**: Connects to MySQL citi_db database to fetch results
- **Safety Enforcement**: SELECT-only execution, blocks DDL/DML operations
- **Angular 19 UI**: Modern web interface with:
  - Query generator with SQL display and copy functionality
  - Tables used extraction and display
  - Results viewer with CSV download
  - Schema browser with table/column details
- **Schema-Driven**: Dynamically adapts to citi_db schema using reflection
- **Evaluation Framework**: 40 test queries with quality metrics

## 🗼 Architecture

The project follows a modular architecture mirroring textToSql:

```
QueryGeneration/
├── nl2sql/              # NL2SQL core logic (mirrors textToSql pattern)
│   ├── query_generator.py   # LangChain-based SQL generation
│   ├── schema_reflector.py  # SQLAlchemy schema introspection
│   ├── server.py             # FastAPI REST API
│   └── cli.py                # Command-line interface
├── scripts/             # Utility scripts
│   ├── load_csv.py           # CSV → MySQL loader
│   └── extract_schema.py    # Schema → JSON/ERD artifacts
├── ui/                  # Angular 19 frontend
├── tests/               # Evaluation queries and scripts
├── artifacts/           # Generated schema files
└── config.py            # Configuration management
```

### Data Flow

1. **CSV Loading**: `scripts/load_csv.py` → citi_db tables
2. **Schema Extraction**: `scripts/extract_schema.py` → artifacts/citi_db_schema.json
3. **Query Generation**: User question → LangChain → Gemini → SQL
4. **Execution**: SQL → MySQL → Results
5. **Display**: Results → Angular UI → User

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- Node.js 18+ and npm
- MySQL 5.7+ or 8.0+
- Google API Key (for Gemini)

### Setup Steps

1. **Clone the Repository**:
   ```bash
   cd /path/to/QueryGeneration
   ```

2. **Set Up Python Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure Environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your settings:
   # - DB_HOST, DB_PORT, DB_USER, DB_PASSWORD
   # - GOOGLE_API_KEY
   # - CSV_PATH (path to MockData/exports/CSV Files/)
   ```

4. **Load CSV Data into MySQL**:
   ```bash
   python scripts/load_csv.py
   ```
   This creates the `citi_db` database and loads all CSV files from MockData.

5. **Extract Schema Artifacts**:
   ```bash
   python scripts/extract_schema.py
   ```
   Generates `artifacts/citi_db_schema.json` and `artifacts/citi_db_erd.md`.

6. **Install Angular Dependencies**:
   ```bash
   cd ui
   npm install
   cd ..
   ```

## 🚀 Usage

### Option 1: Full Stack (Recommended)

1. **Start the FastAPI Backend**:
   ```bash
   python nl2sql/server.py
   ```
   Backend runs on http://localhost:8000

2. **Start the Angular UI** (in a new terminal):
   ```bash
   cd ui
   npm start
   ```
   UI runs on http://localhost:4200

3. **Open Browser**:
   Navigate to http://localhost:4200 and start querying!

### Option 2: CLI Only

```bash
python nl2sql/cli.py "How many customers are there?"
```

Output:
```json
{
  "question": "How many customers are there?",
  "sql": "SELECT COUNT(*) FROM customers",
  "result": "[(500,)]"
}
```

### Option 3: Python API

```python
from nl2sql.query_generator import QueryGenerator

generator = QueryGenerator()
result = generator.generate_and_execute("What is the total balance of all accounts?")

print(result['sql'])      # Generated SQL
print(result['result'])   # Query results
```

## 📊 Evaluation

Run the evaluation suite to test query generation quality:

```bash
python tests/evaluate.py
```

### Metrics

The evaluation tests 40 diverse queries covering:
- Simple aggregations (COUNT, SUM, AVG)
- Filtering (WHERE clauses)
- Joins (multiple tables)
- Grouping (GROUP BY)
- Date filtering
- Text search

**Target Metrics**:
- Syntactic Validity: ≥90%
- Execution Success: ≥80%

Results are saved to `tests/evaluation_results.json`.

## 📁 Project Structure

```
QueryGeneration/
├── config.py                    # Configuration loader (DB, LLM, paths)
├── .env.example                 # Environment template
├── requirements.txt             # Python dependencies
├── README.md                    # This file
│
├── nl2sql/                      # Core NL2SQL logic
│   ├── query_generator.py       # LangChain + Gemini SQL generation
│   ├── schema_reflector.py      # SQLAlchemy schema introspection
│   ├── server.py                # FastAPI REST API
│   └── cli.py                   # CLI wrapper
│
├── scripts/                     # Utility scripts
│   ├── load_csv.py              # CSV → MySQL loader
│   └── extract_schema.py        # Schema → artifacts generator
│
├── ui/                          # Angular 19 frontend
│   ├── src/
│   │   ├── app/
│   │   │   ├── app.component.ts      # Main component logic
│   │   │   ├── app.component.html    # UI template
│   │   │   └── app.component.css     # Styles
│   │   └── environments/
│   │       └── environment.ts        # API URL configuration
│   └── package.json
│
├── tests/                       # Evaluation framework
│   ├── citi_db_examples.json    # 40 test queries
│   ├── evaluate.py              # Evaluation script
│   └── evaluation_results.json  # Generated results
│
└── artifacts/                   # Generated files
    ├── citi_db_schema.json      # Schema metadata
    └── citi_db_erd.md           # Entity Relationship Diagram
```

## 🗄️ Database Schema (citi_db)

The citi_db database contains 11 tables representing a banking system:

**Foundation Tables**:
- `account_type` - Account type definitions
- `branches` - Bank branch information
- `customers` - Customer master data
- `employees` - Employee information

**Primary Entities**:
- `accounts` - Bank accounts
- `credit_cards` - Credit card accounts
- `loan` - Loan accounts

**Relationships & Transactions**:
- `account_customers` - Account-customer junction
- `banking_transactions` - Banking transactions
- `cc_transactions` - Credit card transactions
- `branch_employees` - Employee-branch assignments

See `artifacts/citi_db_erd.md` for detailed schema documentation.

## 🔒 Safety Features

- **SELECT-only execution**: Blocks DDL/DML operations (DROP, DELETE, INSERT, UPDATE, etc.)
- **SQL validation**: Checks for dangerous keywords before execution
- **Error handling**: Graceful error messages for invalid queries
- **Schema-driven**: Uses actual database schema to guide generation

## 🎯 Example Queries

- "How many customers are there?"
- "What is the total balance of all accounts?"
- "List all customers from California"
- "Which customers have more than one account?"
- "Show me all checking accounts"
- "What is the average credit card limit?"
- "List all employees working in New York branches"
- "Which branch has the most accounts?"

## 📝 Configuration

Key environment variables in `.env`:

```bash
# Database
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=citi_db

# LLM
GOOGLE_API_KEY=your_google_api_key
LLM_MODEL=gemini-2.0-flash

# Data Loading
CSV_PATH=../MockData/exports/CSV Files
```

## 🤝 Contributing

This project follows the textToSql architecture patterns. When contributing:
1. Maintain the same module structure and naming conventions
2. Use LangChain for LLM orchestration
3. Keep safety checks (SELECT-only) intact
4. Update tests when adding features

## 📄 License

This project follows the same license as the textToSql reference implementation.

---

**Built with**: Python, LangChain, Google Gemini, FastAPI, Angular 19, MySQL, SQLAlchemy

**Reference Implementation**: Based on textToSql architecture patterns


-------------------------------------------------------

 🎯 Project Overview: QueryGeneration NL2SQL System

  This is a Natural Language to SQL (NL2SQL) application that converts plain English        
  questions into MySQL SQL queries for a banking database called citi_db.

  ---
  🏗️ Architecture - 3 Main Layers

  1. Backend Layer (Python/FastAPI)

  2. Frontend Layer (Angular 19)

  3. Database Layer (MySQL)

  ---
  📂 File-by-File Explanation

  🔧 Core Configuration

  config.py

  - Central configuration file
  - Loads environment variables from .env
  - Contains database credentials, Google API key, CSV paths
  - Provides get_database_url() method for SQLAlchemy connection

  .env (not in git)

  - Stores sensitive credentials:
    - MySQL password
    - Google API Key for Gemini
    - Database connection details
    - Path to CSV data files

  .env.example

  - Template for .env file
  - Shows what variables are needed
  - Safe to commit to git (no real credentials)

  ---
  🧠 Core NL2SQL Logic (nl2sql/ folder)

  nl2sql/query_generator.py ⭐ (Most Important)

  What it does: Converts natural language to SQL using AI
  - Uses LangChain framework to orchestrate the process
  - Uses Google Gemini LLM as the AI model
  - Creates a prompt template that includes database schema
  - Key methods:
    - generate_sql(question) - Converts question to SQL
    - execute_query(sql) - Runs the SQL on database
    - _clean_sql_query(sql) - YOUR FIX: Removes markdown code blocks
    - get_tables_from_sql(sql) - Extracts which tables are used

  Process Flow:
  User Question → Add DB Schema to Context → Send to Gemini → Get SQL → Clean SQL →
  Execute

  nl2sql/schema_reflector.py

  What it does: Inspects database structure automatically
  - Uses SQLAlchemy to read MySQL database metadata
  - Key methods:
    - get_all_tables() - Lists all tables
    - get_table_columns(table) - Gets columns for a table
    - get_primary_keys(table) - Gets primary keys
    - get_foreign_keys(table) - Gets relationships
    - get_table_dependencies() - Determines table load order

  Why needed? The AI needs to know what tables/columns exist to generate correct SQL.       

  nl2sql/server.py ⭐

  What it does: REST API server that the UI talks to
  - Built with FastAPI framework
  - Runs on http://localhost:8000
  - Endpoints:
    - POST /api/query - Generate and execute SQL from question
    - GET /api/schema - Get database schema info
    - GET /api/health - Check if server is running

  Your Fix: Changed error: str = None to error: Optional[str] = None for Pydantic
  validation

  nl2sql/cli.py

  What it does: Command-line interface
  - Allows testing from terminal without UI
  - Usage: python nl2sql/cli.py "How many customers?"
  - Returns JSON with question, SQL, and results

  ---
  📊 Utility Scripts (scripts/ folder)

  scripts/load_csv.py

  What it does: Loads CSV files into MySQL
  - Reads CSV files from MockData folder
  - Creates citi_db database if it doesn't exist
  - Creates tables and loads data using pandas
  - Steps:
    a. Creates database
    b. Connects to MySQL
    c. Reads each CSV file
    d. Creates table with CSV column names
    e. Inserts all rows

  When to run: First time setup, or when data changes

  scripts/extract_schema.py

  What it does: Creates documentation of database structure
  - Generates artifacts/citi_db_schema.json - JSON representation of tables
  - Generates artifacts/citi_db_erd.md - Markdown ERD diagram
  - Output includes:
    - All tables
    - Columns with types
    - Primary keys
    - Foreign key relationships

  When to run: After loading CSV data, or when schema changes

  ---
  🎨 Frontend (ui/ folder - Angular 19)

  ui/src/app/app.component.ts ⭐

  What it does: Main application logic (TypeScript)
  - Features:
    a. Query Tab:
        - Input field for natural language question
      - "Generate SQL" button
      - Shows generated SQL (with copy button)
      - Shows tables used
      - Shows results
      - Download results as CSV
    b. Schema Browser Tab:
        - Lists all database tables
      - Expandable table details
      - Shows columns, types, keys
  - Key methods:
    - generateSQL() - Calls backend API to convert question to SQL
    - loadSchema() - Fetches database schema from backend
    - copySQL() - Copies SQL to clipboard
    - downloadCSV() - Exports results as CSV file
    - formatResult() - Formats query results as table

  ui/src/app/app.component.html

  What it does: UI template (HTML structure)
  - Two tabs: Query Generator and Schema Browser
  - Form with text area for questions
  - Result display area
  - Schema explorer with collapsible sections

  ui/src/app/app.component.css

  What it does: Styling (makes it look nice)

  ui/src/environments/environment.ts

  What it does: Configuration for Angular
  - Sets apiUrl: 'http://localhost:8000/api'
  - Tells frontend where backend is

  ui/package.json

  What it does: Node.js dependencies
  - Lists Angular packages needed
  - Defines npm scripts (npm start, npm build)

  ui/angular.json

  What it does: Angular project configuration
  - Build settings
  - File paths
  - Compiler options

  ---
  🧪 Testing (tests/ folder)

  tests/citi_db_examples.json

  What it does: Test dataset with 40 example questions
  - Each example has:
    - ID
    - Natural language question
    - Expected tables that should be used
  - Examples like:
    - "How many customers are there?"
    - "What is the total balance of all accounts?"
    - "List customers from California"

  tests/evaluate.py

  What it does: Automated testing system
  - Runs all 40 test questions through the system
  - Measures:
    - Syntactic Validity: Is the SQL grammatically correct? (Target: ≥90%)
    - Execution Success: Does the SQL run without errors? (Target: ≥80%)
  - Generates tests/evaluation_results.json with scores
  - Process:
    a. Load test questions
    b. For each question:
        - Generate SQL
      - Validate syntax
      - Try to execute
      - Track success/failure
    c. Calculate percentages
    d. Save results

  When to run: To verify the system is working well

  ---
  📁 Generated Artifacts (artifacts/ folder)

  artifacts/citi_db_schema.json

  What it does: Machine-readable database structure
  - JSON format with all tables, columns, types
  - Used for reference and documentation

  artifacts/citi_db_erd.md

  What it does: Human-readable database diagram
  - Markdown format
  - Lists all tables with columns
  - Shows relationships

  ---
  📚 Documentation Files

  README.md

  What it does: Main project documentation
  - Overview of project
  - Installation instructions
  - Usage examples
  - Architecture diagram
  - Features list

  SETUP_GUIDE.md

  What it does: Step-by-step setup instructions
  - Prerequisites checklist
  - Detailed installation steps
  - Configuration guide
  - Troubleshooting tips

  DEPLOYMENT_SUMMARY.md

  What it does: Deployment notes
  - How to deploy to production
  - Environment setup
  - Server configuration

  requirements.txt

  What it does: Python dependencies
  - Lists all Python packages needed:
    - fastapi - Web server
    - langchain - AI orchestration
    - sqlalchemy - Database ORM
    - pymysql - MySQL driver
    - pandas - Data manipulation
    - uvicorn - ASGI server
    - And more...

  ---
  🔄 How Everything Works Together - Data Flow

  1. SETUP PHASE (One Time)
     ├─ MockData CSVs → scripts/load_csv.py → MySQL citi_db
     ├─ MySQL schema → scripts/extract_schema.py → artifacts/
     └─ Install packages: requirements.txt, package.json

  2. RUNTIME PHASE (Every Time)
     ├─ Start Backend: python nl2sql/server.py (Port 8000)
     ├─ Start Frontend: npm start in ui/ (Port 4200)
     └─ Browser opens http://localhost:4200

  3. USER QUERY FLOW
     User types: "How many customers?"
     ↓
     Angular UI (app.component.ts)
     ↓
     HTTP POST to /api/query
     ↓
     FastAPI server (server.py)
     ↓
     QueryGenerator.generate_sql()
     ↓
     Adds database schema to prompt
     ↓
     Sends to Google Gemini LLM
     ↓
     Receives SQL with markdown: ```sql SELECT...```
     ↓
     _clean_sql_query() removes markdown ← YOUR FIX!
     ↓
     execute_query() runs on MySQL
     ↓
     Returns results
     ↓
     FastAPI returns JSON response
     ↓
     Angular displays SQL + results
     ↓
     User can copy SQL or download CSV

  ---
  🗄️ Database Structure (citi_db)

  11 Tables representing a banking system:

  1. customers - Customer information (name, address, phone)
  2. accounts - Bank accounts (balance, type, branch)
  3. account_type - Account type definitions (checking, savings)
  4. branches - Bank branch locations
  5. employees - Employee information
  6. branch_employees - Links employees to branches
  7. account_customers - Links accounts to customers (many-to-many)
  8. banking_transactions - Transaction history
  9. credit_cards - Credit card accounts
  10. cc_transactions - Credit card transactions
  11. loan - Loan accounts

  ---
  🔒 Security Features

  1. SELECT-only execution - Blocks dangerous SQL commands (DROP, DELETE, INSERT,
  UPDATE)
  2. .env file - Credentials never committed to git
  3. Error handling - Graceful error messages
  4. SQL validation - Checks before execution

  ---
  🐛 Bugs You Fixed

  Bug #1: Markdown Code Blocks in SQL

  - Problem: Gemini returned: ```sql\nSELECT...```
  - Solution: Added _clean_sql_query() method in query_generator.py:63-70
  - How it works: Uses regex to strip ```sql and ``` markers

  Bug #2: Pydantic Validation Error

  - Problem: error: str = None caused type error
  - Solution: Changed to error: Optional[str] = None in server.py:52
  - How it works: Tells Pydantic that error field can be None

  ---
  This is a complete, production-ready NL2SQL system that allows non-technical users to     
  query a banking database using plain English! 🎉
