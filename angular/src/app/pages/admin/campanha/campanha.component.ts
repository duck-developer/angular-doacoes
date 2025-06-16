import { Component, OnInit } from '@angular/core';
import { CampanhaService } from '../../../services/campanha/campanha.service';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';

import {
  faEdit,
  faTrash,
  faEye,
  faBullhorn,
  faPlusSquare,
  faHandHoldingDollar,
} from '@fortawesome/free-solid-svg-icons';
import Swal from 'sweetalert2';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-campanhas',
  templateUrl: './campanha.component.html',
  styleUrls: ['./campanha.component.css'],
  imports: [CommonModule, FontAwesomeModule, FormsModule],
})
export class CampanhaComponent implements OnInit {
  campanhas: any[] = [];
  novaCampanha = {
    nome: '',
    descricao: '',
    dtInicio: '',
    dtFim: '',
    metaArrecadacao: 0,
  };

  faTrash = faTrash;
  faEdit = faEdit;
  faEye = faEye;
  faBullhorn = faBullhorn;
  faPlusSquare = faPlusSquare;
  faHandHoldingDollar = faHandHoldingDollar;

  constructor(private campanhaService: CampanhaService) {}

  ngOnInit(): void {
    this.carregarCampanhas();
  }

  carregarCampanhas() {
    this.campanhaService.listarTodas().subscribe((res) => {
      this.campanhas = res.campanhas;
    });
  }

  campanhaSelecionada: any = null;

  abrirModalCampanha(campanha: any) {
    this.campanhaSelecionada = campanha;
  }

  fecharModalCampanha() {
    this.campanhaSelecionada = null;
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
    this.novaCampanha = {
      nome: '',
      descricao: '',
      dtInicio: '',
      dtFim: '',
      metaArrecadacao: 0,
    };
  }
  formatarDataParaBR(data: string): string {
    if (!data) return '';
    const [ano, mes, dia] = data.split('-');
    return `${dia}/${mes}/${ano}`;
  }

  formatarDataVisual(data: string): string {
    if (!data) return '';
    const partes = data.split(' ')[0].split('-');
    const [ano, mes, dia] = partes;
    return `${dia}/${mes}/${ano}`;
  }
  formatarDataParaInput(data: string): string {
    if (!data) return '';
    const partes = data.split(' ')[0].split('/');
    if (partes.length === 3) {
      const [dia, mes, ano] = partes;
      return `${ano}-${mes}-${dia}`;
    }
    return data.split(' ')[0]; // caso já esteja em yyyy-MM-dd
  }

  cadastrarCampanha() {
    const campanhaFormatada = {
      ...this.novaCampanha,
      dtInicio: this.formatarDataParaBR(this.novaCampanha.dtInicio),
      dtFim: this.formatarDataParaBR(this.novaCampanha.dtFim),
    };

    this.campanhaService.criarCampanha(campanhaFormatada).subscribe({
      next: (res) => {
        Swal.fire({
          icon: 'success',
          title: 'Sucesso',
          text: res.msg,
        });
        this.carregarCampanhas();
        this.fecharFormCadastro();
      },
      error: (err) => {
        console.error('Erro ao cadastrar campanha:', err);

        const mensagem =
          err?.error?.msg || 'Erro ao cadastrar campanha. Tente novamente.';

        Swal.fire({
          icon: 'error',
          title: 'Erro',
          text: mensagem,
        });
      },
    });
  }

  excluirCampanha(id: number) {
    Swal.fire({
      title: 'Deseja realmente excluir este doador?',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonText: 'Sim, excluir',
      cancelButtonText: 'Cancelar',
    }).then((result) => {
      if (result.isConfirmed) {
        this.campanhaService.deletarCampanha(id).subscribe({
          next: (res) => {
            Swal.fire({
              icon: 'success',
              title: 'Sucesso',
              text: res.msg,
            });
            this.carregarCampanhas();
          },
          error: (err) => {
            Swal.fire({
              icon: 'error',
              title: 'Erro',
              text: 'Erro ao excluir doador.' + err.error.msg,
            });
          },
        });
      }
    });
  }

  mostrarFormEdicao = false;
  campanhaEditando: any = null;

  abrirFormEdicao(campanha: any) {
    this.campanhaEditando = { ...campanha };

    // Converter para input type="date"
    this.campanhaEditando.dtInicio = this.formatarDataParaInput(
      this.campanhaEditando.dtInicio
    );
    this.campanhaEditando.dtFim = this.formatarDataParaInput(
      this.campanhaEditando.dtFim
    );
    this.mostrarFormEdicao = true;
  }

  fecharFormEdicao() {
    this.mostrarFormEdicao = false;
    this.campanhaEditando = null;
  }

  salvarEdicao() {
    if (!this.campanhaEditando || !this.campanhaEditando.id) return;
    const dadosParaAtualizar: any = {
      nome: this.campanhaEditando.nome,
      descricao: this.campanhaEditando.descricao,
      dtInicio: this.formatarDataParaBR(this.campanhaEditando.dtInicio),
      dtFim: this.formatarDataParaBR(this.campanhaEditando.dtFim),
      metaArrecadacao: this.campanhaEditando.metaArrecadacao,
    };
    this.campanhaService
      .atualizarCampanha(this.campanhaEditando.id, dadosParaAtualizar)
      .subscribe({
        next: (res) => {
          Swal.fire({
            icon: 'success',
            title: 'Atualizado',
            text: 'Campanha atualizada com sucesso!',
          });
          this.carregarCampanhas();
          this.fecharFormEdicao();
        },
        error: (err) => {
          Swal.fire({
            icon: 'error',
            title: 'Erro',
            text: 'Não foi possível atualizar a campanha.' + err.error.msg,
          });
        },
      });
  }

  // Novo estado
  mostrarModalDoacoes = false;
  doacoesDaCampanha: any[] = [];

  // Inject CampanhaService no constructor já existe

  // Método para abrir a modal de doações
  abrirModalDoacoes(idCampanha: number) {
    this.campanhaService.listarDoacoesPorCampanha(idCampanha).subscribe({
      next: (res: any) => {
        this.doacoesDaCampanha = res.doacoes;
        this.mostrarModalDoacoes = true;
      },
      error: (err) => {
        Swal.fire('Erro', 'Não foi possível carregar as doações.', 'error');
        console.log(err);
      },
    });
  }

  fecharModalDoacoes() {
    this.mostrarModalDoacoes = false;
    this.doacoesDaCampanha = [];
  }
}
