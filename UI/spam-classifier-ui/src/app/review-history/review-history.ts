import { Component, signal } from '@angular/core';
import { CodeReviewerService } from '../code-reviewer-service';
import { MatCardModule } from '@angular/material/card';
import { MatTableModule } from '@angular/material/table';

@Component({
  selector: 'app-review-history',
  imports: [MatCardModule, MatTableModule],
  templateUrl: './review-history.html',
  styleUrl: './review-history.scss'
})
export class ReviewHistory {
reviews = signal([] as any[]);
constructor(private codeReviewerService : CodeReviewerService) {}
ngOnInit() {
    this.codeReviewerService.reviewHistory().subscribe(data => this.reviews.set(data));
  }

  view(review: any) {
    alert(JSON.stringify(review, null, 2));
  }

  delete(review: any) {
    this.codeReviewerService.deleteReviewHistory(review.id).subscribe({
       next: (res) => {
        alert(res.message);
        this.reviews.set(this.reviews().filter(r => r.id !== review.id));
      },
      error: (err) => {
        alert(err.error);
      }
    });
  }
}
