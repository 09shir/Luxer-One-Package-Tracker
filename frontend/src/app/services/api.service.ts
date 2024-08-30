import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Delivery } from '../models/delivery';

@Injectable({
  providedIn: 'root',
})
export class ApiService {

  private apiUrl: string = 'http://0.0.0.0:5000/api/v1/deliveries';

  constructor(private http: HttpClient) {}

  getData(): Observable<{ deliveries: Delivery[] }> {
    return this.http.get<{ deliveries: Delivery[] }>(this.apiUrl);
  }
}
