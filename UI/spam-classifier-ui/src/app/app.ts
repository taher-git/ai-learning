import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { SpamCheck } from './spam-check/spam-check';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet,SpamCheck],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  protected readonly title = signal('spam-classifier-ui');
}
