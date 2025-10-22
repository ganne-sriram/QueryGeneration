#!/usr/bin/env python3
"""
Evaluation script for NL2SQL query generation.
Tests query generation against citi_db examples.
"""
import sys
import os
import json
from pathlib import Path
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nl2sql.query_generator import QueryGenerator


def print_banner():
    print("=" * 80)
    print("  NL2SQL Evaluation for citi_db")
    print("=" * 80)
    print()


def is_valid_sql(sql):
    """Check if SQL is syntactically valid (basic check)."""
    if not sql or not sql.strip():
        return False
    
    sql_lower = sql.lower().strip()
    
    if not sql_lower.startswith('select'):
        return False
    
    if 'from' not in sql_lower:
        return False
    
    dangerous_keywords = ['drop', 'delete', 'insert', 'update', 'alter', 'create', 'truncate']
    for keyword in dangerous_keywords:
        if keyword in sql_lower:
            return False
    
    return True


def can_execute(generator, sql):
    """Try to execute SQL and return success status."""
    try:
        result = generator.execute_query(sql)
        return True
    except Exception as e:
        return False


def evaluate_queries(examples_file):
    """Evaluate all queries in the examples file."""
    print(f"Loading examples from: {examples_file}")
    
    with open(examples_file, 'r') as f:
        examples = json.load(f)
    
    print(f"  ✓ Loaded {len(examples)} test queries")
    print()
    
    print("Initializing query generator...")
    generator = QueryGenerator()
    print("  ✓ Generator ready")
    print()
    
    print("Running evaluation...")
    print("-" * 80)
    
    results = []
    syntactic_valid = 0
    execution_success = 0
    
    for i, example in enumerate(examples, 1):
        question = example['question']
        expected_tables = example.get('expected_tables', [])
        
        print(f"\n[{i}/{len(examples)}] {question}")
        
        try:
            start_time = time.time()
            sql = generator.generate_sql(question)
            gen_time = time.time() - start_time
            
            is_valid = is_valid_sql(sql)
            if is_valid:
                syntactic_valid += 1
                print(f"  ✓ Valid SQL generated ({gen_time:.2f}s)")
            else:
                print(f"  ✗ Invalid SQL generated")
            
            can_exec = False
            if is_valid:
                can_exec = can_execute(generator, sql)
                if can_exec:
                    execution_success += 1
                    print(f"  ✓ Execution successful")
                else:
                    print(f"  ✗ Execution failed")
            
            tables_used = generator.get_tables_from_sql(sql)
            
            results.append({
                'id': example['id'],
                'question': question,
                'sql': sql,
                'syntactically_valid': is_valid,
                'execution_success': can_exec,
                'tables_used': tables_used,
                'expected_tables': expected_tables,
                'generation_time': gen_time
            })
            
            print(f"  SQL: {sql[:100]}{'...' if len(sql) > 100 else ''}")
            print(f"  Tables: {', '.join(tables_used) if tables_used else 'None detected'}")
            
        except Exception as e:
            print(f"  ✗ Error: {e}")
            results.append({
                'id': example['id'],
                'question': question,
                'sql': None,
                'syntactically_valid': False,
                'execution_success': False,
                'tables_used': [],
                'expected_tables': expected_tables,
                'error': str(e)
            })
    
    print()
    print("=" * 80)
    print("  Evaluation Summary")
    print("=" * 80)
    print()
    
    total = len(examples)
    syntactic_pct = (syntactic_valid / total) * 100
    execution_pct = (execution_success / total) * 100
    
    print(f"Total Queries:           {total}")
    print(f"Syntactically Valid:     {syntactic_valid} ({syntactic_pct:.1f}%)")
    print(f"Execution Success:       {execution_success} ({execution_pct:.1f}%)")
    print()
    
    print("Target Metrics:")
    print(f"  Syntactic Validity:    ≥90% {'✓' if syntactic_pct >= 90 else '✗'} (Actual: {syntactic_pct:.1f}%)")
    print(f"  Execution Success:     ≥80% {'✓' if execution_pct >= 80 else '✗'} (Actual: {execution_pct:.1f}%)")
    print()
    
    results_file = Path("tests/evaluation_results.json")
    with open(results_file, 'w') as f:
        json.dump({
            'summary': {
                'total': total,
                'syntactically_valid': syntactic_valid,
                'syntactic_validity_pct': syntactic_pct,
                'execution_success': execution_success,
                'execution_success_pct': execution_pct,
                'meets_targets': syntactic_pct >= 90 and execution_pct >= 80
            },
            'results': results
        }, f, indent=2)
    
    print(f"Results saved to: {results_file}")
    print()
    
    return syntactic_pct >= 90 and execution_pct >= 80


def main():
    print_banner()
    
    examples_file = Path("tests/citi_db_examples.json")
    
    if not examples_file.exists():
        print(f"❌ Examples file not found: {examples_file}")
        return 1
    
    try:
        success = evaluate_queries(examples_file)
        
        if success:
            print("✓ All target metrics met!")
            return 0
        else:
            print("⚠ Some target metrics not met. Review results for details.")
            return 0
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
