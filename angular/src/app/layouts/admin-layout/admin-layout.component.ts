import { Component } from '@angular/core';
import { Router, RouterModule, RouterOutlet } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { CommonModule } from '@angular/common';
import { faUserShield, faBullhorn } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { FormsModule } from '@angular/forms';
import { AdminService } from '../../services/admin/admin.service';
import Swal from 'sweetalert2';

@Component({
  selector: 'app-admin-layout',
  imports: [
    RouterOutlet,
    RouterModule,
    CommonModule,
    FontAwesomeModule,
    FormsModule,
  ],
  templateUrl: './admin-layout.component.html',
  styleUrls: ['./admin-layout.component.css'],
  standalone: true,
})
export class AdminLayoutComponent {
  userRole: string | null = null;
  showCadastroAdmin = false;

  faUserShield = faUserShield;
  faBullhorn = faBullhorn;
  formData = {
    cpf: '',
    email: '',
    nome: '',
    telefone: '',
    senha: '',
  };

  constructor(
    private authService: AuthService,
    private router: Router,
    private adminService: AdminService // injete aqui
  ) {
    const usuarioStr = localStorage.getItem('usuario');
    if (usuarioStr) {
      const usuario = JSON.parse(usuarioStr);
      this.userRole = usuario.tipo;
    }
  }

  toggleCadastroAdmin() {
    this.showCadastroAdmin = !this.showCadastroAdmin;
  }

  cadastrarAdmin() {
    const token = localStorage.getItem('token') || '';

    this.adminService.cadastrarAdmin(this.formData, token).subscribe({
      next: (res) => {
        Swal.fire({
          icon: 'success',
          title: 'Sucesso',
          text: res.msg,
        });
        if (res.msg.toLowerCase().includes('sucesso')) {
          this.toggleCadastroAdmin(); // fecha o modal
          this.formData = {
            cpf: '',
            email: '',
            nome: '',
            telefone: '',
            senha: '',
          }; // limpa o formulário
        }
      },
      error: (err) => {
        Swal.fire({
          icon: 'error',
          title: 'Erro',
          text: err.error?.msg || err.message || 'Erro inesperado',
        });
      },
    });
  }

  logout() {
    this.authService.logout();
    this.router.navigate(['/home']);
  }
}
