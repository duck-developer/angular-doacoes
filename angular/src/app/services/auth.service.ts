import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

interface Usuario {
  id: number;
  nome: string;
  email: string;
  cpf: string;
  primeiroAcesso: string;
  telefone: string;
  tipo: string; // "ADMIN" ou "DOADOR"
}

interface LoginResponse {
  token_jwt: string;
  usuario: Usuario;
}

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private api = 'http://localhost:5000/api/v1';

  constructor(private http: HttpClient) {}

  login(data: { email: string; senha: string }): Observable<LoginResponse> {
    return this.http.post<LoginResponse>(`${this.api}/usuario/logar`, data);
  }

  logout() {
    localStorage.clear();
  }

  isLoggedIn(): boolean {
    return !!localStorage.getItem('token');
  }
}
