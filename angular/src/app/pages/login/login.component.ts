import { Component } from '@angular/core';
import {
  FormBuilder,
  FormGroup,
  Validators,
  ReactiveFormsModule,
} from '@angular/forms';
import { AuthService } from '../../services/auth.service';
import { Router, RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import Swal from 'sweetalert2';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
})
export class LoginComponent {
  form: FormGroup;
  errorMsg: string = '';

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {
    this.form = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      senha: ['', [Validators.required, Validators.minLength(6)]],
    });
  }
  login() {
    this.form.markAllAsTouched();

    if (this.form.invalid) {
      let mensagensErro = [];

      const emailControl = this.form.get('email');
      const senhaControl = this.form.get('senha');

      if (emailControl?.hasError('required')) {
        mensagensErro.push('O campo de e-mail é obrigatório.');
      } else if (emailControl?.hasError('email')) {
        mensagensErro.push('Informe um e-mail válido.');
      }

      if (senhaControl?.hasError('required')) {
        mensagensErro.push('O campo de senha é obrigatório.');
      } else if (senhaControl?.hasError('minlength')) {
        mensagensErro.push('A senha deve ter no mínimo 6 caracteres.');
      }

      Swal.fire({
        icon: 'warning',
        title: 'Campos inválidos',
        html: mensagensErro.join('<br>'),
      });

      return;
    }

    this.authService.login(this.form.value).subscribe({
      next: (res) => {
        localStorage.setItem('token', res.token_jwt);
        localStorage.setItem('usuario', JSON.stringify(res.usuario));
        this.router.navigate(['/admin/perfil']);
        Swal.fire({
          icon: 'success',
          title: 'Success',
          text: 'Usuário Logado',
        });
      },
      error: () => {
        Swal.fire({
          icon: 'error',
          title: 'Erro',
          text: 'Verifique suas credenciais!',
        });
      },
    });
  }
}
