import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {Observable, of, tap, throwError} from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import {Router} from '@angular/router';

@Injectable({
  providedIn: 'root', // This makes the service a singleton accessible throughout the app
})

export class AuthService {
  private accessTokenKey = 'access_token'; // Key for storing the access token in localStorage
  private refreshTokenKey = 'refresh_token'; // Key for storing the refresh token in localStorage

  constructor(private http: HttpClient, private router: Router) {} // Inject the HttpClient and Router services

  // login(credentials: { email: string; password: string }): Observable<any> {
  //   return this.http.post<{ access: string; refresh: string }>(
  //     '/api/login/',
  //     credentials
  //   ).pipe(
  //     tap((tokens) => {
  //       this.saveTokens(tokens);
  //     })
  //   );
  // }

  register(data: { email: string; password: string }): Observable<any> {
    return this.http.post('/api/register/', data);
  }

  // Get the access token from localStorage
  getAccessToken(): string | null {
    return localStorage.getItem(this.accessTokenKey);
  }

  // Save the access token to localStorage
  saveAccessToken(token: string): void {
    localStorage.setItem(this.accessTokenKey, token);
  }

  // Get the refresh token from localStorage
  getRefreshToken(): string | null {
    return localStorage.getItem(this.refreshTokenKey);
  }

  // Refresh the access token using the refresh token
  refreshToken(): Observable<string> {
    const refreshToken = this.getRefreshToken();

    if (!refreshToken) {
      console.error('Refresh token is missing.');
      return throwError(() => new Error('Refresh token is missing.'));
    }

    return this.http.post<{ access: string }>('/api/token/refresh/', { refresh: refreshToken }).pipe(
      map((response) => response.access), // Extract the new access token from the response
      catchError((error) => {
        console.error('Error refreshing token:', error.message);
        return throwError(() => error);
      })
    );
  }

  // Logout the user by blacklisting the refresh token
  logout(): Observable<void> {
    const refreshToken = this.getRefreshToken();
    // If no refresh token exists, simply clear the tokens locally
    if (!refreshToken) {
      console.info('No refresh token to blacklist.');
      this.clearTokens();
      return of(); // Return an empty observable to avoid errors
    }

    // Send the refresh token to the backend to blacklist it
    return this.http.post('/api/logout/', { refresh: refreshToken }).pipe(
      catchError((error) => {
        console.error('Error during logout:', error);
        return throwError(() => error);
      }),
      // On successful logout, clear tokens from localStorage
      map(() => {
        this.clearTokens();
      })
    );
  }

  // Private helper method to clear tokens from localStorage
  private clearTokens(): void {
    localStorage.removeItem(this.accessTokenKey);
    localStorage.removeItem(this.refreshTokenKey);
  }

  exchangeCodeForTokens(code: string): Observable<void> {
    return this.http.post<void>('/api/oauth/exchange/', { code });
  }
}
