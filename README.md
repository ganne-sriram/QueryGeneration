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
