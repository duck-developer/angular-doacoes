// src/app/services/usuario.service.ts
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class UsuarioService {
  private readonly API = 'http://localhost:5000/api/v1';

  constructor(private http: HttpClient) {}

  private getHeaders(): HttpHeaders {
    return new HttpHeaders({
      Authorization: `${localStorage.getItem('token')}`,
    });
  }

  atualizarDados(usuario: {
    nome: string;
    email: string;
    telefone: string;
  }): Observable<any> {
    return this.http.put(`${this.API}/usuario`, usuario, {
      headers: this.getHeaders(),
    });
  }

  obterUsuarioPorToken(): Observable<any> {
    return this.http.get(`${this.API}/usuario/porToken`, {
      headers: this.getHeaders(),
    });
  }

  atualizarSenha(dados: { senha: string; novaSenha: string }): Observable<any> {
    return this.http.put(`${this.API}/usuario/senha`, dados, {
      headers: this.getHeaders(),
    });
  }
}
