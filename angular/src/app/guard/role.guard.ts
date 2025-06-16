import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, Router } from '@angular/router';

@Injectable({
  providedIn: 'root',
})
export class RoleGuard implements CanActivate {
  constructor(private router: Router) {}

  canActivate(route: ActivatedRouteSnapshot): boolean {
    const expectedRoles: string[] = route.data['roles'];
    const userStr = localStorage.getItem('usuario');

    if (userStr) {
      const user = JSON.parse(userStr);
      const userRole = user.tipo;

      if (expectedRoles.includes(userRole)) {
        return true;
      }
    }

    this.router.navigate(['/home']);
    return false;
  }
}
