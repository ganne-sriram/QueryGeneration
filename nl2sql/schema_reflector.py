"""
Schema reflection module using SQLAlchemy.
Automatically detects tables, columns, primary keys, and foreign keys.
"""
from sqlalchemy import create_engine, MetaData, inspect
from sqlalchemy.orm import sessionmaker
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config


class SchemaReflector:
    """Reflects database schema and provides metadata about tables and relationships."""
    
    def __init__(self, database_url=None):
        """Initialize schema reflector with database connection."""
        self.database_url = database_url or Config.get_database_url()
        self.engine = create_engine(self.database_url, echo=False)
        self.metadata = MetaData()
        self.inspector = inspect(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        
    def reflect_schema(self):
        """Reflect all tables from the database."""
        self.metadata.reflect(bind=self.engine)
        return self.metadata
    
    def get_all_tables(self):
        """Get list of all table names in the database."""
        return self.inspector.get_table_names()
    
    def get_table_columns(self, table_name):
        """Get column information for a specific table."""
        return self.inspector.get_columns(table_name)
    
    def get_primary_keys(self, table_name):
        """Get primary key columns for a specific table."""
        pk_constraint = self.inspector.get_pk_constraint(table_name)
        return pk_constraint.get('constrained_columns', [])
    
    def get_foreign_keys(self, table_name):
        """Get foreign key relationships for a specific table."""
        return self.inspector.get_foreign_keys(table_name)
    
    def get_table_dependencies(self):
        """
        Determine table insertion order based on foreign key dependencies.
        Returns tables in topological order (parent tables first).
        """
        tables = self.get_all_tables()
        dependencies = {}
        
        for table in tables:
            fks = self.get_foreign_keys(table)
            deps = set()
            for fk in fks:
                referred_table = fk['referred_table']
                if referred_table != table:
                    deps.add(referred_table)
            dependencies[table] = deps
        
        sorted_tables = []
        visited = set()
        
        def visit(table):
            if table in visited:
                return
            visited.add(table)
            for dep in dependencies.get(table, set()):
                if dep in dependencies:
                    visit(dep)
            if table not in sorted_tables:
                sorted_tables.append(table)
        
        for table in tables:
            visit(table)
        
        return sorted_tables
    
    def get_table_info(self, table_name):
        """Get comprehensive information about a table."""
        return {
            'name': table_name,
            'columns': self.get_table_columns(table_name),
            'primary_keys': self.get_primary_keys(table_name),
            'foreign_keys': self.get_foreign_keys(table_name)
        }
    
    def get_session(self):
        """Get a new database session."""
        return self.Session()
    
    def close(self):
        """Close database connection."""
        self.engine.dispose()
