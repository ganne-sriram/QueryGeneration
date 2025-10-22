#!/usr/bin/env python3
"""
CLI wrapper for NL2SQL query generation.
Provides command-line interface matching textToSql invocation style.
"""
import sys
import os
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from query_generator import QueryGenerator


def main():
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python cli.py <question>")
        print("Example: python cli.py 'How many customers are there?'")
        return 1
    
    question = ' '.join(sys.argv[1:])
    
    try:
        generator = QueryGenerator()
        result = generator.generate_and_execute(question)
        
        print(json.dumps(result, indent=2))
        return 0
        
    except Exception as e:
        print(json.dumps({
            'error': str(e),
            'question': question
        }), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
