import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CampanhaService } from '../../services/campanha/campanha.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import Swal from 'sweetalert2';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
})
export class HomeComponent implements OnInit {
  campanhas: any[] = [];
  pagina = 1;
  itensPorPagina = 4;
  totalPaginas = 1;

  constructor(
    private campanhaService: CampanhaService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.carregarCampanhas();
  }

  formatarDataVisual(data: string): string {
    if (!data) return '';
    const partes = data.split(' ')[0].split('-');
    const [ano, mes, dia] = partes;
    return ` ${dia}/${mes}/${ano} `;
  }
  formatarDataParaBR(data: string): string {
    if (!data) return '';
    const [ano, mes, dia] = data.split('-');
    return `${dia}/${mes}/${ano}`;
  }
  carregarCampanhas() {
    this.campanhaService
      .listarCampanhaAtivas(this.pagina, this.itensPorPagina)
      .subscribe((res: any) => {
        this.campanhas = res.campanhasAtivas;
        this.totalPaginas = res.qtdPaginas;
      });
  }

  proximaPagina() {
    if (this.pagina < this.totalPaginas) {
      this.pagina++;
      this.carregarCampanhas();
    }
  }

  paginaAnterior() {
    if (this.pagina > 1) {
      this.pagina--;
      this.carregarCampanhas();
    }
  }

  detalhesCampanha: any = null;

  verDetalhes(id: number) {
    this.detalhesCampanha = this.campanhas.find((c) => c.id === id);
  }

  fecharDetalhes() {
    this.detalhesCampanha = null;
  }

  mostrarFormularioDoacao = false;
  dadosDoacao = {
    numeroCartao: '',
    nomeCartao: '',
    dtValidadeCartao: '',
    codigoSegurancaCartao: 0,
    valorDoado: 0,
  };
  abrirFormularioDoacao() {
    this.mostrarFormularioDoacao = true;
  }
  enviarDoacao(idCampanha: number) {
    const {
      numeroCartao,
      nomeCartao,
      dtValidadeCartao,
      codigoSegurancaCartao,
      valorDoado,
    } = this.dadosDoacao;

    if (
      !numeroCartao.trim() ||
      !nomeCartao.trim() ||
      !dtValidadeCartao.trim() ||
      codigoSegurancaCartao <= 0 ||
      valorDoado <= 0
    ) {
      Swal.fire({
        icon: 'warning',
        title: 'Campos obrigatórios',
        text: 'Preencha todos os campos corretamente antes de doar.',
      });
      return;
    }

    const usuario = JSON.parse(localStorage.getItem('usuario') || '{}');
    const idDoador = usuario.id;

    const dataFormatada = this.formatarDataParaBR(dtValidadeCartao); // usa sua função

    this.campanhaService
      .realizarDoacao(idCampanha, idDoador, {
        ...this.dadosDoacao,
        dtValidadeCartao: dataFormatada,
      })
      .subscribe({
        next: (res) => {
          Swal.fire({
            icon: 'success',
            title: 'Doação realizada!',
            text: res.msg,
          });

          this.mostrarFormularioDoacao = false;
          this.dadosDoacao = {
            numeroCartao: '',
            nomeCartao: '',
            dtValidadeCartao: '',
            codigoSegurancaCartao: 0,
            valorDoado: 0,
          };
        },
        error: (err) => {
          console.error(err);
          Swal.fire({
            icon: 'error',
            title: 'Erro',
            text: 'Erro ao processar a doação.',
          });
        },
      });
  }
}
