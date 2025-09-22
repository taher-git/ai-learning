import { HttpClient } from '@angular/common/http';
import { Injectable, signal } from '@angular/core';
import { Router } from '@angular/router';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class Auth {
  private apiUrl = 'http://localhost:8000/auth'; // your backend login endpoint
  isLoggedIn = signal(false);
  errorMessage = new BehaviorSubject<string>('');
  

  constructor(private http: HttpClient, private router: Router) {
    this.isLoggedIn.set(!!localStorage.getItem('token'));
  }
  login(username: string, password: string) {
    const requestBody = {
      username: username,
      password: password
    }
    this.errorMessage.next('');
    return this.http.post<{ token: string }>(`${this.apiUrl}/login`, requestBody)
      .subscribe({
        next: (res) => {
          localStorage.setItem('token', res.token);
          this.isLoggedIn.set(true);
          this.rediectToHome();
        },
        error: (err) => {
          // localStorage.setItem('token', "res.token");
          // this.isLoggedIn.set(true);
          // this.rediectToHome();
          console.error('Login failed', err)
          this.errorMessage.next('Login failed: ' + (err.error?.detail));
        }
      });
  }

  logout() {
    localStorage.removeItem('token');
    this.isLoggedIn.set(false);
    this.router.navigate(['/login']);
  }

  getToken(): string | null {
    return localStorage.getItem('token');
  }

  rediectToHome() {
    this.router.navigate(['/home']);
  }

}
