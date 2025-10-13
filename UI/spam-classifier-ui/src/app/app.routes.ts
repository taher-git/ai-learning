import { Routes } from '@angular/router';
import { Login } from './login/login';
import { authGuard } from './auth-guard';
import { Home } from './home/home';
import { SpamCheck } from './spam-check/spam-check';
import { Summarizer } from './summarizer/summarizer';
import { CodeReviewer } from './code-reviewer/code-reviewer';
import { DocAssistant } from './doc-assistant/doc-assistant';
import { Welcome } from './welcome/welcome';

export const routes: Routes = [
  { path: 'login', component: Login },
  { path: 'home', component: Home, canActivate: [authGuard],children: [
      { path: 'spam-check', component: SpamCheck, canActivate: [authGuard]},
      { path: 'summarize-meeting', component: Summarizer, canActivate: [authGuard]},
      { path: 'code-review', component: CodeReviewer, canActivate: [authGuard]},
      { path: 'doc-assistant', component: DocAssistant, canActivate: [authGuard]},
      { path: '', component: Welcome, canActivate: [authGuard],pathMatch: 'full' }
  ]},
  { path: '', redirectTo: 'home', pathMatch: 'full' }
];
