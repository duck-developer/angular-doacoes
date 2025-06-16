// src/app/services/doador.service.ts
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';

interface Doador {
  id: number;
  nome: string;
  email: string;
  telefone: string;
  cpf: string;
}

@Injectable({
  providedIn: 'root',
})
export class DoadorService {
  private api = 'http://localhost:5000/api/v1';

  constructor(private http: HttpClient) {}

  private getHeaders(): HttpHeaders {
    return new HttpHeaders({
      Authorization: `${localStorage.getItem('token')}`,
    });
  }
  getDoadores(pagina = 1, itensPorPagina = 300) {
    return this.http.get<{ doadores: Doador[] }>(
      `${this.api}/doador?pagina=${pagina}&itensPorPagina=${itensPorPagina}`,
      {
        headers: this.getHeaders(),
      }
    );
  }

  criarDoador(doador: Partial<Doador> & { senha: string }) {
    return this.http.post<{ msg: string }>(`${this.api}/doador`, doador, {
      headers: this.getHeaders(),
    });
  }
  deletarDoador(id: number) {
    return this.http.delete<{ msg: string }>(`${this.api}/doador/${id}`, {
      headers: this.getHeaders(),
    });
  }

  atualizarDoador(
    id: number,
    dadosAtualizados: {
      nome: string;
      telefone: string;
      email: string;
      senha: string;
    }
  ) {
    return this.http.put<{ msg: string }>(
      `${this.api}/usuario/${id}`,
      dadosAtualizados,
      { headers: this.getHeaders() }
    );
  }
}
