import { Routes } from '@angular/router';
import { LandingPageComponent } from './pages/landing-page/landing-page.component';
import { LoginPageComponent } from './pages/login-page/login-page.component';
import { RegisterPageComponent } from './pages/register-page/register-page.component';
import { DashboardPageComponent } from './pages/dashboard-page/dashboard-page.component';
import {AuthCallbackComponent} from './pages/auth-callback/auth-callback.component';
import { AuthGuard } from './guards/auth.guard';

export const routes: Routes = [
  { path: '', component: LandingPageComponent }, // Strona główna
  { path: 'login', component: LoginPageComponent }, // Logowanie
  { path: 'register', component: RegisterPageComponent }, // Rejestracja
  { path: 'dashboard', component: DashboardPageComponent, canActivate: [AuthGuard] }, // Panel użytkownika
  { path: 'auth/callback', component: AuthCallbackComponent }, // Obsługa callbacku OAuth
  { path: '**', redirectTo: '' }, // Przekierowanie dla nieistniejących ścieżek
];
