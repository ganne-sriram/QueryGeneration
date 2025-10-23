import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { environment } from '../environments/environment';

interface QueryResponse {
  question: string;
  sql: string;
  tables_used: string[];
  result: any;
  error: string | null;
}

interface SchemaTable {
  columns: Array<{
    name: string;
    type: string;
    nullable: boolean;
  }>;
  primary_keys: string[];
  foreign_keys: any[];
}

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'Query Generation';
  
  question = '';
  loading = false;
  queryResponse: QueryResponse | null = null;
  
  schema: { [key: string]: SchemaTable } = {};
  schemaLoading = false;
  selectedTable: string | null = null;
  
  activeTab: 'query' | 'schema' = 'query';
  
  constructor(private http: HttpClient) {}
  
  ngOnInit() {
    this.loadSchema();
  }
  
  loadSchema() {
    this.schemaLoading = true;
    this.http.get<{ [key: string]: SchemaTable }>(`${environment.apiUrl}/schema`)
      .subscribe({
        next: (data) => {
          this.schema = data;
          this.schemaLoading = false;
        },
        error: (error) => {
          console.error('Error loading schema:', error);
          this.schemaLoading = false;
        }
      });
  }
  
  onKeyDown(event: KeyboardEvent) {
    if (event.key === 'Enter' && event.ctrlKey) {
      event.preventDefault();
      this.generateSQL();
    }
  }

  generateSQL() {
    if (!this.question.trim()) {
      return;
    }
    
    this.loading = true;
    this.queryResponse = null;
    
    this.http.post<QueryResponse>(`${environment.apiUrl}/query`, { question: this.question })
      .subscribe({
        next: (response) => {
          this.queryResponse = response;
          this.loading = false;
        },
        error: (error) => {
          console.error('Error generating SQL:', error);
          this.queryResponse = {
            question: this.question,
            sql: '',
            tables_used: [],
            result: null,
            error: error.message || 'Failed to generate SQL'
          };
          this.loading = false;
        }
      });
  }
  
  copySQL() {
    if (this.queryResponse?.sql) {
      navigator.clipboard.writeText(this.queryResponse.sql);
    }
  }
  
  downloadCSV() {
    if (!this.queryResponse?.result) {
      return;
    }
    
    const result = this.queryResponse.result;
    let csvContent = '';
    
    let data: any[] = [];
    if (typeof result === 'string') {
      const lines = result.split('\n').filter(line => line.trim());
      if (lines.length > 0) {
        csvContent = lines.join('\n');
      }
    } else if (Array.isArray(result)) {
      if (result.length > 0) {
        const headers = Object.keys(result[0]);
        csvContent = headers.join(',') + '\n';
        csvContent += result.map(row => 
          headers.map(h => JSON.stringify(row[h] || '')).join(',')
        ).join('\n');
      }
    }
    
    if (csvContent) {
      const blob = new Blob([csvContent], { type: 'text/csv' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'query_results.csv';
      a.click();
      window.URL.revokeObjectURL(url);
    }
  }
  
  selectTable(tableName: string) {
    this.selectedTable = this.selectedTable === tableName ? null : tableName;
  }
  
  getTableNames(): string[] {
    return Object.keys(this.schema).sort();
  }
  
  formatResult(result: any): string {
    if (!result) {
      return 'No results';
    }

    if (typeof result === 'string') {
      return result;
    }

    if (Array.isArray(result)) {
      if (result.length === 0) {
        return 'No results';
      }

      const headers = Object.keys(result[0]);
      let output = headers.join(' | ') + '\n';
      output += headers.map(() => '---').join(' | ') + '\n';
      output += result.slice(0, 100).map(row =>
        headers.map(h => row[h] || '').join(' | ')
      ).join('\n');

      if (result.length > 100) {
        output += `\n... (${result.length - 100} more rows)`;
      }

      return output;
    }

    return JSON.stringify(result, null, 2);
  }

  isArrayResult(result: any): boolean {
    return Array.isArray(result) && result.length > 0;
  }

  getResultHeaders(result: any): string[] {
    if (this.isArrayResult(result)) {
      return Object.keys(result[0]);
    }
    return [];
  }

  getResultRows(result: any): any[] {
    if (this.isArrayResult(result)) {
      return result.slice(0, 100); // Show first 100 rows
    }
    return [];
  }

  hasMoreRows(result: any): boolean {
    return Array.isArray(result) && result.length > 100;
  }

  getRemainingRowCount(result: any): number {
    if (Array.isArray(result)) {
      return result.length - 100;
    }
    return 0;
  }
}
