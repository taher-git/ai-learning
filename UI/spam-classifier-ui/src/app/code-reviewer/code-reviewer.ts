import { Component,signal } from '@angular/core';
import { CodeReviewerService } from '../code-reviewer-service';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatCardModule } from '@angular/material/card';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatInputModule } from '@angular/material/input';
import { FormsModule } from '@angular/forms';
import { MatListModule } from '@angular/material/list';
import { MatRadioModule } from '@angular/material/radio';
import { ReviewHistory } from '../review-history/review-history';

@Component({
  selector: 'app-code-reviewer',
  imports: [ 
    ReviewHistory,
    MatCardModule,
    MatProgressSpinnerModule,
    CommonModule,
    MatButtonModule,
    MatInputModule,
    FormsModule,
    MatListModule,
    MatRadioModule],
  templateUrl: './code-reviewer.html',
  styleUrl: './code-reviewer.scss'
})
export class CodeReviewer {
  reviewResult = signal({} as any);
  loading = signal(false);
  byCategoryFlag = signal('true');
  fileFormat = signal('pdf');
  showHistory = signal(false);

  constructor(private codeReviewerService : CodeReviewerService) {}

  onFileSelected(event: any) {
    const file: File = event.target.files[0];
    if (file && file.name.endsWith('.java')) {
      this.reset();
      this.codeReview(file);
    } else {
      alert('Please select a valid .java file.');
    }
  }
  codeReview(file: File) {
    this.loading.set(true);
    this.codeReviewerService.codeReview(file,this.byCategoryFlag()).subscribe({
      next: (res) => {
        this.reviewResult.set(res);
        this.loading.set(false);
      },
      error: (err) => {
        console.error(err);
        this.loading.set(false);
      }
    });
  }
  changeByCategoryFlag(value: string) {
    this.reset();
    this.byCategoryFlag.set(value);
  }

  changeFileFormat(value: string) {
    this.fileFormat.set(value);
  }

  downloadReport() {
    if (!this.reviewResult) return;
    // this.loading.set(true);
    this.codeReviewerService.downloadReport(this.reviewResult(), this.fileFormat(), this.byCategoryFlag()).subscribe({
      next: (res) => {
        const url = window.URL.createObjectURL(res);
        const a = document.createElement('a');
        a.href = url;
        a.download = this.fileFormat() === 'pdf' ? 'AI_Code_Review_Report.pdf' : 'AI_Code_Review_Report.txt';
        a.click();
        window.URL.revokeObjectURL(url);
        // this.loading.set(false);
      },
      error: (err) => {
        console.error('Download error:', err);
        // this.loading.set(false);
      }
    });
  }

  reset() {
    this.reviewResult.set(null as any);
    this.loading.set(false);
  }

}
