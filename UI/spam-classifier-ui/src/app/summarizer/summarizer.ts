import { Component, signal } from '@angular/core';
import { SummarizerService } from '../summarizer-service';
import { MatCardModule } from '@angular/material/card';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatInputModule } from '@angular/material/input';
import { FormsModule } from '@angular/forms';
import { MatListModule } from '@angular/material/list';
import { DummayData } from './dummyData';
import { MatRadioModule } from '@angular/material/radio';
import { MatTabChangeEvent, MatTabsModule } from '@angular/material/tabs';
import { Chat } from '../chat/chat';

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
    MatRadioModule,
    MatTabsModule,
    Chat
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
  answer = signal('');
  mode  = signal<'api' | 'dummy'>('api');
  constructor(private summarizerService: SummarizerService) {}

  onFileSelected(event: any, mode: 'api' | 'dummy') {
    this.reset();
    this.mode.set(mode);
    if(this.dummyCall()) return;
    const file: File = event.target.files[0];
    if (!file) return;
    this.loading.set(true);
    this.summarizerService.uploadFile(file).subscribe({
      next: (res) => {
        this.transcript.set(res.transcript);
        this.loading.set(false);
        this.loadSummary(this.summaryType());
      },
      error: (err) => {
        console.error(err);
        this.loading.set(false);
      }
    });
  }

  onTabChange(event: MatTabChangeEvent) {
    console.log('Tab changed to:', event.tab.textLabel);
        // Call other methods or perform actions based on the selected tab
        if (event.tab.id === "actions-tab") {
          if(!this.actionItem())
            this.loadActionItems();
        } else if (event.tab.id === "summary-tab") {
          if(!this.summary())
            this.loadSummary(this.summaryType());
        }
  }


  loadSummary(value: any) {
    this.summaryType.set(value)
    if(this.dummyCall()) return;
    this.loading.set(true);
      this.summarizerService.summarize(this.summaryType()).subscribe({
        next: (res) => {
          this.summary.set(res.summary);
          this.loading.set(false);
        },
        error: (err) => {
          console.error(err);
          this.loading.set(false);
        }
      });
  }

  loadActionItems() {
    console.log("Loading Action Items");
    if(this.dummyCall()) return;
  this.loading.set(true);
    this.summarizerService.actions().subscribe({
      next: (res) => {
        this.actionItem.set(res.action_items);
        this.loading.set(false);
      },
      error: (err) => {
        console.error(err);
        this.loading.set(false);
      }
    });
  }

  dummyCall(){
    if(this.mode() === 'dummy'){
      this.loadDummyData(); 
      return true;
    }
    return false;
  }

  loadDummyData() {
    this.loading.set(true);
    setTimeout(() => {
    this.transcript.set(DummayData.transcript);
    this.loading.set(false);
    if(this.summaryType() === 'paragraph'){
      this.summary.set(DummayData.summary);
    } else {
      this.summary.set(DummayData.summaryBullet);
    }
    this.actionItem.set(DummayData.action_items);
    }, 1000);
  }
  reset() { 
    this.transcript.set('');
    this.summary.set('');
    this.actionItem.set('');
    this.answer.set('');
  }
}
