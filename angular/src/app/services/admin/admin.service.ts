import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

interface AdminData {
  cpf: string;
  email: string;
  nome: string;
  telefone: string;
  senha: string;
}

interface ApiResponse {
  msg: string;
}

@Injectable({
  providedIn: 'root',
})
export class AdminService {
  private url = 'http://localhost:5000/api/v1';

  constructor(private http: HttpClient) {}

  cadastrarAdmin(admin: AdminData, token: string): Observable<ApiResponse> {
    const headers = new HttpHeaders({
      Authorization: `${token}`,
      'Content-Type': 'application/json',
    });

    return this.http.post<ApiResponse>(this.url, admin, { headers });
  }
}
