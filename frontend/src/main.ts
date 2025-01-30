import { bootstrapApplication } from '@angular/platform-browser';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { AppComponent } from './app/app.component';
import { AuthInterceptor } from './app/interceptors/auth.interceptor';
import { appConfig } from './app/app.config';

bootstrapApplication(AppComponent, {
  providers: [
    provideHttpClient(
      withInterceptors([AuthInterceptor])
    ),
    ...appConfig.providers,
  ],
}).catch(err => console.error(err));
