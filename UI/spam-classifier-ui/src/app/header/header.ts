import { Component } from '@angular/core';
import { Auth } from '../auth';
import { RouterLink } from '@angular/router';
import { MatToolbar, MatToolbarModule } from '@angular/material/toolbar';
import { MatIconModule } from '@angular/material/icon';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';

@Component({
  selector: 'app-header',
  imports: [RouterLink, MatToolbarModule, MatIconModule, MatSlideToggleModule],
  templateUrl: './header.html',
  styleUrl: './header.scss'
})
export class Header {
  isDarkMode = false;

  toggleTheme() {
    this.isDarkMode = !this.isDarkMode;
    if (this.isDarkMode) {
      document.body.classList.add('dark-theme');
    } else {
      document.body.classList.remove('dark-theme');
    }
  }

  constructor(private auth: Auth) {}

  logout() {
    this.auth.logout();
  }
}
