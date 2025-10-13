import { CommonModule } from '@angular/common';
import { AfterViewInit, Component, effect, ElementRef, Input, input, OnInit, signal, ViewChild } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { SummarizerService } from '../summarizer-service';
import { DocAssistantService } from '../doc-assistant-service';

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
export class Chat implements AfterViewInit , OnInit{
  @ViewChild('chatContainer') chatContainer!: ElementRef<HTMLDivElement>;
  // make this variable signal
  userInput: string = '';
  botTyping = signal(false);
  @Input() mode: 'api' | 'dummy' = 'api';
  @Input() from: 'meeting' | 'document' = 'meeting';

   messages = signal<Message[]>([]);
  constructor(private summarizerService: SummarizerService, private docAssistantService : DocAssistantService) {
    // auto scroll whenever messages or typing changes
    effect(() => {
      this.messages();
      this.botTyping();
      this.scrollToBottom();
    });
  }
  ngOnInit(): void {
    console.log("From : ", this.from);
    this.messages.set([
      { sender: 'bot', text: 'Hi! Ask me anything about the '+this.from+'.' }
    ]);
    this.docAssistantService.clearChat.subscribe(clear => {
      if(clear) {
        this.messages.set([
          { sender: 'bot', text: 'Hi! Ask me anything about the '+this.from+'.' }
        ]);
        this.docAssistantService.clearChat.next(false);
      }
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
    if(this.from === 'meeting'){
      this.callSummaryService(question);
    } else if(this.from === 'document'){
      this.callDocumentService(question);
    }
    // Clear input
    this.userInput = '';
  }

  callSummaryService(question: string) {
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
  }

  callDocumentService(question: string) {
    // if(!question || question.trim().length === 0) {
    //   question = "What does it says about Account class";
    //   this.messages.update(msgs => [...msgs, { sender: 'user', text: question}]);
    // }
    this.docAssistantService.askQuestion(question).subscribe({
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
  }
}
