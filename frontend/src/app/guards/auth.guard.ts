import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { AuthService } from '../services/auth.service';

export const AuthGuard: CanActivateFn = (route, state) => {
  const authService = inject(AuthService); // Wstrzykiwanie AuthService
  const router = inject(Router); // Wstrzykiwanie Router

  // if (authService.isAuthenticated()) {
  //   return true; // Zezwól na dostęp
  // }

  // Jeśli użytkownik nie jest zalogowany, przekieruj na stronę logowania
  router.navigate(['/login']);
  return false; // Zablokuj dostęp
};
