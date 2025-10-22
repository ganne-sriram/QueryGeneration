#!/usr/bin/env python3
"""
Schema extraction script for citi_db.
Generates schema.json and ERD.md artifacts.
"""
import sys
import os
import json
from pathlib import Path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config
from nl2sql.schema_reflector import SchemaReflector


def print_banner():
    print("=" * 80)
    print("  Schema Extraction for citi_db")
    print("=" * 80)
    print()


def extract_schema_json(reflector, output_path):
    """Extract schema information to JSON."""
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
                    'nullable': col['nullable'],
                    'default': str(col['default']) if col['default'] is not None else None
                }
                for col in columns
            ],
            'primary_keys': primary_keys,
            'foreign_keys': [
                {
                    'constrained_columns': fk['constrained_columns'],
                    'referred_table': fk['referred_table'],
                    'referred_columns': fk['referred_columns']
                }
                for fk in foreign_keys
            ]
        }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(schema, f, indent=2)
    
    return schema


def generate_erd_markdown(reflector, schema, output_path):
    """Generate ERD in Markdown format."""
    tables = reflector.get_all_tables()
    
    erd = []
    erd.append("# Entity Relationship Diagram - citi_db\n")
    erd.append(f"**Total Tables:** {len(tables)}\n")
    erd.append("---\n")
    
    for table_name in sorted(tables):
        table_info = schema[table_name]
        erd.append(f"\n## {table_name}\n")
        
        erd.append("### Columns\n")
        erd.append("| Column | Type | Nullable | Default |\n")
        erd.append("|--------|------|----------|----------|\n")
        
        for col in table_info['columns']:
            nullable = "Yes" if col['nullable'] else "No"
            default = col['default'] if col['default'] else "-"
            erd.append(f"| {col['name']} | {col['type']} | {nullable} | {default} |\n")
        
        if table_info['primary_keys']:
            erd.append(f"\n**Primary Keys:** {', '.join(table_info['primary_keys'])}\n")
        
        if table_info['foreign_keys']:
            erd.append("\n### Foreign Keys\n")
            for fk in table_info['foreign_keys']:
                constrained = ', '.join(fk['constrained_columns'])
                referred = ', '.join(fk['referred_columns'])
                erd.append(f"- `{constrained}` → `{fk['referred_table']}.{referred}`\n")
        
        erd.append("\n---\n")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(erd)


def main():
    print_banner()
    
    print(f"Configuration:")
    print(f"  Database: {Config.DB_NAME}")
    print(f"  Host: {Config.DB_HOST}:{Config.DB_PORT}")
    print()
    
    try:
        print("Step 1: Connecting to database and reflecting schema...")
        reflector = SchemaReflector()
        reflector.reflect_schema()
        tables = reflector.get_all_tables()
        print(f"  ✓ Found {len(tables)} tables")
        print()
        
        artifacts_dir = Path("artifacts")
        artifacts_dir.mkdir(exist_ok=True)
        
        print("Step 2: Extracting schema to JSON...")
        schema_json_path = artifacts_dir / "citi_db_schema.json"
        schema = extract_schema_json(reflector, schema_json_path)
        print(f"  ✓ Schema JSON saved to: {schema_json_path}")
        print()
        
        print("Step 3: Generating ERD markdown...")
        erd_path = artifacts_dir / "citi_db_erd.md"
        generate_erd_markdown(reflector, schema, erd_path)
        print(f"  ✓ ERD saved to: {erd_path}")
        print()
        
        print("=" * 80)
        print("  ✓ Schema extraction completed successfully!")
        print("=" * 80)
        print()
        print("Output files:")
        print(f"  - Schema JSON: {schema_json_path}")
        print(f"  - ERD: {erd_path}")
        print()
        
        reflector.close()
        return 0
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
