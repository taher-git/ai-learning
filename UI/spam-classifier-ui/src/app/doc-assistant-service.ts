import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DocAssistantService {
  
  private uploadDoc = 'http://127.0.0.1:8003/upload-doc/';
  private uploadDocs = 'http://127.0.0.1:8003/upload-docs/';
  private qaApiUrl = 'http://127.0.0.1:8003/ask/';
  private qaMultiDocsUrl = 'http://127.0.0.1:8003/ask-multiple/';
  private listDocs = 'http://127.0.0.1:8003/list-docs/';
  private deleteDocs = 'http://127.0.0.1:8003/delete-doc/';
  private clearSession = 'http://127.0.0.1:8003/clear-session/';

  clearChat = new BehaviorSubject<boolean>(false);

  constructor(private http: HttpClient) {}

  upload(file: File): Observable<any> {
    const formData = new FormData();
    formData.append('file', file, file.name);
    return this.http.post<any>(`${this.uploadDoc}`, formData);
  }

  uploadFiles(files: File[]): Observable<any> {
    const formData = new FormData();
    for (let file of files) {
      formData.append('files', file);
    }
    return this.http.post<any>(`${this.uploadDocs}`, formData);
  }
  askQuestion(question: string): Observable<any> {
    const formData = new FormData();
    formData.append('question', question);
    return this.http.post<any>(`${this.qaMultiDocsUrl}`, formData);
  }
  listAllDocs(): Observable<any> {
    return this.http.get<any>(this.listDocs);
  }
  deleteDocument(docName : string){
    return this.http.delete<any>(`${this.deleteDocs}${docName}`);
  }

  clearChatSession(): Observable<any>{
    return this.http.post<any>(this.clearSession, {});
  }
}
