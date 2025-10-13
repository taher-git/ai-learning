import { Component, signal } from '@angular/core';
import { CodeReviewerService } from '../code-reviewer-service';
import { MatCardModule } from '@angular/material/card';
import { MatTableModule } from '@angular/material/table';
import { DocAssistantService } from '../doc-assistant-service';

@Component({
  selector: 'app-doc-list',
  imports: [MatCardModule, MatTableModule],
  templateUrl: './doc-list.html',
  styleUrl: './doc-list.scss'
})
export class DocList {
docs = signal([] as any[]);
constructor(private docService : DocAssistantService) {}
ngOnInit() {
    this.docService.listAllDocs().subscribe(data => this.docs.set(data));
  }

  // view(review: any) {
  //   alert(JSON.stringify(review, null, 2));
  // }

  delete(doc: any) {
    this.docService.deleteDocument(doc).subscribe({
       next: (res) => {
        alert(res.message);
        this.docs.set(this.docs().filter(d => d.filename !== doc));
      },
      error: (err) => {
        alert(err.error);
      }
    });
  }
}
