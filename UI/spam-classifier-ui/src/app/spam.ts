import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class Spam {
  private apiUrl = 'http://127.0.0.1:8000/predict';

  constructor(private http: HttpClient) {}

  classify(text: string): Observable<{label: string, confidence: number}> {
    return this.http.post<{label: string, confidence: number}>(this.apiUrl, { text });
  }

}
