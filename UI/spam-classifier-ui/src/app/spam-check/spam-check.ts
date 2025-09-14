import { CommonModule } from '@angular/common';
import { Component, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Spam } from '../spam';
import { MatButtonModule } from '@angular/material/button';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatCardModule } from '@angular/material/card';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';

@Component({
  selector: 'app-spam-check',
  imports: [CommonModule, FormsModule,
    MatCardModule, MatFormFieldModule, MatInputModule, MatButtonModule, MatProgressSpinnerModule
  ],
  templateUrl: './spam-check.html',
  styleUrl: './spam-check.scss'
})
export class SpamCheck {
  emailText = '';
  result = signal<{label: string, confidence: number} | null>(null);
  loading = signal(false);
  constructor(private spamService: Spam) {}

  onSubmit() {
    this.loading.set(true);
    this.result.set(null);
    console.log('Email text submitted:', this.emailText);
    this.spamService.classify(this.emailText).subscribe(
      res => {
        this.loading.set(false);
        this.result.set(res);
        console.log('Classification result:', res);
      },
      err => {
        this.loading.set(false);
        console.error('Error:', err)
      }
    );
  }
}
