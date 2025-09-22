import { CommonModule } from '@angular/common';
import { Component, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Auth } from '../auth';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';

@Component({
  selector: 'app-login',
  imports: [FormsModule, CommonModule, MatCardModule,MatFormFieldModule,MatInputModule,MatButtonModule],
  templateUrl: './login.html',
  styleUrl: './login.scss'
})
export class Login {
  username = '';
  password = '';
  errorMessage = signal('');
  constructor(private auth: Auth) {}

  onLogin() {
    if (this.username && this.password)
    this.auth.login(this.username, this.password);
    this.auth.errorMessage.subscribe(msg => {
      this.errorMessage.set(msg);
    });
  }
}
