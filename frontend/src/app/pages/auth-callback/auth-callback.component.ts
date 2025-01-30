import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import {AuthService} from '../../services/auth.service';

@Component({
  selector: 'app-auth-callback',
  imports: [],
  templateUrl: './auth-callback.component.html',
  styleUrl: './auth-callback.component.css'
})
export class AuthCallbackComponent implements OnInit {
  constructor(private route: ActivatedRoute, private authService: AuthService, private router: Router) {}

  ngOnInit(): void {
    // Pobierz kod autoryzacyjny z URL-a
    const code = this.route.snapshot.queryParamMap.get('code');
    if (code) {
      // Prześlij kod do backendu w celu wymiany na tokeny
      this.authService.exchangeCodeForTokens(code).subscribe({
        next: () => this.router.navigate(['/dashboard']), // Przekierowanie na dashboard po zalogowaniu
        error: () => this.router.navigate(['/login']), // Przekierowanie na login w przypadku błędu
      });
    } else {
      this.router.navigate(['/login']); // Jeśli brak kodu, wróć na stronę logowania
    }
  }
}
