"""
NL2SQL Query Generator module.
Converts natural language questions to MySQL SQL queries using LangChain and Google Gemini.
Mirrors the textToSql implementation pattern.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from config import Config


class QueryGenerator:
    """Generates SQL queries from natural language using LLM."""
    
    def __init__(self, database_url=None, api_key=None, model=None):
        """Initialize query generator with database and LLM."""
        self.database_url = database_url or Config.get_database_url()
        self.api_key = api_key or Config.GOOGLE_API_KEY
        self.model = model or Config.LLM_MODEL
        
        self.db = SQLDatabase.from_uri(self.database_url, sample_rows_in_table_info=2)
        
        self.llm = ChatGoogleGenerativeAI(
            model=self.model,
            api_key=self.api_key
        )
        
        template = """Based on the table schema below, write a SQL query that would answer the user's question:
Remember : Only provide me the sql query dont include anything else. Provide me sql query in a single line dont add line breaks
Table Schema: {schema}
Question: {question}
SQL Query:
"""
        self.prompt = ChatPromptTemplate.from_template(template)
        
        self.sql_chain = (
            RunnablePassthrough.assign(schema=lambda _: self.get_schema()) 
            | self.prompt
            | self.llm.bind(stop=["\nSQLResult:"])
            | StrOutputParser()
        )
    
    def get_schema(self):
        """Get the schema of the database."""
        return self.db.get_table_info()
    
    def generate_sql(self, question):
        """Generate SQL query from natural language question."""
        try:
            sql_query = self.sql_chain.invoke({"question": question})
            # Strip markdown code blocks if present
            sql_query = self._clean_sql_query(sql_query)
            return sql_query.strip()
        except Exception as e:
            raise Exception(f"Error generating SQL: {e}")

    def _clean_sql_query(self, sql_query):
        """Remove markdown code blocks and extra formatting from SQL query."""
        import re
        # Remove markdown code blocks (```sql ... ``` or ``` ... ```)
        sql_query = re.sub(r'^```sql\s*\n?', '', sql_query, flags=re.IGNORECASE)
        sql_query = re.sub(r'^```\s*\n?', '', sql_query)
        sql_query = re.sub(r'\n?```$', '', sql_query)
        return sql_query.strip()
    
    def execute_query(self, sql_query):
        """Execute SQL query and return results."""
        try:
            result = self.db.run(sql_query)
            return result
        except Exception as e:
            raise Exception(f"Error executing query: {e}")
    
    def generate_and_execute(self, question):
        """Generate SQL from question and execute it."""
        sql_query = self.generate_sql(question)
        result = self.execute_query(sql_query)
        return {
            'question': question,
            'sql': sql_query,
            'result': result
        }
    
    def get_tables_from_sql(self, sql_query):
        """Extract table names from SQL query."""
        import re
        tables = set()
        
        from_pattern = r'\bFROM\s+`?(\w+)`?'
        tables.update(re.findall(from_pattern, sql_query, re.IGNORECASE))
        
        join_pattern = r'\bJOIN\s+`?(\w+)`?'
        tables.update(re.findall(join_pattern, sql_query, re.IGNORECASE))
        
        return list(tables)
