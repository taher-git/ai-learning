import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CodeReviewerService {

    private review = 'http://127.0.0.1:8002/review/';
    private review_category = 'http://127.0.0.1:8002/review_category/';
    private download_report = 'http://127.0.0.1:8002/download-report/';
    private review_history = 'http://127.0.0.1:8002/review-history/';

    constructor(private http: HttpClient) {}

    codeReview(file: File, byCategoryFlag: string): Observable<any> {
      const url = byCategoryFlag == 'true' ? this.review_category : this.review;
      const formData = new FormData();
      formData.append('file', file, file.name);
      return this.http.post<any>(`${url}`, formData);
    }

    downloadReport(reviewResult:string, format: string, byCategory: string) {
      const blob = new Blob([JSON.stringify(reviewResult)], { type: 'application/json' });
      const formData = new FormData();
      formData.append('file', blob, 'review.json');
      formData.append('format', format);
      formData.append('byCategory', byCategory);
      return this.http.post(this.download_report, formData, { responseType: 'blob' });
    }

    reviewHistory(){
      return this.http.get<any[]>(this.review_history);
    }

    deleteReviewHistory(reviewId : string){
      return this.http.delete<any>(`${this.review_history}${reviewId}`);
    }

}
