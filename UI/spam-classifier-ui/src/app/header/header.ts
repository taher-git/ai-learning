import { Component } from '@angular/core';
import { Auth } from '../auth';
import { RouterLink } from '@angular/router';
import { MatToolbar, MatToolbarModule } from '@angular/material/toolbar';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-header',
  imports: [RouterLink, MatToolbarModule, MatIconModule],
  templateUrl: './header.html',
  styleUrl: './header.scss'
})
export class Header {
  constructor(private auth: Auth) {}

  logout() {
    this.auth.logout();
  }
}
