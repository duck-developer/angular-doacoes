import { Component, OnInit } from '@angular/core';
import { DoadorService } from '../../../services/doador/doador.service';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import {
  faEdit,
  faTrash,
  faEye,
  faUserSlash,
  faUserPlus,
} from '@fortawesome/free-solid-svg-icons';
import Swal from 'sweetalert2';
@Component({
  selector: 'app-perfil-plus',
  imports: [FormsModule, CommonModule, FontAwesomeModule],
  templateUrl: './perfil-plus.component.html',
  styleUrl: './perfil-plus.component.css',
})
export class PerfilPlusComponent implements OnInit {
  doadores: any[] = [];
  novoDoador = {
    nome: '',
    email: '',
    telefone: '',
    cpf: '',
    senha: '',
  };
  faTrash = faTrash;
  faEdit = faEdit;
  faEye = faEye;
  faUserSlash = faUserSlash;
  faUserPlus = faUserPlus;

  constructor(private doadorService: DoadorService) {}
  doadorSelecionado: any = null;
  ngOnInit(): void {
    this.carregarDoadores();
  }

  carregarDoadores() {
    this.doadorService.getDoadores().subscribe((res) => {
      this.doadores = res.doadores;
    });
  }

  mostrarFormCadastro: boolean = false;

  // Função para abrir o formulário
  abrirFormCadastro() {
    this.mostrarFormCadastro = true;
  }

  // Função para fechar o formulário
  fecharFormCadastro() {
    this.mostrarFormCadastro = false;

    // Resetar campos do formulário
    this.novoDoador = {
      nome: '',
      email: '',
      telefone: '',
      cpf: '',
      senha: '',
    };
  }
  cadastrarDoador() {
    this.doadorService.criarDoador(this.novoDoador).subscribe({
      next: (res) => {
        Swal.fire({
          icon: 'success',
          title: 'Sucesso',
          text: res.msg,
        });
        this.carregarDoadores();
        this.fecharFormCadastro();
      },
      error: (err) => {
        console.error('Erro ao cadastrar doador:', err);

        const mensagem =
          err?.error?.msg || 'Erro ao cadastrar doador. Tente novamente.';

        Swal.fire({
          icon: 'error',
          title: 'Erro',
          text: mensagem,
        });
      },
    });
  }
  excluirDoador(id: number) {
    Swal.fire({
      title: 'Deseja realmente excluir este doador?',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonText: 'Sim, excluir',
      cancelButtonText: 'Cancelar',
    }).then((result) => {
      if (result.isConfirmed) {
        this.doadorService.deletarDoador(id).subscribe({
          next: (res) => {
            Swal.fire({
              icon: 'success',
              title: 'Sucesso',
              text: res.msg,
            });
            this.carregarDoadores();
          },
          error: (err) => {
            Swal.fire({
              icon: 'error',
              title: 'Erro',
              text: 'Erro ao excluir doador.' + err,
            });
            console.error(err);
          },
        });
      }
    });
  }

  abrirModal(doador: any) {
    this.doadorSelecionado = doador;
  }

  fecharModal() {
    this.doadorSelecionado = null;
  }

  mostrarFormEdicao = false;
  doadorEditando: any = null;

  abrirFormularioEdicao(doador: any) {
    this.doadorEditando = { ...doador }; // cópia para edição
    this.mostrarFormEdicao = true;
  }

  fecharFormEdicao() {
    this.mostrarFormEdicao = false;
    this.doadorEditando = null;
  }

  salvarEdicao() {
    if (!this.doadorEditando || !this.doadorEditando.id) return;

    // Criar objeto para enviar com os campos editáveis
    const dadosParaAtualizar: any = {
      nome: this.doadorEditando.nome,
      email: this.doadorEditando.email,
      telefone: this.doadorEditando.telefone,
      senha: 'senha vazia',
    };

    this.doadorService
      .atualizarDoador(this.doadorEditando.id, dadosParaAtualizar)
      .subscribe({
        next: (res) => {
          Swal.fire('Sucesso', res.msg, 'success');
          this.carregarDoadores();
          this.fecharFormEdicao();
        },
        error: (err) => {
          Swal.fire('Erro', 'Erro ao atualizar doador.', 'error');
          console.error(err);
        },
      });
  }
}
