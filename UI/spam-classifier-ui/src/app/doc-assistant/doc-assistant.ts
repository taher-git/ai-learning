import { Component, signal } from '@angular/core';
import { DocAssistantService } from '../doc-assistant-service';
import { Chat } from '../chat/chat';
import { MatCardModule } from '@angular/material/card';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatInputModule } from '@angular/material/input';
import { FormsModule } from '@angular/forms';
import { MatListModule } from '@angular/material/list';
import { MatRadioModule } from '@angular/material/radio';
import { DocList } from '../doc-list/doc-list';

@Component({
  selector: 'app-doc-assistant',
  imports: [Chat, MatCardModule,
    MatProgressSpinnerModule,
    CommonModule,
    MatButtonModule,
    MatInputModule,
    FormsModule,
    MatListModule,
    MatRadioModule,
    DocList],
  templateUrl: './doc-assistant.html',
  styleUrl: './doc-assistant.scss'
})
export class DocAssistant {
  uploadStatus = signal({} as any);
  loading = signal(false);
  showHistory = signal(false);
  docs = signal([] as any[]);
  constructor(private docAssistantService : DocAssistantService) {}

  ngOnInit() {
    this.docAssistantService.listAllDocs().subscribe(data => this.docs.set(data));
  }
  onFileSelected(event: any) {
    const files: File[] = event.target.files;
    this.upload(files)
  }

  upload(files: File[]) {
    this.loading.set(true);
    this.docAssistantService.uploadFiles(files).subscribe({
      next: (res) => {
        this.uploadStatus.set(res);
        this.loading.set(false);
      },
      error: (err) => {
        console.error(err);
        this.loading.set(false);
      }
    });
  }

  clearChatHistory(){
    this.docAssistantService.clearChat.next(true);
    this.docAssistantService.clearChatSession().subscribe({
      next: (res) => {
        alert(res.message);
      },
      error: (err) => {
        console.error(err);
        alert("Failed to clear chat session. Please try again.");
      }
    });
  }

  reset() {
    this.uploadStatus.set(null as any);
    this.loading.set(false);
  }
}
