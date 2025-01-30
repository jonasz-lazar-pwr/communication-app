import {
  HttpEvent,
  HttpHandlerFn,
  HttpRequest,
  HttpInterceptorFn,
  HttpErrorResponse,
} from '@angular/common/http';
import { inject } from '@angular/core';
import { Observable, throwError } from 'rxjs';
import { catchError, switchMap } from 'rxjs/operators';
import { AuthService } from '../services/auth.service';
import { environment } from '../../environments/environment';

export const AuthInterceptor: HttpInterceptorFn = (req: HttpRequest<any>, next: HttpHandlerFn): Observable<HttpEvent<any>> => {
  const authService = inject(AuthService); // Dependency injection for AuthService
  const apiUrl = environment.apiUrl; // Get base API URL from environment configuration

  // Add access token to the Authorization header if it exists
  const token = authService.getAccessToken();
  if (token) {
    req = req.clone({
      setHeaders: {
        Authorization: `Bearer ${token}`,
      },
    });
  }

  // Add base URL to the request if it does not already include a full URL
  if (!req.url.startsWith('http')) {
    req = req.clone({
      url: `${apiUrl}${req.url}`,
    });
  }

  // Handle the HTTP request and any errors
  return next(req).pipe(
    catchError((error: HttpErrorResponse) => {
      switch (error.status) {
        case 401: // Unauthorized
          console.warn('Access token has expired. Attempting to refresh...');
          return authService.refreshToken().pipe(
            switchMap((newToken: string) => {
              console.log('Access token refreshed. Retrying request...');
              authService.saveAccessToken(newToken); // Save the new access token
              req = req.clone({
                setHeaders: {
                  Authorization: `Bearer ${newToken}`,
                },
              });
              return next(req); // Retry the request with the new token
            }),
            catchError(() => {
              console.error('Failed to refresh token. Logging out user...');
              authService.logout(); // Logout the user if token refresh fails
              return throwError(() => error); // Propagate the error
            })
          );
        case 403: // Forbidden
          console.error('Access forbidden: You do not have permission to access this resource.');
          break;
        case 404: // Not Found
          console.error('Resource not found: The requested resource does not exist.');
          break;
        case 408: // Request Timeout
          console.error('Request timeout: The server took too long to respond.');
          break;
        case 500: // Internal Server Error
          console.error('Server error: An unexpected error occurred on the server.');
          break;
        default:
          console.error(`Unexpected HTTP error (${error.status}): ${error.message}`);
          break;
      }
      return throwError(() => error); // Propagate the error for further handling
    })
  );
};
