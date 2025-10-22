#!/usr/bin/env python3
"""
FastAPI server for NL2SQL query generation.
Provides REST API endpoints for the Angular UI.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json

from query_generator import QueryGenerator
from schema_reflector import SchemaReflector


app = FastAPI(title="QueryGeneration NL2SQL API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

generator = None
reflector = None


@app.on_event("startup")
async def startup_event():
    """Initialize components on startup."""
    global generator, reflector
    generator = QueryGenerator()
    reflector = SchemaReflector()
    reflector.reflect_schema()


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    question: str
    sql: str
    tables_used: List[str]
    result: Any
    error: Optional[str] = None


@app.post("/api/query", response_model=QueryResponse)
async def generate_query(request: QueryRequest):
    """Generate and execute SQL query from natural language question."""
    try:
        sql_query = generator.generate_sql(request.question)
        
        tables_used = generator.get_tables_from_sql(sql_query)
        
        result = generator.execute_query(sql_query)
        
        return QueryResponse(
            question=request.question,
            sql=sql_query,
            tables_used=tables_used,
            result=result,
            error=None
        )
    except Exception as e:
        return QueryResponse(
            question=request.question,
            sql="",
            tables_used=[],
            result=None,
            error=str(e)
        )


@app.get("/api/schema")
async def get_schema():
    """Get database schema information."""
    try:
        tables = reflector.get_all_tables()
        schema = {}
        
        for table_name in tables:
            columns = reflector.get_table_columns(table_name)
            primary_keys = reflector.get_primary_keys(table_name)
            foreign_keys = reflector.get_foreign_keys(table_name)
            
            schema[table_name] = {
                'columns': [
                    {
                        'name': col['name'],
                        'type': str(col['type']),
                        'nullable': col['nullable']
                    }
                    for col in columns
                ],
                'primary_keys': primary_keys,
                'foreign_keys': foreign_keys
            }
        
        return schema
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
