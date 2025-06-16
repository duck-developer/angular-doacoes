import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import Swal from 'sweetalert2';
import { UsuarioService } from '../../../services/usuarios/usuario.service';

interface Usuario {
  id: number;
  nome: string;
  email: string;
  cpf: string;
  primeiroAcesso: string;
  telefone: string;
  tipo: string;
}

@Component({
  selector: 'app-perfil',
  standalone: true,
  imports: [CommonModule, RouterModule, FormsModule],
  templateUrl: './perfil.component.html',
  styleUrls: ['./perfil.component.css'], // Corrigido para styleUrls (plural)
})
export class PerfilComponent {
  usuario!: Usuario;
  editando = false;
  editandoSenha = false;

  senhaAtual = '';
  novaSenha = '';
  confirmarNovaSenha = '';

  constructor(private usuarioService: UsuarioService) {}

  ngOnInit(): void {
    const userStr = localStorage.getItem('usuario');
    if (userStr) {
      this.usuario = JSON.parse(userStr);
    }
  }

  salvar() {
    const { nome, email, telefone } = this.usuario;
    const dadosParaAtualizar = { nome, email, telefone };
    this.usuarioService.atualizarDados(dadosParaAtualizar).subscribe({
      next: () => {
        localStorage.setItem('usuario', JSON.stringify(this.usuario));
        Swal.fire('Sucesso', 'Dados atualizados com sucesso!', 'success');
        this.editando = false;
      },
      error: (err) => {
        Swal.fire(
          'Erro',
          'Erro ao atualizar dados: ' + (err.error?.msg || err.message),
          'error'
        );
      },
    });
  }

  cancelar() {
    const userStr = localStorage.getItem('usuario');
    if (userStr) {
      this.usuario = JSON.parse(userStr);
    }
    this.editando = false;
  }

  alterarSenha() {
    if (this.novaSenha !== this.confirmarNovaSenha) {
      Swal.fire('Erro', 'A nova senha e a confirmação não coincidem.', 'error');
      return;
    }

    const dadosSenha = {
      senha: this.senhaAtual,
      novaSenha: this.novaSenha,
    };

    this.usuarioService.atualizarSenha(dadosSenha).subscribe({
      next: () => {
        Swal.fire('Sucesso', 'Senha alterada com sucesso!', 'success');
        this.editandoSenha = false;
        this.limparCamposSenha();
      },
      error: (err) => {
        Swal.fire(
          'Erro',
          'Erro ao alterar senha: ' + (err.error?.msg || err.message),
          'error'
        );
      },
    });
  }

  cancelarSenha() {
    this.editandoSenha = false;
    this.limparCamposSenha();
  }

  limparCamposSenha() {
    this.senhaAtual = '';
    this.novaSenha = '';
    this.confirmarNovaSenha = '';
  }
}
