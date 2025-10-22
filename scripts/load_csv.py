#!/usr/bin/env python3
"""
CSV Loader script for citi_db.
Loads CSV files from MockData exports into MySQL database.
"""
import sys
import os
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine, text
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config
from nl2sql.schema_reflector import SchemaReflector


def print_banner():
    print("=" * 80)
    print("  CSV Loader for citi_db")
    print("=" * 80)
    print()


def create_database_if_not_exists():
    """Create database if it doesn't exist."""
    base_url = f"mysql+pymysql://{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.DB_HOST}:{Config.DB_PORT}"
    engine = create_engine(base_url, echo=False)
    
    with engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {Config.DB_NAME}"))
        conn.commit()
    
    engine.dispose()
    print(f"✓ Database '{Config.DB_NAME}' ready")


def load_csv_to_table(csv_path, table_name, engine):
    """Load a CSV file into a database table."""
    try:
        df = pd.read_csv(csv_path)
        
        df.columns = df.columns.str.strip()
        
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        
        return len(df)
    except Exception as e:
        print(f"  ❌ Error loading {table_name}: {e}")
        return 0


def main():
    print_banner()
    
    print(f"Configuration:")
    print(f"  Database: {Config.DB_NAME}")
    print(f"  Host: {Config.DB_HOST}:{Config.DB_PORT}")
    print(f"  CSV Path: {Config.CSV_PATH}")
    print()
    
    try:
        print("Step 1: Creating database...")
        create_database_if_not_exists()
        print()
        
        print("Step 2: Connecting to database...")
        engine = create_engine(Config.get_database_url(), echo=False)
        print(f"  ✓ Connected to {Config.DB_NAME}")
        print()
        
        print("Step 3: Loading CSV files...")
        csv_dir = Path(Config.CSV_PATH)
        
        if not csv_dir.exists():
            print(f"  ❌ CSV directory not found: {csv_dir}")
            return 1
        
        csv_files = list(csv_dir.glob("*.csv"))
        if not csv_files:
            print(f"  ❌ No CSV files found in: {csv_dir}")
            return 1
        
        print(f"  Found {len(csv_files)} CSV files")
        
        total_records = 0
        for csv_file in sorted(csv_files):
            table_name = csv_file.stem
            print(f"  Loading {table_name}...", end=" ")
            count = load_csv_to_table(csv_file, table_name, engine)
            total_records += count
            print(f"✓ {count} records")
        
        print()
        print(f"  ✓ Total records loaded: {total_records}")
        print()
        
        print("Step 4: Verifying tables...")
        reflector = SchemaReflector()
        reflector.reflect_schema()
        tables = reflector.get_all_tables()
        print(f"  ✓ Found {len(tables)} tables: {', '.join(tables)}")
        print()
        
        print("=" * 80)
        print("  ✓ CSV loading completed successfully!")
        print("=" * 80)
        print()
        
        engine.dispose()
        return 0
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
