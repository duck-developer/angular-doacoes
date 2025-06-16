import { Routes } from '@angular/router';

import { LoginComponent } from './pages/login/login.component';
import { PerfilComponent } from './pages/admin/perfil/perfil.component';
import { AuthGuard } from './auth.guard';
import { HomeComponent } from './pages/home/home.component';
import { PerfilPlusComponent } from './pages/admin/perfil-plus/perfil-plus.component';
import { AdminLayoutComponent } from './layouts/admin-layout/admin-layout.component';
import { RoleGuard } from './guard/role.guard';
import { CampanhaComponent } from './pages/admin/campanha/campanha.component';

export const routes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
  { path: 'home', component: HomeComponent, canActivate: [AuthGuard] },
  {
    path: 'admin',
    component: AdminLayoutComponent,
    canActivate: [AuthGuard],
    children: [
      { path: 'perfil', component: PerfilComponent },
      {
        path: 'novo-perfil',
        component: PerfilPlusComponent,
        canActivate: [RoleGuard],
        data: { roles: ['ADMIN'] },
      },
      {
        path: 'campanhas',
        component: CampanhaComponent,
        canActivate: [RoleGuard],
        data: { roles: ['ADMIN'] },
      },

      { path: '', redirectTo: 'perfil', pathMatch: 'full' },
    ],
  },

  { path: '**', redirectTo: 'home' },
];
