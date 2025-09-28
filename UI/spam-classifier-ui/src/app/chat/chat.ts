import { CommonModule } from '@angular/common';
import { AfterViewInit, Component, effect, ElementRef, Input, input, signal, ViewChild } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { SummarizerService } from '../summarizer-service';

interface Message {
  sender: 'user' | 'bot';
  text: string;
}

@Component({
  selector: 'app-chat',
  imports: [CommonModule,FormsModule],
  templateUrl: './chat.html',
  styleUrl: './chat.scss'
})
export class Chat implements AfterViewInit {
  @ViewChild('chatContainer') chatContainer!: ElementRef<HTMLDivElement>;
  // make this variable signal
 messages = signal<Message[]>([
    { sender: 'bot', text: 'Hi! Ask me anything about the meeting.' }
  ]);

  userInput: string = '';
  botTyping = signal(false);
  @Input() mode: 'api' | 'dummy' = 'api';
  constructor(private summarizerService: SummarizerService) {
    // auto scroll whenever messages or typing changes
    effect(() => {
      this.messages();
      this.botTyping();
      this.scrollToBottom();
    });
  }

  ngAfterViewInit() {
    this.scrollToBottom();
  }


  private scrollToBottom() {
    if (this.chatContainer) {
      setTimeout(() => {
        const el = this.chatContainer.nativeElement;
        el.scrollTop = el.scrollHeight;
      }, 0);
    }
  }
  sendMessage() {
    if (!this.userInput.trim()) return;

    // Push user message
    this.messages.update(msgs => [...msgs, { sender: 'user', text: this.userInput }]);
   // show typing loader
    this.botTyping.set(true);
    // Simulate bot reply (later you’ll connect this to your backend / LangChain API)
    const question = this.userInput;
    if(this.mode === 'dummy'){
      // hide typing loader
      setTimeout(() => {
        this.botTyping.set(false);
        this.messages.update(msgs => [...msgs, { sender: 'bot', text: `You asked: "${question}"` }]);
      }, 1000);
      this.userInput = '';
      return;
    }
    this.summarizerService.askQuestion(question).subscribe({
      next: (res) => {
        this.botTyping.set(false);
        this.messages.update(msgs => [...msgs, { sender: 'bot', text: res.answer }]);
      },
      error: (err) => {
        console.error(err);
        this.botTyping.set(false);
        this.messages.update(msgs => [...msgs, { sender: 'bot', text: 'Sorry, something went wrong. Please try again later.' }]);
      }
    });
    // Clear input
    this.userInput = '';
  }
}
