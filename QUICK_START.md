# Quick Start Guide - Query Generation

## 🚀 Run Application in 3 Steps

### Step 1: Start Backend (Terminal 1)
```bash
cd C:\Users\srira\Documents\QueryGeneration
venv\Scripts\activate
python nl2sql/server.py
```
✓ Backend running on **http://localhost:8000**

---

### Step 2: Start Frontend (Terminal 2)
```bash
cd C:\Users\srira\Documents\QueryGeneration\ui
npm start
```
✓ Frontend running on **http://localhost:4200**

---

### Step 3: Open Browser
Navigate to: **http://localhost:4200**

---

## 📝 Example Queries to Try

1. "How many customers are there?"
2. "What is the total balance of all accounts?"
3. "List all customers from California"
4. "Show me all checking accounts"
5. "Which customers have more than one account?"
6. "List all employees working in New York branches"
7. "What is the average credit card limit?"
8. "Show me accounts with balance greater than 50000"

---

## 🧪 Run Tests
```bash
cd C:\Users\srira\Documents\QueryGeneration
venv\Scripts\activate
python tests/evaluate.py
```

**Expected Results:**
- 40 queries tested
- 100% syntactically valid
- 95% execution success

---

## 🛑 Stop Application
- Press **Ctrl+C** in both terminals
- Run: `deactivate`

---

## 📚 Full Documentation
See: `RUN_APPLICATION_GUIDE.md` for complete details

---

## 🔗 Quick Links
- Frontend: http://localhost:4200
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- GitHub: https://github.com/ganne-sriram/QueryGeneration
