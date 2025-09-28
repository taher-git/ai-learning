import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SummarizerService {
  private uploadUrl = 'http://127.0.0.1:8000/upload/';
  private summarizeUrl = 'http://127.0.0.1:8000/summarize/';
  private actionUrl = 'http://127.0.0.1:8000/actions/';
  private qaApiUrl = 'http://127.0.0.1:8000/ask/';

  constructor(private http: HttpClient) {}

  uploadFile(file: File): Observable<any> {
    const formData = new FormData();
    formData.append('file', file);
    return this.http.post<any>(`${this.uploadUrl}`, formData);
  }

  summarize( summaryType: 'bullet' | 'paragraph'): Observable<any> {
    const formData = new FormData();
    formData.append('summary_type', summaryType);
    return this.http.post<any>(`${this.summarizeUrl}`, formData);
  }
  
  actions(): Observable<any> {
    const formData = new FormData();
    return this.http.get<any>(`${this.actionUrl}`);
  }

  askQuestion(question: string): Observable<any> {
     const formData = new FormData();
    formData.append('question', question);
    return this.http.post<any>(`${this.qaApiUrl}`, formData);
  }
}
