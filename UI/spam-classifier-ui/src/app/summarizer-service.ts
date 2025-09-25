import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SummarizerService {
  private apiUrl = 'http://127.0.0.1:8000/summarize/';

  constructor(private http: HttpClient) {}

  uploadFile(file: File, mode: 'local' | 'api', summaryType: 'bullet' | 'paragraph'): Observable<any> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('summary_type', summaryType);


    return this.http.post<any>(`${this.apiUrl}?mode=${mode}`, formData);
  }
}
