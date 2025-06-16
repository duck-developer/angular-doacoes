import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

interface Campanha {
  id: number;
  nome: string;
  descricao: string;
  dtFim: string;
  dtInicio: string;
  metaArrecadacao: number;
}

@Injectable({
  providedIn: 'root',
})
export class CampanhaService {
  private api = 'http://localhost:5000/api/v1';

  constructor(private http: HttpClient) {}

  private getHeaders(): HttpHeaders {
    return new HttpHeaders({
      Authorization: `${localStorage.getItem('token')}`,
    });
  }

  listarCampanhaAtivas(pagina = 1, itensPorPagina = 4) {
    return this.http.get<{ campanhas: Campanha[] }>(
      `${this.api}/campanha/ativas?pagina=${pagina}&itensPorPagina=${itensPorPagina}`,
      {
        headers: this.getHeaders(),
      }
    );
  }
  listarTodas(pagina = 1, itensPorPagina = 300) {
    return this.http.get<{ campanhas: Campanha[] }>(
      `${this.api}/campanha?pagina=${pagina}&itensPorPagina=${itensPorPagina}`,
      {
        headers: this.getHeaders(),
      }
    );
  }

  criarCampanha(campanha: Partial<Campanha>) {
    return this.http.post<{ msg: string }>(`${this.api}/campanha`, campanha, {
      headers: this.getHeaders(),
    });
  }

  deletarCampanha(id: number) {
    return this.http.delete<{ msg: string }>(`${this.api}/campanha/${id}`, {
      headers: this.getHeaders(),
    });
  }

  atualizarCampanha(
    id: number,
    dadosAtualizados: {
      nome: string;
      metaArrecadacao: number;
      descricao: string;
      dtInicio: string;
      dtFim: string;
    }
  ) {
    return this.http.put<{ msg: string }>(
      `${this.api}/campanha/${id}`,
      dadosAtualizados,
      { headers: this.getHeaders() }
    );
  }

  realizarDoacao(
    idCampanha: number,
    idDoador: number,
    dadosPagamento: {
      numeroCartao: string;
      nomeCartao: string;
      dtValidadeCartao: string;
      codigoSegurancaCartao: number | null;
      valorDoado: number | null;
    }
  ) {
    return this.http.post<{ msg: string }>(
      `${this.api}/doacao/${idCampanha}/${idDoador}`,
      dadosPagamento,
      { headers: this.getHeaders() }
    );
  }

  listarDoacoesPorCampanha(
    idCampanha: number,
    pagina = 1,
    itensPorPagina = 100
  ) {
    return this.http.get<{ doacoes: any[] }>(
      `${this.api}/doacao/${idCampanha}?pagina=${pagina}&itensPorPagina=${itensPorPagina}`,
      { headers: this.getHeaders() }
    );
  }
}
