import { Component, signal } from '@angular/core';
import { SummarizerService } from '../summarizer-service';
import { MatCardModule } from '@angular/material/card';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatInputModule } from '@angular/material/input';
import { FormsModule } from '@angular/forms';
import { MatListModule } from '@angular/material/list';
// import { DummayData } from './dummyData';
import { MatRadioModule } from '@angular/material/radio';

@Component({
  selector: 'app-summarizer',
  imports: [
    MatCardModule,
    MatProgressSpinnerModule,
    CommonModule,
    MatButtonModule,
    MatInputModule,
    FormsModule,
    MatListModule,
    MatRadioModule
  ],
  templateUrl: './summarizer.html',
  styleUrl: './summarizer.scss'
})
export class Summarizer {
  transcript = signal('');
  summary = signal('');
  loading = signal(false);
  actionItem  = signal('');
  showFullTranscript = signal(false);
  summaryType = signal<'bullet' | 'paragraph'>('paragraph');

  constructor(private summarizerService: SummarizerService) {}

  onFileSelected(event: any, mode: 'local' | 'api') {
    if(mode === 'api'){
      // this.loadDummyData(); //Enable this line to load dummy data without calling API, Create dummyData.ts file in the same folder with transcript, summary and action_items variables
      return;
    }
    const file: File = event.target.files[0];
    if (!file) return;
    this.loading.set(true);
    this.summarizerService.uploadFile(file, mode, this.summaryType()).subscribe({
      next: (res) => {
        this.transcript.set(res.transcript);
        this.summary.set(res.summary);
        this.actionItem.set(res.action_items);
        this.loading.set(false);
      },
      error: (err) => {
        console.error(err);
        this.loading.set(false);
      }
    });
  }

  // loadDummyData() {
  //   this.transcript.set(DummayData.transcript);
  //   if(this.summaryType() === 'paragraph'){
  //     this.summary.set(DummayData.summary);
  //   } else {
  //     this.summary.set(DummayData.summaryBullet);
  //   }
  //   this.actionItem.set(DummayData.action_items);
  // }
}
