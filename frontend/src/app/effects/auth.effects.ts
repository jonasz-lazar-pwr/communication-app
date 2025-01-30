import { Injectable } from '@angular/core';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { AuthService } from '../services/auth.service';
import { login, loginSuccess, logout } from '../actions/auth.actions';
import { map, mergeMap, catchError } from 'rxjs/operators';
import { of } from 'rxjs';

@Injectable()
export class AuthEffects {
  // login$ = createEffect(() =>
  //   this.actions$.pipe(
  //     ofType(login),
  //     mergeMap((action) =>
  //       this.authService.login({ email: action.email, password: action.password }).pipe(
  //         map((tokens) => loginSuccess(tokens)),
  //         catchError(() => of(logout()))
  //       )
  //     )
  //   )
  // );

  constructor(private actions$: Actions, private authService: AuthService) {}
}
